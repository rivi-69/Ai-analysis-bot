import pandas as pd
import openai
import streamlit as st

# Set OpenAI API key (Replace with your actual key)
openai.api_key = "your-api-key"

# Function to analyze uploaded data
def analyze_data(df, question):
    data_str = df.to_string()
    prompt = f"Given the following dataset:\n{data_str}\n\nAnswer this question: {question}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a professional data analyst."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Function to analyze answers without file upload
def analyze_answers(answers):
    prompt = f"A client has provided these answers: {answers}. Generate an insightful business report based on these responses."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a business consultant providing insights based on client responses."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Streamlit UI
st.title("Welcome to Your AI Business Assistant!")
st.write("I can help you generate reports based on your data or answers. Choose an option below!")

option = st.radio("How would you like to proceed?", ("Upload a CSV file", "Answer Questions"))

if option == "Upload a CSV file":
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.subheader("Dataset Preview")
        st.dataframe(df.head())

        question = st.text_input("Ask a question about your data")
        if st.button("Get AI Insights") and question:
            insights = analyze_data(df, question)
            st.subheader("AI Insights & Recommendations")
            st.text(insights)

elif option == "Answer Questions":
    st.subheader("Answer a few questions to get a personalized report")
    industry = st.text_input("What industry is your business in?")
    goal = st.text_input("What is your main business goal?")
    challenge = st.text_input("What is your biggest challenge right now?")

    if st.button("Generate Report"):
        answers = f"Industry: {industry}, Goal: {goal}, Challenge: {challenge}"
        insights = analyze_answers(answers)
        st.subheader("Your AI-Generated Business Report")
        st.text(insights)
