# Sorta AI - Smart Email Summarizer/Organizer (AWS Summit 2025)

Sorta AI is an intelligent inbox assistant that connects to Gmail, retrieves messages securely through OAuth, and uses Amazon Bedrock AI to summarize, classify, and prioritize your emails.

## Tech Stack

- Frontend: Streamlit
- Backend: Flask
- Language: Python
- Tool: AWS Bedrock, Amazon Q
- Authentication: Google OAuth (UCLA Gmail required)

## Useful Commands

Run streamlit: 
```bash
streamlit run app.py
```

Run flask:
```bash
cd backend
flask run
```

## What's next for Sorta
- **Adapting dynamically**: Sorta continues to learn from user habits and priorities to group emails by true importance.
- **Learning automatically**: It refines its understanding of your reading patterns and preferences, removing the need for manual rules.
- **Integration with productivity tools**: Future versions will connect with calendar and task management apps, allowing Sorta to automatically create reminders, events, or to-dos from emails.
- **Expanding beyond Gmail**: We plan to support multiple email platforms to reach a wider range of users and workflows.
- **Multilingual capability**: Sorta will evolve to understand and translate emails across languages, using AI-powered translation (e.g., Amazon Translate) to ensure seamless communication in multilingual inboxes.
