import os
import json
import shutil
import sqlite3

db_path = './db/resumes.db'
temp_resume_dir = "./temp_resumes"

def fetch_resumes_from_db():
    conn = sqlite3.connect(db_path)
    print("Fetching resumes from database...")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resumes")
    resumes = cursor.fetchall()
    conn.close()
    print(f"Fetched {len(resumes)} resumes.")
    return resumes

def save_evaluation_score(result):
    print(f"Saving result for {result['email']} into database...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM resumes WHERE email = ?", (result['email'],))
    resume_id = cursor.fetchone()
    if resume_id:
        resume_id = resume_id[0]
        cursor.execute('''INSERT INTO processed_resumes (
                            resume_id, email, name, social_links, technical_skills, total_experience, education,
                            candidate_summary, experience_score, skills_score, responsibilities_score,
                            requirements_score, softskills_score, final_score) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
            resume_id,
            result['email'],
            result['name'],
            json.dumps(result['social_links']),
            json.dumps(result['Technical_Skills']),
            result['Total_Experience'],
            json.dumps(result['Education']),
            result['Candidate_Summary'],
            result['Score_Breakdown']['Experience'],
            result['Score_Breakdown']['Skills'],
            result['Score_Breakdown']['Responsibilities'],
            result['Score_Breakdown']['Requirements'],
            result['Score_Breakdown']['Softskills'],
            result['CV_Score']
        ))
    conn.commit()
    conn.close()
    print(f"Successfully saved result for {result['email']}.")

def save_resume_to_file(email, resume_blob):
    """Save resume blob as a temporary PDF file and return file path."""
    os.makedirs(temp_resume_dir, exist_ok=True)
    resume_file_path = os.path.join(temp_resume_dir, f"{email.replace('@', '_')}.pdf")
    
    with open(resume_file_path, "wb") as f:
        f.write(resume_blob)
    
    print(f"Saved resume for {email} as {resume_file_path}")
    return resume_file_path

def fetch_evaluated_resumes(TOP_N=1):
    """Fetch evaluated resumes from the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT pr.*, r.resume 
        FROM processed_resumes pr
        JOIN resumes r ON pr.resume_id = r.id
        ORDER BY CAST(pr.final_score AS REAL) DESC
        LIMIT ?
    ''', (TOP_N,))
    results = cursor.fetchall()
    print(f"Fetched {len(results)} resumes.")
    conn.close()
    return results

def cleanup_temp_resumes():
    """Delete temporary resume files after processing."""
    print("Cleaning up temporary resume files...")
    shutil.rmtree(temp_resume_dir, ignore_errors=True)
    print("Temporary resumes cleaned up.")