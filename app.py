import streamlit as st
import requests
import json
from typing import Dict

# Groq API configuration
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = "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"  # Your provided key

class DevelopmentalPredictor:
    def __init__(self):
        # Expanded symptom categories
        self.symptom_categories = {
            "Social Interaction": [
                "Limited eye contact",
                "Difficulty with social reciprocity",
                "Lack of peer relationships",
                "Excessive social disinhibition",
                "Avoids social situations"
            ],
            "Communication": [
                "Delayed speech development",
                "Repetitive language",
                "Difficulty with conversation",
                "Speech articulation problems",
                "Lack of nonverbal communication",
                "Selective mutism (refusal to speak in certain situations)"
            ],
            "Behavior": [
                "Repetitive movements",
                "Intense focus on specific interests",
                "Resistance to change",
                "Impulsivity",
                "Aggressive outbursts",
                "Defiance of rules/authority",
                "Motor tics or vocal tics"
            ],
            "Emotional Regulation": [
                "Excessive anxiety or fear",
                "Persistent sadness",
                "Extreme mood swings",
                "Temper tantrums beyond age expectation",
                "Obsessive thoughts or compulsive behaviors",
                "Difficulty separating from caregivers"
            ],
            "Cognitive/Learning": [
                "Difficulty with reading/writing (dyslexia)",
                "Problems with math skills (dyscalculia)",
                "Poor memory or attention",
                "Delayed developmental milestones",
                "General intellectual impairment"
            ],
            "Motor Skills": [
                "Clumsiness or poor coordination",
                "Difficulty with fine motor tasks (e.g., writing)",
                "Sleepwalking or night terrors"
            ],
            "Sensory/Feeding": [
                "Sensory sensitivities (e.g., to noise, textures)",
                "Restricted food intake (picky eating beyond normal)",
                "Eating non-food items (pica)",
                "Regurgitation of food (rumination)"
            ],
            "Sleep": [
                "Difficulty falling/staying asleep",
                "Frequent nightmares",
                "Sleep terrors or sleepwalking"
            ]
        }
        
        self.criteria = [
            "Age of symptom onset (months)",
            "Family history of mental health or developmental disorders",
            "Exposure to trauma or significant stress",
            "Developmental milestone delays",
            "Severity of symptoms (1-10 scale)"
        ]

    def call_groq_api(self, prompt: str) -> str:
        # Correct API call to Groq
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama3-70b-8192",  # You can change to another Groq-supported model
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 300
        }
        
        try:
            response = requests.post(GROQ_API_URL, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # Parse the Groq API response format
            result = response.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content", "No prediction returned")
        
        except requests.exceptions.RequestException as e:
            return f"API Error: {str(e)}"

    def format_prompt(self, input_data: Dict) -> str:
        prompt = "Based on the following symptoms and criteria, predict the most likely early childhood developmental, emotional, or behavioral disorder:\n\n"
        prompt += "Symptoms:\n"
        for symptom in input_data["symptoms"]:
            prompt += f"- {symptom}\n"
        
        prompt += "\nCriteria:\n"
        for criterion, value in input_data["criteria"].items():
            prompt += f"- {criterion}: {value}\n"
            
        prompt += "\nPossible disorders to consider:\n"
        prompt += "- Neurodevelopmental: ASD, ADHD, Intellectual Disability, Communication Disorders (Speech Sound, Language, Social Pragmatic), Specific Learning Disorders (Dyslexia, Dyscalculia), DCD, Tic Disorders (Tourette's)\n"
        prompt += "- Emotional/Behavioral: Separation Anxiety, GAD, Selective Mutism, Social Anxiety, ODD, CD, DMDD, OCD\n"
        prompt += "- Mood: MDD, Persistent Depressive Disorder, Bipolar Disorder\n"
        prompt += "- Trauma/Stress: RAD, DSED, PTSD, Adjustment Disorders\n"
        prompt += "- Feeding/Eating: ARFID, Pica, Rumination Disorder\n"
        prompt += "- Sleep: Insomnia, Nightmare Disorder, Sleep Arousal Disorders\n"
        prompt += "- Other: Sensory Processing Disorder, Childhood-Onset Schizophrenia\n"
        prompt += "Provide a prediction with confidence level and brief explanation, including possible differential diagnoses."
        
        return prompt

def main():
    predictor = DevelopmentalPredictor()
    
    # Streamlit app layout
    st.title("Childhood Disorder Predictor")
    st.write("Select symptoms and criteria to predict potential developmental, emotional, or behavioral disorders.")
    
    # Symptom selection
    st.subheader("Symptoms")
    selected_symptoms = []
    
    for category, symptoms in predictor.symptom_categories.items():
        with st.expander(category, expanded=False):
            for symptom in symptoms:
                if st.checkbox(symptom, key=symptom):
                    selected_symptoms.append(symptom)
    
    # Additional criteria
    st.subheader("Additional Criteria")
    age_onset = st.number_input("Age of symptom onset (months)", min_value=0, max_value=120, value=0)
    family_history = st.checkbox("Family history of mental health or developmental disorders")
    trauma_exposure = st.checkbox("Exposure to trauma or significant stress")
    milestone_delays = st.checkbox("Developmental milestone delays")
    severity = st.slider("Severity of symptoms (1-10)", min_value=1, max_value=10, value=5)
    
    # Collect input data
    input_data = {
        "symptoms": selected_symptoms,
        "criteria": {
            "Age of symptom onset (months)": age_onset,
            "Family history of mental health or developmental disorders": family_history,
            "Exposure to trauma or significant stress": trauma_exposure,
            "Developmental milestone delays": milestone_delays,
            "Severity of symptoms (1-10 scale)": severity
        }
    }
    
    # Predict button
    if st.button("Predict Disorder"):
        if not input_data["symptoms"]:
            st.warning("Please select at least one symptom")
        else:
            try:
                prompt = predictor.format_prompt(input_data)
                prediction = predictor.call_groq_api(prompt)
                st.subheader("Prediction Result")
                st.text_area("Result", prediction, height=250)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    # Disclaimer
    st.markdown("---")
    st.write("*Note: This is a preliminary screening tool. Consult a healthcare professional for an official diagnosis.*")

if __name__ == "__main__":
    main()