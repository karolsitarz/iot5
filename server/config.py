import os
from tinydb import TinyDB

server_id = "sitarz-iot5-server"
topic = "sitarz/iot5"
ip = "test.mosquitto.org"

file_path = os.path.join(os.path.dirname(__file__), 'store.json')
db = TinyDB(file_path)
