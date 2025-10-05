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

@app.route('/api/emails/<email_id>/summary')
def get_summary(email_id):
    # Check if summary already exists
    existing = next((s for s in summaries if s['emailId'] == email_id), None)
    if existing:
        return jsonify(existing)
    
    # Generate new summary using AI
    email = next((e for e in emails if e['id'] == email_id), None)
    if not email:
        return jsonify({"error": "Email not found"}), 404
    
    ai_summary = summarize_emails(email['body'])
    summary = {
        "id": f"summary_{email_id}",
        "emailId": email_id,
        "summary": ai_summary
    }
    summaries.append(summary)
    return jsonify(summary)

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