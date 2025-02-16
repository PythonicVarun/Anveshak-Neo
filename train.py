import pickle

import pandas as pd
import neattext.functions as nfx

from lightgbm import LGBMClassifier

from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK datasets
nltk.download('wordnet')
nltk.download('stopwords')

# Initialize text processing tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    """
    Cleans and preprocesses the input text by:
    - Converting to lowercase
    - Removing URLs
    - Removing punctuation and numbers
    - Lemmatizing words and removing stopwords
    """
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'http\\S+|www\\S+', '', text)  # Remove URLs
    text = re.sub(r'[^a-zA-Z]', ' ', text)  # Remove punctuation and numbers
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words])  # Lemmatization
    return text

# Load Dataset
def load_dataset(filepath):
    """Loads the dataset from a CSV file."""
    df = pd.read_csv(filepath)
    return df

# Preprocess Text Data
def preprocess_text(df):
    """Cleans the text data by removing user handles and applying text cleaning functions."""
    df['Clean_Text'] = df['Text'].apply(nfx.remove_userhandles)
    df['Clean_Text'] = df['Clean_Text'].apply(clean_text)
    return df

# Split Data
def split_data(df):
    """Splits the dataset into training and testing sets."""
    x = df['Clean_Text']
    y = df['Emotion']
    return train_test_split(x, y, test_size=0.3, random_state=42)

# Train and Evaluate Model
def train_and_evaluate_model(x_train, x_test, y_train, y_test):
    """
    Trains multiple machine learning models and evaluates their accuracy.
    Returns trained models and their respective scores.
    """
    models = {
        'Logistic Regression': Pipeline([('tfidf', TfidfVectorizer()), ('lr', LogisticRegression(max_iter=10000, solver='saga'))]),
        'SVM': Pipeline([('tfidf', TfidfVectorizer()), ('svc', SVC(kernel='rbf', C=10, probability=True))]),
        'Random Forest': Pipeline([('tfidf', TfidfVectorizer()), ('rf', RandomForestClassifier(n_estimators=10))]),
        'Naive Bayes': Pipeline([('tfidf', TfidfVectorizer()), ('nb', MultinomialNB())]),
        'LightGBM': Pipeline([('tfidf', TfidfVectorizer(ngram_range=(1, 2))), ('lgbm', LGBMClassifier())])
    }

    scores = {}
    for model_name, pipeline in models.items():
        pipeline.fit(x_train, y_train)
        score = pipeline.score(x_test, y_test)
        scores[model_name] = score
        print(f"{model_name} Accuracy: {score:.2f}")

    return models, scores

# Save Model
def save_model(model, filename):
    """Saves the trained model to a file using pickle."""
    with open(filename, 'wb') as file:
        pickle.dump(model, file)

# Main Execution
if __name__ == '__main__':
    df = load_dataset('models/dataset/emotion_dataset_raw.csv')
    df = preprocess_text(df)
    x_train, x_test, y_train, y_test = split_data(df)
    models, scores = train_and_evaluate_model(x_train, x_test, y_train, y_test)

    # Save the best model (based on accuracy)
    best_model_name = max(scores, key=scores.get)
    best_model = models[best_model_name]
    print(f"Best Model: {best_model_name} with Accuracy: {scores[best_model_name]:.2f}")

    save_model(best_model, 'models/text_emotion.pkl')
    print("Model saved successfully as 'text_emotion.pkl'")
