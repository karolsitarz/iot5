import json
from datetime import datetime
from tinydb import Query, where
from config import db, datetime_format


def terminal(data):
    terminals = db.table('terminals')
    if len(data) == 1:
        return "\n\t".join(("Available subcommands:", "list", "add <terminal-id>", "remove <terminal-id>"))

    if data[1] == "list":
        return "\n".join(t['id'] for t in terminals)

    if data[1] == "add":
        if len(data) != 3:
            return "Incorrect argument number! Expected `terminal add <terminal-id>`"

        terminal_id = data[2]
        search = terminals.search(where('id') == terminal_id)
        if not search:
            terminals.insert({'id': terminal_id})
            return "Terminal added successfully!"

        return "Terminal already added!"

    if data[1] == "remove":
        if len(data) != 3:
            return "Incorrect argument number! Expected `terminal remove <terminal-id>`"

        terminal_id = data[2]
        search = terminals.search(where('id') == terminal_id)
        if search:
            terminals.remove(where('id') == terminal_id)
            return "Terminal removed successfully!"

        return "No such terminal exists!"

    return "No such command!"


def cards(data):
    cards = db.table('cards')
    if len(data) == 1:
        return "\n\t".join(("Available subcommands:", "list"))

    if len(data) == 2 and data[1] == "list":
        return '\n'.join(c['id'] for c in cards)

    return "No such command!"


def person(data):
    people = db.table('people')
    if len(data) == 1:
        return "\n\t".join(("Available subcommands:", "list", "add <person-id> <name>", "remove <person-id>", "assign <person-id> <card-id>"))

    if data[1] == "list":
        return '\n'.join(p['id'] + "\t" + p['name'] + "\t" + p['card_id'] for p in people)

    if data[1] == "add":
        if len(data) > 4:
            return "Incorrect argument number! Expected `person add <person-id> <name>`"

        person_id = data[2]
        search = people.search(where('id') == person_id)
        if not search:
            people.insert({'id': person_id, 'name': data[3], 'card_id': ''})
            return "Person added successfully!"

        return "Person already exists! Aborted."

    if data[1] == "remove":
        if len(data) != 3:
            return "Incorrect argument number! Expected `person remove <person-id>`"

        person_id = data[2]
        search = people.search(where('id') == person_id)
        if search:
            people.remove(where('id') == person_id)
            return "Person removed successfully!"

        return "No such person exists!"

    if data[1] == "assign":
        if len(data) != 4:
            return "Incorrect argument number! Expected `person assign <person-id> <card-id>`"

        person_id = data[2]
        search = people.search(where('id') == person_id)
        if search:
            card_id = data[3]
            card_search = db.table('cards').search(where('id') == card_id)
            if card_search:
                people.update({ 'card_id': card_id }, where('id') == person_id)
                return "Person got the card assigned successfully!"

            return "No such card exists!"

        return "No such person exists!"

    return "No such command!"


def login(data):
    logins = db.table('logins')
    if len(data) == 1:
        return "\n\t".join(("Available subcommands:", "list <person-id>", "save <person-id>"))

    if data[1] == "list":
        if len(data) != 3:
            return "Incorrect argument number! Expected `login list <person-id>`"

        person_id = data[2]
        search = db.table('people').search(where('id') == person_id)
        if not search:
            return "No person with such id!"

        card_id = search[0]["card_id"]
        if len(card_id) == 0:
            return "The person doesn't have any card assigned!"

        login_search = logins.search(where('card_id') == card_id)
        string = "time" + "\t\t\t" + "terminal id" + "\n"
        for l in login_search:
            string += datetime.utcfromtimestamp(l["time"]).strftime(datetime_format)
            string += "\t" + l["terminal_id"] + "\n"

        return string

    return "No such command!"


def command():
    print("> ", end="")
    data = input().split()

    if len(data) == 0:
        return command()

    if data[0] == "terminal":
        print(terminal(data))
        return command()

    if data[0] == "card":
        print(cards(data))
        return command()

    if data[0] == "person":
        print(person(data))
        return command()

    if data[0] == "login":
        print(login(data))
        return command()

    if data[0] == "exit":
        return

    print("Available commands:", "terminal", "card", "person", "login", "exit", sep="\n\t")
    return command()
