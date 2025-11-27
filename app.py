import streamlit as st
import anthropic
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="HR Assistant Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Custom CSS
st.markdown("""
    <style>
        /* Force background gradient */
        .stApp, .main, [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        }
        
        /* White sidebar */
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
        }
        
        /* Sidebar text color */
        [data-testid="stSidebar"] .element-container {
            color: #1f2937 !important;
        }
        
        /* Main title white */
        .main h1 {
            color: #ffffff !important;
            text-align: center !important;
            font-size: 3rem !important;
            font-weight: 800 !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2) !important;
        }
        
        /* Subtitle white */
        .main .subtitle {
            color: #ffffff !important;
            text-align: center !important;
            font-size: 1.2rem !important;
            margin-bottom: 2rem !important;
        }
        
        /* Chat message cards - white background */
        .stChatMessage {
            background-color: #ffffff !important;
            border-radius: 15px !important;
            padding: 20px !important;
            margin: 15px 0 !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        }
        
        /* Chat message text - dark for readability */
        .stChatMessage p, .stChatMessage li, .stChatMessage span {
            color: #1f2937 !important;
        }
        
        /* Category badge */
        .category-badge {
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            color: #ffffff !important;
            padding: 6px 16px !important;
            border-radius: 20px !important;
            font-size: 11px !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            display: inline-block !important;
            margin-bottom: 10px !important;
        }
        
        /* Buttons gradient */
        .stButton > button {
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 12px 20px !important;
            font-weight: 600 !important;
            width: 100% !important;
            transition: transform 0.2s !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 12px rgba(102, 126, 234, 0.3) !important;
        }
        
        /* Chat input white */
        .stChatInput {
            background-color: #ffffff !important;
            border-radius: 15px !important;
        }
        
        /* Footer */
        .footer {
            text-align: center !important;
            color: #ffffff !important;
            padding: 20px !important;
            background: rgba(255,255,255,0.1) !important;
            border-radius: 15px !important;
            margin-top: 30px !important;
        }
    </style>
""", unsafe_allow_html=True)

# HR Knowledge Base
HR_KNOWLEDGE_BASE = {
    "policies": {
        "remote work": "Our remote work policy allows employees to work from home up to 3 days per week. Managers must approve remote work schedules in advance. Employees must be available during core hours (10 AM - 3 PM) and maintain productivity standards.",
        "dress code": "We maintain a business casual dress code. Jeans are permitted on Fridays. Client-facing roles should dress in business professional attire during client meetings.",
        "code of conduct": "All employees must maintain professional behavior, respect diversity, prevent harassment, and maintain confidentiality of company information.",
        "expense": "Employees can submit expenses through our portal within 30 days. Requires receipts for amounts over $25. Reimbursement processed within 2 weeks.",
        "training": "Each employee receives $2,000 annual training budget. Must be pre-approved by manager and relate to role development.",
        "attendance": "Employees are expected to work standard business hours unless otherwise approved. Flexible scheduling available with manager approval. Report absences to your manager as soon as possible.",
        "performance review": "Annual performance reviews conducted each December. Mid-year check-ins in June. Reviews include goal setting, competency assessment, and development planning."
    },
    "leave": {
        "pto": "Full-time employees receive 15 days PTO annually, accruing at 1.25 days per month. PTO requests should be submitted 2 weeks in advance for manager approval.",
        "sick leave": "Employees receive 10 sick days per year. Can be used for personal illness or to care for immediate family members. No advance notice required for emergency illness.",
        "parental": "Primary caregivers receive 16 weeks paid parental leave. Secondary caregivers receive 8 weeks. Must be used within 12 months of birth or adoption.",
        "bereavement": "Employees receive 5 days bereavement leave for immediate family members (spouse, children, parents, siblings). 3 days for extended family.",
        "holidays": "We observe 10 company holidays annually including New Year's Day, Memorial Day, Independence Day, Labor Day, Thanksgiving (2 days), and Christmas (2 days). Plus 2 floating holidays.",
        "balance": "Check your leave balance in the HR portal under 'My Benefits > Time Off'. Current accruals are updated monthly."
    },
    "benefits": {
        "health insurance": "We offer comprehensive medical, dental, and vision coverage. Company covers 80% of premiums for employees, 60% for dependents. Plans include PPO and HMO options.",
        "retirement": "401(k) with 5% company match. Vested immediately. Can contribute up to IRS limit ($23,000 for 2024). Enrollment available within 30 days of hire.",
        "life insurance": "Company provides 2x annual salary in basic life insurance at no cost. Supplemental coverage available up to 5x salary.",
        "wellness": "$500 annual wellness stipend for gym memberships, fitness classes, or wellness apps. Mental health support through EAP with 24/7 counseling access.",
        "education": "Tuition reimbursement up to $5,250 annually for job-related degrees. Must maintain B grade or higher and stay employed 1 year post-completion.",
        "commuter": "Pre-tax commuter benefits up to $315/month for transit and parking expenses.",
        "stock": "Eligible employees receive annual stock grants based on performance and level. 4-year vesting schedule with 1-year cliff."
    }
}

def get_hr_response(user_query):
    """Process user query and return appropriate response"""
    query = user_query.lower()
    
    # Handle general policy questions
    if ("policy" in query or "policies" in query) and len(query.split()) < 5:
        return {
            "response": """I can help you with information about our company policies:

• Remote Work Policy - Work from home options
• Dress Code - What to wear to work
• Code of Conduct - Professional behavior standards
• Expense Policy - How to submit expenses
• Training Policy - Professional development budget
• Attendance Policy - Working hours and flexibility
• Performance Reviews - When and how reviews happen

Which policy would you like to know more about?""",
            "category": "Company Policies"
        }
    
    # Handle general leave questions
    if ("leave" in query or "time off" in query) and len(query.split()) < 5:
        return {
            "response": """I can help you with information about leave and time off:

• PTO/Vacation - Paid time off policy
• Sick Leave - When you're ill
• Parental Leave - For new parents
• Bereavement Leave - Family loss support
• Company Holidays - Observed holidays
• Leave Balance - How to check your balance

What would you like to know about?""",
            "category": "Leave Options"
        }
    
    # Handle general benefits questions
    if "benefit" in query and len(query.split()) < 5:
        return {
            "response": """Here are the benefits we offer:

• Health Insurance - Medical, dental, and vision
• 401(k) Retirement - Company match program
• Life Insurance - Coverage options
• Wellness Programs - Fitness and mental health
• Education Benefits - Tuition reimbursement
• Commuter Benefits - Transit and parking
• Stock Options - Equity compensation

Which benefit would you like details about?""",
            "category": "Benefits Overview"
        }
    
    # Search specific policies
    for key, value in HR_KNOWLEDGE_BASE["policies"].items():
        if key in query or key.replace(" ", "") in query:
            return {"response": value, "category": "Company Policy"}
    
    # Search leave information
    for key, value in HR_KNOWLEDGE_BASE["leave"].items():
        if (key in query or 
            (key == "pto" and ("vacation" in query or "paid time" in query)) or
            (key == "holidays" and "holiday" in query) or
            (key == "balance" and ("how much" in query or "check my" in query))):
            return {"response": value, "category": "Leave Policy"}
    
    # Search benefits
    for key, value in HR_KNOWLEDGE_BASE["benefits"].items():
        if (key in query or 
            (key == "health insurance" and ("medical" in query or "dental" in query or "vision" in query)) or
            (key == "retirement" and ("401" in query or "retire" in query)) or
            (key == "wellness" and ("gym" in query or "fitness" in query))):
            return {"response": value, "category": "Benefits"}
    
    # Use AI for complex queries
    try:
        if "ANTHROPIC_API_KEY" in st.secrets:
            client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
            
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": f"""You are an HR assistant. Based on this company HR information:

POLICIES: {json.dumps(HR_KNOWLEDGE_BASE["policies"], indent=2)}

LEAVE: {json.dumps(HR_KNOWLEDGE_BASE["leave"], indent=2)}

BENEFITS: {json.dumps(HR_KNOWLEDGE_BASE["benefits"], indent=2)}

Answer this employee question: "{user_query}"

Provide a helpful, professional response. If the information isn't in the knowledge base, politely say you'll need to check with HR and suggest they email hr@company.com."""
                }]
            )
            
            return {
                "response": message.content[0].text,
                "category": "AI Response"
            }
    except Exception as e:
        st.error(f"AI Error: {str(e)}")
    
    # Fallback response
    return {
        "response": "I'm not sure about that specific question. Please try rephrasing or contact HR at hr@company.com for assistance.",
        "category": "General"
    }

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """👋 **Welcome to HR Assistant!**

I'm here to help you with all your HR-related questions. Here's what I can assist you with:

✨ **Company Policies**
• Remote work, dress code, expenses, training, and more

🏖️ **Leave Management**
• PTO, sick leave, parental leave, holidays, and balance checks

💼 **Benefits & Perks**
• Health insurance, 401(k), wellness programs, and education benefits

🎯 **Quick Start**
Use the Quick Actions in the sidebar or simply type your question below!

💬 *How can I help you today?*""",
            "category": "Welcome"
        }
    ]

# Sidebar
with st.sidebar:
    st.markdown("<h1>🤖 HR Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='margin-bottom: 20px;'>⚡ Quick Actions</h3>", unsafe_allow_html=True)
    
    if st.button("📋 View All Policies", use_container_width=True):
        st.session_state.messages.append({
            "role": "user",
            "content": "Tell me about policies"
        })
        result = get_hr_response("Tell me about policies")
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["response"],
            "category": result["category"]
        })
        st.rerun()
    
    if st.button("🏖️ Check PTO Info", use_container_width=True):
        st.session_state.messages.append({
            "role": "user",
            "content": "Tell me about PTO"
        })
        result = get_hr_response("Tell me about PTO")
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["response"],
            "category": result["category"]
        })
        st.rerun()
    
    if st.button("💊 Health Benefits", use_container_width=True):
        st.session_state.messages.append({
            "role": "user",
            "content": "Tell me about health insurance"
        })
        result = get_hr_response("Tell me about health insurance")
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["response"],
            "category": result["category"]
        })
        st.rerun()
    
    if st.button("💰 401(k) Retirement", use_container_width=True):
        st.session_state.messages.append({
            "role": "user",
            "content": "Tell me about retirement"
        })
        result = get_hr_response("Tell me about retirement")
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["response"],
            "category": result["category"]
        })
        st.rerun()
    
    if st.button("🏥 Sick Leave", use_container_width=True):
        st.session_state.messages.append({
            "role": "user",
            "content": "Tell me about sick leave"
        })
        result = get_hr_response("Tell me about sick leave")
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["response"],
            "category": result["category"]
        })
        st.rerun()
    
    if st.button("🎉 Company Holidays", use_container_width=True):
        st.session_state.messages.append({
            "role": "user",
            "content": "Tell me about holidays"
        })
        result = get_hr_response("Tell me about holidays")
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["response"],
            "category": result["category"]
        })
        st.rerun()
    
    st.markdown("<hr style='margin: 25px 0;'>", unsafe_allow_html=True)
    st.markdown("<h3>ℹ️ About</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='about-box'>
        <p><strong>AI-Powered HR Assistant</strong></p>
        <p style='margin-top: 10px;'>Get instant answers about:</p>
        <ul style='margin: 10px 0; padding-left: 20px;'>
            <li>Company policies</li>
            <li>Leave and time off</li>
            <li>Benefits and perks</li>
        </ul>
        <p style='margin-top: 15px;'><strong>Need urgent help?</strong></p>
        <p style='margin: 5px 0;'>📧 hr@company.com</p>
        <p style='margin: 5px 0;'>📞 (555) 123-4567</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()

# Main chat interface
st.markdown("<h1>💼 HR Assistant Agent</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your intelligent companion for all HR-related questions</p>", unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and "category" in message:
            st.markdown(f'<div class="category-badge">{message["category"]}</div>', 
                       unsafe_allow_html=True)
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about policies, leave, or benefits..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = get_hr_response(prompt)
            st.markdown(f'<div class="category-badge">{result["category"]}</div>', 
                       unsafe_allow_html=True)
            st.markdown(result["response"])
    
    # Add assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["response"],
        "category": result["category"]
    })

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    f'''<div class="footer">
        <p style="font-weight: 600; font-size: 15px; margin-bottom: 8px;">HR Assistant Agent v1.0</p>
        <p style="font-size: 12px; opacity: 0.8;">Powered by Claude AI ✨</p>
        <p style="font-size: 11px; margin-top: 10px; opacity: 0.6;">Last updated: {datetime.now().strftime("%B %d, %Y")}</p>
    </div>''',
    unsafe_allow_html=True
)
