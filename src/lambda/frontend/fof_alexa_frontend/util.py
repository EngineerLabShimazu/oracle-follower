from ask_sdk_model.services.monetization import InSkillProduct
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.services.monetization import (
    EntitledState, PurchasableState,
    )


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
    """
    :return: {
        '_InSkillProductsResponse__discriminator_value': None
        'in_skill_products': [
            {
                "active_entitlement_count": int,
                "entitled": "NOT_ENTITLED",
                "entitlement_reason": "NOT_PURCHASED",
                "name": str,
                "object_type": "CONSUMABLE",
                "product_id": str,
                "purchasable": "PURCHASABLE",
                "purchase_mode": ex) "TEST",
                "reference_name": ex) "gem_300",
                "summary": ex) "神界のあらゆる奇跡と交換できる信用物"
                },
            ]
        'is_truncated': None,
        'next_token': None,
        'truncated': False
        }
    """
    locale = handler_input.request_envelope.request.locale
    ms = handler_input.service_client_factory.get_monetization_service()
    return ms.get_in_skill_products(locale)


def get_purchasable_products(in_skill_response) -> list:
    return [product for product in in_skill_response.in_skill_products
            if product.entitled == EntitledState.NOT_ENTITLED
            and product.purchasable == PurchasableState.PURCHASABLE]


def get_speakable_products(in_skill_response, products=None) -> str:
    if not products:
        products = in_skill_response.in_skill_products
    product_names = [product.name for product in products]
    if len(product_names) > 1:
        # If more than one, add and 'and' in the end
        speech = " と ".join(
            [", ".join(product_names[:-1]), product_names[-1]])
    else:
        # If one or none, then return the list content in a string
        speech = ", ".join(product_names)
    return speech


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
                      purchase_product_id=None,
                      product_id=None) -> InSkillProduct:
    """
    :return: InSkillProduct attributes are {
        "active_entitlement_count": int,
        "entitled": "NOT_ENTITLED",
        "entitlement_reason": "NOT_PURCHASED",
        "name": str,
        "object_type": "CONSUMABLE",
        "product_id": str,
        "purchasable": "PURCHASABLE",
        "purchase_mode": ex) "TEST",
        "reference_name": ex) "gem_300",
        "summary": ex) "神界のあらゆる奇跡と交換できる信用物"
        }
    """
    for skill_product in in_skill_response.in_skill_products:
        if purchase_product_id and \
                skill_product.reference_name == purchase_product_id:
            return skill_product
        if product_id and skill_product.product_id == product_id:
            return skill_product
