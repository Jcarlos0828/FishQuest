from .base import QueryService


class ComnamesService(QueryService):
    table_name = "comnames"
    allowed_filters = {
        "spec_code": "SpecCode",
        "language": "Language",
        "c_code": "C_Code",
        "name_type": "NameType",
        "preferred_name": "PreferredName",
    }
