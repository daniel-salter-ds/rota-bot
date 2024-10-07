from datetime import datetime

from model.task import Task
from model.housemate import Housemate
from model.area import Area


class Rota:
  areas: list[Area] = []

  def __init__(self, values):
    dates = [datetime.strptime(d, "%m/%d/%y") for d in values[0][4:]]
    for row in values[1:]:
      area_name = row[0]
      name = row[1]
      frequency=row[2]
      responsible = {i: Housemate(initials=i) for i in row[3].split(',')}
      schedule = dict(zip(dates, row[4:]))
      task = Task(area_name=area_name, name=name, frequency=frequency, responsible=responsible, schedule=schedule)

      if task.area_name in [area.name for area in self.areas]:
        area = next(a for a in self.areas if a.name == task.area_name)
        area.add_task(task)
      else:
        self.areas.append(Area(name=task.area_name, tasks=[task]))

  def __str__(self):
    return '\n'.join(area.__str__() for area in self.areas)

  def get_message_by_area(self, date: datetime) -> str:
    message_parts = ["Hi! Here's this week's responsibilities:"]
    for area in self.areas:
      message_parts.append(f"\n{area.name}:")
      for task in area.tasks:
        who_is_on = task.who_is_on(date)
        if who_is_on:
          message_parts.append(f"{task.name} - @{who_is_on}")
    return '\n'.join(message_parts)

  def get_message_by_housemate(self, date: datetime) -> str:
    hm_areas = self.get_housemate_areas(date)

    message_parts = ["Hi! Here's this week's responsibilities:"]
    for initials in hm_areas:
      housemate = Housemate(initials=initials)
      message_parts.append(f"\n[{housemate.get_name()}](tg://user?id={housemate.get_id()}):")
      for area in hm_areas[initials]:
        message_parts.append(f"    {area.name}:")
        for task in area.tasks:
          who_is_on = task.who_is_on(date)
          if who_is_on:
            message_parts.append(f"        {task.name}")

    return '\n'.join(message_parts)



  def get_housemate_areas(self, date: datetime) -> dict[str, list[Area]]:
    hm_areas = {}
    for area in self.areas:
      for task in area.tasks:
        who_is_on = task.who_is_on(date)
        if who_is_on:
          initials = who_is_on.initials
          if initials in hm_areas:
            hm_areas_list = hm_areas[initials]
            current_area = [a for a in hm_areas_list if a.name == area.name]
            if len(current_area) == 0:
              hm_areas[initials].append(Area(name=task.area_name, tasks=[task]))
            elif len(current_area) == 1:
              current_area[0].add_task(task)
          else:
            hm_areas[initials] = [Area(name=task.area_name, tasks=[task])]

    return hm_areas

