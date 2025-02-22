import streamlit as st
import pandas as pd
import openai

# Set OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your actual API key

st.title("📊 AI Data Analysis & Insights Bot")
st.write("Welcome! Upload a file or answer a few questions, and I'll generate a personalized report for you.")

# User choice: File Upload, Questionnaire, or Both
choice = st.radio("How would you like to proceed?", ["Upload a File", "Answer Questions", "Both"])

def analyze_file(file):
    try:
        df = pd.read_csv(file)  # Assuming CSV for simplicity
        data_preview = df.head().to_string()
        prompt = f"Analyze the following dataset and provide insights:
{data_preview}"
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a data analyst."},
                      {"role": "user", "content": prompt}],
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error processing file: {e}"

def analyze_answers(answers):
    prompt = f"Based on these answers, provide personalized insights:
{answers}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a business and data insights expert."},
                  {"role": "user", "content": prompt}],
    )
    return response["choices"][0]["message"]["content"]

# Handling file upload
if choice in ["Upload a File", "Both"]:
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        st.write("✅ File uploaded successfully!")
        st.subheader("Analysis Results:")
        st.write(analyze_file(uploaded_file))

# Handling questionnaire
if choice in ["Answer Questions", "Both"]:
    st.subheader("📋 Quick Questionnaire")
    q1 = st.text_input("What is your main goal with this analysis?")
    q2 = st.text_input("What industry are you in?")
    q3 = st.text_input("What specific insights are you looking for?")

    if st.button("Get Insights"):
        user_answers = f"Goal: {q1}
Industry: {q2}
Insights Needed: {q3}"
        st.subheader("📊 Personalized Insights:")
        st.write(analyze_answers(user_answers))
