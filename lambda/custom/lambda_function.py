# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK.
import json
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

import sfn_ctl
import util

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_user_id(handler_input):
    return handler_input.request_envelope.context.system.user.user_id


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        destinations_choice = handler_input.attributes_manager.session_attributes.get(
            'destinations_choice')
        fof_sfn_input = {
            'alexa_user_id': handler_input.request_envelope.context.system.user.user_id,
            'IsPreResponse': False,
            'state': 'launch',
            'destinations_choice': destinations_choice,
            'env_type': util.get_env_type(handler_input)
        }
        response = sfn_ctl.execute(fof_sfn_input)
        if response.get('destinations_choice'):
            handler_input.attributes_manager.session_attributes[
                'destinations_choice'] = response['destinations_choice']
        handler_input.attributes_manager.session_attributes['state'] = \
            response['state']
        print(f'response: {response}, type: {type(response)}')
        speech_text = response["response_text"]
        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_should_end_session(
            response.get('set_should_end_session', True))
        return handler_input.response_builder.response


class DestinationIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):  # type: (HandlerInput) -> bool
        return is_intent_name("DestinationIntent")(handler_input)

    def handle(self,
               handler_input):  # type: (HandlerInput) -> Union[None, Response]
        village = handler_input.request_envelope.request.intent.slots[
            'village'].value
        destinations_choice = handler_input.attributes_manager.session_attributes.get(
            'destinations_choice')
        fof_sfn_input = {
            'alexa_user_id': handler_input.request_envelope.context.system.user.user_id,
            'IsPreResponse': False,
            'state': 'Oracle',
            'destination': village,
            'destinations_choice': destinations_choice,
            'env_type': util.get_env_type(handler_input)
        }
        response = sfn_ctl.execute(fof_sfn_input)
        speech_text = response["response_text"]
        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_should_end_session(
            response.get('set_should_end_session', True))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        fof_sfn_input = {
            'alexa_user_id': handler_input.request_envelope.context.system.user.user_id,
            'IsPreResponse': True,
            'intent': 'HelpIntent',
            'destinations':
                handler_input.attributes_manager.session_attributes[
                    'destinations'],
            'env_type': util.get_env_type(handler_input)
        }
        response = sfn_ctl.execute(fof_sfn_input)
        speech_text = response["response_text"]
        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        fof_sfn_input = {
            'alexa_user_id': handler_input.request_envelope.context.system.user.user_id,
            'IsPreResponse': True,
            'intent': 'CancelOrStopIntent',
            'env_type': util.get_env_type(handler_input)
        }
        response = sfn_ctl.execute(fof_sfn_input)
        handler_input.response_builder.speak(response["response_text"])
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


# The intent reflector is used for interaction model testing and debugging.
# It will simply repeat the intent the user said. You can create custom handlers
# for your intents by defining them above, then also adding them to the request
# handler chain below.
class IntentReflectorHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = handler_input.request_envelope.request.intent.name
        speech_text = ("You just triggered {}").format(intent_name)
        handler_input.response_builder.speak(
            speech_text).set_should_end_session(True)
        return handler_input.response_builder.response


# Generic error handling to capture any syntax or routing errors. If you receive an error
# stating the request handler chain is not found, you have not implemented a handler for
# the intent being invoked or included it in the skill builder below.
class ErrorHandler(AbstractExceptionHandler):
    """Catch-all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        speech_text = "Sorry, I couldn't understand what you said. Please try again."
        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_should_end_session(True)
        return handler_input.response_builder.response


# This handler acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.
sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(DestinationIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(
    IntentReflectorHandler())  # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(ErrorHandler())

handler = sb.lambda_handler()
