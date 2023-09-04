from enum import Enum


class Role(Enum):
    organizer = 1
    member = 2


class ProductState(Enum):
    not_added = 1
    added = 2
    in_cart = 3
    bought = 4
