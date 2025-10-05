from flask import Flask, request, jsonify
from flask_cors import CORS
from email_data import emails
from generator import summarize_emails

app = Flask(__name__)
CORS(app)

summaries = []

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