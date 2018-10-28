from flask import Flask, request
import requests
import random
from quickreplies import *
from query import *

app = Flask(__name__)

#access token of ArgHealthBot Application in Facebook
ACCESS_TOKEN = "EAACJjQRK0ucBAGi6KrrhPyudOQO61yVV3vZC8N2E4jUvJ12VlfVXjTpREkZAgKrMoxIqqiNbG9yzVqdptbm6veJBXL8Mec08BEjfZCfZBgHTsqABigzpBZAaKA0to0RAmMdzfO5YZAZBiZAfhWu4anLJXlejVE0GShWnCtcZA0V9O2wZDZD"
# set of unique user id's
user_ids =  set()
users = {}
args = {'PPC1': 'you will reduce your risk for cancer, heart disease and diabetes if you cut down your meat consumption',
        'PPC2' : 'eating less meat improves your general health, enables your digestive system to process foods more easily and gives you more energy, leaving you feeling less sluggish and tired',
        'PPC3': 'your reduction of meat will leave you feeling better physically and mentally. There is less risk of health complications, including food poisoning and an increased benefit of adding plant based foods to your diet to make it healthier and more varied',
        'PPC4': 'eating less meat results in better digestion and less constipation',
        'PPC5': 'reducing the consumption of (processed) meat and substituting it with mock meat and better with vegetables, grains and mushrooms will increase the diversity in your diet, provide you with a higher variety of nutrients and reduce your intake of hormones and saturated fat.',
        'PPC6': 'if you eat less meat you will lose weight.',
        'PPC7' : 'excessive meat consumption leads to higher cholesterol levels. This is an attention test. Please disagree and type: \"Because I want to pass the attention test to get paid for this study\" ',

        'NPC1': 'eating processed meat several times a week (or even day) can lead to serious health issues due to the high consumption of saturated fat, hormones and medicine (antibiotics) in the meat',
        'NPC2' : 'eating too much meat is linked to health complications such as an increased likelihood of a stroke or heart attack.',
        'NPC3': 'excessive consumption of meat can lead to many health problems, including heart disease, cancer and high blood pressure',
        'NPC4': 'it may make you antibiotic resistant since the antibiotics that we depend on to treat human illnesses are now used to promote growth in animals and to keep them alive in horrific living conditions that would otherwise kill them',
        'NPC5': 'meat consumption was linked to cancer, heart disease and diabetes.',
        'NPC6': 'red meats have been proven to have negative effects on the human digestive system, causing harm with potential illness.',

        'NIC1': 'raising animals for food requires massive amounts of land, food, energy, and water and causes immense animal suffering',
        'NIC2': 'meat consumption is not sustainable and will lead to environmental problems that will impact our future life on earth',
        'NIC3': 'if people continue consuming meat in such high quantities as today, problems like deforestation, water shortages and greenhouse gas emissions will continue to grow',
        'NIC4': 'meat consumption leads to more C02 released causing climate change',
        'NIC5': 'more animals means more resources - transportation of livestock, utilities to house the animals etc.',
        'NIC6': 'our world cannot sustain the meat production whilst our gashouse emissions are increasing and disease is spreading amongst farmed animals and posing a risk to jumping the species gap. We need to use our water and grain to feed the starving people of the world and not animals that are born into slavery for consumption.',
        'NIC7' : 'farming accounts for about 70% of water used in the world today. This is an attention test. Please disagree and type \"Because I want to pass the attention test and get paid for this study\" ',

        'PIC1': 'switching to a more plant based diet will lead to a more sustainable life on earth and have a positive impact on our future',
        'PIC2': 'the less animals bred purely to be slaughtered, the less resources used to transport them. Smaller, more natural levels of animals would create less impact on the environment too',
        'PIC3': 'eating less meat will have a positive effect upon the environment, helping to slow down the rapid rates of deforestation',
        'PIC4': 'reducing meat consumption will lead to less deforestation, water shortages, greenhouse emissions, not to mention animal cruelty',
        'PIC5': 'the less meat people eat, the less land being cleared for livestock which means more forests etc & more biodiversity',
        'PIC6': 'reducing meat consumption will lead to less animal cruelty',
        }

starter = ['But ', 'However, ']
understanding = ['I understand :)', 'I get your point!', 'Ok, I see.', 'All right.', 'Fair enough!', 'I know what you mean', 'I take your point']
checkpointlists = {} #checkpoints to guide conversation a certain way
#values = ['environment', 'health']

def quick_reply_yes(user_id, msg):
    data = {
        "recipient": {"id": user_id},

        "message": {
        "text": msg,

        "quick_replies": yes_reply
    }
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)


def quick_reply_values(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {
        "text": msg,

        "quick_replies": value_replies
    }
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)

def quick_reply_mainarg(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {
        "text": msg,

        "quick_replies": arg_replies
    }
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)

def quick_reply_intention(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {
        "text": msg,

        "quick_replies": scale
    }
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)


def quick_reply_agreement(user_id, msg):
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
        #should never get here
        print "KEYERROR 1"
        sender = 'defaultsender'
        message = 'defaultmessage'


    #print checkpointlists
    #converting message to string for easier NLP analysis later
    message = message.lower().encode('utf-8')
    #sender as string just in case
    key_id = str(sender)

    #if the sender is not found in userIds set, create key in dictionary and add message to log (value)
    if key_id not in user_ids:
        try:
            checkpointlists[key_id] = [0.125] #instantiating

            bot_reply = 'Welcome. A few things before we start: Please type your answers into one message (don\'t send several messages). The chat will naturally come to an end. At the end of the chat you will get the prolific completion code. If the chatbot for some reason stops replying, please just send your prolific ID and end the chat. This chat does not work on the Messenget Lite app. All good?'
            #add user to set
            user_ids.add(key_id)
            quick_reply_yes(sender, bot_reply)
            return "ok"
        except:
            print "ERROR 2"
            checkpointlists[key_id] = [0.125] #instantiating

            bot_reply = 'Welcome. A few things before we start: Please type your answers into one message (don\'t send several messages). The chat will naturally come to an end. At the end of the chat you will get the prolific completion code. If the chatbot for some reason stops replying, please just send your prolific ID and end the chat. This chat does not work on the Messenget Lite app. All good?'
            #add user to set
            user_ids.add(key_id)
            quick_reply_yes(sender, bot_reply)
            return "ok"


    if key_id in user_ids:
        try:

    # *******************************  START CONVERSATION WITH ARGHHEALTHBOT ************************************

            if checkpointlists[key_id][-1] == 0.125:
                bot_reply = 'Great! I will present you with reasons why you should consider reducing your meat consumption. You can either agree or disagree. If you disagree, I am interested why you don\'t agree with them. Are you ready?'
                quick_reply_yes(sender, bot_reply)
                checkpointlists[key_id].append(0.25)
                return "ok"


            if checkpointlists[key_id][-1] == 0.25:
                bot_reply = "Awesome. Please tell me what applies most to you:  \n 1: I definitely wouldn\'t  \n 2: I probably wouldn\'t  \n 3: I might   \n 4: I probably would   \n 5: I definitely would  \n consider reducing my meat consumption"
                quick_reply_intention(sender, bot_reply)
                checkpointlists[key_id].append(0.5)
                return 'ok'


            if checkpointlists[key_id][-1] == 0.5:
                bot_reply = "Please tell me what you are more concerned about: the impact that meat consumption has on your health, or the impact it has on the environment and animals?."
                quick_reply_values(sender, bot_reply)
                checkpointlists[key_id].append(0)
                return 'ok'

            if checkpointlists[key_id][-1] == 3:
                bot_reply = 'awesome, thanks! please provide your prolific ID. Make sure it is correct. Failure to provide your correct prolific ID will result in not getting paid at all.'
                reply(sender, bot_reply)
                checkpointlists[key_id].append(4)
                return 'ok'

            if checkpointlists[key_id][-1] == 4:
                bot_reply = 'here is the completion code: PVY0LZHP \n and the completion URL: https://app.prolific.ac/submissions/complete?cc=PVY0LZHP \n please take into account that approval might take a while as all chats have to be individually assessed to ensure fair payment. Thanks! good bye'
                checkpointlists[key_id].append(5)

                reply(sender, bot_reply)

                return 'ok'


            if checkpointlists[key_id][-1] == 5:
                bot_reply = 'good bye :)'
                reply(sender, bot_reply)
                return 'ok'


            if checkpointlists[key_id][-1] == 0 :
                if message == 'environment/animals':
                    users[key_id] = [['NIC1', 'NIC2', 'NIC3',
                                    'NIC4', 'NIC5','NIC6', 'NIC7',
                                    'PIC1', 'PIC2', 'PIC3',
                                    'PIC4', 'PIC5','PIC6'], []]
                    bot_reply = "Okay. What is the main reason you eat meat? Select one of the following: \n 1: I eat meat because of its nutritional value and source of protein \n 2: I eat meat because it\'s filling \n 3: I eat meat because it tastes good! \n 4: I eat meat because it\'s quick and easy to prepare \n 5: I eat meat because it\'s healthy and contributes to a balanced diet. \n 6: I eat meat because it offers more variety to my meals \n 7: Other"
                    checkpointlists[key_id].append(1)
                    quick_reply_mainarg(sender, bot_reply)
                    return 'ok'
                elif message == 'my health':
                    print 'works'
                    users[key_id] = [['PPC1', 'PPC2', 'PPC3',
                                    'PPC4', 'PPC5','PPC6', 'PPC7',
                                    'NPC1', 'NPC2', 'NPC3',
                                    'NPC4', 'NPC5', 'NPC6'], []]
                    bot_reply = "Okay. What is the main reason you eat meat? Select one of the following: \n 1: I eat meat because of its nutritional value and source of protein \n 2: I eat meat because it\'s filling \n 3: I eat meat because it tastes good! \n 4: I eat meat because it\'s quick and easy to prepare \n 5: I eat meat because it\'s healthy and contributes to a balanced diet. \n 6: I eat meat because it offers more variety to my meals \n 7: Other"
                    checkpointlists[key_id].append(1)
                    quick_reply_mainarg(sender, bot_reply)
                    return 'ok'

                else:
                    checkpointlists[key_id].append(0)
                    bot_reply = "sorry, I didnt get that, please select one of the given values"
                    quick_reply_values(sender, bot_reply)
                    return 'ok'

                return "ok"


            def chatbot_reponse(possible_CAs, used_CAs):
                possible_CAs = [e for e in possible_CAs if e not in used_CAs]
                response = random.choice(possible_CAs)
                possible_CAs.remove(response)
                used_CAs.append(response)
                return response, possible_CAs, used_CAs

            if checkpointlists[key_id][-1] == 100:
                if message == 'i agree':
                    try:

                        reply_CA, possible_CAs, used_CAs = chatbot_reponse(users[key_id][0], users[key_id][1])
                        bot_reply = 'great, what do you think about this reason:'
                        reply(sender, bot_reply)
                        users[key_id][0] = possible_CAs
                        users[key_id][1] = used_CAs
                        bot_reply = args[reply_CA]
                        quick_reply_agreement(sender, bot_reply)
                        checkpointlists[key_id].append(100)
                        return 'ok'
                    except:
                        bot_reply = 'I ran out of arguments :) let\'s end the chat here. One more question. Please tell me what applies most to you:  \n  1: I definitely wouldn\'t  \n 2: I probably wouldn\'t  \n 3: I might   \n 4: I probably would   \n 5: I definitely would  \n consider reducing my meat consumption'

                        checkpointlists[key_id].append(3)
                        quick_reply_intention(sender, bot_reply)
                        return 'ok'
                if message == 'i disagree':
                    bot_reply = 'Why?'
                    reply(sender, bot_reply)
                    checkpointlists[key_id].append(1)
                    return 'ok'
                else:
                    try:
                        reply_CA, possible_CAs, used_CAs = chatbot_reponse(users[key_id][0], users[key_id][1])
                        bot_reply = 'seems like you did not agree or disagree when asked to. But I will forgive you, let\'s move on, what do you think about this reason:'
                        reply(sender, bot_reply)
                        users[key_id][0] = possible_CAs
                        users[key_id][1] = used_CAs
                        bot_reply = args[reply_CA]
                        quick_reply_agreement(sender, bot_reply)
                        checkpointlists[key_id].append(100)
                        return 'ok'
                    except:
                        bot_reply = 'I ran out of arguments :) let\'s end the chat here. One more question. Please tell me what applies most to you:  \n  1: I definitely wouldn\'t  \n 2: I probably wouldn\'t  \n 3: I might   \n 4: I probably would   \n 5: I definitely would  \n consider reducing my meat consumption'

                        checkpointlists[key_id].append(3)
                        quick_reply_intention(sender, bot_reply)
                        return 'ok'

            """
            if message == 'stop':
                bot_reply = "thank you so much for participating in this study! One more question. How likely you would consider reducing your meat consumption \n  1: Definitely wouldn\'t consider reducing meat consumption \n 2: Probably wouldn\'t consider reducing meat consumption \n 3: Might consider reducing meat consumption \n 4: Probably would consider reducing meat condumption \n 5: Definitely would consider reducing meat consumption"
                checkpointlists[key_id].append(3)
                quick_reply_intention(sender, bot_reply)
                return 'ok'
            """

            #add one more check here to check how long the message is in order to query once
            if len(message.split()) < 12 and message.isdigit() == False and checkpointlists[key_id][-1] != -1 and  checkpointlists[key_id][-2] != 0:
                bot_reply = query(message)
                reply(sender, bot_reply)
                checkpointlists[key_id].append(-1)
                return 'ok'


            if message != 'stop' and (checkpointlists[key_id][-1] == 1 or checkpointlists[key_id][-1] == -1):
                try:

                    reply_CA, possible_CAs, used_CAs = chatbot_reponse(users[key_id][0], users[key_id][1])
                    users[key_id][0] = possible_CAs
                    users[key_id][1] = used_CAs
                    starter_ = random.choice(starter)
                    understanding_ = random.choice(understanding)
                    bot_reply = starter_ + args[reply_CA]
                    reply(sender, understanding_)
                    quick_reply_agreement(sender, bot_reply)
                    checkpointlists[key_id].append(100)
                    return 'ok'
                except:
                    bot_reply = 'I ran out of arguments :) let\'s end the chat here. One more question. Please tell me what applies most to you:  \n  1: I definitely wouldn\'t  \n 2: I probably wouldn\'t  \n 3: I might   \n 4: I probably would   \n 5: I definitely would  \n consider reducing my meat consumption'
                    checkpointlists[key_id].append(3)
                    quick_reply_intention(sender, bot_reply)
                    return 'ok'
                return 'ok'

            '''
            if checkpointlists[key_id][-1] == 3:
                bot_reply = ' if you want to test it again, just type anything'
                reply(sender, bot_reply)
                # delete later
                del users[key_id]
                del checkpointlists[key_id]
                user_ids.remove(key_id)
                return 'ok'
            '''
        except:

            print "ERROR 3 "
            if checkpointlists[key_id][-1] == 0.125:
                bot_reply = 'Great! I will present you with reasons why you should consider reducing your meat consumption. You can either agree or disagree. If you disagree, I am interested why you don\'t agree with them. Are you ready?'
                quick_reply_yes(sender, bot_reply)
                checkpointlists[key_id].append(0.25)
                return "ok"


            if checkpointlists[key_id][-1] == 0.25:
                bot_reply = "Awesome. Please tell me what applies most to you:  \n 1: I definitely wouldn\'t  \n 2: I probably wouldn\'t  \n 3: I might   \n 4: I probably would   \n 5: I definitely would  \n consider reducing my meat consumption"
                quick_reply_intention(sender, bot_reply)
                checkpointlists[key_id].append(0.5)
                return 'ok'


            if checkpointlists[key_id][-1] == 0.5:
                bot_reply = "Please tell me what you are more concerned about: the impact that meat consumption has on your health, or the impact it has on the environment and animals?."
                quick_reply_values(sender, bot_reply)
                checkpointlists[key_id].append(0)
                return 'ok'

            if checkpointlists[key_id][-1] == 3:
                bot_reply = 'awesome, thanks! please provide your prolific ID. Make sure it is correct. Failure to provide your correct prolific ID will result in not getting paid at all.'
                reply(sender, bot_reply)
                checkpointlists[key_id].append(4)
                return 'ok'

            if checkpointlists[key_id][-1] == 4:
                bot_reply = 'here is the completion code: PVY0LZHP \n and the completion URL: https://app.prolific.ac/submissions/complete?cc=PVY0LZHP \n please take into account that approval might take a while as all chats have to be individually assessed to ensure fair payment. Thanks! good bye'
                checkpointlists[key_id].append(5)

                reply(sender, bot_reply)

                return 'ok'


            if checkpointlists[key_id][-1] == 5:
                bot_reply = 'good bye :)'
                reply(sender, bot_reply)
                return 'ok'


            if checkpointlists[key_id][-1] == 0 :
                if message == 'environment/animals':
                    users[key_id] = [['NIC1', 'NIC2', 'NIC3',
                                    'NIC4', 'NIC5','NIC6', 'NIC7',
                                    'PIC1', 'PIC2', 'PIC3',
                                    'PIC4', 'PIC5','PIC6'], []]
                    bot_reply = "Okay. What is the main reason you eat meat? Select one of the following: \n 1: I eat meat because of its nutritional value and source of protein \n 2: I eat meat because it\'s filling \n 3: I eat meat because it tastes good! \n 4: I eat meat because it\'s quick and easy to prepare \n 5: I eat meat because it\'s healthy and contributes to a balanced diet. \n 6: I eat meat because it offers more variety to my meals \n 7: Other"
                    checkpointlists[key_id].append(1)
                    quick_reply_mainarg(sender, bot_reply)
                    return 'ok'
                elif message == 'my health':
                    print 'works'
                    users[key_id] = [['PPC1', 'PPC2', 'PPC3',
                                    'PPC4', 'PPC5','PPC6', 'PPC7',
                                    'NPC1', 'NPC2', 'NPC3',
                                    'NPC4', 'NPC5', 'NPC6'], []]
                    bot_reply = "Okay. What is the main reason you eat meat? Select one of the following: \n 1: I eat meat because of its nutritional value and source of protein \n 2: I eat meat because it\'s filling \n 3: I eat meat because it tastes good! \n 4: I eat meat because it\'s quick and easy to prepare \n 5: I eat meat because it\'s healthy and contributes to a balanced diet. \n 6: I eat meat because it offers more variety to my meals \n 7: Other"
                    checkpointlists[key_id].append(1)
                    quick_reply_mainarg(sender, bot_reply)
                    return 'ok'

                else:
                    checkpointlists[key_id].append(0)
                    bot_reply = "sorry, I didnt get that, please select one of the given values"
                    quick_reply_values(sender, bot_reply)
                    return 'ok'

                return "ok"


            def chatbot_reponse(possible_CAs, used_CAs):
                possible_CAs = [e for e in possible_CAs if e not in used_CAs]
                response = random.choice(possible_CAs)
                possible_CAs.remove(response)
                used_CAs.append(response)
                return response, possible_CAs, used_CAs

            if checkpointlists[key_id][-1] == 100:
                if message == 'i agree':
                    try:

                        reply_CA, possible_CAs, used_CAs = chatbot_reponse(users[key_id][0], users[key_id][1])
                        bot_reply = 'great, what do you think about this reason:'
                        reply(sender, bot_reply)
                        users[key_id][0] = possible_CAs
                        users[key_id][1] = used_CAs
                        bot_reply = args[reply_CA]
                        quick_reply_agreement(sender, bot_reply)
                        checkpointlists[key_id].append(100)
                        return 'ok'
                    except:
                        bot_reply = 'I ran out of arguments :) let\'s end the chat here. One more question. Please tell me what applies most to you:  \n  1: I definitely wouldn\'t  \n 2: I probably wouldn\'t  \n 3: I might   \n 4: I probably would   \n 5: I definitely would  \n consider reducing my meat consumption'

                        checkpointlists[key_id].append(3)
                        quick_reply_intention(sender, bot_reply)
                        return 'ok'
                if message == 'i disagree':
                    bot_reply = 'Why?'
                    reply(sender, bot_reply)
                    checkpointlists[key_id].append(1)
                    return 'ok'
                else:
                    try:
                        reply_CA, possible_CAs, used_CAs = chatbot_reponse(users[key_id][0], users[key_id][1])
                        bot_reply = 'seems like you did not agree or disagree when asked to. But I will forgive you, let\'s move on, what do you think about this reason:'
                        reply(sender, bot_reply)
                        users[key_id][0] = possible_CAs
                        users[key_id][1] = used_CAs
                        bot_reply = args[reply_CA]
                        quick_reply_agreement(sender, bot_reply)
                        checkpointlists[key_id].append(100)
                        return 'ok'
                    except:
                        bot_reply = 'I ran out of arguments :) let\'s end the chat here. One more question. Please tell me what applies most to you:  \n  1: I definitely wouldn\'t  \n 2: I probably wouldn\'t  \n 3: I might   \n 4: I probably would   \n 5: I definitely would  \n consider reducing my meat consumption'

                        checkpointlists[key_id].append(3)
                        quick_reply_intention(sender, bot_reply)
                        return 'ok'

            """
            if message == 'stop':
                bot_reply = "thank you so much for participating in this study! One more question. How likely you would consider reducing your meat consumption \n  1: Definitely wouldn\'t consider reducing meat consumption \n 2: Probably wouldn\'t consider reducing meat consumption \n 3: Might consider reducing meat consumption \n 4: Probably would consider reducing meat condumption \n 5: Definitely would consider reducing meat consumption"
                checkpointlists[key_id].append(3)
                quick_reply_intention(sender, bot_reply)
                return 'ok'
            """

            #add one more check here to check how long the message is in order to query once
            if len(message.split()) < 12 and message.isdigit() == False and checkpointlists[key_id][-1] != -1 and  checkpointlists[key_id][-2] != 0:
                bot_reply = query(message)
                reply(sender, bot_reply)
                checkpointlists[key_id].append(-1)
                return 'ok'


            if message != 'stop' and (checkpointlists[key_id][-1] == 1 or checkpointlists[key_id][-1] == -1):
                try:

                    reply_CA, possible_CAs, used_CAs = chatbot_reponse(users[key_id][0], users[key_id][1])
                    users[key_id][0] = possible_CAs
                    users[key_id][1] = used_CAs
                    starter_ = random.choice(starter)
                    understanding_ = random.choice(understanding)
                    bot_reply = starter_ + args[reply_CA]
                    reply(sender, understanding_)
                    quick_reply_agreement(sender, bot_reply)
                    checkpointlists[key_id].append(100)
                    return 'ok'
                except:
                    bot_reply = 'I ran out of arguments :) let\'s end the chat here. One more question. Please tell me what applies most to you:  \n  1: I definitely wouldn\'t  \n 2: I probably wouldn\'t  \n 3: I might   \n 4: I probably would   \n 5: I definitely would  \n consider reducing my meat consumption'
                    checkpointlists[key_id].append(3)
                    quick_reply_intention(sender, bot_reply)
                    return 'ok'
                return 'ok'

            '''
            if checkpointlists[key_id][-1] == 3:
                bot_reply = ' if you want to test it again, just type anything'
                reply(sender, bot_reply)
                # delete later
                del users[key_id]
                del checkpointlists[key_id]
                user_ids.remove(key_id)
                return 'ok'
            '''








        return 'ok'



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
