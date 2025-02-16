from collections import defaultdict
import pickle

# Load pre-trained text emotion classification model using pickle
model = pickle.load(open("models/text_emotion.pkl", "rb"))

# Extract emotion labels from the final step of the model pipeline
EMOTIONS = model.named_steps[list(model.named_steps.keys())[-1]].classes_

def get_prediction_proba(msg):
    """
    Predict the probability distribution over emotion classes for a given message.

    Args:
        msg (str): The input message (text) to classify.

    Returns:
        dict: A dictionary with emotion labels as keys and corresponding prediction probabilities (in percentage) as values.
    """
    final_prob = defaultdict(float)
    
    # Get prediction probabilities from the model for the input message
    for prob in model.predict_proba([msg]):
        for idx, p in enumerate(prob):
            final_prob[EMOTIONS[idx]] += p

    # Convert probabilities to percentages
    for k, v in final_prob.items():
        final_prob[k] = v * 100

    return final_prob
