import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# load trained model
model = joblib.load("risk_model.pkl")

st.title("Healthcare Risk Stratification App")

st.write("Enter patient details to predict risk level")


if "prediction" not in st.session_state:
    st.session_state.prediction = None

tab1, tab2,tab3 = st.tabs(["Prediction", "Recommendation","Dashboard"])

# user inputs
#tab-1
with tab1:
    st.header("Enter Patient Details")

    age = st.number_input("Age", min_value=0, max_value=100)

    gender = st.selectbox("Gender", ["Male", "Female"])

    diagnosis = st.selectbox("Diagnosis", [
        "Diabetes","Asthma","Arthritis","COPD",
        "Cancer","Kidney Disease","Stroke","Hypertension"
    ])

    length_of_stay = st.number_input("Length of Stay", min_value=0, step=1, format="%d")
    treatment_cost = st.number_input("Treatment Cost", min_value=0, step=1, format="%d")

    # encode inputs
    gender_val = 1 if gender == "Male" else 0

    diagnosis_list = [
        "Diabetes","Asthma","Arthritis","COPD",
        "Cancer","Kidney Disease","Stroke","Hypertension"
    ]

    diagnosis_val = diagnosis_list.index(diagnosis)

    # prediction button
    if st.button("Predict Risk"):

        input_data = pd.DataFrame(
            [[age, gender_val, diagnosis_val, length_of_stay, treatment_cost]],
            columns=["Age","Gender","diagnosis name","Length of Stay","TreatmentCost"]
        )
        st.session_state.diagnosis = diagnosis
        st.session_state.gender = gender

        # prediction
        prediction = model.predict(input_data)

        # IMPORTANT: store everything for tab2
        st.session_state.prediction = prediction[0]
        st.session_state.age = age
        st.session_state.stay = length_of_stay
        st.session_state.cost = treatment_cost

        # show result
        st.success(f"Predicted Risk Level: {prediction[0]}")
    

#tab-2
with tab2:
    st.header("🩺 Medical Recommendation System")

    if st.session_state.prediction is not None:

        risk = st.session_state.prediction

        # 🔹 Top Section
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Patient Risk Summary")
            st.metric("Predicted Risk Level", risk)

        with col2:
            if "High" in risk:
                st.error("High")
            elif "Medium" in risk:
                st.warning("Moderate")
            else:
                st.success("Low")

        st.markdown("---")

        # 🔹 Middle Section
        colA, colB = st.columns(2)

        # LEFT → Actions
        with colA:
            st.subheader("Recommended Actions")

            if "High" in risk:
                st.write("• Immediate hospitalization")
                st.write("• Continuous monitoring required")
                st.write("• Emergency care support")
                st.write("• Advanced diagnostic testing")

            elif "Medium" in risk:
                st.write("• Regular health monitoring")
                st.write("• Follow medication schedule")
                st.write("• Periodic doctor consultation")
                st.write("• Lifestyle improvements")

            else:
                st.write("• Maintain healthy lifestyle")
                st.write("• Routine medical check-ups")
                st.write("• Preventive care measures")

        # RIGHT → Doctor Suggestion
        with colB:
            st.subheader("Recommended Specialist")

            if "High" in risk:
                st.info("Critical Care Specialist / ICU Team")
            elif "Medium" in risk:
                st.info("General Physician")
            else:
                st.info("Primary Care Doctor")

        st.markdown("---")

        # 🔥 Colored Risk Indicator
        st.subheader("Risk Indicator")

        if "High" in risk:
            percent = 100
            color = "#ff4b4b"
            label = "High Risk"

        elif "Medium" in risk:
            percent = 60
            color = "#ffa500"
            label = "Moderate Risk"

        else:
            percent = 30
            color = "#00c853"
            label = "Low Risk"

        st.markdown(f"""
        <div style="background-color:#e0e0e0;border-radius:10px;padding:5px">
            <div style="
                width:{percent}%;
                background-color:{color};
                padding:10px;
                border-radius:10px;
                text-align:center;
                color:white;
                font-weight:bold;">
                {label} ({percent}%)
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # 🔹 Footer
        st.caption(
            "This recommendation is generated using a machine learning model. "
            "Final medical decisions should be made by qualified healthcare professionals."
        )

    else:
        st.warning("Please complete prediction in the Prediction tab first.")

#tab-3
with tab3:
    st.header("🧾 Patient Dashboard")

    if "age" in st.session_state:

        age = st.session_state.get("age", 0)
        stay = st.session_state.get("stay", 0)
        cost = st.session_state.get("cost", 0)
        diagnosis = st.session_state.get("diagnosis", "Not Available")
        gender = st.session_state.get("gender", "Not Available")

        # 🔹 Card style with fixed size, heading top, value vertically centered
        card_style = """
        padding:12px;
        border-radius:12px;
        text-align:center;
        min-height:140px;
        max-height:140px;
        display:flex;
        flex-direction:column;
        justify-content:flex-start; /* Heading at top */
        align-items:center;
        color:white;
        """

        heading_style = "margin:0; font-size:16px;"

        value_style = """
        margin-top:auto;
        margin-bottom:auto;
        font-size:clamp(16px, 2vw, 24px); /* auto scales */
        word-wrap:break-word;
        overflow-wrap:break-word;
        """

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.markdown(f"""
            <div style="{card_style} background-color:#4e73df;">
                <h5 style="{heading_style}">Age</h5>
                <h3 style="{value_style}">{age}</h3>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="{card_style} background-color:#e74a3b;">
                <h5 style="{heading_style}">Gender</h5>
                <h3 style="{value_style}">{gender}</h3>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style="{card_style} background-color:#f6c23e;">
                <h5 style="{heading_style}">Diagnosis</h5>
                <h3 style="{value_style}">{diagnosis}</h3>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div style="{card_style} background-color:#1cc88a;">
                <h5 style="{heading_style}">Stay</h5>
                <h3 style="{value_style}">{stay} days</h3>
            </div>
            """, unsafe_allow_html=True)

        with col5:
            st.markdown(f"""
            <div style="{card_style} background-color:#36b9cc;">
                <h5 style="{heading_style}">Cost</h5>
                <h3 style="{value_style}">₹{cost:,}</h3>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # 🔹 Alerts
        st.subheader("Alerts & Conditions")
        if age > 60:
            st.warning("Patient belongs to high-risk age group.")
        if stay > 10:
            st.warning("Hospital stay is longer than average.")
        if cost > 50000:
            st.error("Cost is significantly high.")
        if age <= 60 and stay <= 10 and cost <= 20000:
            st.success("All parameters are within normal range.")

        st.markdown("---")

        # 🔹 Smart Summary
        st.subheader("Smart Summary")
        summary = []
        if age > 60:
            summary.append("higher age risk")
        if stay > 10:
            summary.append("extended hospital stay")
        if cost > 50000:
            summary.append("high cost")
        if diagnosis != "Not Available":
            summary.append(f"diagnosis of {diagnosis}")

        if summary:
            st.info(
                "Patient shows " + ", ".join(summary) +
                ". Clinical attention may be required."
            )
        else:
            st.success("Patient condition appears stable with normal parameters.")

        st.markdown("---")
        st.caption("This dashboard summarizes patient inputs used in the machine learning model.")

    else:
        st.info("Enter patient details in Prediction tab.")

#Create a launcher script
import subprocess
import os
import psutil

# Change working directory to the folder where your app is
os.chdir(r"C:\Users\krush\OneDrive\Documents\learning python\healthcare")

# Function to check if Streamlit is already running
def is_streamlit_running():
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            if proc.info['cmdline'] and 'streamlit' in ' '.join(proc.info['cmdline']):
                return True
        except:
            continue
    return False

# Launch Streamlit only if not running
if not is_streamlit_running():
    subprocess.Popen(["python", "-m", "streamlit", "run", "app.py"])
else:
    print("Streamlit app is already running!")
