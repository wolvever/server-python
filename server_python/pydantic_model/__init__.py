
import json

from pydantic import BaseModel, Field, field_serializer, field_validator


class ClientModel(BaseModel):

    # As those methods are not stable and clearly supported in future versions
    # we define them explicitly here to avoid breaking changes in the future.
    @classmethod
    def from_json(cls, json_str: str):
        """Creates an instance of the model from a JSON string."""
        data = json.loads(json_str)
        return cls(**data)  

    def to_json(self, **kwargs) -> str:
        """Returns a JSON string representation of the model."""
        data = self.model_dump(**kwargs)
        return json.dumps(data)

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the model."""
        return self.model_dump()    


class SettingModel(ClientModel):

    class Config:
        arbitrary_types_allowed = True
