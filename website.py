import streamlit as st
import os
import requests
import html
from datetime import datetime, timedelta
from dotenv import load_dotenv
from auth import Authenticator

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .email-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .email-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .category-badge {
        background: #f0f2f6;
        color: #262730;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    .priority-high { border-left: 4px solid #ff4444; }
    .priority-medium { border-left: 4px solid #ffaa00; }
    .priority-low { border-left: 4px solid #00aa44; }
    .summary-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #2c3e50;
    }
    .metric-card {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

load_dotenv()

# emails of users that are allowed to login
allowed_users = os.getenv("ALLOWED_USERS").split(",")

# Function to generate relative time string
def get_relative_time(email_date, current_time):
    # Make both datetimes timezone-naive for comparison
    if email_date.tzinfo is not None:
        email_date = email_date.replace(tzinfo=None)
    if current_time.tzinfo is not None:
        current_time = current_time.replace(tzinfo=None)
    
    delta = current_time - email_date
    seconds = delta.total_seconds()
    
    if seconds < 3600:  # Less than 1 hour
        minutes = int(seconds // 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:  # Less than 1 day
        hours = int(seconds // 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 604800:  # Less than 1 week
        days = int(seconds // 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif seconds < 2592000:  # Less than 1 month (30 days)
        weeks = int(seconds // 604800)
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    elif seconds < 31536000:  # Less than 1 year
        months = int(seconds // 2592000)
        return f"{months} month{'s' if months != 1 else ''} ago"
    else:
        years = int(seconds // 31536000)
        return f"{years} year{'s' if years != 1 else ''} ago"

# Function to fetch emails from backend
def fetch_and_summarize_emails():
    # Try to get Gmail emails first if credentials are available
    if "google_creds" in st.session_state:
        try:
            creds = st.session_state["google_creds"]
            creds_dict = {
                "token": creds.token,
                "refresh_token": creds.refresh_token,
                "token_uri": creds.token_uri,
                "client_id": creds.client_id,
                "client_secret": creds.client_secret,
                "scopes": creds.scopes,
                "id_token": creds.id_token,
                "expiry": creds.expiry.isoformat(),
            }
            
            response = requests.post("http://127.0.0.1:3000/api/gmail-emails", json=creds_dict)
            if response.status_code == 200:
                gmail_emails = response.json()
                emails = []
                for email in gmail_emails:
                    try:
                        # Parse Gmail date format
                        email_date = datetime.strptime(email["timestamp"][:25], "%a, %d %b %Y %H:%M:%S")
                    except:
                        email_date = datetime.now()
                    
                    emails.append({
                        "id": email["id"],
                        "sender": email["sender"],
                        "subject": email["subject"],
                        "body": email["body"],
                        "date": email_date,
                        "category": email.get("category", "Work"),
                        "priority": "Medium",
                        "summary": email["body"][:100] + "..."
                    })
                return emails
        except Exception as e:
            st.warning(f"Gmail fetch failed: {e}. Using demo data.")
    
    # Fallback to demo data
    try:
        response = requests.get("http://127.0.0.1:3000/api/emails")
        if response.status_code == 200:
            backend_emails = response.json()
            emails = []
            for email in backend_emails:
                emails.append({
                    "id": email["id"],
                    "sender": email["sender"],
                    "subject": email["subject"],
                    "body": email["body"],
                    "date": datetime.fromisoformat(email["timestamp"].replace('Z', '+00:00')).replace(tzinfo=None),
                    "category": email.get("category", "Work"),
                    "priority": "Medium",
                    "summary": email["body"][:100] + "..."
                })
            return emails
        else:
            st.error("Failed to fetch emails from backend")
            return []
    except requests.exceptions.RequestException:
        st.error("Backend not available")
        return []

# Function to apply custom rules
def apply_custom_rules(emails, rules):
    for email in emails:
        for rule in rules:
            if rule["keyword"] in email["subject"].lower() or rule["keyword"] in email["body"].lower():
                if rule["action"] == "Category":
                    email["category"] = rule["value"]
                elif rule["action"] == "Priority":
                    email["priority"] = rule["value"]
    return emails

# Function to generate mini-summary for a category
def get_mini_summary(emails):
    senders = [email["sender"].split('@')[0].capitalize() for email in emails]
    return ", ".join(senders[:3]) + ("..." if len(senders) > 3 else "")

# Authentication
authenticator = Authenticator(
    allowed_users=allowed_users,
    token_key=os.getenv("TOKEN_KEY"),
    secret_path="credentials.json",
    redirect_uri="http://localhost:8501",
)
authenticator.check_auth()

if not st.session_state.get("connected", False):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", width=300)
    
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Sorta - AI Email Summarizer</h1>
        <h3>Please log in to access your email summary</h3>
        <p>Connect your Gmail to get started with AI-powered email organization</p>
    </div>
    """, unsafe_allow_html=True)
    authenticator.login()
    st.stop()

# Send credentials to backend
if "google_creds" in st.session_state:
    creds = st.session_state["google_creds"]
    creds_dict = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
        "id_token": creds.id_token,
        "expiry": creds.expiry.isoformat(),
    }

    try:
        response = requests.post("http://127.0.0.1:3000/gmail-labels", json=creds_dict)
        if response.status_code != 200:
            st.warning("Gmail connection issue - using demo data")
    except requests.exceptions.RequestException:
        st.warning("Backend not available - using demo data")

# Streamlit app
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.png", width=300)

st.markdown(f"""
<div class="main-header">
    <h1>🎯 Sorta</h1>
    <h3>AI-Powered Inbox Declutterer and Summarizer</h3>
    <p>Welcome back, {st.session_state['user_info'].get('email')}! 👋</p>
</div>
""", unsafe_allow_html=True)





# Fetch emails if not already loaded
if "emails" not in st.session_state:
    emails = fetch_and_summarize_emails()
    st.session_state.emails = emails



# Current time for relative time calculation
current_time = datetime.now()

# Summaries section
st.header("AI-Generated Inbox Summary")
st.markdown("A high-level overview of your inbox, grouped by category.")

# Fetch AI summary from backend
try:
    # Try to use Gmail credentials if available
    if "google_creds" in st.session_state:
        try:
            creds = st.session_state["google_creds"]
            creds_dict = {
                "token": creds.token,
                "refresh_token": creds.refresh_token,
                "token_uri": creds.token_uri,
                "client_id": creds.client_id,
                "client_secret": creds.client_secret,
                "scopes": creds.scopes,
                "id_token": creds.id_token,
                "expiry": creds.expiry.isoformat(),
            }
            response = requests.post("http://127.0.0.1:3000/api/summarize", json=creds_dict)
        except:
            response = requests.get("http://127.0.0.1:3000/api/summarize")
    else:
        response = requests.get("http://127.0.0.1:3000/api/summarize")
    
    if response.status_code == 200:
        data = response.json()
        st.markdown(f"""
        <div class="summary-card">
            <h3 style="color: #2c3e50; margin-top: 0;">🤖 AI Analysis</h3>
            <div style="background: white; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                <p style="color: #2c3e50; margin: 0;"><strong>📊 Analyzed {data['emailCount']} emails</strong></p>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px; margin-top: 0.5rem; color: #34495e;">
                    {data['summary']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("AI summary not available - showing basic overview")
except requests.exceptions.RequestException:
    st.warning("Backend not available - showing basic overview")



# Full inbox section
st.header("Your Full Inbox")
st.markdown("Browse all your emails in chronological order.")

st.write(f"Showing {len(st.session_state.emails)} emails")

# Display all emails
filtered_emails = st.session_state.emails
if not filtered_emails:
    st.info("No emails found.")
else:
    filtered_emails.sort(key=lambda e: e["date"], reverse=True)
    with st.container(height=500):
        for email in filtered_emails:
            if email["date"].date() == current_time.date():
                date_str = email["date"].strftime("%I:%M %p")
            else:
                date_str = email["date"].strftime("%a, %b %d, %I:%M %p")
            relative_time = get_relative_time(email["date"], current_time)
            date_display = f"{date_str} ({relative_time})"
            
            with st.container():
                st.markdown(f"<div id='email-{html.escape(email['id'])}'></div>", unsafe_allow_html=True)
                priority_class = f"priority-{email['priority'].lower()}"
                st.markdown(
                    f"""
                    <div class="email-card {priority_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <h4 style="margin: 0; color: #2c3e50;">{html.escape(email['subject'])}</h4>
                            <span class="category-badge">{html.escape(email.get('category', 'Email'))}</span>
                        </div>
                        <div style="color: #7f8c8d; font-size: 0.9rem; margin-bottom: 0.5rem;">
                            📧 {html.escape(email['sender'])} • ⏰ {html.escape(date_display)} • 🎯 {html.escape(email['priority'])}
                        </div>
                        <div style="color: #34495e; line-height: 1.4;">
                            {html.escape(email['summary'])}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                with st.expander("View Full Email"):
                    st.write(f"**Full Body:** {email['body']}")
                    st.button("Mark as Read", key=f"read_{email['id']}")
                    st.button("Archive", key=f"archive_{email['id']}")

# Feedback form
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
    <h4 style="color: #2c3e50; margin-top: 0;">💬 Share Your Feedback</h4>
    <p style="color: #34495e; margin-bottom: 1rem;">Help us improve Sorta! What do you think?</p>
</div>
""", unsafe_allow_html=True)

if "feedback_key" not in st.session_state:
    st.session_state.feedback_key = 0

feedback = st.text_input(
    "Your feedback:",
    placeholder="Type your feedback and press Enter...",
    key=f"feedback_{st.session_state.feedback_key}"
)

if feedback:
    st.success("✨ Thank you for your feedback!")
    st.session_state.feedback_key += 1
    st.rerun()

# Logout button
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if st.button("🚪 Log out", type="secondary"):
        authenticator.logout()