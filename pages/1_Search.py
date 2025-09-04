import streamlit as st
import pandas as pd

# Load dataset
df_clean = pd.read_csv("Dataset/cleaned_college_data.csv")

st.title("🔎 College Search")

# Input fields
state = st.text_input("Enter State")
course = st.text_input("Enter Course/Stream")
max_fee = st.number_input("Max Fee (₹)", min_value=0, step=10000)
min_placement = st.number_input("Min Placement %", min_value=0, max_value=100, step=5)
top_n = st.number_input("Top N Results", min_value=1, value=10)

# Filter
df_filtered = df_clean.copy()

if state:
    df_filtered = df_filtered[df_filtered['State'].str.lower() == state.lower()]

if course:
    df_filtered = df_filtered[df_filtered['Stream'].str.lower().str.contains(course.lower(), na=False)]

if max_fee > 0:
    df_filtered = df_filtered[df_filtered['UG_fee'] <= max_fee]

if min_placement > 0:
    df_filtered = df_filtered[df_filtered['Placement'] * 10 >= min_placement]

# Show results
result = df_filtered[['College_Name', 'State', 'UG_fee', 'Placement', 'Rating', 'Stream']]\
             .sort_values(by='Placement', ascending=False).head(top_n)

st.subheader("Results")
st.dataframe(result)

# Download button
if not result.empty:
    csv = result.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download results", csv, "colleges.csv", "text/csv")
