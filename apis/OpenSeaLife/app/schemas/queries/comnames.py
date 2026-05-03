from datetime import datetime

from common.base.models import BaseApiModel
from pydantic import ConfigDict, Field

from app.schemas.queries.page import PageEnvelope


class ComnamesRow(BaseApiModel):
    model_config = ConfigDict(populate_by_name=True)

    autoctr: int | None = Field(default=None, validation_alias="autoctr")
    com_name: str | None = Field(default=None, validation_alias="ComName")
    transliteration: str | None = Field(
        default=None, validation_alias="Transliteration"
    )
    stock_code: int | None = Field(default=None, validation_alias="StockCode")
    spec_code: int | None = Field(default=None, validation_alias="SpecCode")
    c_code: str | None = Field(default=None, validation_alias="C_Code")
    language: str | None = Field(default=None, validation_alias="Language")
    script: str | None = Field(default=None, validation_alias="Script")
    unicode_text: str | None = Field(default=None, validation_alias="UnicodeText")
    name_type: str | None = Field(default=None, validation_alias="NameType")
    preferred_name: bool | None = Field(default=None, validation_alias="PreferredName")
    misspelling: bool | None = Field(default=None, validation_alias="Misspelling")
    trade_name: int | None = Field(default=None, validation_alias="TradeName")
    trade_name_ref: int | None = Field(default=None, validation_alias="TradeNameRef")
    com_names_ref_no: int | None = Field(default=None, validation_alias="ComNamesRefNo")
    size: str | None = Field(default=None, validation_alias="Size")
    sex: str | None = Field(default=None, validation_alias="Sex")
    language2: str | None = Field(default=None, validation_alias="Language2")
    locality2: str | None = Field(default=None, validation_alias="Locality2")
    rank: int | None = Field(default=None, validation_alias="Rank")
    remarks: str | None = Field(default=None, validation_alias="Remarks")
    second_word: str | None = Field(default=None, validation_alias="SecondWord")
    third_word: str | None = Field(default=None, validation_alias="ThirdWord")
    fourth_word: str | None = Field(default=None, validation_alias="FourthWord")
    entered: int | None = Field(default=None, validation_alias="Entered")
    date_entered: datetime | None = Field(default=None, validation_alias="DateEntered")
    modified: int | None = Field(default=None, validation_alias="Modified")
    date_modified: datetime | None = Field(
        default=None, validation_alias="DateModified"
    )
    expert: int | None = Field(default=None, validation_alias="Expert")
    date_checked: datetime | None = Field(default=None, validation_alias="DateChecked")
    core: str | None = Field(default=None, validation_alias="Core")
    modifier1: str | None = Field(default=None, validation_alias="modifier1")
    modifier2: str | None = Field(default=None, validation_alias="modifier2")
    cloffsca: int | None = Field(default=None, validation_alias="CLOFFSCA")

    plural: bool | None = Field(default=None, validation_alias="Plural")

    e_append: int | None = Field(default=None, validation_alias="E_Append")
    e_date_append: datetime | None = Field(
        default=None, validation_alias="E_DateAppend"
    )
    ts: datetime | None = Field(default=None, validation_alias="TS")


ComnamesPage = PageEnvelope[ComnamesRow]
