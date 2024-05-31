import streamlit as st
import pandas as pd

# Load the Excel file
file_path = "REInvAnalysis.xlsx"
excel_data = pd.ExcelFile(file_path)

# Display the sheet names
st.sidebar.header("Select Sheet to Display")
sheet_name = st.sidebar.selectbox("Sheet Names", excel_data.sheet_names)

# Read the selected sheet into a dataframe
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Display the dataframe
st.title("Real Estate Investment Analysis")
st.write(f"Displaying sheet: {sheet_name}")
st.dataframe(df)

# Save as an interactive web app
