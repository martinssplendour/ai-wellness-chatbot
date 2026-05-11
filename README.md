# AI Wellness Chatbot

AI Wellness Chatbot is a Flask prototype for supportive, wellness-oriented conversation using a small local knowledge base and an OpenAI-backed chat interface. It is a cleaned and safer public version of earlier AI therapist experiments, reframed as a general wellbeing prototype rather than a clinical or therapy product.

## What This Project Does

The app provides a simple web interface where a user can enter a wellbeing-related message and receive a supportive AI-generated response. The backend can combine the user message with local knowledge-base context before calling the language model. The project is useful as a compact example of Flask routing, environment-based API configuration, template rendering, and safe framing for sensitive AI use cases.

## The Work Behind The Project

This project started from several local AI therapist experiments and was cleaned into a safer public wellness-chatbot repository. The important work was not just putting a language model behind a text box; it was reframing the product, removing logs, separating secrets, and documenting the limitations clearly.

The backend uses Flask to serve the web page and process user messages. A local JSON knowledge base provides support context that can be injected into the model prompt, giving the app a simple retrieval-style pattern without requiring a separate vector database. API keys are read from environment variables so the public repo can be shared without exposing credentials.

The project was also deliberately renamed and documented as a wellness chatbot rather than a therapy product. That matters because mental-health-adjacent tools can create user trust they have not earned. The README and codebase avoid presenting the project as diagnosis, treatment, crisis support, or a replacement for professional care.

## Response Flow

1. The user submits a message through the HTML form.
2. Flask receives the request in `tbackend.py`.
3. The app can load relevant support context from `uk_therapy_knowledge_base.json`.
4. The backend builds a model prompt with safety-aware framing.
5. The language model response is returned to the template for display.

## Key Features

- Flask web application.
- HTML template and static image asset.
- OpenAI API integration through environment variables.
- Local JSON knowledge base for contextual support content.
- WSGI entry point for deployment.
- `.env.example` for safe configuration without committing secrets.
- Public safety framing to avoid presenting the app as medical care.

## Tech Stack

- Python
- Flask
- OpenAI API
- HTML templates
- JSON knowledge base

## What This Demonstrates

- Flask application structure for a small AI web app.
- Environment-based secret handling through `.env.example`.
- Use of local structured knowledge as prompt context.
- Public cleanup of conversation logs and virtual environments.
- Safety-conscious product framing for sensitive AI interactions.
- Simple WSGI deployment readiness.

## Repository Structure

```text
tbackend.py                       # Main Flask application
wsgi.py                           # WSGI deployment entry point
templates/
  index.html                      # Web UI
static/
  therapist_image.jpg             # UI image asset
uk_therapy_knowledge_base.json    # Local wellbeing/support context
requirements.txt
runtime.txt
.env.example
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
python tbackend.py
```

On macOS/Linux:

```bash
source .venv/bin/activate
cp .env.example .env
python tbackend.py
```

Add your own API key to `.env` before using real model calls.

## Public Repository Notes

This cleaned repo excludes virtual environments, local logs, raw conversation logs, private `.env` files, and deployment secrets. In particular, the previous `therapy_log.txt` file is not included.

## Safety Disclaimer

This is a wellness chatbot prototype. It is not a therapist, doctor, medical device, diagnostic tool, crisis service, or substitute for professional care. It should not be used for emergencies, self-harm risk, crisis support, diagnosis, or treatment decisions. Users in immediate danger should contact local emergency services or a qualified crisis support service.
