# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK.
import logging
from typing import Optional

from ask_sdk.standard import StandardSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model import ui
from ask_sdk_model.interfaces.display import (
    RenderTemplateDirective, BodyTemplate7, BackButtonBehavior,
    ImageInstance, Image)
from ask_sdk_model.interfaces.connections import SendRequestDirective
from ask_sdk_model.interfaces.monetization.v1 import PurchaseResult

import sfn_ctl
import util

from with_context_handler import WithContextIntentHandler

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
            'state': 'Launch',
            'destinations_choice': destinations_choice,
            'env_type': util.get_env_type(handler_input)
        }
        response = sfn_ctl.execute(fof_sfn_input)
        if response.get('destinations_choice'):
            handler_input.attributes_manager.session_attributes[
                'destinations_choice'] = response['destinations_choice']
        handler_input.attributes_manager.session_attributes['state'] = \
            response['state']

        if response.get('node'):
            handler_input.attributes_manager.session_attributes['node'] = \
                response['node']

        print(f'response: {response}, type: {type(response)}')
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


# class DestinationIntentHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):  # type: (HandlerInput) -> bool
#         return is_intent_name("DestinationIntent")(handler_input)
#
#     def handle(self,
#                handler_input):  # type: (HandlerInput) -> Union[None, Response]
#         village = handler_input.request_envelope.request.intent.slots[
#             'village'].value
#         destinations_choice = handler_input.attributes_manager.session_attributes.get(
#             'destinations_choice')
#         state = handler_input.attributes_manager.session_attributes.get(
#             'state')
#         fof_sfn_input = {
#             'alexa_user_id': handler_input.request_envelope.context.system.user.user_id,
#             'IsPreResponse': False,
#             'state': state,
#             'destination': village,
#             'destinations_choice': destinations_choice,
#             'env_type': util.get_env_type(handler_input),
#         }
#
#         node = handler_input.attributes_manager.session_attributes.get(
#             'node')
#         if node:
#             fof_sfn_input['node'] = node
#
#         response = sfn_ctl.execute(fof_sfn_input)
#         speech_text = response["response_text"]
#
#         if response.get('node'):
#             handler_input.attributes_manager.session_attributes['node'] = \
#                 response['node']
#
#         image_url = response.get('image_url')
#         if image_url:
#             handler_input.response_builder.set_card(
#                 ui.StandardCard(
#                     title='title sample',
#                     text='text sample',
#                     image=ui.Image(
#                         small_image_url=image_url,
#                         large_image_url=image_url
#                     )
#                 )
#             )
#
#         handler_input.response_builder.speak(speech_text).ask(
#             speech_text).set_should_end_session(
#             response.get('set_should_end_session', True))
#         return handler_input.response_builder.response


class GaneshaShopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("GaneshaShopIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Optional[Response]:
        session = handler_input.attributes_manager.session_attributes
        destinations_choice = session.get('destinations_choice')

        fof_sfn_input = {
            'alexa_user_id': handler_input.request_envelope.context.system.user.user_id,
            'IsPreResponse': False,
            'state': 'Ganesha',
            'destinations_choice': destinations_choice,
            'env_type': util.get_env_type(handler_input),
        }

        if 'node' in session:
            if session.get('state') == 'Ganesha':
                fof_sfn_input['node'] = session['node']

        response = sfn_ctl.execute(fof_sfn_input)
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
            speech_text)
        return handler_input.response_builder.response


# class TurnTimesIntentHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):  # type: (HandlerInput) -> bool
#         return is_intent_name("TurnTimesIntent")(handler_input)
#
#     def valid_turn_times(self, turn_times: int) -> bool:
#         if turn_times in [1, 10]:
#             return True
#         return False
#
#     def handle(self,
#                handler_input):  # type: (HandlerInput) -> Union[None, Response]
#         turn_times = int(handler_input.request_envelope.request.intent.slots[
#                              'turn_times'].value)
#         if not self.valid_turn_times(turn_times):
#             speech_text = '一回か十回で！'
#             handler_input.response_builder.speak(speech_text).ask(
#                 speech_text)
#             return handler_input.response_builder.response
#
#         state = handler_input.attributes_manager.session_attributes.get(
#             'state')
#
#         fof_sfn_input = {
#             'alexa_user_id': handler_input.request_envelope.context.system.user.user_id,
#             'IsPreResponse': False,
#             'state': state,
#             'turn_times': turn_times,
#             'env_type': util.get_env_type(handler_input),
#         }
#
#         node = handler_input.attributes_manager.session_attributes.get(
#             'node')
#         if node:
#             fof_sfn_input['node'] = node
#
#         response = sfn_ctl.execute(fof_sfn_input)
#         handler_input.attributes_manager.session_attributes['state'] = \
#             response['state']
#         speech_text = response["response_text"]
#
#         if response.get('node'):
#             handler_input.attributes_manager.session_attributes['node'] = \
#                 response['node']
#
#         if response.get('turn_times'):
#             handler_input.attributes_manager.session_attributes['turn_times'] = \
#                 response['turn_times']
#
#         if response.get('total_ticket_amount'):
#             handler_input.attributes_manager.session_attributes[
#                 'total_ticket_amount'] = \
#                 response['total_ticket_amount']
#
#         image_url = response.get('image_url')
#         if image_url:
#             handler_input.response_builder.set_card(
#                 ui.StandardCard(
#                     title='title sample',
#                     text='text sample',
#                     image=ui.Image(
#                         small_image_url=image_url,
#                         large_image_url=image_url
#                     )
#                 )
#             )
#
#         handler_input.response_builder.speak(speech_text).ask(
#             speech_text)
#         return handler_input.response_builder.response


class UseIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name('UseIntent')(handler_input)

    def handle(self, handler_input: HandlerInput) -> Optional[Response]:
        session = handler_input.attributes_manager.session_attributes
        node = session.get('node')
        fof_sfn_input = {
            'alexa_user_id': handler_input.request_envelope.context.system.user.user_id,
            'IsPreResponse': True,
            'intent': 'UseIntent',
            'node': node,
            'env_type': util.get_env_type(handler_input)
        }
        response = sfn_ctl.execute(fof_sfn_input)

        if response.get('state') == 'Buy':
            in_skill_response = util.in_skill_product_response(
                handler_input)

            # TODO: gem_3000/日 が実装されたら未購入なら3000を優先。
            skill_product = util.get_skill_product(
                in_skill_response, 'gem_300')

            return handler_input.response_builder.add_directive(
                SendRequestDirective(
                    name='Buy',
                    payload={
                        'InSkillProduct': {
                            'productId': skill_product.product_id
                        }
                    },
                    token='correlationToken'
                )
            ).response

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
        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response


# class TurnIntentHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         # type: (HandlerInput) -> bool
#         return is_intent_name("TurnIntent")(handler_input)
#
#     def handle(self, handler_input):
#         # type: (HandlerInput) -> Response
#
#         state = handler_input.attributes_manager.session_attributes.get(
#             'state')
#
#         turn_times = handler_input.attributes_manager.session_attributes.get(
#             'turn_times', 0)
#
#         destinations_choice = handler_input.attributes_manager.session_attributes.get(
#             'destinations_choice')
#
#         fof_sfn_input = {
#             'alexa_user_id': handler_input.request_envelope.context.system.user.user_id,
#             'IsPreResponse': False,
#             'state': state,
#             'turn_times': turn_times,
#             'destinations_choice': destinations_choice,
#             'env_type': util.get_env_type(handler_input)
#         }
#
#         node = handler_input.attributes_manager.session_attributes.get(
#             'node')
#         if node:
#             fof_sfn_input['node'] = node
#
#         response = sfn_ctl.execute(fof_sfn_input)
#
#         if response.get('node'):
#             handler_input.attributes_manager.session_attributes['node'] = \
#                 response['node']
#
#         if response.get('turn_times'):
#             handler_input.attributes_manager.session_attributes['turn_times'] = \
#                 response['turn_times']
#
#         speech_text = response["response_text"]
#         handler_input.response_builder.speak(speech_text).ask(speech_text)
#         return handler_input.response_builder.response


# class ResultIntentHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         # type: (HandlerInput) -> bool
#         return is_intent_name("ResultIntent")(handler_input)
#
#     def handle(self, handler_input):
#         # type: (HandlerInput) -> Response
#
#         total_ticket_amount = handler_input.attributes_manager.session_attributes.get(
#             'total_ticket_amount')
#
#         state = handler_input.attributes_manager.session_attributes.get(
#             'state')
#
#         fof_sfn_input = {
#             'alexa_user_id': handler_input.request_envelope.context.system.user.user_id,
#             'IsPreResponse': False,
#             'state': state,
#             'node': 'result',
#             'total_ticket_amount': total_ticket_amount,
#             'env_type': util.get_env_type(handler_input)
#         }
#
#         response = sfn_ctl.execute(fof_sfn_input)
#
#         speech_text = response["response_text"]
#         handler_input.response_builder.speak(speech_text).ask(speech_text)
#         return handler_input.response_builder.response


# class SkipIntentHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         # type: (HandlerInput) -> bool
#         return is_intent_name("SkipIntent")(handler_input) or is_intent_name(
#             "AMAZON.NextIntent")(handler_input)
#
#     def handle(self, handler_input):
#         # type: (HandlerInput) -> Response
#
#         total_ticket_amount = handler_input.attributes_manager.session_attributes.get(
#             'total_ticket_amount')
#
#         state = handler_input.attributes_manager.session_attributes.get(
#             'state')
#
#         fof_sfn_input = {
#             'alexa_user_id': handler_input.request_envelope.context.system.user.user_id,
#             'IsPreResponse': False,
#             'state': state,
#             'node': 'result',
#             'total_ticket_amount': total_ticket_amount,
#             'env_type': util.get_env_type(handler_input)
#         }
#
#         response = sfn_ctl.execute(fof_sfn_input)
#
#         speech_text = response["response_text"]
#         handler_input.response_builder.speak(speech_text).ask(speech_text)
#         return handler_input.response_builder.response


class YesIntentHandler(AbstractRequestHandler):
    """Handler for Yes Intent."""

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        session = handler_input.attributes_manager.session_attributes
        state = session.get('state')
        node = session.get('node')
        destinations_choice = session.get('destinations_choice')
        total_ticket_amount = session.get('total_ticket_amount')
        turn_times = session.get('turn_times')
        fof_sfn_input = {
            'alexa_user_id': handler_input.request_envelope.context.system.user.user_id,
            'IsPreResponse': False,
            'intent': 'AMAZON.YesIntent',
            'state': state,
            'node': node,
            'destinations_choice': destinations_choice,
            'total_ticket_amount': total_ticket_amount,
            'turn_times': turn_times,
            'env_type': util.get_env_type(handler_input)
        }

        node = session.get('node')
        if node:
            fof_sfn_input['node'] = node
            if node == 'recommend_gem':
                in_skill_response = util.in_skill_product_response(
                    handler_input)

                # TODO: gem_3000/日 が実装されたら未購入なら3000を優先。
                skill_product = util.get_skill_product(
                    in_skill_response, 'gem_300')

                return handler_input.response_builder.add_directive(
                    SendRequestDirective(
                        name='Buy',
                        payload={
                            'InSkillProduct': {
                                'productId': skill_product.product_id
                            }
                        },
                        token='correlationToken'
                    )
                ).response

        print(fof_sfn_input)
        response = sfn_ctl.execute(fof_sfn_input)

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

        speech_text = response["response_text"]
        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response


# class NoIntentHandler(AbstractRequestHandler):
#     """Handler for Help Intent."""
#
#     def can_handle(self, handler_input):
#         # type: (HandlerInput) -> bool
#         return is_intent_name("AMAZON.NoIntent")(handler_input)
#
#     def handle(self, handler_input):
#         # type: (HandlerInput) -> Response
#         fof_sfn_input = {
#             'alexa_user_id': handler_input.request_envelope.context.system.user.user_id,
#             'IsPreResponse': False,
#             'turn_times': 0,
#             'intent': 'No',
#             'env_type': util.get_env_type(handler_input)
#         }
#
#         state = handler_input.attributes_manager.session_attributes.get(
#             'state')
#         if state:
#             fof_sfn_input['state'] = state
#
#         node = handler_input.attributes_manager.session_attributes.get(
#             'node')
#         if node:
#             fof_sfn_input['node'] = node
#
#         response = sfn_ctl.execute(fof_sfn_input)
#
#         if response.get('node'):
#             handler_input.attributes_manager.session_attributes['node'] = \
#                 response['node']
#
#         if response.get('turn_times'):
#             handler_input.attributes_manager.session_attributes['turn_times'] = \
#                 response['turn_times']
#
#         speech_text = response["response_text"]
#         handler_input.response_builder.speak(speech_text).ask(speech_text)
#
#         end_session = response.get('set_should_end_session', False)
#         handler_input.response_builder.set_should_end_session(end_session)
#
#         return handler_input.response_builder.response


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
            'destinations_choice':
                handler_input.attributes_manager.session_attributes.get(
                    'destinations_choice'),
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

        image_url = response.get('image_url')
        if image_url:
            handler_input.response_builder.set_card(
                ui.StandardCard(
                    title='title sample',
                    text='text sample',
                    image=ui.Image(
                        small_image_url=image_url,
                        large_image_url=image_url
                    )
                )
            )

        handler_input.response_builder.set_should_end_session(True)

        return handler_input.response_builder.response


class BuyHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name('BuyIntent')(handler_input)

    def handle(self, handler_input: HandlerInput):
        purchase_product = util.get_purchase_product(
            handler_input, 'product_category')

        if not purchase_product:
            speech_text = 'すみません、分かりませんでした。'
            ask = 'もう一度お願いできますか？'
            handler_input.response_builder.speak(speech_text + ask).ask(
                ask).set_should_end_session(False)
            return handler_input.response_builder.response

        in_skill_response = util.in_skill_product_response(handler_input)
        if not in_skill_response:
            raise ValueError('購入できる商品を見つけられませんでした。')

        skill_product = util.get_skill_product(
            in_skill_response, purchase_product.id)

        return handler_input.response_builder.add_directive(
            SendRequestDirective(
                name='Buy',
                payload={
                    'InSkillProduct': {
                        'productId': skill_product.product_id
                    }
                },
                token='correlationToken'
            )
        ).response


class BuyResponseHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return (is_request_type('Connections.Response')(handler_input)
                and handler_input.request_envelope.request.name == 'Buy')

    def handle(self, handler_input: HandlerInput):
        in_skill_response = util.in_skill_product_response(handler_input)
        if not in_skill_response:
            return handler_input.response_builder.speak(
                '購入処理でエラーが発生しました。'
                'もう一度試すか、カスタマーサービスにご連絡ください。'
            ).response
        purchase_result = handler_input.request_envelope.request.payload.get(
            'purchaseResult')
        should_end_session = False
        speech = '購入フローにはいりませんでした。'
        if purchase_result == PurchaseResult.ACCEPTED.value:
            # ユーザーは製品の購入オファーを受け入れました

            # ex) amzn1.adg.product.XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
            product_id = handler_input.request_envelope.request.payload.get(
                'productId')

            product = util.get_skill_product(
                in_skill_response, product_id=product_id)
            fof_sfn_input = {
                'alexa_user_id': handler_input.request_envelope.context.system.user.user_id,
                'IsPreResponse': True,
                'intent': 'Connections.Response',
                'product_reference_name': product.reference_name,
                'env_type': util.get_env_type(handler_input)
            }
            response = sfn_ctl.execute(fof_sfn_input)
            speech = response["response_text"]
        elif purchase_result == PurchaseResult.DECLINED.value:
            # ユーザーは製品の購入オファーを拒否しました
            speech = 'ユーザーは製品の購入オファーを拒否しました'
        elif purchase_result == PurchaseResult.ERROR.value:
            # 内部エラーが発生しました
            speech = '内部エラーが発生しました'
            should_end_session = True
        elif purchase_result == PurchaseResult.ALREADY_PURCHASED.value:
            # ユーザーはすでに製品を購入しています
            speech = 'ユーザーはすでに製品を購入しています'
        elif purchase_result == PurchaseResult.NOT_ENTITLED.value:
            # ユーザーは資格のない製品をキャンセル/返品しようとしました
            speech = 'ユーザーは資格のない製品をキャンセルまたは返品しようとしました'
        handler_input.response_builder.speak(speech).ask(
            speech).set_should_end_session(should_end_session)
        return handler_input.response_builder.response


class WhatCanIBuyHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name('WhatCanIBuyIntent')(handler_input)

    def handle(self, handler_input: HandlerInput):
        in_skill_response = util.in_skill_product_response(handler_input)
        if not in_skill_response:
            handler_input.response_builder.set_should_end_session(True)
            return handler_input.response_builder.speak('現在購入できる商品がございません。')

        purchasable_products = util.get_speakable_products(in_skill_response)
        speech = f'現在購入可能な商品は、{purchasable_products}です。' \
                 f'詳しく知りたい場合には、ジェムパック大について教えて、のように言ってください。'
        handler_input.response_builder.speak(speech)

        skill_product = util.get_skill_product(
            in_skill_response, 'gem_1000')

        return handler_input.response_builder.add_directive(
            SendRequestDirective(
                name='Buy',
                payload={
                    'InSkillProduct': {
                        'productId': skill_product.product_id
                    }
                },
                token='correlationToken'
            )
        ).response


class ProductDetailHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name('ProductDetailIntent')(handler_input)

    def handle(self, handler_input):
        in_skill_response = util.in_skill_product_response(handler_input)
        if not in_skill_response:
            handler_input.response_builder.speak('現在購入できる商品はございません。')
            handler_input.response_builder.set_should_end_session(True)
            return handler_input.response_builder.response

        purchase_product = util.get_purchase_product(
            handler_input, 'product_category')
        skill_product = util.get_skill_product(
            in_skill_response, purchase_product.id)

        handler_input.response_builder.speak(skill_product.summary)
        return handler_input.response_builder.add_directive(
            SendRequestDirective(
                name='Buy',
                payload={
                    'InSkillProduct': {
                        'productId': skill_product.product_id
                    }
                },
                token='correlationToken'
            )
        ).response


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
sb = StandardSkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(WithContextIntentHandler())
# sb.add_request_handler(DestinationIntentHandler())
sb.add_request_handler(GaneshaShopIntentHandler())
# sb.add_request_handler(TurnTimesIntentHandler())
sb.add_request_handler(UseIntentHandler())
# sb.add_request_handler(TurnIntentHandler())
# sb.add_request_handler(ResultIntentHandler())
# sb.add_request_handler(SkipIntentHandler())
sb.add_request_handler(YesIntentHandler())
# sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_request_handler(BuyHandler())
sb.add_request_handler(BuyResponseHandler())
sb.add_request_handler(WhatCanIBuyHandler())
sb.add_request_handler(ProductDetailHandler())

sb.add_request_handler(
    IntentReflectorHandler())  # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(ErrorHandler())

handler = sb.lambda_handler()
