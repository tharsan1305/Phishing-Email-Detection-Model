import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import pickle
import os

# Ensure the dataset exists
dataset_path = os.path.join("dataset", "emails.csv")
if not os.path.exists(dataset_path):
    raise FileNotFoundError(f"Dataset not found at {dataset_path}. Please create it first.")

# Load dataset
print("Loading dataset...")
df = pd.read_csv(dataset_path)

# Features and labels
X = df["text"]
y = df["label"]

# Convert text to numbers
print("Vectorizing email text using TF-IDF...")
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Split data
print("Splitting dataset into train/test sets...")
X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

# Train model
print("Training Multinomial Naive Bayes model...")
model = MultinomialNB()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Training Complete!")
print(f"Accuracy on test set: {accuracy:.4f} ({accuracy * 100:.2f}%)")

# Save model + vectorizer
print("Saving model.pkl and vectorizer.pkl...")
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))
print("Files saved successfully!")
