import pandas as pd

def load_and_shuffle_data(file_path="data/Questions_Test.csv"):
    """Charge le fichier CSV, enlève les valeurs NaN et mélange les questions une seule fois."""
    df = pd.read_csv(file_path)
    df = df.dropna(subset=['Question'])  # Supprime les lignes avec des questions vides
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # Mélange les questions une seule fois
    return df