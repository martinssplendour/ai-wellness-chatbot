# AI Wellness Chatbot

AI Wellness Chatbot is a Flask prototype for supportive, wellness-oriented conversation using retrieval-style context and an OpenAI-backed chat interface.

## Overview

This project explores how conversational AI can provide general wellbeing support and signpost users toward helpful resources. It includes a lightweight Flask backend, templates/static assets, and a small knowledge base.

## Features

- Flask web application.
- OpenAI API integration through environment variables.
- Local knowledge-base JSON for contextual responses.
- Basic deployment files for WSGI hosting.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
python tbackend.py
```

## Safety Disclaimer

This is a wellness chatbot prototype. It is not a therapist, medical device, crisis service, or substitute for professional care. Do not use it for emergency mental-health support.

