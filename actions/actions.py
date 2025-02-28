# Import necessary libraries
import pyqrcode  
import firebase_admin  
from firebase_admin import credentials, firestore  
import whisper  
from rasa_nlu.model import Interpreter  

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")  
firebase_admin.initialize_app(cred)  
db = firestore.client()  

# Load AI models (Chatbot & Speech-to-Text)
whisper_model = whisper.load_model("base")  
chatbot = Interpreter.load("models/current_rasa_model")  # Load Rasa chatbot model  

# Generate a QR Code for Patient's Health Records
def generate_qr(patient_id):  
    """
    Generates a QR Code that links to the patient's encrypted medical record.
    """
    qr_data = f"https://healthsync.com/patient/{patient_id}"  
    qr = pyqrcode.create(qr_data)  
    qr.png(f"{patient_id}_qr.png", scale=8)  
    return f"{patient_id}_qr.png"  

# Fetch Patient Medical Data from Firebase
def get_patient_data(patient_id):  
    """
    Retrieves the patient's health data securely from Firebase.
    """
    doc_ref = db.collection("patients").document(patient_id)  
    doc = doc_ref.get()  
    return doc.to_dict() if doc.exists else {"error": "Patient record not found"}  

# Process Patient Queries with Vernacular Chatbot
def process_chatbot_query(user_input):  
    """
    Takes user input (text) and generates a response in the user's language.
    """
    response = chatbot.parse(user_input)  
    return response["text"]  # Returns chatbot-generated response  

# Convert Speech-to-Text (For Voice-Based Queries)
def transcribe_audio(file_path):  
    """
    Converts an audio file (patient's voice) into text for chatbot processing.
    """
    result = whisper_model.transcribe(file_path)  
    return result["text"]  # Extract transcribed text  

# Complete Workflow - Process Patient Request
def handle_patient_interaction(patient_id, user_input=None, audio_file=None):  
    """
    Manages the complete interaction:
    - Fetch patient data
    - Process chatbot query (text or voice)
    - Return response in local language
    """
    patient_data = get_patient_data(patient_id)  

    if "error" in patient_data:  
        return patient_data["error"]  # Return error if patient not found  

    if audio_file:  
        user_input = transcribe_audio(audio_file)  # Convert speech to text  

    chatbot_response = process_chatbot_query(user_input)  
    return chatbot_response  # Return chatbot’s response  

# Example Usage:
# patient_id = "123456"
# print(handle_patient_interaction(patient_id, user_input="Show my last diagnosis"))
