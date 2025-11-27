🚀 Local Installation Guide - HR Assistant Agent

This guide will help you set up and run the HR Assistant Agent on your local machine.

📋 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher ([Download Python](https://www.python.org/downloads/))
- pip (Python package installer - comes with Python)
- Git (optional, for cloning the repository)

🔧 Step-by-Step Installation

Step 1: Download the Project

Option A: Clone with Git

git clone https://github.com/yourusername/HR-assistant-agent.git
cd HR-assistant-agent

Option B: Download ZIP
1. Download the project ZIP file from GitHub
2. Extract it to your desired location
3. Open terminal/command prompt in that folder

Step 2: Create a Virtual Environment (Recommended)

On Windows:
python -m venv venv
venv\Scripts\activate

On Mac/Linux:
python3 -m venv venv
source venv/bin/activate

You should see (venv) in your terminal prompt.

Step 3: Install Dependencies
pip install -r requirements.txt

This will install:
- streamlit - Web framework
- anthropic - AI API client
- python-dotenv - Environment variable management

If you encounter errors, try installing packages individually:

pip install streamlit anthropic python-dotenv

Step 4: Configure API Key (Optional)

The app works without an API key using the built-in knowledge base. For AI-powered responses:

Option A: Using Streamlit Secrets (Recommended)

1. Create a .streamlit folder in the project directory:
mkdir .streamlit

2. Create a file named secrets.toml inside .streamlit:

# On Windows
type nul > .streamlit\secrets.toml

# On Mac/Linux
touch .streamlit/secrets.toml

3. Open .streamlit/secrets.toml and add:

ANTHROPIC_API_KEY = "your-api-key-here"

Option B: Using Environment Variable

On Windows:

set ANTHROPIC_API_KEY=your-api-key-here

On Mac/Linux:

export ANTHROPIC_API_KEY="your-api-key-here"

Get your API key:
- Sign up at [Anthropic Console](https://console.anthropic.com/)
- Navigate to API Keys section
- Create a new API key

Step 5: Run the Application
streamlit run app.py

You should see output like:
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501

Step 6: Access the App

Open your web browser and go to:
http://localhost:8501


The HR Assistant Agent should now be running! 🎉

🛑 Stopping the Application

To stop the server:
- Press `Ctrl + C` in the terminal
- Or close the terminal window

🔄 Running Again

After the initial setup, you only need to:

1. Activate virtual environment (if using one):
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   
2. Run the app:
   streamlit run app.py
   
