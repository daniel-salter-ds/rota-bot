import os

from model.rota import Rota
from sheet import Sheet


def main():
  spreadsheet_id = os.environ.get('SAMPLE_SPREADSHEET_ID')
  range_name = os.environ.get('SAMPLE_RANGE_NAME')

  sheet = Sheet(spreadsheet_id, range_name)
  values = sheet.read_values()

  if not values:
    print("No data found.")
    return

  rota = Rota(values)
  print(rota)


if __name__ == "__main__":
  main()