from datetime import datetime, timedelta

from pydantic import BaseModel
from model.frequency import Frequency
from model.housemate import Housemate

def _get_start_of_week(date: datetime) -> datetime:
  # Calculate how many days have passed since the most recent Monday
  days_since_monday = date.weekday()  # Monday is 0, Sunday is 6
  # Subtract the days since Monday to get this week's Monday and set time to midnight
  return (date - timedelta(days=days_since_monday)).replace(hour=0, minute=0, second=0, microsecond=0)


class Task(BaseModel):
  area_name: str
  name: str
  frequency: Frequency
  responsible: dict[str, Housemate]
  schedule: dict[datetime, str]

  def __str__(self, indent=''):
    return f'''{indent}Task: {{
{indent}  Area: {self.area_name},
{indent}  Name: {self.name},
{indent}  Frequency: {self.frequency.name},
{indent}  Responsible: [ {', '.join([hm.get_name() for hm in self.responsible])} ]
{indent}}}'''

  def who_is_on(self, date: datetime) -> Housemate | None:
    sow = _get_start_of_week(date)
    try:
      initials = self.schedule[sow]
      return self.responsible[initials]
    except KeyError:
      return None
