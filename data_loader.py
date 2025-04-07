import pandas as pd

def load_and_shuffle_data(file_path="data/Questions_Test.csv"):
    """Charge le fichier CSV, enlève les valeurs NaN, mélange et sélectionne 50 questions aléatoires."""
    df = pd.read_csv(file_path)
    df = df.dropna(subset=['Question'])  # Supprime les lignes avec des questions vides
    df = df.sample(n=50).reset_index(drop=True)  # Tire 50 questions aléatoires à chaque appel
    return df

def format_for_markdown(text):
    """
    Corrige les retours à la ligne littéraux dans un texte venant d'un CSV pour les rendre Markdown-friendly.
    """
    if not isinstance(text, str):
        return text

    # Cas où le texte contient '\\n' au lieu de vrais retours
    text = text.replace("\\n", "\n")  # interpréter le \n texte

    # Ensuite, convertir tous les vrais retours à la ligne en markdown-friendly
    return text.replace("\n", "  \n")