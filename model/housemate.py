from pydantic import BaseModel
from pydantic.functional_validators import field_validator

housemates = {
    "DS": {
        "id": "5883075633",
        "name": "Dan S"
    },
    "MH": {
        "id": "",
        "name": "Millie"
    },
    "HB": {
        "id": "",
        "name": "Holly"
    },
    "JL": {
        "id": "",
        "name": "James"
    },
    "AK": {
        "id": "",
        "name": "Alex"
    },
    "DW": {
        "id": "",
        "name": "Dan W"
    }
}

class Housemate(BaseModel):
  initials: str

  @field_validator("initials")
  @classmethod
  def validate_initials(cls, initials):
    assert initials in housemates
    return initials

  def get_name(self):
    return housemates[self.initials]["name"]

  def get_id(self):
    return housemates[self.initials]["id"]

  def __str__(self):
    return self.initials
