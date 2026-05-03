from .base import QueryService


class CountrefService(QueryService):
    table_name = "countref"
    allowed_filters = {
        "c_code": "C_Code",
        "abb": "ABB",
        "language": "Language",
        "marine_flag": "MarineFlag",
    }
