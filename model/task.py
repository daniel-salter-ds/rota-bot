from pydantic import BaseModel
from model.frequency import Frequency
from model.housemate import Housemate

class Task(BaseModel):
  area_name: str
  name: str
  frequency: Frequency
  responsible: list[Housemate]

  def __str__(self, indent=''):
    return f'''{indent}Task: {{
{indent}  Area: {self.area_name},
{indent}  Name: {self.name},
{indent}  Frequency: {self.frequency.name},
{indent}  Responsible: [ {', '.join([hm.get_name() for hm in self.responsible])} ]
{indent}}}'''
