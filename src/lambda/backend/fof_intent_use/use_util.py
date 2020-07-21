from fof_sdk.user import User


def has_chronus_ticket(user: User):
    amount: int = user.get_item('chronus_ticket')
    if not amount:
        return False
    if amount <= 0:
        return False
    return True


def use_ticket(user: User, use_amount=1):
    amount: int = user.get_item('chronus_ticket')
    if not amount:
        raise KeyError('chronus_ticket が user.item_storage に存在しません。')
    user.set_item('chronus_ticket', amount - use_amount)
