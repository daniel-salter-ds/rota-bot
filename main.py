import os

from model.rota import Rota
from sheet import Sheet


def main():
  sheet = Sheet()
  values = sheet.read_values()

  if not values:
    print("No data found.")
    return

  rota = Rota(values)
  print(rota)

  link = sheet.get_link()


if __name__ == "__main__":
  main()