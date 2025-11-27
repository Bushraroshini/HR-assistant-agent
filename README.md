🤖 HR Assistant Agent

An intelligent AI-powered HR assistant that helps employees get instant answers to their questions about company policies, leave management, and benefits.

📋 Overview

The HR Assistant Agent is a conversational AI chatbot designed to provide employees with instant, accurate information about:

- Company Policies: Remote work, dress code, expenses, training, attendance, performance reviews
- Leave Management: PTO, sick leave, parental leave, bereavement, holidays
- Benefits: Health insurance, 401(k), life insurance, wellness programs, education reimbursement

The agent uses a hybrid approach combining a structured knowledge base for common queries with Claude AI for complex questions.

✨ Features

Core Capabilities

✅ Instant Answers - Get immediate responses to HR queries  
✅ Natural Language Processing - Ask questions in plain English  
✅ Comprehensive Knowledge Base - Covers 20+ HR topics  
✅ AI-Powered Intelligence - Uses Claude Sonnet 4 for complex queries  
✅ Quick Actions - Pre-defined buttons for common questions  
✅ Chat History - Maintains conversation context  
✅ Category Tagging - Responses labeled by topic area  
✅ Mobile Responsive - Works on all devices  

User Experience

- Clean, intuitive chat interface
- Quick action buttons for common queries
- Real-time responses with loading indicators
- Categorized responses for easy navigation
- Chat history with clear conversation flow

🚫 Limitations

1. Static Knowledge Base: Information is hardcoded and needs manual updates
2. No Authentication: Does not verify employee identity or access levels
3. No Database Integration: Cannot access real-time employee data (PTO balances, etc.)
4. Limited Personalization: Provides general information, not employee-specific data
5. No Action Capabilities: Cannot submit leave requests or make changes
6. English Only: Does not support multiple languages
7. API Dependency: Requires Anthropic API for complex queries

🛠 Tech Stack

Frontend
- Streamlit (1.31.0) - Web application framework
- Custom CSS - UI styling and theming

Backend
- Python (3.8+) - Core programming language
- JSON - Knowledge base storage

AI & APIs
- Anthropic Claude API - AI-powered responses
- Claude Sonnet 4 - Latest language model for complex queries

Dependencies

streamlit==1.31.0
anthropic==0.18.1
python-dotenv==1.0.1

📦 Setup & Installation

Prerequisites
- Python 3.8 or higher
- Anthropic API key (optional but recommended)
- Git (for cloning repository)

Local Setup

1. Clone the Repository

git clone https://github.com/yourusername/hr-assistant-agent.git
cd hr-assistant-agent

2. Create Virtual Environment

python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

4. Configure API Key (Optional)

Create a .streamlit/secrets.toml file:
ANTHROPIC_API_KEY = "your-api-key-here"

Or set environment variable:
export ANTHROPIC_API_KEY="your-api-key-here"

5. Run the Application

streamlit run app.py

6. Access the App
Open your browser and navigate to:

http://localhost:8501


🚀 Deployment

Streamlit Cloud (Recommended)

1. Push code to GitHub repository
2. Go to (https://share.streamlit.io)
3. Connect your GitHub account
4. Select your repository
5. Add ANTHROPIC_API_KEY in Secrets (Settings)
6. Deploy!

Docker Deployment

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501"]


Build and run:

docker build -t hr-assistant .
docker run -p 8501:8501 hr-assistant

🔄 Potential Improvements

Short-term Enhancements

1. Multi-language Support - Add translations for global teams
2. Voice Input - Allow voice queries via speech recognition
3. Export Chat - Download conversation history as PDF
4. Sentiment Analysis - Detect frustrated users and escalate
5. Search History - Show frequently asked questions

Medium-term Features

6. Database Integration - Connect to HRIS for real-time data
7. Employee Authentication - SSO integration for personalized data
8. Action Capabilities - Submit leave requests, update info
9. Analytics Dashboard - Track query patterns and satisfaction
10. Email Notifications - Send summaries of policy changes

Long-term Vision

11. Multi-modal Input - Process document uploads (offer letters, etc.)
12. Predictive Assistance - Proactive policy reminders
13. Integration Hub - Connect with Slack, Teams, email
14. Workflow Automation - Automated approval routing
15. Knowledge Graph - Advanced semantic search
16. Custom Training - Fine-tune on company-specific data


