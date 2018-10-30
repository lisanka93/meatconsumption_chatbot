from flask import Flask, request
import requests
import random
from quickreplies_tony import *
from query import *

app = Flask(__name__)

#access token of ArgHealthBot Application in Facebook
ACCESS_TOKEN = "EAAFEzTNmiTwBANJP8NFyHvhKTdtB91Jbm9SVR5sTxpsQtZBEdZALLpf6R5bvhZCpLTHbxaRt2CY7Mo8faLjvC54S2iddZBhGb8zTSUCcVrwJhdD05cmjShcPtXliAuRAxQ5sVXNsmIjaGAPbiTwhJeTomq6hBuZAmtR18dqdFqwZDZD"

# set of unique user id's
user_ids =  set()

# example of a quick reply where user has options to choose from
def quick_reply_yesno(user_id, msg):
    data = {
        "recipient": {"id": user_id},

        "message": {
        "text": msg,

        "quick_replies": yesno_reply
    }
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)

# dont change following code:
@app.route('/', methods=['GET'])
def handle_verification():
    return request.args['hub.challenge']

def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)



##########################################################################

@app.route('/', methods=['POST'])
def handle_incoming_messages():

    data = request.json

    try:
        sender = data['entry'][0]['messaging'][0]['sender']['id']  #unicode, should i typecast it into string or int? lets see...
        message = data['entry'][0]['messaging'][0]['message']['text']

    except KeyError:

        sender = 'bla'
        message = 'bla'

    #converting message to string for easier NLP analysis later
    message = message.lower().encode('utf-8')

    #sender as string just in case
    key_id = str(sender)

    #if the sender is not found in userIds set, create key in dictionary and add message to log (value)
    if key_id not in user_ids:
        try:

            bot_reply = 'Hello, do you want to chat with me?'
            #add user to set
            user_ids.add(key_id)
            quick_reply_yesno(sender, bot_reply)
            return "ok"
        except:
            print "ERROR 2"
            return "ok"


    if key_id in user_ids:
        try:
            if message == 'yes':
                bot_reply = 'Great! Type \'hello\''
                reply(sender, bot_reply)
                return "ok"
            elif message == 'no':
                bot_reply = 'I don\'t care. type \'hello\''
                reply(sender, bot_reply)
                return "ok"
            elif message == 'hello':
                bot_reply = 'Hello Anthony. This is a demo. Type anything you want and I\'ll keep on talking'
                reply(sender, bot_reply)
                return "ok"
            else:
                possible_replies = ['I like fish and chips', 'I like tea', 'I don\'t like it when people don\'t  queue','I don\'t like Nigel Farage', 'I like the queen', 'I am British', 'I can\'t make my mind up about the EU']
                bot_reply = random.choice(possible_replies)
                reply(sender, bot_reply)
                return "ok"

        except:

            print "ERROR 3 "


        return 'ok'




if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5555, threaded=True)
