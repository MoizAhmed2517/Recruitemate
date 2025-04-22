from multiprocessing import resource_tracker
import os
import re
import yaml
from datetime import datetime
from dotenv import load_dotenv
from crew import RecruitMateCrew
from src.tools.ResumeFetcher import ResumeFetcher
from src.smtp.send_mail import send_email
from src.storage.store import (fetch_resumes_from_db, 
                               save_evaluation_score, 
                               cleanup_temp_resumes, 
                               save_resume_to_file, 
                               fetch_evaluated_resumes)

temp_resume_dir = "./temp_resumes"

def run():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path)
        
        # Fetch resumes from Google Sheets and store them in DB
        print("Fetching resumes from Google Sheets...")
        fetcher = ResumeFetcher("./src/config/google.yaml")
        fetcher.fetch_all_resumes()
        resumes = fetch_resumes_from_db()
        
        for _, email, name, resume_blob in resumes:
            resume_file_path = save_resume_to_file(email, resume_blob)
            print(f"Processing resume for {name} ({email})...")
            inputs = {
                'path_to_csv': resume_file_path,
                'current_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'path_to_jd': './src/jd/jd.pdf'
            }
            result = RecruitMateCrew().crew().kickoff(inputs=inputs)
            result_dict = result.to_dict()
            result_dict['email'] = email
            result_dict['name'] = name
            save_evaluation_score(result_dict)  # Save result immediately
            
        print("Resume processing completed successfully!")
    else:
        raise Exception("No .env file found")
    cleanup_temp_resumes()

if __name__ == "__main__":
    print("\nResume evaluation has started\n")
    try:
        run()
        config_path = r'src\config\smtp.yaml'
        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
            result = fetch_evaluated_resumes(config['TOP_N'])
            send_email(subject=config['subject'] + config['JOB_TITLE'],
                    results=result,
                    sender_email=config['SENDER_EMAIL'], 
                    sender_password=config['SENDER_PASSWORD'], 
                    recipient_emails=config['RECEIVER_EMAIL'], 
                    cc_email=config['CC_EMAIL'], 
                    job_title=config['JOB_TITLE'], 
                    top_n=config['TOP_N']
                    )
        print("\nCrew executed with status okay\n")
    except Exception as e:
        print(f"\nCrew executed with status not okay\n {e}")
    
    