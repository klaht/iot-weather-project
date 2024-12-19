import tensorflow as tf
import pickle
import os
from sklearn.preprocessing import StandardScaler

import paho.mqtt.client as mqtt


MQTT_URL = os.getenv('MQTT_URL')
MQTT_PORT = int(os.getenv('MQTT_PORT'))


# Needed for predicting
model = tf.keras.models.load_model('classify.h5')
scaler = StandardScaler()
with open('classify_hotEncoder.pkl', 'rb') as f:
	encoder = pickle.load(f)




def predict(value):

	value_normalized = scaler.transform(value)

	# Make prediction
	predictions = model.predict(value_normalized)

	# Decode prediction back to categorial label
	prediction = encoder.inverse_transform(predictions)

	return prediction[0]





def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("#")


def on_message(client, userdata, message):
    print("received message =",str(message.payload.decode("utf-8")))

    # Assuming the sensor data is a number
    try:
        value = float(message.payload.decode("utf-8")) # needs to be of the form: np.array([[10.0, 1015]])  # Temperature (C) and Pressure (millibars)
        prediction = model.predict(value)
        print(f"Prediction for the received sensor data ({value}): {prediction}")
    except ValueError:
        print("Invalid data received. Could not parse as a number.")





if __name__ == "__main__":

	client = mqtt.Client()

	client.on_connect = on_connect
	client.on_message = on_message

	client.connect(MQTT_URL, MQTT_PORT, 60)


	client.loop_forever()

