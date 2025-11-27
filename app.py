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

# Custom CSS
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}
.stChatMessage {
    background-color: white;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.category-badge {
    background-color: #4F46E5;
    color: white;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 8px;
}
h1 {
    color: #1F2937;
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
    st.session_state.messages = [{
        "role": "assistant",
        "content": """Hello! I'm your HR Assistant. I can help you with:

• Company policies
• Leave requests and balance
• Benefits information
• Holiday schedules

What would you like to know?""",
        "category": "Welcome"
    }]

# Sidebar
with st.sidebar:
    st.title("🤖 HR Assistant")
    st.markdown("---")
    
    st.subheader("Quick Actions")
    
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
    
    if st.button("🏖 Check PTO Info", use_container_width=True):
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
    
    st.markdown("---")
    st.subheader("About")
    st.info("""This HR Assistant uses AI to answer your questions about:
- Company policies
- Leave and time off
- Benefits and perks

For urgent matters, contact:
📧 hr@company.com
📞 (555) 123-4567""")
    
    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()

# Main chat interface
st.title("💼 HR Assistant Agent")
st.markdown("Ask me anything about company policies, leave, or benefits!")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and "category" in message:
            st.markdown(
                f'<div class="category-badge">{message["category"]}</div>',
                unsafe_allow_html=True
            )
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
            st.markdown(
                f'<div class="category-badge">{result["category"]}</div>',
                unsafe_allow_html=True
            )
            st.markdown(result["response"])
    
    # Add assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["response"],
        "category": result["category"]
    })

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #6B7280; font-size: 14px;">'
    'HR Assistant Agent v1.0 | Powered by Claude AI | '
    f'Last updated: {datetime.now().strftime("%Y-%m-%d")}'
    '</div>',
    unsafe_allow_html=True
)
