# google_doc_svc.py
from svc.svc import Svc
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive.readonly'
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'credentials.json')
TOKEN_PATH = os.path.join(BASE_DIR, 'token.pickle')

class GoogleDocSvc(Svc):
    def __init__(self, document_name: str):
        self.doc_service = self._build_doc_service()
        self.drive_service = self._build_drive_service()
        self.document_id = self._get_or_create_doc(document_name)

    def _get_creds(self):
        creds = None
        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def _build_doc_service(self):
        return build('docs', 'v1', credentials=self._get_creds())
    
    def _build_drive_service(self):
        return build('drive', 'v3', credentials=self._get_creds())
    
    def _get_or_create_doc(self, doc_name: str):
        query = (
        f"name = '{doc_name}' "
        "and mimeType = 'application/vnd.google-apps.document' "
        "and trashed = false "
        )
        results = self.drive_service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)',
            pageSize=1
        ).execute()
        files = results.get('files', [])
        if files:
            print("Найден файл: " + doc_name)
            return files[0]['id']
        else:
            print("Создан новый файл: " + doc_name)
            doc = self.doc_service.documents().create(body={'title': doc_name}).execute()
            return doc['documentId']

    #Override
    def write(self, text: str) -> None:
        requests = [
            {
                'insertText': {
                    'text': text + ' ',
                    'endOfSegmentLocation': {}
                }
            }
        ]
        self.doc_service.documents().batchUpdate(
            documentId=self.document_id, body={'requests': requests}
        ).execute()
