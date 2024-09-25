import os

from model.task import Task
from model.housemate import Housemate
from model.area import Area
from sheet import Sheet

def main():
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  spreadsheet_id = os.environ.get('SAMPLE_SPREADSHEET_ID')
  range_name = os.environ.get('SAMPLE_RANGE_NAME')

  sheet = Sheet(spreadsheet_id, range_name)
  values = sheet.read_values()

  if not values:
    print("No data found.")
    return

  # --- Calculate Tasks in each Area from sheet values ---
  areas = []

  for row in values[1:]:
    responsible = [Housemate(initials=i) for i in row[3].split(',')]
    task = Task(area_name=row[0], name=row[1], frequency=row[2], responsible=responsible)
    # print(task)

    if task.area_name in [area.name for area in areas]:
      area = next(a for a in areas if a.name == task.area_name)
      area.add_task(task)
    else:
      areas.append(Area(name=task.area_name, tasks=[task]))

  for area in areas:
    print(area)


if __name__ == "__main__":
  main()