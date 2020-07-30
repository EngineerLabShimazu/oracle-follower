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
                or is_intent_name("GaneshaShopIntent")(handler_input)
                or is_intent_name("TurnTimesIntent")(handler_input)
                or is_intent_name("TurnIntent")(handler_input)
                or is_intent_name("ResultIntent")(handler_input)
                or is_intent_name("SkipIntent")(handler_input)
                or is_intent_name("AMAZON.NextIntent")(handler_input)
                or is_intent_name("AMAZON.YesIntent")(handler_input)
                or is_intent_name("AMAZON.NoIntent")(handler_input))

    def handle(self, handler_input: HandlerInput) -> Response:
        session = handler_input.attributes_manager.session_attributes
        state = session.get('state')
        node = session.get('node')
        destinations_choice = session.get('destinations_choice')
        total_ticket_amount = session.get('total_ticket_amount')

        fof_sfn_input = {
            'alexa_user_id': handler_input.request_envelope.context.system.user.user_id,
            'IsPreResponse': False,
            'state': state,
            'node': node,
            'destinations_choice': destinations_choice,
            'total_ticket_amount': total_ticket_amount,
            'env_type': util.get_env_type(handler_input)
        }

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

        speech_text = response["response_text"]

        image_url = response.get('image_url')
        bg_image_url = response.get('bg_image_url')
        image_title = response.get('image_title')
        image_text = response.get('image_text')
        if image_url:
            img_obj = Image(sources=[ImageInstance(url=image_url)])
            bg_img_obj = Image(sources=[ImageInstance(url=bg_image_url)])
            if util.is_support_display(handler_input):
                handler_input.response_builder.add_directive(
                    RenderTemplateDirective(
                        BodyTemplate7(
                            back_button=BackButtonBehavior.VISIBLE,
                            image=img_obj,
                            background_image=bg_img_obj,
                            title=image_title)
                    )
                )
            else:
                handler_input.response_builder.set_card(
                    ui.StandardCard(
                        title=image_title,
                        text=image_text,
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
