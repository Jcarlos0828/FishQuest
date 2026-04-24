from pydantic import BaseModel, ConfigDict


class BaseApiModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
