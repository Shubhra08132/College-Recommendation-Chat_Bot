import streamlit as st
import pandas as pd

# Load dataset
df_clean = pd.read_csv("Dataset/cleaned_college_data.csv")

st.title("📊 College Recommendation Dashboard")

# Example cards
st.metric("Total Colleges", len(df_clean))
st.metric("Average UG Fee", f"₹{int(df_clean['UG_fee'].mean()):,}")
st.metric("Top Placement %", f"{int(df_clean['Placement'].max() * 10)}%")

# Stream distribution
st.subheader("Stream Distribution")
st.bar_chart(df_clean['Stream'].value_counts())

# Placements by state
st.subheader("Placement by State")
state_placement = df_clean.groupby("State")["Placement"].mean() * 10
st.bar_chart(state_placement)
