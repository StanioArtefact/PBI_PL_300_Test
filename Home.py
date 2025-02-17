import streamlit as st
import pandas as pd
from data_loader import load_and_shuffle_data

# Appliquer un style CSS global
st.markdown(
    """
    <style>
        .header-image {
            width: 200px;
            display: block;
            margin: 0 auto 20px auto;
        }
        .question-image {
            max-width: 100%;
            margin: 10px 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Afficher le logo en haut
st.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/New_Power_BI_Logo.svg/1200px-New_Power_BI_Logo.svg.png",
    width=200,
)

# Charger et mélanger les données au démarrage
if "df" not in st.session_state:
    st.session_state["df"] = load_and_shuffle_data()

df = st.session_state["df"]

# Initialisation des variables de session
if "score" not in st.session_state:
    st.session_state["score"] = 0
if "current_index" not in st.session_state:
    st.session_state["current_index"] = 0
if "answered" not in st.session_state:
    st.session_state["answered"] = False

# Vérifier si le quiz est terminé
if st.session_state["current_index"] >= min(len(df), 50):
    st.subheader("🎉 You have finished the quiz!")
    percentage_score = (st.session_state["score"] / 50) * 100
    st.write(f"**Your final score:** {st.session_state['score']} out of 50 ({percentage_score:.2f}%)")

    if percentage_score > 70:
        st.success("✅ Certification passed!")
    else:
        st.error("❌ Certification failed")
else:
    # Sélectionner la question actuelle
    question = df.iloc[st.session_state["current_index"]]
    
    st.subheader(f"Question {st.session_state['current_index'] + 1}:")
    st.write(question["Question"])

    # Afficher une image si une URL est fournie dans une colonne "Image"
    if "Image" in df.columns and pd.notna(question["Image"]):
        st.image(question["Image"], caption="Question illustration", use_container_width=True)

    # Mélanger et afficher les choix de réponse
    choices = [question["Choix 1"], question["Choix 2"], question["Choix 3"], question["Choix 4"]]
    selected_answer = st.radio("Select an answer:", choices, key="selected_answer")

    if st.button("Validate"):
        if not st.session_state["answered"]:
            correct_answer = question["Solution"]
            if selected_answer == correct_answer:
                st.success("✅ Correct answer!")
                st.session_state["score"] += 1
            else:
                st.error(f"❌ Incorrect answer! The correct answer was: **{correct_answer}**")

            # Affichage de l'explication
            st.info(f"ℹ️ **Explanation:** {question['Explication']}")
            st.session_state["answered"] = True

    # Affichage du score
    st.write(f"**Current Score:** {st.session_state['score']}")

    # Bouton pour la question suivante
    if st.session_state["answered"]:
        if st.button("Next question"):
            st.session_state["current_index"] += 1
            st.session_state["answered"] = False
            st.rerun()