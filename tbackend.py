import openai
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import json
import os
from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from datetime import timedelta

# Flask app setup
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "your_secret_key")
app.permanent_session_lifetime = timedelta(minutes=30)

# OpenAI API key check
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable not set.")
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Load knowledge base
with open("uk_therapy_knowledge_base.json", "r") as f:
    knowledge_base = json.load(f)

# Prepare embeddings
texts = [
    f"{entry['situation']} {entry['analysis']} {', '.join(entry.get('resources', []))}"
    for entry in knowledge_base
]
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(texts)
faiss_index = faiss.IndexFlatL2(embeddings.shape[1])
faiss_index.add(np.array(embeddings, dtype=np.float32))

# Retrieve relevant knowledge base entries
def retrieve_relevant_docs(query, k=3):
    query_embedding = model.encode([query])
    D, I = faiss_index.search(np.array(query_embedding, dtype=np.float32), k)
    return [knowledge_base[i] for i in I[0]]

# Generate a therapeutic response
def generate_response(scenario, context, conversation_history):
    full_history = "\n".join([f"User: {turn['user']}\nTherapist: {turn['therapist']}" for turn in conversation_history])

    prompt = f"""
    You are an AI therapist with advanced training in psychology. You offer empathetic, evidence-based guidance using proven therapeutic techniques (e.g., CBT, ACT, DBT, attachment theory, etc.). Your tone is human, emotionally attuned, conversational, and kind—like a thoughtful therapist in a real session. do not say what it sounds like, do not use the phrase "it sounds like".

🧠 Behavior Rules:
If it's the first message or vague:

Respond with warmth and gentle curiosity. do not say what it sounds like, address the issues based on the information given however, do not say what it sounds like.

Ask open-ended questions that encourage emotional exploration or self-reflection (e.g., “What’s been on your mind lately?” or “How have you been feeling about that?”).

Avoid assumptions. Guide the person to talk more about what they’re going through.

If the user shares something emotional or situational:

Validate their experience. Be present and understanding.

Offer meaningful insight or feedback only if appropriate.

Suggest practical, evidence-based strategies—but only after listening well.

If they’re seeking relationship or personal advice:

Give clear, actionable techniques from proven psychology practices.

For example, if someone says “my partner ignores me,” and they've tried kindness and vulnerability, you might suggest:

“It might help to create a bit of space—sometimes stepping back shows strength and self-respect, which can shift the dynamic.”

If they ask about you:

You can say: “I'm doing well, thank you—but I'm here for you. You don't have to worry about me.”

🗣️ Style Guidelines:
Keep messages very brief.

Make it feel like a conversation, not a lecture.

Ask one thoughtful follow-up question unless you’re clearly offering advice.

Always return focus to the user’s emotions, values, or experience.

Be professional, gentle, and human.


    

    {full_history}
    User: {scenario}
    Therapist:
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message['content'].strip()

# Analyze and respond to user scenario
@app.route("/analyze", methods=["POST"])
def analyze():
    session.permanent = True
    data = request.get_json()
    scenario = data.get("scenario")

    if not scenario:
        return jsonify({"error": "No scenario provided"}), 400

    # Retrieve or initialize conversation history
    if "conversation" not in session:
        session["conversation"] = []

    # Retrieve relevant docs for context (optional but not shown to user)
    relevant_docs = retrieve_relevant_docs(scenario)
    context = "\n".join([
        f"Situation: {doc['situation']}\nAnalysis: {doc['analysis']}\nPotential Errors: {', '.join(doc.get('potential_errors', []))}\nImprovement Strategies: {', '.join(doc.get('improvement_strategies', []))}\nResources: {', '.join(doc.get('resources', []))}"
        for doc in relevant_docs
    ])

    # Generate therapeutic response
    conversation_history = session["conversation"]
    response_text = generate_response(scenario, context, conversation_history)

    # Update session memory
    session["conversation"].append({
        "user": scenario,
        "therapist": response_text
    })
    session.modified = True

    # Log to file
    with open("therapy_log.txt", "a") as f:
        f.write(f"\nScenario: {scenario}\nResult: {response_text}\n{'-'*50}\n")

    return jsonify({"result": response_text})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
