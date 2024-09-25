import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Sheet:

  def __init__(self, sheet_id: str = None, range_name: str = None, scopes: list[str] = None) -> None:
    self.sheet_id = os.environ.get('ROTA_SPREADSHEET_ID') if scopes is None else sheet_id
    self.range_name = os.environ.get('ROTA_RANGE_NAME') if scopes is None else range_name
    self.scopes = os.environ.get('DEFAULT_SCOPE') if scopes is None else scopes

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", self.scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", self.scopes
        )
        creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open("token.json", "w") as token:
        token.write(creds.to_json())

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
