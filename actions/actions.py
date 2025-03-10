import json
import cv2
from pyzbar.pyzbar import decode
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ScanQRCode(Action):
    """Scans QR code and detects language"""
    def name(self):
        return "action_scan_qr"

    def run(self, dispatcher, tracker, domain):
        cap = cv2.VideoCapture(0)
        qr_content = None
        lang = 'en'
        
        while True:
            ret, frame = cap.read()
            decoded = decode(frame)
            
            if decoded:
                qr_content = decoded[0].data.decode('utf-8')
                # Detect language from QR content (basic script detection)
                if any('\u0900' <= c <= '\u097F' for c in qr_content):  # Hindi
                    lang = 'hi'
                elif any('\u0B80' <= c <= '\u0BFF' for c in qr_content):  # Tamil
                    lang = 'ta'
                elif any('\u0C00' <= c <= '\u0C7F' for c in qr_content):  # Telugu
                    lang = 'te'
                break
                
            cv2.imshow('QR Scanner', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
        return [SlotSet("qr_content", qr_content), SlotSet("user_language", lang)]

class FetchHealthData(Action):
    """Fetches medical data based on user language"""
    def name(self):
        return "action_fetch_health_data"

    def run(self, dispatcher, tracker, domain):
        user_lang = tracker.get_slot("user_language")
        user_id = tracker.get_slot("qr_content")
        
        # Load mock medical data
        with open("data/medicine_data.json", encoding='utf-8') as f:
            data = json.load(f)
            
        user_data = data.get(user_lang, {}).get(user_id, {})
        
        if not user_data:
            dispatcher.utter_message(template=f"utter_not_found_{user_lang}")
            return []
            
        response = (
            f"📄 {user_data['report']}\n"
            f"💊 {user_data['medicines']}\n"
            f"📅 {user_data['appointment']}"
        )
        dispatcher.utter_message(text=response)
        return []
