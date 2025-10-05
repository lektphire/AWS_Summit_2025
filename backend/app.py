from flask import Flask, request, jsonify
from flask_cors import CORS
from email_data import emails
from generator import summarize_emails
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import datetime
from strands import Agent, tool
from strands_tools import calculator, current_time
from strands.models import BedrockModel
from base64 import urlsafe_b64decode

def get_gmail_helpers(service):
    @tool
    def read_recent_emails(num_emails=3):
        """
        Fetches the full content of the most recent emails from Gmail.

        Args:
            service: An authorized Gmail API service object.
            num_emails: The number of recent emails to retrieve. Defaults to 3.

        Returns:
            A list of dictionaries, where each dictionary contains the subject,
            sender, date, and body of an email. Returns an empty list on error.
        """
        emails = []
        try:
            # Get the IDs of the most recent emails
            results = service.users().messages().list(userId='me', maxResults=num_emails).execute()
            messages = results.get('messages', [])

            if not messages:
                print("No new emails found.")
                return []

            # Iterate through the messages and fetch their full content
            for msg in messages:
                msg_id = msg['id']
                message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
                
                # Extract relevant parts
                headers = message['payload']['headers']
                subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
                sender = next((header['value'] for header in headers if header['name'] == 'From'), 'Unknown Sender')
                date = next((header['value'] for header in headers if header['name'] == 'Date'), 'Unknown Date')

                # Extract the email body (prefers plain text over HTML)
                body = ""
                if 'parts' in message['payload']:
                    for part in message['payload']['parts']:
                        if part['mimeType'] == 'text/plain':
                            body = urlsafe_b64decode(part['body']['data']).decode('utf-8')
                            break
                elif 'body' in message['payload'] and 'data' in message['payload']['body']:
                    body = urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')

                emails.append({
                    'subject': subject,
                    'sender': sender,
                    'date': date,
                    'body': body
                })

        except Exception as error:
            print(f'An error occurred: {error}')
            return []

        return emails
    return read_recent_emails
@tool
def letter_counter(word: str, letter: str) -> int:
    """
    Count occurrences of a specific letter in a word.

    Args:
        word (str): The input word to search in
        letter (str): The specific letter to count

    Returns:
        int: The number of occurrences of the letter in the word
    """
    if not isinstance(word, str) or not isinstance(letter, str):
        return 0

    if len(letter) != 1:
        raise ValueError("The 'letter' parameter must be a single character")

    return word.lower().count(letter.lower())

app = Flask(__name__)
CORS(app)

summaries = []

model = BedrockModel(
    model_id="amazon.nova-lite-v1:0",
    temperature=0.3,
    region_name='us-east-1'
)

SYSTEM_PROMPT = """
    You are a helpful assistant for helping the user manage their Gmail inbox. 
    Summarize the most recent emails with the read_recent_emails() tool call
"""
# @app.route("/test-chat", methods=['POST'])
# def test_chat():
# # Ask the agent a question that uses the available tools
#     message = """
#     I have 4 requests:

#     1. What is the time right now?
#     2. Calculate 3111696 / 74088
#     3. Tell me how many letter R's are in the word "strawberry" 🍓
#     """
#     agent = Agent(
#         model=model,
#         tools=[calculator, current_time, letter_counter],
#         # system_prompt="You are a helpful assistant. Be concise in your responses."
#     )

#     agent(message)
#     result = agent.messages[-1]['content'][0]['text']
#     return jsonify({"message": result})
@app.route("/summarize-emails", methods=["POST"])
def summarize_emails():
    if not request.json:
        return jsonify({"error": "Invalid request, JSON not found"}), 400

    creds_dict = request.json

    try:
        # Convert the expiry back to a datetime object
        creds_dict["expiry"] = datetime.datetime.fromisoformat(creds_dict["expiry"])

        # Recreate the Credentials object from the received dictionary
        creds = Credentials(**creds_dict)

        # Now, you can use these credentials to build the Gmail service
        gmail_service = build("gmail", "v1", credentials=creds)

        agent = Agent(
            model=model,
            tools=[get_gmail_helpers(gmail_service)],
            system_prompt=SYSTEM_PROMPT,
        )

        message = """
        Tell me what's in my most recent 3 emails
        """

        agent(message)
        result = agent.messages[-1]['content'][0]['text']

        return jsonify({"message": "Successfully accessed Gmail!", "content": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/gmail-labels", methods=["POST"])
def gmail_access():
    if not request.json:
        return jsonify({"error": "Invalid request, JSON not found"}), 400

    creds_dict = request.json

    try:
        # Convert the expiry back to a datetime object
        creds_dict["expiry"] = datetime.datetime.fromisoformat(creds_dict["expiry"])

        # Recreate the Credentials object from the received dictionary
        creds = Credentials(**creds_dict)

        # Now, you can use these credentials to build the Gmail service
        gmail_service = build("gmail", "v1", credentials=creds)

        # Example: List the user's labels
        results = gmail_service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        
        if not labels:
            return jsonify({"message": "No labels found."})
        else:
            label_names = [label["name"] for label in labels]
            return jsonify({"message": "Successfully accessed Gmail!", "labels": label_names})

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

@app.route('/api/summarize')
def summarize_all_emails():
    # Get all email bodies
    all_email_content = "\n\n---\n\n".join([f"Subject: {e['subject']}\nFrom: {e['sender']}\nBody: {e['body']}" for e in emails])
    
    # Generate summary for all emails
    ai_summary = summarize_emails(all_email_content)
    
    return jsonify({
        "summary": ai_summary,
        "emailCount": len(emails)
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