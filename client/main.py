# import lib.rfid.MFRC522 as MFRC522
import paho.mqtt.client as mqtt
import os
import time
import json

topic = "sitarz/iot5"
ip = "test.mosquitto.org"

def readTerminalId():
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'terminal_id.config')
        s = open(file_path, mode='r', encoding="utf-8")
        terminal_id = s.read(8)
        s.close()
        return terminal_id
    except Exception as exc:
        print("File open error:", exc)
        print('Using default terminal_id - "00000000"')
        return "00000000"

def main():
    terminal_id = readTerminalId()
    client = mqtt.Client("sitarz-iot5-" + terminal_id)

    client.connect(ip)

    while True:
        if not client.is_connected:
            time.sleep(1)
            continue
        data = input()
        if data == "exit" or len(data) == 0:
            break

        client.publish(topic, json.dumps({ 'card_id': data, 'terminal_id': terminal_id }))

    # MIFAREReader = MFRC522.MFRC522()
    # while True:
    #     (status, _) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    #     if status == MIFAREReader.MI_OK:
    #         (status, uid) = MIFAREReader.MFRC522_Anticoll()
    #         if status == MIFAREReader.MI_OK:
    #             card_id = ''.join(uid)
    #             client.publish(topic, json.dumps({ 'card_id': card_id, 'terminal_id': terminal_id }))

if __name__ == "__main__":
    main()
