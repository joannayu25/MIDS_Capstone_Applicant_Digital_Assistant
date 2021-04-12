import json
import dateutil.parser
import datetime
from datetime import date
import time
import os
import math
import random
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': {
                'contentType': 'PlainText',
                'content': message
            }
        }
    }


def confirm_intent(session_attributes, intent_name, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': {
                'contentType': 'PlainText',
                'content': message
            }
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': {
                'contentType': 'PlainText',
                'content': message
            }
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }

def elicit_intent(session_attributes, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitIntent',
            'message': {
                'contentType': 'PlainText',
                'content': message
            }
        }
    }


def build_response_card(title, subtitle, options):
    """
    Build a responseCard with a title, subtitle, and an optional set of options which should be displayed as buttons.
    """
    buttons = None
    if options is not None:
        buttons = []
        for i in range(min(5, len(options))):
            buttons.append(options[i])

    return {
        'contentType': 'application/vnd.amazonaws.card.generic',
        'version': 1,
        'genericAttachments': [{
            'title': title,
            'subTitle': subtitle,
            'buttons': buttons
        }]
    }


""" --- Helper Functions --- """


def parse_int(n):
    try:
        return int(n)
    except ValueError:
        return float('nan')


def try_ex(func):
    """
    Call passed in function in try block. If KeyError is encountered return None.
    This function is intended to be used to safely access dictionary.

    Note that this function would have negative impact on performance.
    """

    try:
        return func()
    except KeyError:
        return None



def get_random_int(minimum, maximum):
    """
    Returns a random integer between min (included) and max (excluded)
    """
    min_int = math.ceil(minimum)
    max_int = math.floor(maximum)

    return random.randint(min_int, max_int - 1)


def agent(intent_request):
    user_name = ''
    if 'UserName' in intent_request['sessionAttributes']:
        user_name = ', '+ str(intent_request['sessionAttributes']['UserName'])
        
    need_agent = intent_request['currentIntent']['slots']['need_agent']
    leave_email = str(intent_request['currentIntent']['slots']['leave_email'])
    email = intent_request['currentIntent']['slots']['email']

    affirm = ['yes', 'yeah', 'yea', 'y', 'ye', 'sure', 'of course', 'you bet', 'i think so', 'yep', 'yup', 'okay', 'ok', 'k', 'absolutely']

    if need_agent in affirm and leave_email == 'None':
        msg = 'Would you like to provide your email address so one of our agents can follow up with you'+user_name+'?'
        return elicit_slot(
            intent_request['sessionAttributes'] , 
            intent_request['currentIntent']['name'], 
            intent_request['currentIntent']['slots'],             
            'leave_email', 
            msg)

    elif need_agent in affirm and leave_email in affirm and email == None:
        msg = 'Please provide your email address.'
        return elicit_slot(
            intent_request['sessionAttributes'] , 
            intent_request['currentIntent']['name'], 
            intent_request['currentIntent']['slots'],              
            'email', 
            msg)
            
    elif email != None:
        msg = 'Thank you for providing your email. Anything else you would like to know about MIDS? You can explore one of the other popular topics, like admissions requirement, curriculum difficulty, MIDS vs. bootcamp, or career prospect.'
        return elicit_intent(
            intent_request['sessionAttributes'],
            msg
            )   
    else: 
        msg = 'I see that you are not interested in requesting a follow-up with an agent by providing an email address. Anything else you would like to know about MIDS? You can explore one of the other popular topics, like admissions requirement, curriculum difficulty, MIDS vs. bootcamp, or career prospect.'
        return elicit_intent(
            intent_request['sessionAttributes'],
            msg
            ) 

""" --- Intents --- """


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'lambda_agent':
        return agent(intent_request)
    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)