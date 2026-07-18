import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

# ... (rest of imports)

# ... (data loading and training)

# ... (rest of imports)

# Defines paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(os.path.dirname(BASE_DIR), 'autism_web', 'ml_model')

# Ensure model directory exists
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

print(f"Loading data from {BASE_DIR}/train.csv...")
df = pd.read_csv(os.path.join(BASE_DIR, "train.csv"))

# Features used in the notebook
features = [
    'age', 'jaundice', 'austim',
    'A1_Score','A2_Score','A3_Score','A4_Score','A5_Score',
    'A6_Score','A7_Score','A8_Score','A9_Score','A10_Score'
]

X = df[features]
y = df['Class/ASD']

# Encoding categorical variables
binary_cols = ['jaundice','austim']
encoder = LabelEncoder()

# Note: In real production, we should fit this on the full set or handle unseen labels.
# For this dataset, we fit on the training data.
for col in binary_cols:
    X[col] = encoder.fit_transform(X[col])

# Saving Encoder (We need to save it to handle 'jaundice' input in the web app)
# However, the web app usually receives these as 0/1 from the form directly or we map them manually.
# Let's save it just in case.
pickle.dump(encoder, open(os.path.join(MODEL_DIR, "encoder.pkl"), "wb"))


# Scaling Age
scaler = StandardScaler()
X[['age']] = scaler.fit_transform(X[['age']])
pickle.dump(scaler, open(os.path.join(MODEL_DIR, "scaler.pkl"), "wb"))


# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model Training
print("Training Logistic Regression Model...")
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Saving Model
pickle.dump(model, open(os.path.join(MODEL_DIR, "autism_model.pkl"), "wb"))
print(f"Model saved to {MODEL_DIR}")
