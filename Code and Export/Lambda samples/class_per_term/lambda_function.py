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


def class_per_term(intent_request):
    affirm = ['yes', 'yeah', 'yea', 'y', 'ye', 'sure', 'of course', 'you bet', 'i think so', 'yep', 'yup', 'okay', 'ok', 'k', 'absolutely']
    class_count = int(intent_request['currentIntent']['slots']['class_count'])

    if class_count > 3:
        msg = 'You can only take up to 3 classes per semester. Considering the workload of each class, it will require careful planning to take 3 classes per semester.'
        return elicit_intent(
            intent_request['sessionAttributes'],
            msg
            )
    elif class_count == 3:
        msg = 'You can take 3 classes per semester, but students have said it is very challenging. It will require careful planning to take 3 classes per semester.'
        return elicit_intent(
            intent_request['sessionAttributes'],
            msg
            )
    elif class_count == 2:
        msg = 'Taking 2 classes per semester is manageable, but you would want to pair the right classes to control the workload if you also work full-time job and/or have family obligations.'
        return elicit_intent(
            intent_request['sessionAttributes'],
            msg
            ) 
    else:
        msg = 'Sure. You can take 1 class per semester, but you are required to take 2 classes in the first semester of MIDS.'
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
    if intent_name == 'lambda_classesPerTerm':
        return class_per_term(intent_request)
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