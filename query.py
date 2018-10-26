import random
from collections import Counter
expl = ['that is', 'because', 'due to', 'since', 'that\'s', 'thats', 'hence', 'therefore']
neg = ['not', 'dont', 'arent', 'cant', 'wouldnt', 'isnt', 'don\'t', 'aren\'t', 'can\'t', 'wouldn\'t', 'isn\'t']
def query(statement):  #statement = userinput

    quest = "? "
    statement = statement.lower()

    word_tok = statement.split()
    statement_length = len(word_tok)
    if statement_length == 1:
        responses = ['can you expand that please :) why so?',
                    'that\'s not enough, elaborate please',
                    'please tell me more...', 'expand please...',
                    'please expand :)']
        resp = random.choice(responses)
        response = statement + quest + resp
        return response



    k = dict((i, statement.count(i)) for i in neg)
    neg_nr = sum(k.values())

    if neg_nr > 0:
        responses = ['Why not?',
                    'Tell me a bit more. Why not?']
        response = random.choice(responses)
        return response

    d = dict((i, statement.count(i)) for i in expl)
    expl_nr = sum(d.values())

    if expl_nr > 0:
        print "i should be here"
        responses = ['Okay, but what makes you say that?',
                    'Could you go into more detail? Why do you say that?',
                    'Fair enough. But what makes you say that?',
                    'Elaborate please. Why do you say that? ',
                    'A bit more detail please. What makes you say that?']
        response = random.choice(responses)
        return response




    if statement_length <= 5:
        responses = ['a bit more detail please! Why?',
                    'Why?', 'Okay, but why?',
                    'Why? Tell me :)']
        response = random.choice(responses)
        return response

    if statement_length > 5:
        responses = ['can you expand that please :) why so?',
                    'elaborate please...',
                    'please tell me more...',
                    'expand please...', 'please expand :)']
        response = random.choice(responses)
        return response
