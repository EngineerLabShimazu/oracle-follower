from ask_sdk_model.services.monetization import InSkillProduct
from ask_sdk_core.handler_input import HandlerInput


def get_env_type(handler_input):
    if 'prd' in handler_input.context.invoked_function_arn:
        return 'prd'
    return 'stg'


def is_support_display(handler_input):
    try:
        if hasattr(
                handler_input.request_envelope.context.system.device.supported_interfaces,
                'display'):
            return (
                    handler_input.request_envelope.context.system.device.
                    supported_interfaces.display is not None)
    except:
        return False


def in_skill_product_response(handler_input: HandlerInput):
    locale = handler_input.request_envelope.request.locale
    ms = handler_input.service_client_factory.get_monetization_service()
    return ms.get_in_skill_products(locale)


def get_purchase_product(handler_input: HandlerInput, slot_name: str):
    resolutions_per_authority = \
    handler_input.request_envelope.request.intent.slots[
        slot_name].resolutions.resolutions_per_authority
    try:
        if not resolutions_per_authority:
            return None
        if not resolutions_per_authority[0]:
            return None
        if not resolutions_per_authority[0].values:
            return None
        if not resolutions_per_authority[0].values[0]:
            return None

        product = resolutions_per_authority[0].values[0].value
        return product
    except (AttributeError, ValueError, KeyError, IndexError):
        return None


def get_skill_product(in_skill_response,
                      purchase_product_id) -> InSkillProduct:
    for skill_product in in_skill_response.in_skill_products:
        if skill_product.reference_name == purchase_product_id:
            return skill_product
