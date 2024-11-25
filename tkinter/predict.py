import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import joblib

# Load the Keras models for feature extraction (24 models for image features)
feature_models = []
for i in range(24):
    try:
        model = load_model(f'../models/feature_model_{i}.keras')
        feature_models.append(model)
        print(f"Loaded model {i}")
    except:
        feature_models.append(None)

# Load the joblib model for price prediction
price_model = joblib.load('../models/random_forest_model.pkl')
# price_model = joblib.load('random_forest_model.joblib')

img_height, img_width = 180, 180

def preprocess_image(filepath):
    """Preprocess the image to match the input shape of the image models."""
    img = load_img(filepath, target_size=(img_height, img_width))
    img_array = img_to_array(img) / 255.0  # Normalize the image
    return img_array

def generate_feature_tags(image_path):
    """Generate feature tags (X) from the image using the feature extraction models."""
    feature_tags = []
    
    # Process the image input for the image models
    image_data = preprocess_image(image_path)
    
    # Get features from image models (24 Keras models)
    for i in range(24):  # Assuming the first 24 models work with images
        if not feature_models[i]:
            feature_tags.append(0)
            continue
        feature = feature_models[i].predict(image_data)
        # if feature.ndim > 1:
        #     feature = feature.flatten()
        feature_tags.append(feature)
    
    # Combine all the feature tags into a single vector (1D array)
    return feature_tags

def predict_price(image_path):
    """Predict the price from an image."""
    # Generate feature tags using the feature models
    feature_tags = generate_feature_tags(image_path)
    
    # Predict the price using the joblib model
    predicted_price = price_model.predict([feature_tags])

    return predicted_price
