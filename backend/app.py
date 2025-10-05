from flask import Flask, request, jsonify
from flask_cors import CORS
from email_data import emails
from generator import summarize_emails
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import datetime
from base64 import urlsafe_b64decode



app = Flask(__name__)
CORS(app)

summaries = []

def get_gmail_emails(service, num_emails=10):
    """Fetch recent emails from Gmail"""
    try:
        results = service.users().messages().list(userId='me', maxResults=num_emails).execute()
        messages = results.get('messages', [])
        
        if not messages:
            return []
        
        gmail_emails = []
        for i, msg in enumerate(messages):
            msg_id = msg['id']
            message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
            
            headers = message['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')
            
            body = ""
            if 'parts' in message['payload']:
                for part in message['payload']['parts']:
                    if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                        body = urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        break
            elif 'body' in message['payload'] and 'data' in message['payload']['body']:
                body = urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')
            
            gmail_emails.append({
                'id': f'gmail_{i+1}',
                'subject': subject,
                'sender': sender,
                'body': body[:500] + '...' if len(body) > 500 else body,
                'timestamp': date,
                'category': 'Work'
            })
        
        return gmail_emails
    except Exception as e:
        print(f'Gmail fetch error: {e}')
        return []
    
@app.route("/gmail-labels", methods=["POST"])
def gmail_access():
    if not request.json:
        return jsonify({"error": "Invalid request, JSON not found"}), 400

    creds_dict = request.json

    try:
        creds_dict["expiry"] = datetime.datetime.fromisoformat(creds_dict["expiry"])
        creds = Credentials(**creds_dict)
        gmail_service = build("gmail", "v1", credentials=creds)
        
        results = gmail_service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])
        
        if not labels:
            return jsonify({"message": "No labels found."})
        else:
            label_names = [label["name"] for label in labels]
            return jsonify({"message": "Successfully accessed Gmail!", "labels": label_names})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/gmail-emails", methods=["POST"])
def get_gmail_emails_route():
    if not request.json:
        return jsonify({"error": "Invalid request, JSON not found"}), 400

    creds_dict = request.json

    try:
        creds_dict["expiry"] = datetime.datetime.fromisoformat(creds_dict["expiry"])
        creds = Credentials(**creds_dict)
        gmail_service = build("gmail", "v1", credentials=creds)
        
        gmail_emails = get_gmail_emails(gmail_service)
        return jsonify(gmail_emails)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Email routes
@app.route('/api/emails')
def get_emails():
    return jsonify(emails)

@app.route('/api/emails/<email_id>')
def get_email(email_id):
    email = next((e for e in emails if e['id'] == email_id), None)
    return jsonify(email) if email else jsonify({"error": "Not found"}), 404

@app.route('/api/summarize', methods=['GET', 'POST'])
def summarize_all_emails():
    emails_to_summarize = emails  # Default to demo emails
    
    # Try to use Gmail data if credentials provided
    if request.method == 'POST' and request.json:
        try:
            creds_dict = request.json
            creds_dict["expiry"] = datetime.datetime.fromisoformat(creds_dict["expiry"])
            creds = Credentials(**creds_dict)
            gmail_service = build("gmail", "v1", credentials=creds)
            
            gmail_emails = get_gmail_emails(gmail_service)
            if gmail_emails:
                emails_to_summarize = gmail_emails
        except Exception as e:
            print(f"Gmail summarize error: {e}")
    
    # Get all email bodies
    all_email_content = "\n\n---\n\n".join([f"Subject: {e['subject']}\nFrom: {e['sender']}\nBody: {e['body']}" for e in emails_to_summarize])
    
    # Generate summary for all emails
    ai_summary = summarize_emails(all_email_content)
    
    return jsonify({
        "summary": ai_summary,
        "emailCount": len(emails_to_summarize)
    })

@app.route('/api/summaries')
def get_summaries():
    return jsonify(summaries)

@app.route('/api/search')
def search_emails():
    q = request.args.get('q', '').lower()
    filtered = [e for e in emails if q in e['subject'].lower() or q in e['body'].lower()]
    return jsonify(filtered)

if __name__ == '__main__':
    app.run(port=3000)