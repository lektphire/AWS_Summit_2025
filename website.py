import streamlit as st
import os
import requests
import html
from datetime import datetime, timedelta
from dotenv import load_dotenv
from auth import Authenticator

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
    try:
        response = requests.get("http://127.0.0.1:3000/api/emails")
        if response.status_code == 200:
            backend_emails = response.json()
            # Convert backend email format to frontend format
            emails = []
            for email in backend_emails:
                emails.append({
                    "id": email["id"],
                    "sender": email["sender"],
                    "subject": email["subject"],
                    "body": email["body"],
                    "date": datetime.fromisoformat(email["timestamp"].replace('Z', '+00:00')).replace(tzinfo=None),
                    "category": email.get("category", "Work"),  # Use backend category
                    "priority": "Medium",  # Default priority
                    "summary": email["body"][:100] + "..."  # Simple summary
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
    st.title("Sorta - AI Email Summarizer")
    st.markdown("### Please log in to access your email summary")
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
st.title("Sorta")
st.markdown("### AI-Powered Inbox Declutterer and Summarizer")
st.write(f"Welcome! {st.session_state['user_info'].get('email')}")

st.markdown("""
**Instructions:**
1. Use the sidebar on the left to customize rules for categorizing, prioritizing, or archiving your emails.
2. In the 'AI-Generated Inbox Summary' section below, view summaries of all emails grouped by category.
3. Scroll down to 'Your Full Inbox' to browse all emails organized by category using tabs.
4. At the bottom, view demo metrics and provide feedback to help us improve.
""")

# Sidebar for customization
st.sidebar.header("Customization")
st.sidebar.markdown("Define your own rules for categories, priorities, and filters.")

# Store rules in session state
if "rules" not in st.session_state:
    st.session_state.rules = []

# Form to add new rule
with st.sidebar.form(key="add_rule_form"):
    keyword = st.text_input("Keyword to match (e.g., 'promo')")
    action = st.selectbox("Action", ["Category", "Priority", "Auto-Archive"])
    value = st.text_input("Value (e.g., 'Promotions' for category, 'Low' for priority)")
    submit = st.form_submit_button("Add Rule")
    
    if submit and keyword and value:
        st.session_state.rules.append({"keyword": keyword.lower(), "action": action, "value": value})
        st.sidebar.success("Rule added!")

# Display current rules
if st.session_state.rules:
    st.sidebar.subheader("Current Rules")
    for i, rule in enumerate(st.session_state.rules):
        st.sidebar.write(f"{rule['keyword']} → {rule['action']}: {rule['value']}")
        if st.sidebar.button(f"Remove Rule {i+1}", key=f"remove_{i}"):
            del st.session_state.rules[i]
            st.rerun()

# Fetch emails and apply rules if not already loaded
if "emails" not in st.session_state:
    emails = fetch_and_summarize_emails()
    emails = apply_custom_rules(emails, st.session_state.rules)
    st.session_state.emails = emails

# Button to refresh and reapply rules
if st.button("Refresh and Apply Rules"):
    emails = fetch_and_summarize_emails()
    emails = apply_custom_rules(emails, st.session_state.rules)
    st.session_state.emails = emails
    st.success("Inbox refreshed and rules applied!")



# Current time for relative time calculation
current_time = datetime.now()

# Summaries section
st.header("AI-Generated Inbox Summary")
st.markdown("A high-level overview of your inbox, grouped by category.")

# Fetch AI summary from backend
try:
    response = requests.get("http://127.0.0.1:3000/api/summarize")
    if response.status_code == 200:
        data = response.json()
        st.info(f"AI Summary for {data['emailCount']} emails")
        st.markdown("### 🤖 AI Analysis")
        st.write(data['summary'])
    else:
        st.warning("AI summary not available - showing basic overview")
except requests.exceptions.RequestException:
    st.warning("Backend not available - showing basic overview")

# Group emails by category
all_categories = ["Work", "Education", "Finance", "Personal", "Subscriptions", "Promotions", "Spam"]
existing_categories = list(set(email["category"] for email in st.session_state.emails))
categories = [cat for cat in all_categories if cat in existing_categories] + [cat for cat in existing_categories if cat not in all_categories]

# Reorder Categories section (moved here after categories are defined)
st.sidebar.subheader("Reorder Categories")
if "category_order" not in st.session_state:
    st.session_state.category_order = categories

reordered_categories = st.sidebar.multiselect(
    "Drag to reorder (top = first tab):",
    options=categories,
    default=[cat for cat in st.session_state.category_order if cat in categories],
    key="category_reorder"
)

if reordered_categories:
    st.session_state.category_order = reordered_categories
    categories = reordered_categories

category_emails = {cat: [e for e in st.session_state.emails if e["category"] == cat] for cat in categories}

st.markdown("### 📂 Category Breakdown")
for category in categories:
    emails = category_emails[category]
    mini_summary = get_mini_summary(emails)
    with st.expander(f"{category} ({len(emails)}) - {mini_summary}"):
        emails.sort(key=lambda e: e["date"], reverse=True)
        st.markdown("**Recent emails:**")
        for email in emails:
            st.markdown(f"- [{email['summary']}](#email-{email['id']})")

# Full inbox section
st.header("Your Full Inbox")
st.markdown("Scroll through your entire inbox, organized by category.")

# Add refresh button for inbox
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🔄 Refresh Inbox"):
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
                        "category": "Work",
                        "priority": "Medium",
                        "summary": email["body"][:100] + "..."
                    })
                emails = apply_custom_rules(emails, st.session_state.rules)
                st.session_state.emails = emails
                st.success(f"Refreshed {len(emails)} emails from backend!")
            else:
                st.error("Failed to refresh emails")
        except requests.exceptions.RequestException as e:
            st.error(f"Backend connection error: {e}")
with col2:
    st.write(f"Showing {len(st.session_state.emails)} emails from backend API")

# Create tabs with "All" first, followed by categories
tabs = st.tabs(["All"] + categories)

# "All" tab
with tabs[0]:
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
                    st.markdown(
                        f"""
                        <div style='background-color: rgba(0,0,0,0.05); padding: 8px; border-radius: 8px; border-left: 3px solid #1f77b4;'>
                            <b>{html.escape(email['subject'])} - From: {html.escape(email['sender'])} (Priority: {html.escape(email['priority'])})</b>
                        </div>
                        <div style='padding: 5px; color: #666;'>
                            {html.escape(date_display)} - {html.escape(email['summary'])}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    with st.expander("View Full Email"):
                        st.write(f"**Full Body:** {email['body']}")
                        st.button("Mark as Read", key=f"read_{email['id']}_All")
                        st.button("Archive", key=f"archive_{email['id']}_All")

# Category tabs
for i, category in enumerate(categories, 1):
    with tabs[i]:
        filtered_emails = category_emails[category]
        if not filtered_emails:
            st.info("No emails in this category.")
            continue
        
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
                    st.markdown(
                        f"""
                        <div style='background-color: rgba(0,0,0,0.05); padding: 8px; border-radius: 8px; border-left: 3px solid #1f77b4;'>
                            <b>{html.escape(email['subject'])} - From: {html.escape(email['sender'])} (Priority: {html.escape(email['priority'])})</b>
                        </div>
                        <div style='padding: 5px;'>
                            {html.escape(date_display)} - {html.escape(email['summary'])}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    with st.expander("View Full Email"):
                        st.write(f"**Full Body:** {email['body']}")
                        st.button("Mark as Read", key=f"read_{email['id']}_{category}")
                        st.button("Archive", key=f"archive_{email['id']}_{category}")

# Metrics section
st.header("Usage Metrics (Demo)")
col1, col2, col3 = st.columns(3)
col1.metric("Time Saved", "15 min/day")
col2.metric("Unread Reduction", "50%")
col3.metric("Satisfaction Score", "4.8/5")

# Feedback form
st.header("Provide Feedback")
with st.form(key="feedback_form"):
    feedback = st.text_area("How can we improve Sorta?")
    rating = st.slider("Rate your experience", 1, 5, 3)
    submit_feedback = st.form_submit_button("Submit")
    if submit_feedback:
        st.success("Thank you for your feedback!")

# Logout button
if st.button("Log out"):
    authenticator.logout()