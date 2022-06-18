import joblib

# Fichero test.py

# Realizar unas predicciones de prueba
classifier_loaded = joblib.load("saved_models/knn_iris_dataset.pkl")
encoder_loaded = joblib.load("saved_models/iris_label_encoder.pkl")
print(" --- Pickle classifier y label encoder load executed ---")

# Prediction test con vectores aleatorios
X_manual_test = [[20.1, 20.1, 100.1, 100.1]]
print("X_manual_test", X_manual_test)

prediction_raw = classifier_loaded.predict(X_manual_test)
print("Prediction_raw", prediction_raw)

prediction_real = encoder_loaded.inverse_transform(
                            classifier_loaded.predict(X_manual_test))
print("Real prediction", prediction_real)