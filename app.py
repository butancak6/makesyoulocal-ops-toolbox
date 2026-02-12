import streamlit as st
import pandas as pd
import google.generativeai as genai
import io

# Setup: Configuration and Model Initialization
st.set_page_config(page_title="Ops & Automation Toolbox", layout="wide", page_icon="🛠️")

# Pulling Secrets from Streamlit
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# Using the specific 'models/' prefix for stability
model = genai.GenerativeModel('models/gemini-flash-latest')

# --- SIDEBAR ACCESS CONTROL ---
st.sidebar.title("🔐 Access Control")
access_password = st.sidebar.text_input("Enter Access Key:", type="password")
st.sidebar.info("Note: This key protects the API from unauthorized use.")

st.title("🛠️ Automation Operations Toolbox")
st.write("Supporting MakesYouLocal's mission through AI-driven operational clarity.")

# Check if the user entered the correct password from secrets
if access_password == st.secrets["APP_PASSWORD"]:

    tab1, tab2 = st.tabs(["📝 Friction-to-SOP", "📊 Ticket Insight Triage"])

    # --- TAB 1: SOP GENERATOR ---
    with tab1:
        st.header("Friction-to-SOP Generator")
        st.info("Turn messy process descriptions into structured documentation.")
        
        messy_input = st.text_area("Describe the process (as a brain dump):", 
                                   placeholder="e.g., First I open Dixa, look for the customer's email, then check the order ID in Shopify...",
                                   height=200,
                                   max_chars=3000)

        if st.button("Generate SOP"):
            if messy_input:
                with st.spinner("Gemini is structuring your documentation..."):
                    prompt = (
                        f"Convert the following messy process description into a professional Standard Operating Procedure (SOP). "
                        f"Use these Markdown headings: Objective, Prerequisites, Step-by-Step Instructions, and Common Troubleshooting. "
                        f"Keep it concise and clear for a new hire. Process: {messy_input}"
                    )
                    response = model.generate_content(prompt)
                    st.markdown("---")
                    st.markdown(response.text)
            else:
                st.warning("Please enter a process description.")

    # --- TAB 2: TICKET TRIAGE ---
    with tab2:
        st.header("Ticket-to-Insight Triage")
        st.info("Upload a CSV of support tickets to identify automation opportunities.")
        
        uploaded_file = st.file_uploader("Upload Ticket Export (CSV)", type="csv")
        
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.write("Preview of data:", df.head())
            
            if st.button("Analyze for Automation"):
                with st.spinner("Gemini is identifying recurring manual work..."):
                    # Limit data sent to AI to stay within free tier limits
                    ticket_data = df.to_string(index=False)[:5000]
                    prompt = (
                        f"Analyze these customer support tickets from an e-commerce agency context. "
                        f"1. Identify the top 3 recurring themes. "
                        f"2. Suggest one specific automation for each theme (e.g., using Make.com or Dixa) to reduce manual work. "
                        f"Be practical and focus on stability. Data: {ticket_data}"
                    )
                    response = model.generate_content(prompt)
                    st.subheader("🤖 AI Insights & Recommendations")
                    st.write(response.text)

else:
    # Message shown when the password hasn't been entered yet
    if access_password == "":
        st.warning("Please enter the Access Key in the sidebar to unlock the AI features.")
    else:
        st.error("Incorrect Access Key. Please check your credentials.")
