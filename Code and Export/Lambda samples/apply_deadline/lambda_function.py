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


def deadline(intent_request):
    summer21_start = date(2021, 5, 3)
        
    fall21_start = date(2021, 8, 23)
    fall21_early = date(2021, 3, 31)
    fall21_priority = date(2021, 4, 28)
    fall21_final = date(2021, 5, 26)
    
    spring22_start = date(2022, 1, 3)
    spring22_early = date(2021, 8, 11)
    spring22_priority = date(2021,9,8)
    spring22_final = date(2021,9,29)

    today = date.today()
    months_deadline = int((fall21_final - today).days/30)

    user_name = str(intent_request['sessionAttributes']['UserName'])

    fall_deadline = intent_request['currentIntent']['slots']['fall_deadline']
    affirm = ['yes', 'yeah', 'yea', 'y', 'ye', 'sure', 'of course', 'you bet', 'i think so', 'yep', 'yup', 'okay', 'ok', 'k', 'absolutely']
    if fall_deadline.lower() in affirm:
        msg = 'I am glad you are interested in the application deadline, '+user_name+'! The Fall semester will start '+str(fall21_start)+'. The deadline is '+str(fall21_final)+'. There is still '+str(months_deadline)+' months to apply! Would you like to find out about the application requirement?'
        #elicit_slot(intent_request['sessionAttributes'] , intent_request['currentIntent']['name'], msg)
        return confirm_intent(
            intent_request['sessionAttributes'],
            'Application_GeneralRequirements',
            {}, 
            msg 
            )
    else:
        msg = 'Sure. Anything else you would like to know about MIDS? You can explore one of the other most popular topics, like curriculum difficulty, MIDS vs. bootcamp, or career prospect.'
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
    if intent_name == 'lambda_deadline':
        return deadline(intent_request)
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
