import os
from tinydb import TinyDB

server_id = "sitarz-iot5-server"
topic = "sitarz/iot5"
ip = "test.mosquitto.org"

datetime_format = '%Y-%m-%d %H:%M:%S'

def file_location(name):
  return os.path.join(os.path.dirname(__file__), name)

db = TinyDB(file_location("store.json"))
