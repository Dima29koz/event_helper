from enum import Enum, auto


class Role(Enum):
    organizer = 1
    member = 2


class ProductState(Enum):
    not_added = 1
    added = 2
    in_cart = 3
    bought = 4


class EntityType(Enum):
    event = auto()
    location = auto()
    members = auto()
    member = auto()
    member_me = auto()
    products = auto()
