Customer-support-chatbot

chatbot using Numpy, Pydantic, Tensorflow, SpaCy, Rasa, Flask,


Project Overview

This AI chatbot uses Rasa for NLP, GPT-3.5 for advanced responses, and Flask with PostgreSQL for its web interface and session management. It handles FAQs, escalates complex issues, and learns from interactions.

Key Features:

NLP: Rasa & spaCy for intent recognition and entity extraction.
Smart Responses: GPT-3.5 integration for human-like answers.
Issue Escalation: Routes unresolved queries to human agents.
Learning & Improvement: Logs interactions for continuous enhancement.
Web Platform: Flask web app with PostgreSQL for session data.

Technologies:

1. Rasa Open Source
2. spaCy
3. GPT-3.5 (OpenAI API)
4. Python 3.8+
5. Flask
6. PostgreSQL

Setup Instructions

1. Environment Setup

Create and activate a Python virtual environment:

python -m venv chatbot_env
source chatbot_env/bin/activate 

Windows: .\chatbot_env\Scripts\activate

2. Install Dependencies

pip install rasa spacy Flask Flask-SQLAlchemy Flask-Migrate psycopg2-binary openai
python -m spacy download en_core_web_md

3. Configure PostgreSQL

Set up your PostgreSQL database (e.g., chatbot_db).

4. Configure OpenAI API Key

Set your OpenAI API key as an environment variable:

export OPENAI_API_KEY="YOUR_OPENAI_API_KEY" # Windows: set OPENAI_API_KEY="YOUR_OPENAI_API_KEY"

5. Initialize Rasa Project

If not done:

rasa init --no-prompt

6. Populate Rasa Data

Define your chatbot's understanding in data/nlu.yml, conversation flows in data/stories.yml, and overall configuration in domain.yml.

7. Implement Custom Actions (actions.py)

Update actions.py for database connections (action_lookup_order_status) and GPT-3.5 fallback (action_fallback_with_gpt). Remember to update PostgreSQL credentials in actions.py.

8. Configure Flask App (app.py)

Uncomment and configure the SQLALCHEMY_DATABASE_URI in app.py for conversation logging with PostgreSQL.

9. Create HTML Template

Place index.html in a templates/ folder.

Running the Chatbot

Open three separate terminal windows, activate your virtual environment in each, and run:

1. Train Rasa Model:
   rasa train
2. Run Rasa Server:
   rasa run --enable-api --cors "*"
3. Run Custom Actions Server:
   rasa run actions

Run Flask App:
python app.py
