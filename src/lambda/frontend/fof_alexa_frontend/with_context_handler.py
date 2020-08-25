from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model import ui
from ask_sdk_model.interfaces.display import (
    RenderTemplateDirective, BodyTemplate7, BackButtonBehavior,
    ImageInstance, Image)

import sfn_ctl
import util


def valid_turn_times(turn_times: int) -> bool:
    if turn_times in [1, 10]:
        return True
    return False


class WithContextIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return (is_intent_name("DestinationIntent")(handler_input)
                or is_intent_name("TurnTimesIntent")(handler_input)
                or is_intent_name("TurnIntent")(handler_input)
                or is_intent_name("ResultIntent")(handler_input)
                or is_intent_name("SkipIntent")(handler_input)
                or is_intent_name("AMAZON.NextIntent")(handler_input)
                or is_intent_name("AMAZON.NoIntent")(handler_input))

    def handle(self, handler_input: HandlerInput) -> Response:
        session = handler_input.attributes_manager.session_attributes
        state = session.get('state')
        node = session.get('node')
        destinations_choice = session.get('destinations_choice')
        total_ticket_amount = session.get('total_ticket_amount')
        turn_times = session.get('turn_times')
        not_enough_gem = session.get('not_enough_gem')

        fof_sfn_input = {
            'alexa_user_id': handler_input.request_envelope.context.system.user.user_id,
            'IsPreResponse': False,
            'intent': handler_input.request_envelope.request.intent.name,
            'state': state,
            'node': node,
            'destinations_choice': destinations_choice,
            'total_ticket_amount': total_ticket_amount,
            'turn_times': turn_times,
            'not_enough_gem': not_enough_gem,
            'env_type': util.get_env_type(handler_input)
        }

        if state == 'ganesha' and node == 'launch':
            if handler_input.request_envelope.request.intent.name == 'AMAZON.NoIntent':
                speech = '本日も祈りを受け入れてくださり、ありがとうございました。 ' \
                         'また信仰を捧げさせていただく機会を、どうか、お与えくださいませ。'
                handler_input.response_builder.speak(speech).ask(
                    speech).set_should_end_session(True)
                return handler_input.response_builder.response

        slots = handler_input.request_envelope.request.intent.slots
        if slots:
            village = slots['village'].value if 'village' in slots else ''
            fof_sfn_input['destination'] = village

            if 'turn_times' in slots:
                turn_times = int(slots['turn_times'].value)
                if not valid_turn_times(turn_times):
                    speech_text = '一回か十回で！'
                    handler_input.response_builder.speak(speech_text).ask(
                        speech_text)
                    return handler_input.response_builder.response
                fof_sfn_input['turn_times'] = turn_times

        response = sfn_ctl.execute(fof_sfn_input)
        print(f'response: {response}, type: {type(response)}')

        if 'state' in response:
            session['state'] = response['state']

        if 'node' in response:
            session['node'] = response['node']

        if 'destinations_choice' in response:
            session['destinations_choice'] = response['destinations_choice']

        if 'turn_times' in response:
            session['turn_times'] = response['turn_times']

        if 'total_ticket_amount' in response:
            session['total_ticket_amount'] = response['total_ticket_amount']

        if 'product_name' in response:
            session['product_name'] = response['product_name']

        if 'not_enough_gem' in response:
            session['not_enough_gem'] = response['not_enough_gem']

        speech_text = response["response_text"]

        image_url = response.get('image_url')
        if image_url:
            handler_input.response_builder.set_card(
                ui.StandardCard(
                    title='',
                    text='',
                    image=ui.Image(
                        small_image_url=image_url,
                        large_image_url=image_url
                    )
                )
            )

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_should_end_session(
            response.get('set_should_end_session', True))
        return handler_input.response_builder.response
