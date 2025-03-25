import pandas as pd

def load_and_shuffle_data(file_path="data/Questions_Test.csv"):
    """Charge le fichier CSV, enlève les valeurs NaN, mélange et sélectionne 50 questions aléatoires."""
    df = pd.read_csv(file_path)
    df = df.dropna(subset=['Question'])  # Supprime les lignes avec des questions vides
    df = df.sample(n=50).reset_index(drop=True)  # Tire 50 questions aléatoires à chaque appel
    return df