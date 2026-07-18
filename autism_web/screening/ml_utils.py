import pickle
import os
import numpy as np
from django.conf import settings

MODEL_DIR = os.path.join(settings.BASE_DIR, 'ml_model')

# ✅ Load model first
model = pickle.load(open(os.path.join(MODEL_DIR, 'autism_model.pkl'), 'rb'))
scaler = pickle.load(open(os.path.join(MODEL_DIR, 'scaler.pkl'), 'rb'))
encoder = pickle.load(open(os.path.join(MODEL_DIR, 'encoder.pkl'), 'rb'))

# ✅ Now this works
print("MODEL EXPECTS FEATURES:", model.n_features_in_)

def predict_autism(features):
    # scale age (ONLY if age was scaled during training)
    features[0] = scaler.transform([[features[0]]])[0][0]

    features = np.array(features).reshape(1, -1)

    probability = model.predict_proba(features)[0][1]
    prediction = model.predict(features)[0]

    return prediction, probability
