import os

from google.auth import default
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Sheet:
  def __init__(self, sheet_id: str = None, range_name: str = None, scopes: list[str] = None) -> None:
    self.sheet_id = os.environ.get('ROTA_SPREADSHEET_ID') if scopes is None else sheet_id
    self.range_name = os.environ.get('ROTA_RANGE_NAME') if scopes is None else range_name
    self.scopes = os.environ.get('DEFAULT_SCOPE') if scopes is None else scopes

    # Retrieve credentials from Application Default Credentials
    creds, _ = default()

    try:
      self.service = build("sheets", "v4", credentials=creds)

    except HttpError as err:
      print(f'ERROR: Failed to setup Sheets service: {err}')

  def read_values(self):
    try:
      # Call the Sheets API
      sheet = self.service.spreadsheets()
      result = (
          sheet.values()
          .get(spreadsheetId=self.sheet_id, range=self.range_name)
          .execute()
      )
      return result.get("values", [])

    except HttpError as err:
      print(err)
      return []

  def get_link(self):
    return f"https://docs.google.com/spreadsheets/d/{self.sheet_id}"
