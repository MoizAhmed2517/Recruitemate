# RecruitMate

**RecruitMate** is an AI-powered recruitment agent that automates the process of screening, evaluating, and ranking candidates based on a provided Job Description (JD). It also facilitates interview scheduling and communication.

## Features

- ✅ Fetches candidate data from Google Sheets.
- ✅ Reads and analyzes resumes.
- ✅ Evaluates resumes based on the provided JD.
- ✅ Ranks candidates according to relevance.
- ✅ Sends the list of shortlisted candidates to your email.
- ✅ (Upcoming) Auto-sends Calendly links for interview scheduling.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/RecruitMate.git
   cd RecruitMate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up Google Sheets and Gmail API credentials.
4. Configure the `.env` file with required API keys and credentials.

## Usage

1. Run the agent:
   ```bash
   python main.py
   ```
2. Monitor logs for candidate evaluation and ranking.
3. Receive an email with the shortlisted candidates.

## Configuration

- **Google Sheets API**: Required for fetching candidate data.
- **Resume Parser**: Uses AI to analyze resumes.
- **JD Matching Algorithm**: Evaluates resumes against job descriptions.
- **Email Integration**: Sends results to your personal email.
- **(Upcoming) Calendly API**: Automates interview scheduling.

## Future Enhancements

- [ ] Improve NLP-based resume parsing.
- [ ] Support multiple job descriptions simultaneously.
- [ ] Enhance ranking algorithm with ML models.
- [ ] Integrate with ATS (Applicant Tracking Systems).

## Contributions

Contributions are welcome! Feel free to submit a PR or raise an issue.

## License

This project is licensed under the MIT License.

---
Developed with ❤️ by Moiz Ahmed