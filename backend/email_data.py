emails = [
    # Work emails
    {"id": "1", "subject": "Q4 Sales Report - Action Required", "sender": "sarah.manager@company.com", "body": "Hi John, Please review the attached Q4 sales report. We need to discuss the 15% decline in the Northeast region and develop an action plan for Q1. The board meeting is scheduled for next Friday.", "timestamp": "2024-01-15T09:30:00Z", "isRead": False, "category": "Work"},
    {"id": "2", "subject": "Project Alpha Update - API Issues", "sender": "dev.team@company.com", "body": "Update on Project Alpha: We're experiencing significant delays due to third-party API rate limiting. Frontend is nearly complete at 85% but backend integration is blocked. Need to discuss alternative solutions.", "timestamp": "2024-01-14T09:15:00Z", "isRead": False, "category": "Work"},
    
    # Education emails
    {"id": "3", "subject": "Course Registration Deadline", "sender": "registrar@university.edu", "body": "Reminder: Course registration for Spring 2024 semester closes on January 20th. Please complete your enrollment to secure your spot in required classes. Late registration fees apply after the deadline.", "timestamp": "2024-01-16T10:00:00Z", "isRead": False, "category": "Education"},
    {"id": "4", "subject": "Final Exam Schedule Released", "sender": "academics@university.edu", "body": "The final exam schedule for Fall 2023 has been posted. Check your student portal for exam dates, times, and locations. Study groups are available in the library starting next week.", "timestamp": "2024-01-12T14:30:00Z", "isRead": True, "category": "Education"},
    
    # Finance emails
    {"id": "5", "subject": "Monthly Bank Statement Available", "sender": "statements@bank.com", "body": "Your January 2024 bank statement is now available online. Account balance: $3,247.89. Recent transactions include salary deposit and utility payments. Review for any discrepancies.", "timestamp": "2024-01-31T08:00:00Z", "isRead": False, "category": "Finance"},
    {"id": "6", "subject": "Credit Card Payment Due", "sender": "billing@creditcard.com", "body": "Your credit card payment of $892.45 is due on February 5th. Minimum payment: $25. Pay online or set up autopay to avoid late fees. Current balance includes recent purchases and interest charges.", "timestamp": "2024-01-28T12:00:00Z", "isRead": False, "category": "Finance"},
    
    # Personal emails
    {"id": "7", "subject": "Family Dinner This Weekend", "sender": "mom@family.com", "body": "Hi honey! We're having family dinner this Sunday at 6 PM. Your sister is bringing her new boyfriend. Can you bring dessert? Also, don't forget Dad's birthday is next week. Love, Mom", "timestamp": "2024-01-17T15:30:00Z", "isRead": True, "category": "Personal"},
    {"id": "8", "subject": "Doctor Appointment Reminder", "sender": "appointments@clinic.com", "body": "Reminder: You have a doctor's appointment scheduled for January 25th at 2:30 PM with Dr. Smith. Please arrive 15 minutes early and bring your insurance card and ID.", "timestamp": "2024-01-23T09:00:00Z", "isRead": False, "category": "Personal"},
    
    # Subscriptions emails
    {"id": "9", "subject": "Netflix: New Shows This Week", "sender": "info@netflix.com", "body": "Check out what's new on Netflix this week! New releases include 'Mystery Manor' season 2, 'Tech Titans' documentary, and 'Comedy Central Roast'. Watch now on all your devices.", "timestamp": "2024-01-22T11:00:00Z", "isRead": True, "category": "Subscriptions"},
    {"id": "10", "subject": "Spotify Premium Renewal", "sender": "billing@spotify.com", "body": "Your Spotify Premium subscription will renew on February 1st for $9.99. Enjoy ad-free music, offline downloads, and high-quality audio. Manage your subscription in account settings.", "timestamp": "2024-01-26T07:45:00Z", "isRead": False, "category": "Subscriptions"},
    
    # Promotions emails
    {"id": "11", "subject": "50% Off Winter Sale - Limited Time!", "sender": "deals@retailstore.com", "body": "Huge winter clearance sale! Save 50% on all winter clothing, boots, and accessories. Free shipping on orders over $75. Sale ends January 31st. Shop now before items sell out!", "timestamp": "2024-01-20T13:15:00Z", "isRead": False, "category": "Promotions"},
    {"id": "12", "subject": "Flash Sale: Electronics 30% Off", "sender": "sales@techstore.com", "body": "24-hour flash sale on electronics! Save 30% on laptops, tablets, headphones, and smart home devices. Use code FLASH30 at checkout. Sale ends tomorrow at midnight!", "timestamp": "2024-01-19T16:20:00Z", "isRead": True, "category": "Promotions"},
    
    # Spam emails
    {"id": "13", "subject": "You've Won $1,000,000!", "sender": "winner@lottery.fake", "body": "Congratulations! You've won our international lottery! Claim your $1,000,000 prize by clicking this link and providing your bank details. Act fast - this offer expires soon!", "timestamp": "2024-01-21T03:22:00Z", "isRead": False, "category": "Spam"},
    {"id": "14", "subject": "Urgent: Verify Your Account", "sender": "security@phishing.fake", "body": "Your account has been compromised! Click here immediately to verify your identity and secure your account. Failure to act within 24 hours will result in permanent account suspension.", "timestamp": "2024-01-18T02:15:00Z", "isRead": False, "category": "Spam"},
    
    # Additional mixed emails
    {"id": "15", "subject": "Gym Membership Renewal", "sender": "billing@fitnessgym.com", "body": "Your annual gym membership expires on February 15th. Renew now and save 20% on your next year. New classes added: yoga, pilates, and HIIT training. Visit us or renew online.", "timestamp": "2024-01-24T10:30:00Z", "isRead": False, "category": "Personal"}
]