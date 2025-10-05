from flask import Flask, request, jsonify
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import datetime

app = Flask(__name__)

@app.route("/gmail-access", methods=["POST"])
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

if __name__ == "__main__":
    app.run(debug=True)