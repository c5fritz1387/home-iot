import bme280
import smbus2
from time import sleep
from json import dumps
import json
from datetime import date, datetime
import requests
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

port = 1
address = 0x76
bus = smbus2.SMBus(port)
bme280.load_calibration_params(bus, address)


def main():
    cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
    url = os.getenv('FIREBASE_DB_URL')

    db = firebase_creds(cred, url)

    # # with open('data.json', 'r') as json_file:
    # #     json_data = json.load(json_file)
    #
    # post_firebase(bme280_db, json_data)

    read_data(bus, address, db)

def firebase_creds(credentials, firebase_db_url):
    # Initialize the app with a custom auth variable, limiting the server's access
    app = firebase_admin.initialize_app(credentials, {

        'databaseURL': firebase_db_url

    })
    sensor_db = db.reference()

    return sensor_db

def post_firebase(db, json_data):
    data = db.child('bme280').push(json_data)
    print("data inserted")
    return data

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


def read_data(bus, address, db):
    while True:
        data = {}
        data['reading'] = []
        bme280_data = bme280.sample(bus, address)
        id = bme280_data.id
        timestamp = bme280_data.timestamp
        humidity = bme280_data.humidity
        pressure = bme280_data.pressure
        ambient_temperature = bme280_data.temperature
        data['reading'].append({
            'id': str(id),
            'timestamp': str(timestamp),
            'humidity': humidity,
            'pressure': pressure,
            'ambient_temperature': ambient_temperature
            })

        print(id, timestamp, humidity, pressure, ambient_temperature)
        print(bme280_data)
        print(data)
        sleep(10)

        post_firebase(db, data)

        # with open('data.json', 'w') as json_file:
        #     json.dump(data, json_file)

if __name__ == "__main__":
    main()
