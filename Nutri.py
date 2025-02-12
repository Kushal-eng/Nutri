import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load dataset
def load_data():
    csv_path = "CSV_VERSION.csv"  # Update with actual path
    df = pd.read_csv(csv_path, delimiter=";")
    for col in df.columns[2:]:
        df[col] = df[col].astype(str).str.replace(',', '.').astype(float, errors='ignore')
    return df

df = load_data()

# Streamlit App
st.title("Nutrient Deficiency Detection Dashboard")

# User Input: Daily Food Intake & Symptoms
st.sidebar.header("Log Your Food Intake")
food_input = st.sidebar.text_area("Enter food items you consumed today (comma-separated):")

st.sidebar.header("Report Symptoms")
symptoms_input = st.sidebar.text_area("Enter any symptoms (fatigue, hair loss, dizziness, etc.)")

# AI Deficiency Detection (Simplified Example)
def detect_deficiency(food_list):
    consumed_nutrients = df[df["Shrt_Desc"].str.contains('|'.join(food_list), case=False, na=False)]
    avg_nutrient_intake = consumed_nutrients.mean()
    deficiency_threshold = df.mean() * 0.5  # Example threshold for deficiency
    deficiencies = deficiency_threshold[avg_nutrient_intake < deficiency_threshold].index.tolist()
    return deficiencies

if food_input:
    food_list = [food.strip() for food in food_input.split(",")]
    deficiencies = detect_deficiency(food_list)
    if deficiencies:
        st.subheader("Potential Nutrient Deficiencies Detected:")
        st.write(deficiencies)
    else:
        st.success("No significant deficiencies detected!")

# Meal Plan Suggestion
st.subheader("Personalized Meal Plan Suggestions")
if deficiencies:
    for nutrient in deficiencies:
        suggested_foods = df.nlargest(5, nutrient)["Shrt_Desc"].tolist()
        st.write(f"For {nutrient}, consider eating: {', '.join(suggested_foods)}")

# Grocery List Generation
st.subheader("Smart Grocery List")
if deficiencies:
    grocery_list = []
    for nutrient in deficiencies:
        grocery_list.extend(df.nlargest(3, nutrient)["Shrt_Desc"].tolist())
    st.write(", ".join(set(grocery_list)))
    
# Visualization
st.subheader("Nutrient Intake Overview")
plt.figure(figsize=(8, 4))
plt.bar(df.columns[2:10], df.mean()[2:10])
plt.xticks(rotation=45)
st.pyplot(plt)
