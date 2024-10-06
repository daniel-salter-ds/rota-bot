from pydantic import BaseModel
from pydantic.functional_validators import field_validator

housemates = {
  'DS': 'Dan S',
  'MH': 'Millie',
  'HB': 'Holly',
  'JL': 'James',
  'AK': 'Alex',
  'DW': 'Dan W'
}

class Housemate(BaseModel):
  initials: str

  @field_validator("initials")
  @classmethod
  def validate_initials(cls, initials):
    assert initials in housemates
    return initials

  def get_name(self):
    return housemates[self.initials]

  def __str__(self):
    return self.get_name()
