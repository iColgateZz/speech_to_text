# google_doc_svc.py
from svc import Svc
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive.readonly'
]

class GoogleDocSvc(Svc):
    def __init__(self, document_name: str):
        self.doc_service = self._build_doc_service()
        self.drive_service = self._build_drive_service()
        self.document_id = self._get_or_create_doc(document_name)
        
        print("Document id is " + str(self.document_id))
        
    def _get_creds(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
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
            print("File found")
            return files[0]['id']
        else:
            print("File created")
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
