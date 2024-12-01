# ClothesPredicting

## Check Files

Ensure the following files are present in their respective folders:

- DEMO/
  - app.py
  - feature_list.csv
  - predict.py
  - requirements.txt
- models/
  - model_brand_0.keras
  - model_length_0.keras
  - model_feature_0_{0/1}.keras
  - model_feature_1_{0/1}.keras
  - model_feature_2_{0/1}.keras
  - ...
  - model_feature_23_{0/1}.keras
  - model_prediction.keras
  - random_forest_model.joblib
  - random_forest_model.pkl

## Run the Application

Change to DEMO folder:
```
cd DEMO
```
Install required packages:
```
pip install -r requirements.txt
```
Run:
```
python app.py
```

## Predict

1. Upload photo.
2. Choose model (NN/RF).
3. Predict.
