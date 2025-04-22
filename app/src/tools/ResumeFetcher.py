import re
import spacy
import yaml
import gspread
import sqlite3
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

class ResumeFetcher:
    
    def __init__(self, config_path: str):
        # Load configuration from google.yaml
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        self.scopes = self.config['scopes']
        self.creds = Credentials.from_service_account_file("./src/secrets/credentials_gsheet.json", scopes=self.scopes)
        self.client = gspread.authorize(self.creds)
        self.drive_service = build("drive", "v3", credentials=self.creds)
        self.ner = spacy.load(self.config['nerModel'])
        
        # Extract the sheet ID from the Google Sheets link
        gsheet_link = self.config['gSheetLink']
        self.sheet_id = self.extract_sheet_id(gsheet_link)
        self.init_db()
    
    def extract_sheet_id(self, gsheet_link: str) -> str:
        match = re.search(r'/d/([a-zA-Z0-9-_]+)', gsheet_link)
        if match:
            return match.group(1)
        else:
            raise ValueError("Invalid Google Sheets link")
    
    def init_db(self):
        # Connect to SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect('./db/resumes.db')
        self.cursor = self.conn.cursor()
        
        # Create table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                name TEXT,
                resume BLOB
            )
        ''')
    
        self.cursor.execute(
                    '''CREATE TABLE IF NOT EXISTS processed_resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_id INTEGER,
                email TEXT,
                name TEXT,
                social_links TEXT,
                technical_skills TEXT,
                total_experience INTEGER,
                education TEXT,
                candidate_summary TEXT,
                experience_score TEXT,
                skills_score TEXT,
                responsibilities_score TEXT,
                requirements_score TEXT,
                softskills_score TEXT,
                final_score TEXT,
                FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE)
            '''
            )
        
        self.conn.commit()
    
    def fetch_all_resumes(self):
        """Fetch all resume data from Google Sheets."""
        sheet = self.client.open_by_key(self.sheet_id)
        values_list = sheet.sheet1.get_all_values()  # Get all rows
        
        for row in values_list[1:]:  # Skip header row
            self.process_row(row)
    
    def process_row(self, row):
        """Extracts data from a single row and stores it in the database."""
        row_text = " ".join(row)
        
        # Extract email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+', row_text)
        email = email_match.group() if email_match else None
        
        # Check if email already exists in the database
        if self.email_exists(email):
            print(f"Email {email} already exists. Skipping row.")
            return
        
        # Extract name using NER
        doc = self.ner(row_text)
        name = next((ent.text for ent in doc.ents if ent.label_ == "PERSON"), None)
        
        # Extract resume file link
        pdf_link = re.search(r'https://drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)', row_text)
        file_id = pdf_link.group(1) if pdf_link else None
        
        if file_id:
            request = self.drive_service.files().get_media(fileId=file_id)
            resume = request.execute()
            print(f"Processing: {name} ({email})")
            self.store_data(email, name, resume)
    
    def email_exists(self, email: str) -> bool:
        """Check if an email already exists in the database."""
        self.cursor.execute('SELECT 1 FROM resumes WHERE email = ?', (email,))
        return self.cursor.fetchone() is not None
    
    def store_data(self, email: str, name: str, resume: bytes):
        self.cursor.execute('''
            INSERT INTO resumes (email, name, resume)
            VALUES (?, ?, ?)
        ''', (email, name, resume))
        self.conn.commit()
        
    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

        
# if __name__ == "__main__":
#     fetcher = ResumeFetcher("../config/google.yaml")
#     fetcher.fetch_all_resumes()