## **ArogyaVaani**
 ArogyaVaani is an AI-powered healthcare assistant designed to provide **low-cost diagnostics** and **vernacular chatbot support** for rural healthcare settings. This repository contains the **code structure** for the application, including both the **Python-based backend** and the **Rasa-powered multilingual chatbot**.  

## **Overview**  
Healthcare accessibility in rural areas is often limited by **language barriers, lack of medical professionals, and inadequate infrastructure**. ArogyaVaani aims to bridge this gap by:  
- Enabling **symptom triage and medical guidance** in multiple **Indian regional languages**  
- Providing **QR-based health records management**  
- Supporting **both text and voice interactions** for ease of use  
- Ensuring **secure medical data handling** for rural environments  

## **Key Features**  
- **Multilingual AI Chatbot** – Supports multiple Indian languages using **Rasa NLU**  
- **Symptom Triage & Guidance** – Provides preliminary medical advice based on symptoms  
- **Voice & Text Support** – Uses **Whisper AI** for speech-to-text conversion  
- **QR-Based Health Records** – Securely stores and retrieves patient records using QR codes  
- **Low Infrastructure Requirement** – Works on basic hardware and minimal internet connectivity  
- **Scalable & Extendable** – Can integrate with **telemedicine platforms** and **government health initiatives**  

## **Impact**  
- **Bridges the healthcare gap** for rural populations with AI-driven support  
- **Empowers non-tech-savvy users** through vernacular support and voice interactions  
- **Reduces hospital overload** by providing preliminary medical advice remotely  
- **Enhances patient data management** via secure QR-based health records  

## **Technology Stack**  
- **Python** – Core application logic and backend processing  
- **Rasa NLU** – AI-powered chatbot for multilingual symptom triage  
- **Whisper AI** – Speech-to-text for vernacular voice interactions  
- **FastAPI/Flask** – API for chatbot and health record management  
- **MongoDB** – Database for patient records and chatbot conversations  
- **QR Code Generation** – For secure access to medical records  

## **Repository Structure**  
```bash
ArogyaVaani/
├── data/
│   ├── nlu.yml               # Training data for chatbot understanding
│   ├── stories.yml           # Conversation flow examples
│   ├── rules.yml             # Rule-based chatbot responses
├── actions/
│   ├── actions.py            # Custom chatbot actions (e.g., fetching health data)
├── models/                   # Stores trained Rasa models (empty initially)
├── domain.yml                # Defines chatbot responses, intents, and entities
├── config.yml                # Configuration for chatbot training
├── credentials.yml           # API keys and authentication settings
├── endpoints.yml             # API endpoints for chatbot integration
├── README.md                 # Project documentation
```

## **Getting Started**  
### **1. Clone the Repository**  
```bash
git clone https://github.com/yourusername/ArogyaVaani.git
cd ArogyaVaani
```

### **2. Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **3. Run the Application**  
- Start the backend API:  
  ```bash
  python backend/app.py
  ```
- Start the chatbot:  
  ```bash
  rasa run --enable-api
  ```

## **Future Enhancements**  
- **Integration with Government Health Databases**  
- **AI-based Disease Prediction** for early diagnosis  
- **WhatsApp & SMS Chatbot Support** for wider accessibility  
- **Mobile App Version** for improved user experience  
