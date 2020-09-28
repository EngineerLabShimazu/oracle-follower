import sfn_ctl
import util

from typing import Optional

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import Response
from ask_sdk_model import ui
from ask_sdk_model.interfaces.display import (
    RenderTemplateDirective, BodyTemplate7, BackButtonBehavior,
    ImageInstance, Image)

from scenes import Scenes


class GaneshaShopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        session = handler_input.attributes_manager.session_attributes
        scene = session.get('scene')
        if not scene:
            return False
        return scene == 'gods_world' and \
               is_intent_name("GaneshaShopIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Optional[Response]:
        session = handler_input.attributes_manager.session_attributes
        destinations_choice = session.get('destinations_choice')

        fof_sfn_input = {
            'alexa_user_id': handler_input.request_envelope.context.system.user.user_id,
            'IsPreResponse': False,
            'intent': 'GaneshaShopIntent',
            'state': 'Ganesha',
            'destinations_choice': destinations_choice,
            'env_type': util.get_env_type(handler_input),
        }

        if 'node' in session:
            if session.get('state') == 'Ganesha':
                fof_sfn_input['node'] = session['node']

        response = sfn_ctl.execute(fof_sfn_input)
        session['scene'] = Scenes.ganesha_shop

        if 'state' in response:
            session['state'] = response['state']

        if 'node' in response:
            session['node'] = response['node']

        if 'turn_times' in response:
            session['turn_times'] = response['turn_times']

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
                            title='')
                    )
                )
            else:
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
            speech_text)
        return handler_input.response_builder.response
