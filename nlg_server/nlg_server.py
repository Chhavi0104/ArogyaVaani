import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Path to your language folder
LANGUAGE_FOLDER = r"C:\Users\HP\ArogyaVaani\languages"  # Update if your folder has a different name

# Load all language files
responses = {}
for file in os.listdir(LANGUAGE_FOLDER):
    if file.endswith(".json"):
        lang_code = file.replace(".json", "")  # Extract language code
        with open(os.path.join(LANGUAGE_FOLDER, file), "r", encoding="utf-8") as f:
            responses[lang_code] = json.load(f)

@app.route('/nlg', methods=['POST'])
def generate_response():
    """Handles requests from Rasa for NLG responses."""
    data = request.get_json()
    
    # Extract response_id and requested language
    response_id = data.get("response_id")
    lang = data.get("tracker", {}).get("slots", {}).get("language", "en")  # Default to English

    # Fetch response from the existing language file
    response_text = responses.get(lang, {}).get(response_id, {"text": f"No response found for {response_id}"})

    return jsonify(response_text)

if __name__ == '__main__':
    app.run(port=5055, debug=True)
