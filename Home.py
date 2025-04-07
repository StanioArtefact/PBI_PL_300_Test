import streamlit as st
import pandas as pd
from data_loader import load_and_shuffle_data
from data_loader import format_for_markdown

# Appliquer un style CSS global
st.markdown(
    """
    <style>
        body {
            background-color: #FFEB3B !important;  /* Light yellow background with !important */
        }
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
if "df" not in st.session_state or "restart_quiz" in st.session_state:
    full_df = load_and_shuffle_data()
    # Mélanger et stocker dans la session
    st.session_state["df"] = full_df.sample(n=50).reset_index(drop=True)
    st.session_state["score"] = 0
    st.session_state["current_index"] = 0
    st.session_state["answered_questions"] = {}  # Stocke les réponses et explications
    if "restart_quiz" in st.session_state:
        del st.session_state["restart_quiz"]

df = st.session_state["df"]

# Vérifier si le quiz est terminé
if len(st.session_state["answered_questions"]) >= min(len(df), 50):
    st.subheader("🎉 You have finished the quiz!")
    percentage_score = (st.session_state["score"] / 50) * 100
    st.write(f"**Your final score:** {st.session_state['score']} out of 50 ({percentage_score:.2f}%)")

    if percentage_score > 70:
        st.success("✅ Certification passed!")
    else:
        st.error("❌ Certification failed!")

    if st.button("🔄 Restart the quiz"):
        st.session_state["restart_quiz"] = True
        st.rerun()
else:
    # Menu déroulant pour accéder à une question spécifique
    selected_question = st.selectbox(
        "Go to question:",
        options=[f"Question {i+1} ✅" if i in st.session_state["answered_questions"] else f"Question {i+1}" for i in range(min(len(df), 50))],
        index=st.session_state["current_index"],
    )

    # Mettre à jour l'index si l'utilisateur change de question
    selected_index = int(selected_question.split(" ")[1]) - 1
    if selected_index != st.session_state["current_index"]:
        st.session_state["current_index"] = selected_index
        st.rerun()

    # Sélectionner la question actuelle
    question = df.iloc[st.session_state["current_index"]]
    
    st.subheader(f"Question {st.session_state['current_index'] + 1}:")

    # Gérer les sauts de ligne Markdown-friendly dans la Question
    st.markdown(format_for_markdown(question["Question"]))

    # Afficher une image si disponible
    if "Image" in df.columns and pd.notna(question["Image"]):
        st.image(question["Image"], caption="Question illustration", use_container_width=True)

    # Récupérer la réponse enregistrée s'il y en a une
    answered_data = st.session_state["answered_questions"].get(st.session_state["current_index"], {})
    answered = answered_data.get("answer")
    
    # Sélectionner les choix de réponses (2 ou 4 selon la question)
    if pd.notna(question["Choix 3"]) and pd.notna(question["Choix 4"]):
        choices = [question["Choix 1"], question["Choix 2"], question["Choix 3"], question["Choix 4"]]
    else:
        choices = [question["Choix 1"], question["Choix 2"]]

    # Afficher les choix de réponse avec radio désactivé si déjà répondu
    selected_answer = st.radio(
        "Select an answer:", choices, index=choices.index(answered) if answered else None, disabled=bool(answered)
    )

    if st.button("Validate") and not answered:
        correct_answer = question["Solution"]
        is_correct = selected_answer == correct_answer
        st.session_state["answered_questions"][st.session_state["current_index"]] = {
            "answer": selected_answer,
            "correct": is_correct,
            "explanation": format_for_markdown(question['Explication'])
        }
        if is_correct:
            st.success("✅ Correct answer!")
            st.session_state["score"] += 1
        else:
            st.error(f"❌ Incorrect answer! The correct answer was: **{correct_answer}**")

        st.markdown(f"""
        <div style="background-color:#e1f5fe;padding:10px;border-radius:6px">
        <b>ℹ️ Explanation:</b><br>{format_for_markdown(question['Explication'])}
        </div>
        """, unsafe_allow_html=True)
        st.rerun()

    # Affichage de l'explication si déjà répondu
    if answered:
        if answered_data["correct"]:
            st.success("✅ Correct answer!")
        else:
            st.error(f"❌ Incorrect answer! The correct answer was: **{question['Solution']}**")

        st.markdown(f"""
        <div style="background-color:#e1f5fe;padding:10px;border-radius:6px">
        <b>ℹ️ Explanation:</b><br>{format_for_markdown(question['Explication'])}
        </div>
        """, unsafe_allow_html=True)

    # Affichage du score
    st.write(f"**Current Score:** {st.session_state['score']}")

    # Boutons de navigation
    col1, col2 = st.columns(2)

    with col1:
        if st.session_state["current_index"] > 0:
            if st.button("⬅️ Previous question"):
                st.session_state["current_index"] -= 1
                st.rerun()

    with col2:
        if st.session_state["current_index"] < min(len(df), 50) - 1:
            if st.button("Next question ➡️"):
                st.session_state["current_index"] += 1
                st.rerun()