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
        lang = 'en'  # Default language
        
        while True:
            ret, frame = cap.read()
            decoded_objects = decode(frame)
            
            if decoded_objects:
                qr_content = decoded_objects[0].data.decode('utf-8')
                
                # Detect language from QR content using Unicode ranges
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
    """Fetches and localizes medical data"""
    def name(self):
        return "action_fetch_health_data"

    def run(self, dispatcher, tracker, domain):
        user_lang = tracker.get_slot("user_language")
        user_id = tracker.get_slot("qr_content")
        
        # 1. Load language file
        try:
            with open(f"languages/{user_lang}.json", "r", encoding="utf-8") as f:
                lang = json.load(f)
        except FileNotFoundError:
            dispatcher.utter_message(text="Language support not available")
            return []
        
        # 2. Load medical data
        try:
            with open("data/medicine_data.json", "r", encoding="utf-8") as f:
                med_data = json.load(f)
        except FileNotFoundError:
            dispatcher.utter_message(text=lang["not_found"])
            return []
        
        # 3. Get user-specific data
        user_data = med_data.get(user_lang, {}).get(user_id)
        
        if not user_data:
            dispatcher.utter_message(text=lang["not_found"])
            return []
        
        # 4. Build localized response
        response = (
            f"📄 {lang['report']} {user_data['report']}\n"
            f"💊 {lang['medicines']} {user_data['medicines']}\n"
            f"📅 {lang['appointment']} {user_data['appointment']}"
        )
        
        dispatcher.utter_message(text=response)
        return []
