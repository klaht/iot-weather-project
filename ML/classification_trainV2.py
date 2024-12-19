import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer




features = [
	'Formatted Date',
 	'Summary',
 	'Precip Type',
 	'Temperature (C)',
 	'Apparent Temperature (C)',
 	'Humidity',
 	'Wind Speed (km/h)',
 	'Wind Bearing (degrees)',
	'Visibility (km)',
	 'Loud Cover',
 	'Pressure (millibars)',
 	'Daily Summary'
]








if __name__ == "__main__":
	print("[*] sanity check!")

	dataset = "weatherHistory_edit.csv"
	df_weather = pd.read_csv(dataset)
	# print(df_weather["Temperature (C)"].min())
	# print(df_weather["Temperature (C)"].max())
	# print(df_weather.columns.to_list())

	# df_weather_row_count, df_weather_column_count=df_weather.shape
	# print('Total number of rows:', df_weather_row_count)
	# print('Total number of columns:', df_weather_column_count)


	# Summary_Weather=df_weather["Summary"].value_counts().reset_index()
	# Summary_Weather.columns=["Weather Type","Count"]
	# print(Summary_Weather)


	X = df_weather[['Temperature (C)', 'Pressure (millibars)']]
	y_summary = df_weather['Summary']



	# One-hot encode the targets
	encoder_summary = OneHotEncoder()
	y_summary_encoded = encoder_summary.fit_transform(y_summary.values.reshape(-1, 1)).toarray()



	scaler = StandardScaler()
	X_normalized = scaler.fit_transform(X)


	X_train, X_test, y_train, y_test = train_test_split(X_normalized, y_summary_encoded, test_size=0.2, random_state=42)



	# Define the model
	model = tf.keras.Sequential([
		tf.keras.layers.Input(shape=(X_train.shape[1],)),
		tf.keras.layers.Dense(64, activation='relu'),
		tf.keras.layers.Dense(32, activation='relu'),
		tf.keras.layers.Dense(y_summary_encoded.shape[1], activation='softmax')  # Output for Summary
	])

	# Compile the model
	model.compile(optimizer='adam',
				loss='categorical_crossentropy',
				metrics=['accuracy'])


	es_callback = tf.keras.callbacks.EarlyStopping(monitor="accuracy", min_delta=0, patience=5)

	checkpoint_cb = tf.keras.callbacks.ModelCheckpoint(
		'multi_output_model_checkpoint.h5',
		monitor="accuracy",
		verbose=1,
		save_weights_only=True,
		save_best_only=True,
	)


	# 5. Train the Model
	history = model.fit(
		X_train,
		y_train,
		epochs=20,
		batch_size=32,
		validation_split=0.2,
		callbacks=[es_callback, checkpoint_cb]
	)


	# 6. Evaluate the Model
	loss, accuracy = model.evaluate(X_test, y_test)
	print(f"Test Accuracy: {accuracy:.2f}")



	# 7. Make Predictions

	# Example input for prediction
	new_data = np.array([[10.0, 1015]])  # Temperature (C) and Pressure (millibars)
	new_data_normalized = scaler.transform(new_data)

	# Predict
	predictions = model.predict(new_data_normalized)

	# Decode predictions
	predicted_summary = encoder_summary.inverse_transform(predictions)

	print(f"Predicted Summary: {predicted_summary[0]}")
