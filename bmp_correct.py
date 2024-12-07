import machine
from machine import Pin, deepsleep
from bmp280 import BMP280
import time
import asyncio
from umqtt.simple import MQTTClient
import network

i2c = machine.I2C(id=1, sda=Pin(14), scl=Pin(15)) #id=channel
bmp = BMP280(i2c)

BUFFER_SIZE = 10
SENSOR_READ_OCCURENCE = 20 # 5 minutes
SENSOR_READ_DELAY = 1

ID = "mqtt_client"
MQTT_BROKER = "34.88.121.143"
TEMPERATURE_MEDIAN_TOPIC = "temperature"


PRESSURE_MEDIAN_TOPIC = "pressure"
WLAN_SSID = "A54"
WLAN_PASSWORD = "12345678"


async def read_sensor():
    print("STARTING SENSOR READ")
    global temperature_data_buffer
    global pressure_data_buffer
    
    while True:
        temperature_data_buffer = []
        pressure_data_buffer = []
        for i in range(10):
            temperature_data_buffer.append(bmp.temperature)
            pressure_data_buffer.append(bmp.pressure)
            
            await asyncio.sleep(SENSOR_READ_DELAY)
        
        client.publish(TEMPERATURE_MEDIAN_TOPIC, str(median(temperature_data_buffer)))
        client.publish(PRESSURE_MEDIAN_TOPIC, str(median(pressure_data_buffer)))

        #deepsleep(30000)
        
        await asyncio.sleep(SENSOR_READ_OCCURENCE)

#https://stackoverflow.com/a/24101534
def median(lst):
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2
   
    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0
                 
async def main():
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WLAN_SSID, WLAN_PASSWORD)
    
    while not wlan.isconnected():
        print("Connecting to wifi")
        time.sleep(1)
    print("Connected to wifi")
    
    global client
    
    client = MQTTClient(ID, MQTT_BROKER)
    
    while True:
        try:
            print("Connecting to broker")
            client.connect()
            print("Connected to broker")
            break
        except OSError as e:
            print(f"Connection failed, retrying")
            time.sleep(1)
    
    await asyncio.gather(
        read_sensor()
        )
    
    
asyncio.run(main())