import paho.mqtt.client as mqtt
import time
import json
import math
from tinydb import Query, where
from command import command
from config import db, server_id, topic, ip


def disconnect(client):
    client.loop_stop()


def on_disconnect(client, userdata,rc=0):
    disconnect(client)


def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    if not data["terminal_id"] or not data["card_id"]:
        return

    terminals = db.table('terminals')
    search = terminals.search(where('id') == data["terminal_id"])

    if not search:
        print("Unpermitted connection from", data["terminal_id"], "terminal.")
        return

    cards = db.table('cards')
    search = cards.search(where('id') == data["card_id"])
    if not search:
        cards.insert({ 'id': data["card_id"] })
        print("New card registered with id ", data["card_id"])

    logins = db.table('logins')
    t = time.time()
    logins.insert({ 'time': t, 'card_id': data["card_id"], 'terminal_id': data["terminal_id"] })
    print("New", data["card_id"], "login from", data["terminal_id"], "at", t)


def main():
    client = mqtt.Client(server_id)

    client.connect(ip)
    client.on_message = on_message
    client.loop_start()
    client.subscribe(topic)

    # wait until client is connected, temporary solution
    while not client.is_connected:
        pass

    # expect a cli command
    command()

    disconnect(client)


if __name__ == "__main__":
    main()
