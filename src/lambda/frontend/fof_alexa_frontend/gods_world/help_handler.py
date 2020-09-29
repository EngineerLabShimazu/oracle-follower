from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import ui

import util


class GodsWorldHelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session = handler_input.attributes_manager.session_attributes
        scene = session.get('scene')
        if not scene:
            return False
        return scene == 'gods_world' and is_intent_name("AMAZON.HelpIntent")(
            handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = 'ここは神様の国、神界。神界ではさまざまな神様の力を借りることができます。現在はオルぺの力で、物語３つを遊ぶことができます。「拒否部下と魔王軍」「魔女と猫と盲目の狩人」「夜道騒動フォリス」から選んでください。オルぺによるその他の物語追加や、「神、ガネーシャ」によるショップなどは、後日追加される予定です。楽しみにお待ちください。どの物語を遊びますか？'
        handler_input.response_builder.speak(speech_text).ask(speech_text)
        handler_input.response_builder.set_should_end_session(False)
        handler_input.response_builder.set_card(
            ui.StandardCard(
                title='どの物語を遊びますか？',
                text='・拒否部下と魔王軍\r\n'
                     '・魔女と猫と盲目の狩人\r\n'
                     '・夜道騒動フォリス'
            )
        )
        return handler_input.response_builder.response
