from model.task import Task
from model.housemate import Housemate
from model.area import Area

class Rota:
  areas: list[Area] = []

  def __init__(self, values):
    for row in values[1:]:
      responsible = [Housemate(initials=i) for i in row[3].split(',')]
      task = Task(area_name=row[0], name=row[1], frequency=row[2], responsible=responsible)

      if task.area_name in [area.name for area in self.areas]:
        area = next(a for a in self.areas if a.name == task.area_name)
        area.add_task(task)
      else:
        self.areas.append(Area(name=task.area_name, tasks=[task]))

  def __str__(self):
    return '\n'.join(area.__str__() for area in self.areas)