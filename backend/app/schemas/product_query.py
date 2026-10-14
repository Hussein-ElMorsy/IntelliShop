from enum import Enum


class ProductSortField(str, Enum):
    name = "name"
    price = "price"
  #  created = "created"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"