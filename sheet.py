import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Sheet:
  sheet_id: str
  range_name: str
  # If modifying these scopes, delete the file token.json.
  scopes: list[str]


  def __init__(self, sheet_id: str, range_name: str, scopes: list[str] = None) -> None:
    self.sheet_id = sheet_id
    self.range_name = range_name
    self.scopes = os.environ.get('DEFAULT_SCOPE') if scopes is None else scopes


  def read_values(self):
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
      service = build("sheets", "v4", credentials=creds)

      # Call the Sheets API
      sheet = service.spreadsheets()
      result = (
          sheet.values()
          .get(spreadsheetId=self.sheet_id, range=self.range_name)
          .execute()
      )
      return result.get("values", [])

    except HttpError as err:
      print(err)
      exit(1)
