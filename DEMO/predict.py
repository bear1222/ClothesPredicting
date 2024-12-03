import numpy as np
import pandas as pd
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from joblib import load
import pickle

model_dir = "../models"
img_height, img_width = 180, 180

try:
    feature_list = list(pd.read_csv("feature_list.csv")["name"])
    feature_model = [None] * len(feature_list)
except Exception as e:
    print("please add feature_list.csv to the DEMO folder")

feature_model = [None] * len(feature_list)

for i in range(len(feature_list)):
    try:
        feature_model[i] = load_model(os.path.join(model_dir, f"model_feature_{i}_0.keras"))
    except Exception as e:
        try:
            feature_model[i] = load_model(os.path.join(model_dir, f"model_feature_{i}_1.keras"))
        except Exception as e:
            print(f"please add model_feature_{i}_0/1.keras to the models folder")
            pass

try:
    brand_model = load_model(os.path.join(model_dir, f"model_brand_0.keras"))
except Exception as e:
    print("please add model_brand_0.keras to the models folder")
try:
    length_model = load_model(os.path.join(model_dir, f"model_length_0.keras"))
except Exception as e:
    print("please add model_length_0.keras to the models folder")
try:
    nn_model = load_model(os.path.join(model_dir, f"model_prediction.keras"))
except Exception as e:
    print("please add model_prediction.keras to the models folder")
try:
    rf_model = load(os.path.join(model_dir, "random_forest_model.joblib"))
except Exception as e:
    try:
        with open(os.path.join(model_dir, "random_forest_model.pkl"), 'rb') as f:
            rf_model = pickle.load(f)
    except Exception as e:
        print("please add random_forest_model.joblib or .pkl to the models folder")

def load_and_preprocess_image(filepath):
    """Preprocess the image to match the input shape of the image models."""
    img = load_img(filepath, target_size=(img_height, img_width))
    img_array = img_to_array(img) / 255.0
    return img_array

def predict_one_feature(test_image, feature_id):
    try:
        test_image = np.expand_dims(test_image, axis=0)
        prediction = feature_model[feature_id].predict(test_image, verbose=0)
        return 1 if prediction[0][0] > 0.5 else 0
    except Exception as e:
        print(feature_id)
        return 0

def predict_brand(test_image):
    try:
        test_image = np.expand_dims(test_image, axis=0)
        prediction = brand_model.predict(test_image, verbose=0)
        predicted_classes = np.argmax(prediction, axis=1)
        return predicted_classes
    except Exception as e:
        print(e)
        pass


def predict_length(test_image):
    try:
        test_image = np.expand_dims(test_image, axis=0)
        prediction = length_model.predict(test_image, verbose=0)
        return 1 if prediction[0][0] > 0.5 else 0
    except Exception as e:
        print(e)
        pass

def predict_all(test_img):
    predictions = {}
    brand = predict_brand(test_img)
    for i in range(16):
        predictions[f"品牌 Brand_{i}"] = 1 if brand == i else 0
    for i in range(len(feature_list)):
        feature = feature_list[i]
        pred = predict_one_feature(test_img, i)
        predictions[feature] = pred
    predictions_df = pd.DataFrame([predictions])
    predictions_df = predictions_df[sorted(predictions_df.columns)]
    return predictions_df

def predict_price(classify_res, model_type="RF"):
    if model_type == "NN":
        price = nn_model.predict(classify_res, verbose=0)
    else:
        price = rf_model.predict(classify_res)
    return price
