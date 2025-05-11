import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# Step 1: Load Dataset
df = pd.read_csv(
    r"C:\Web\Sentiment_Analysis\my-app\twitter_training.csv",
    encoding="ISO-8859-1",
    header=1,  # skip the first header row that exists in the CSV
    quotechar='"',
    usecols=[0, 1, 2, 3],
    names=["tweet_id", "entity", "sentiment", "content"]
)

# Step 2: Clean Data
df = df.dropna(subset=["sentiment", "content"])
df["sentiment"] = df["sentiment"].str.strip().str.capitalize()
df = df[df["sentiment"].isin(["Positive", "Negative", "Neutral"])]

# Step 3: Split Data into Training and Test Sets
X = df["content"]
y = df["sentiment"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Step 4: Create Machine Learning Pipeline
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english", max_features=5000)),
    ("clf", LogisticRegression(max_iter=1000, solver="lbfgs", multi_class="multinomial"))
])

# Step 5: Train the Model
pipeline.fit(X_train, y_train)

# Step 6: Evaluate the Model
y_pred = pipeline.predict(X_test)
print("Classification Report:\n")
print(classification_report(y_test, y_pred))

# Step 7: Save the Trained Model
joblib.dump(pipeline, "twitter_sentiment_model.pkl")

# Step 8: Prediction Helper Function
def predict_sentiment(text):
    return pipeline.predict([text])[0]

# Example Usage
print("Sample prediction:")
print(predict_sentiment("I'm so happy with the latest update!"))
