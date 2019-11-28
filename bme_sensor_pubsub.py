import bme280
import smbus2
from time import sleep
from json import dumps
import json
from google.cloud import pubsub

port = 1
address = 0x76
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus, address)


def main():
    project_id = "home-weather-iot-firebase"
    topic_name = "device-signals"

    publisher = pubsub.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    # # with open('data.json', 'r') as json_file:
    # #     json_data = json.load(json_file)
    #

    data = {}
    data['reading'] = []
    sensor_data = read_data(bus, address, data, publisher, topic_path)

def publish_message(data, publisher, topic_path):
    # Data must be a bytestring
    data_encode = data.encode('utf-8')
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data=data_encode)
    print(future.result())


def read_data(bus, address, data, publisher, topic_path):
    while True:
        bme280_data = bme280.sample(bus, address)
        id = bme280_data.id
        timestamp = bme280_data.timestamp
        humidity = bme280_data.humidity
        pressure = bme280_data.pressure
        ambient_temperature = bme280_data.temperature
        data = {
            'id': str(id),
            'timestamp': str(timestamp),
            'humidity': humidity,
            'pressure': pressure,
            'ambient_temperature': ambient_temperature
            }

        print(id, timestamp, humidity, pressure, ambient_temperature)
        print(bme280_data)
        print(data)
        sleep(10)

        publish_message(data, publisher, topic_path)


        # with open('data.json', 'w') as json_file:
        #     json.dump(data, json_file)

if __name__ == "__main__":
    main()