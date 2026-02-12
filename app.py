import streamlit as st
import pandas as pd
import google.generativeai as genai
import io

# Setup: Pulling Gemini API Key from Streamlit Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Ops & Automation Toolbox", layout="wide", page_icon="🛠️")

st.title("🛠️ Automation Operations Toolbox")
st.write("Supporting MakesYouLocal's mission through AI-driven operational clarity.")

tab1, tab2 = st.tabs(["📝 Friction-to-SOP", "📊 Ticket Insight Triage"])

# --- TAB 1: SOP GENERATOR ---
with tab1:
    st.header("Friction-to-SOP Generator")
    st.info("Turn messy process descriptions into structured documentation.")
    
    messy_input = st.text_area("Describe the process (as a brain dump):", 
                               placeholder="e.g., First I open Dixa, look for the customer's email, then check the order ID in Shopify...",
                               height=200)

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
                # Converting the dataframe to a string for the AI to read
                ticket_data = df.to_string(index=False)
                prompt = (
                    f"Analyze these customer support tickets from an e-commerce agency context. "
                    f"1. Identify the top 3 recurring themes. "
                    f"2. Suggest one specific automation for each theme (e.g., using Make.com or Dixa) to reduce manual work. "
                    f"Be practical and focus on stability. Data: {ticket_data}"
                )
                
                response = model.generate_content(prompt)
                st.subheader("🤖 AI Insights & Recommendations")
                st.write(response.text)
