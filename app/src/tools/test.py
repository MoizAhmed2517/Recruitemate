import re
import gspread
import spacy
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds = Credentials.from_service_account_file("../secrets/credentials_gsheet.json", scopes=scopes)
client = gspread.authorize(creds)

# Initialize Google Drive API
drive_service = build("drive", "v3", credentials=creds)

nlp = spacy.load("../../ner/pak_names_ner_model")

sheet_id = "1QFaCRAEwNWWoBuRrvAMd-a2RCCxTavOXXb03Edjbrjs"
sheet = client.open_by_key(sheet_id)
values_list = sheet.sheet1.row_values(4)

#extraction
row_test = " ".join(values_list)
print(row_test)
email_match = re.search(r'[\w\.-]+@[\w\.-]+', row_test)
email = email_match.group() if email_match else None

print(email)

# Extract Google Drive Link
drive_match = re.search(r'https://drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)', row_test)
file_id = drive_match.group(1) if drive_match else None

doc = nlp(row_test)
name = None

for ent in doc.ents:
    if ent.label_ == "PERSON":  # Look for entities classified as PERSON
        name = ent.text
        break
print(name)

output_path = f'../data/{name}.pdf'
print(output_path)
# request = drive_service.files().get_media(fileId=file_id)
# with open(output_path, "wb") as f:
#     f.write(request.execute())

# print(f"Downloaded resume to {output_path}")