import streamlit as st
import pandas as pd
import random
import requests
from datetime import datetime, timedelta

# Function to generate relative time string
def get_relative_time(email_date, current_time):
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

# Mock function to simulate email fetching for Bob Parr's inbox
def fetch_and_summarize_emails():
    now = datetime.now()
    # Generate random times for each email
    random_times = [
        now - timedelta(hours=random.randint(0, 5)),
        now - timedelta(hours=random.randint(6, 12)),
        now - timedelta(days=1, hours=random.randint(0, 23)),
        now - timedelta(days=1, hours=random.randint(0, 23)),
        now - timedelta(days=2, hours=random.randint(0, 23)),
        now - timedelta(days=2, hours=random.randint(0, 23)),
        now - timedelta(days=3, hours=random.randint(0, 23)),
        now - timedelta(days=3, hours=random.randint(0, 23)),
        now - timedelta(days=4, hours=random.randint(0, 23)),
        now - timedelta(days=4, hours=random.randint(0, 23)),
    ]
    
    emails = [
        {
            "id": "1",
            "sender": "woody@fanclub.com",
            "subject": "Toy Story Fan Club Newsletter",
            "body": "Hi Bob, welcome to the Toy Story Fan Club newsletter! This week, we’re sharing updates on new collectible Woody and Buzz action figures, a sneak peek at Toy Story 5, and a 15% off coupon for our online store. Join our virtual fan meetup on Saturday!",
            "date": random_times[0],
            "category": "Subscriptions",
            "priority": "Low",
            "summary": "Woody shares Toy Story 5 sneak peek and 15% off coupon."
        },
        {
            "id": "2",
            "sender": "mikewazowski@work.com",
            "subject": "Urgent Meeting: Insurance Claims Review",
            "body": "Hey Bob, we need you at a meeting at 4 PM today in the Insuricare boardroom. We’ll review the backlog of superhero-related insurance claims and discuss the new policy for Metroville clients. Your expertise is crucial, so come prepared with ideas!",
            "date": random_times[1],
            "category": "Work",
            "priority": "High",
            "summary": "Mike Wazowski requests meeting at 4 PM for claims review."
        },
        {
            "id": "3",
            "sender": "dash@family.com",
            "subject": "Track Meet This Weekend",
            "body": "Dad, I’m super excited for my track meet this Sunday at 10 AM! Can you and Mom come cheer me on? It’s at Metroville High, and I’m aiming to break my personal record. Also, can we grab pizza after? Love, Dash.",
            "date": random_times[2],
            "category": "Personal",
            "priority": "Medium",
            "summary": "Dash invites you to his track meet on Sunday."
        },
        {
            "id": "4",
            "sender": "buzz@galactictoys.com",
            "subject": "Star Command Sale!",
            "body": "To infinity and beyond, Bob! Galactic Toys is having a 40% off sale on all superhero action figures, including Mr. Incredible collectibles. Sale ends in 48 hours. Shop at galactictoys.com with code HERO40!",
            "date": random_times[3],
            "category": "Promotions",
            "priority": "Low",
            "summary": "Buzz offers 40% off superhero action figures."
        },
        {
            "id": "5",
            "sender": "simba@bank.com",
            "subject": "October Bank Statement",
            "body": "Dear Bob Parr, your October 2025 bank statement is ready. Current balance: $7,500. Transactions include: $3,000 deposit on Oct 1, $600 withdrawal for Violet’s school trip on Oct 2, and $1,500 for home repairs. Review for discrepancies.",
            "date": random_times[4],
            "category": "Finance",
            "priority": "Medium",
            "summary": "Simba sent October statement with $7,500 balance."
        },
        {
            "id": "6",
            "sender": "nemo@metrovillehigh.edu",
            "subject": "Violet’s Science Project Deadline",
            "body": "Dear Mr. Parr, this is a reminder that Violet’s science project on renewable energy is due Thursday, October 9, 2025. She needs to submit a 2000-word report via the Metroville High portal. Please support her in meeting this deadline.",
            "date": random_times[5],
            "category": "Education",
            "priority": "High",
            "summary": "Nemo reminds Violet’s science project due Thursday."
        },
        {
            "id": "7",
            "sender": "lotso@shadydeals.com",
            "subject": "You’ve Won a Free Vacation!",
            "body": "Congratulations, Bob! You’ve won a free vacation package to Sunnyside Resort. Click the link to claim by providing your credit card details for verification. Hurry, this offer expires soon!",
            "date": random_times[6],
            "category": "Spam",
            "priority": "Low",
            "summary": "Lotso claims you won a free vacation."
        },
        {
            "id": "8",
            "sender": "helen@family.com",
            "subject": "Family Dinner Plans",
            "body": "Hi honey, let’s plan a family dinner this Friday at 6 PM. I’m thinking we try that new Italian place in Metroville. Also, Jack-Jack has a playdate Saturday, so we’ll need to coordinate. Love you! - Helen",
            "date": random_times[7],
            "category": "Personal",
            "priority": "Medium",
            "summary": "Helen suggests family dinner on Friday."
        },
        {
            "id": "9",
            "sender": "sully@work.com",
            "subject": "Weekly Claims Report",
            "body": "Hi Bob, here’s the weekly claims report for Insuricare. We processed 25 new superhero damage claims, up 10% from last week. Top issues: property damage from villain fights. Let me know if you need details for the team meeting.",
            "date": random_times[8],
            "category": "Work",
            "priority": "Medium",
            "summary": "Sully shares claims report with 10% increase."
        },
        {
            "id": "10",
            "sender": "wall-e@ecogear.com",
            "subject": "Eco-Friendly Gym Gear Offer",
            "body": "Beep boop, Bob! EcoGear is offering 25% off eco-friendly gym gear, perfect for superhero workouts. Includes recycled-material weights and yoga mats. Valid until October 31, 2025. Shop at ecogear.com with code ECO25!",
            "date": random_times[9],
            "category": "Promotions",
            "priority": "Low",
            "summary": "Wall-E offers 25% off eco-friendly gym gear."
        },
    ]
    return emails

# Mock function to apply custom rules
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
    senders = []
    for email in emails:
        sender = email["sender"].split('@')[0]
        # Handle specific sender name formatting
        if sender.lower() == sender:
            if sender == "mikewazowski":
                sender = "Mike Wazowski"
            elif sender == "wall-e":
                sender = "Wall-E"
            else:
                sender = sender.capitalize()
        senders.append(sender)
    return ", ".join(senders[:3]) + ("..." if len(senders) > 3 else "")

# Static color palette for categories (default values)
default_colors = {
    "Work": "#4B8BBE",  # Blue
    "Education": "#2ECC71",  # Green
    "Finance": "#F1C40F",  # Yellow
    "Personal": "#3498DB",  # Light Blue
    "Subscriptions": "#9B59B6",  # Purple
    "Promotions": "#E67E22",  # Orange
    "Spam": "#E74C3C"  # Red
}

# Initialize category colors and order in session state
if "category_colors" not in st.session_state:
    st.session_state.category_colors = default_colors.copy()

default_priority = ["Work", "Education", "Finance", "Personal", "Subscriptions", "Promotions", "Spam"]
categories = sorted(list(set(email["category"] for email in fetch_and_summarize_emails())))
if "category_order" not in st.session_state:
    st.session_state.category_order = [cat for cat in default_priority if cat in categories]

# Streamlit app
st.title("Sorta")
st.markdown(
    """
    <h2 style='margin-top: 2px;'>Your AI-Powered Inbox Declutterer and Summarizer</h2>
    """,
    unsafe_allow_html=True
)

st.markdown("""
Welcome to Sorta, Bob Parr!

**Instructions:**
1. In the 'AI-Generated Inbox Summary' section below, view summaries of all emails grouped by category. Click a category to see a list of key points for each email, with links to jump to the full email.
2. Scroll down to 'Your Full Inbox' to browse all emails organized by category using tabs. Each email shows key details; expand to view the full body and actions.
3. Use the sidebar on the left to customize rules for categorizing, prioritizing, or archiving your emails. Add rules by entering a keyword, selecting an action, and providing a value.
4. At the bottom, view demo metrics and provide feedback to help us improve.
""")

# JavaScript for email highlight on link click
st.markdown(
    """
    <script>
        window.addEventListener('hashchange', function() {
            const hash = window.location.hash;
            if (hash) {
                const element = document.querySelector(hash);
                if (element) {
                    element.classList.add('highlight');
                    setTimeout(() => {
                        element.classList.remove('highlight');
                    }, 5000);
                }
            }
        });
        // Trigger highlight on page load if hash exists
        window.addEventListener('load', function() {
            const hash = window.location.hash;
            if (hash) {
                const element = document.querySelector(hash);
                if (element) { element.classList.add('highlight'); }
            }
        });
    </script>
    <style>
        .highlight {
            background-color: #FFFFCC !important;
            animation: fadeOut 5s forwards;
        }
        @keyframes fadeOut {
            from { background-color: #FFFFCC; }
            to { background-color: transparent; }
        }
        /* Compact color picker styling */
        .color-picker-container label {
            font-size: 14px;
            margin-bottom: 2px;
        }
        .color-picker-container input[type='color'] {
            width: 50px;
            height: 30px;
            margin: 2px 0;
        }
        /* Horizontal button styling */
        div[data-testid='stHorizontalBlock'] button {
            margin: 2px;
            padding: 5px 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

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

# Refresh and apply rules button
if st.sidebar.button("Refresh and Apply Rules"):
    emails = fetch_and_summarize_emails()
    emails = apply_custom_rules(emails, st.session_state.rules)
    st.session_state.emails = emails
    st.success("Inbox refreshed and rules applied!")

# Reorder categories
st.sidebar.subheader("Reorder Categories")
st.sidebar.markdown("Select and arrange categories to set their display order.")
new_order = st.sidebar.multiselect(
    "Category Order",
    options=categories,
    default=st.session_state.category_order,
    key="category_order_input"
)
if st.sidebar.button("Refresh with New Order"):
    if set(new_order) == set(categories) and len(new_order) == len(categories):
        st.session_state.category_order = new_order
        st.rerun()
    else:
        st.sidebar.error("Please select all categories in the desired order.")

# Improved color selection tool
st.sidebar.subheader("Customize Category Colors")
st.sidebar.markdown("Select a color for each category.")
cols = st.sidebar.columns(2)
for i, cat in enumerate(categories):
    with cols[i % 2]:
        st.markdown(f"**{cat}**")
        color = st.color_picker("", value=st.session_state.category_colors.get(cat, "#CCCCCC"), key=f"color_{cat}")
        if color != st.session_state.category_colors.get(cat, "#CCCCCC"):
            st.session_state.category_colors[cat] = color
            st.rerun()

# Template mode toggle
use_template = st.sidebar.checkbox("Use Baseline Template Mode", value=True)
if use_template:
    st.sidebar.info("Template mode enabled: Default categorization and prioritization applied.")

# Fetch emails and apply rules if not already loaded
if "emails" not in st.session_state:
    emails = fetch_and_summarize_emails()
    emails = apply_custom_rules(emails, st.session_state.rules)
    st.session_state.emails = emails

# Current time for relative time calculation
current_time = datetime.now()

# Summaries section
st.header("AI-Generated Inbox Summary")
st.markdown("A high-level overview of your inbox, grouped by category. Click a category to view summaries of all emails, with links to jump to the full email. Categories are sorted by your custom order.")

# Group emails by category
category_emails = {cat: [e for e in st.session_state.emails if e["category"] == cat] for cat in categories}

# Use custom category order
sorted_categories = [cat for cat in st.session_state.category_order if cat in category_emails]

for category in sorted_categories:
    emails = category_emails[category]
    mini_summary = get_mini_summary(emails)
    color = st.session_state.category_colors.get(category, "#CCCCCC")
    with st.expander(f"{category} ({len(emails)}) - {mini_summary}", expanded=False):
        # Apply solid colored background to expander header
        st.markdown(
            f"""
            <style>
                div[data-testid='stExpander'] div[role='button'] {{
                    background-color: {color} !important;
                    color: #FFFFFF !important;
                    border-radius: 5px;
                    padding: 10px;
                }}
                div[data-testid='stExpander'] div[role='button'] p {{
                    color: #FFFFFF !important;
                    font-weight: bold;
                }}
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown("**Summary of emails:**")
        for email in emails:
            st.markdown(f"- [{email['summary']}](#email-{email['id']})")

# Full inbox section
st.header("Your Full Inbox")
st.markdown("Scroll through your entire inbox, organized by category. Use the tabs to switch categories or view all. Each email shows key details; expand to view the full body and actions.")

# Create tabs with "All" first, followed by sorted categories
tabs = st.tabs(["All"] + sorted_categories)

# "All" tab
with tabs[0]:
    filtered_emails = st.session_state.emails
    if not filtered_emails:
        st.info("No emails in this category.")
    else:
        # Sort by date descending
        filtered_emails.sort(key=lambda e: e["date"], reverse=True)
        # Scrollable container (height ~500px to show 5-7 emails)
        with st.container(height=500):
            for email in filtered_emails:
                # Format date: 12-hour with relative time
                if email["date"].date() == current_time.date():
                    date_str = email["date"].strftime("%I:%M %p")
                else:
                    date_str = email["date"].strftime("%a, %b %d, %I:%M %p")
                relative_time = get_relative_time(email["date"], current_time)
                
                with st.container():
                    # Anchor tag for email linking
                    st.markdown(f"<div id='email-{email['id']}'></div>", unsafe_allow_html=True)
                    # Apply colored border based on category
                    color = st.session_state.category_colors.get(email["category"], "#CCCCCC")
                    st.markdown(
                        f"""
                        <div style='border-left: 4px solid {color}; padding-left: 10px;'>
                            <div style='background-color: #f0f0f0; padding: 5px; border-radius: 5px;'>
                                <b>{email['subject']} - {email['summary']}</b>
                            </div>
                            <div style='display: flex; justify-content: space-between; padding: 5px;'>
                                <span>From: {email['sender']} (Priority: {email['priority']})</span>
                                <span>{date_str} ({relative_time})</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    # Expander for full body and actions
                    with st.expander("View Full Email"):
                        st.write(f"**Full Body:** {email['body']}")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.button("Mark as Read", key=f"read_{email['id']}_All_{random.randint(0,10000)}")
                        with col2:
                            st.button("Archive", key=f"archive_{email['id']}_All_{random.randint(0,10000)}")

# Category tabs
for i, category in enumerate(sorted_categories, 1):
    with tabs[i]:
        filtered_emails = category_emails[category]
        if not filtered_emails:
            st.info("No emails in this category.")
            continue
        
        # Sort by date descending
        filtered_emails.sort(key=lambda e: e["date"], reverse=True)
        # Scrollable container (height ~500px to show 5-7 emails)
        with st.container(height=500):
            for email in filtered_emails:
                # Format date: 12-hour with relative time
                if email["date"].date() == current_time.date():
                    date_str = email["date"].strftime("%I:%M %p")
                else:
                    date_str = email["date"].strftime("%a, %b %d, %I:%M %p")
                relative_time = get_relative_time(email["date"], current_time)
                
                with st.container():
                    # Anchor tag for email linking
                    st.markdown(f"<div id='email-{email['id']}'></div>", unsafe_allow_html=True)
                    # Apply colored border based on category
                    color = st.session_state.category_colors.get(category, "#CCCCCC")
                    st.markdown(
                        f"""
                        <div style='border-left: 4px solid {color}; padding-left: 10px;'>
                            <div style='background-color: #f0f0f0; padding: 5px; border-radius: 5px;'>
                                <b>{email['subject']} - {email['summary']}</b>
                            </div>
                            <div style='display: flex; justify-content: space-between; padding: 5px;'>
                                <span>From: {email['sender']} (Priority: {email['priority']})</span>
                                <span>{date_str} ({relative_time})</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    # Expander for full body and actions
                    with st.expander("View Full Email"):
                        st.write(f"**Full Body:** {email['body']}")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.button("Mark as Read", key=f"read_{email['id']}_{category}_{random.randint(0,10000)}")
                        with col2:
                            st.button("Archive", key=f"archive_{email['id']}_{category}_{random.randint(0,10000)}")

# Metrics section (for testing success)
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