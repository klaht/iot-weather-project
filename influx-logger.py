print("STARTING INFLUX-LOGGER SCRIPT")
import os
import paho.mqtt.client as mqtt
from influxdb_client import WritePrecision, InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("Starting influx-logger script")

load_dotenv()

MQTT_URL = os.getenv('MQTT_URL')
MQTT_PORT = int(os.getenv('MQTT_PORT'))
BUCKET = os.getenv('INFLUXDB_BUCKET')
INFLUX_URL = os.getenv('INFLUXDB_URL')
INFLUX_USERNAME = os.getenv('INFLUXDB_USERNAME')
INFLUX_PASSWORD = os.getenv('INFLUXDB_PASSWORD')
ORG = os.getenv('INFLUXDB_ORG')


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("#")


def on_message(client, userdata, message):
    print("received message =",str(message.payload.decode("utf-8")))
    
    try:
        value = float(message.payload.decode("utf-8"))
        point = Point(BUCKET).field(message.topic, value)
        userdata.write(bucket=BUCKET, record=point)
    except ValueError:
        print("Received non-numeric data, skipping write to InfluxDB")


def main():
    print("Starting InfluxDB logger")
    url = f"http://{INFLUX_URL}:8086"    
    
    print("Connecting to InfluxDB at", url)

    influxclient = InfluxDBClient(url=url,
                                    username=INFLUX_USERNAME,
                    password=INFLUX_PASSWORD, org=ORG
                    )
    print("Connected to InfluxDB")
    write_api = influxclient.write_api(write_options=ASYNCHRONOUS)
    client = mqtt.Client(userdata=write_api)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_URL, MQTT_PORT, 60)      
    client.loop_forever()
    
if __name__ == "__main__":
    main()