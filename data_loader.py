import pandas as pd

def load_and_shuffle_data(file_path="data/Questions_Test.csv"):
    """Charge le fichier CSV, enlève les valeurs NaN, mélange et sélectionne 50 questions aléatoires."""
    df = pd.read_csv(file_path)
    df = df.dropna(subset=['Question'])  # Supprime les lignes avec des questions vides
    df = df.sample(n=50).reset_index(drop=True)  # Tire 50 questions aléatoires à chaque appel
    return df

def format_for_markdown(text):
    """
    Convertit un texte avec des '\\n' ou '\n' en texte Markdown-friendly avec des sauts de ligne visibles.
    Utilisable avec st.markdown().
    """
    if not isinstance(text, str):
        return text

    # Normaliser les deux cas : vrais \n ou littéraux \\n
    text = text.replace("\\n", "\n")

    # Convertir tous les sauts de ligne en version Markdown-friendly
    return text.replace("\n", "  \n")