import json
from tinydb import Query, where
from config import db


def terminal(data):
    terminals = db.table('terminals')
    if len(data) == 1:
        print("Available subcommands:", "list", "add <terminal-id>",
              "remove <terminal-id>", sep="\n\t")

    elif data[1] == "list":
        list = '\n'.join(t['id'] for t in terminals)
        print(list)

    elif data[1] == "add":
        if len(data) != 3:
            print("Incorrect argument number! Expected `terminal add <terminal-id>`")
        else:
            terminal_id = data[2]
            search = terminals.search(where('id') == terminal_id)
            if not search:
                terminals.insert({'id': terminal_id})
                print("Terminal added successfully!")
            else:
                print("Terminal already added!")

    elif data[1] == "remove":
        if len(data) != 3:
            print("Incorrect argument number! Expected `terminal remove <terminal-id>`")
        else:
            terminal_id = data[2]
            search = terminals.search(where('id') == terminal_id)
            if search:
                terminals.remove(where('id') == terminal_id)
                print("Terminal removed successfully!")
            else:
                print("No such terminal exists!")
    else:
        print("No such command!")


def cards(data):
    cards = db.table('cards')
    if len(data) == 1:
        print("Available subcommands:", "list", sep="\n\t")

    elif len(data) == 2 and data[1] == "list":
        list = '\n'.join(c['id'] for c in cards)
        print(list)

    else:
        print("No such command!")


def person(data):
    people = db.table('people')
    if len(data) == 1:
        print("Available subcommands:", "list",
              "add <person-id> <name>", "remove <person-id>", "assign <person-id> <card-id>", sep="\n\t")

    elif data[1] == "list":
        list = '\n'.join(p['id'] + "\t" + p['name'] +
                         "\t" + p['card_id'] for p in people)
        print(list)

    elif data[1] == "add":
        if len(data) > 4:
            print("Incorrect argument number! Expected `person add <person-id> <name>`")
        else:
            person_id = data[2]
            search = people.search(where('id') == person_id)
            if not search:
                people.insert({'id': person_id, 'name': data[3], 'card_id': ''})
                print("Person added successfully!")
            else:
                print("Person already exists! Aborted.")

    elif data[1] == "remove":
        if len(data) != 3:
            print("Incorrect argument number! Expected `person remove <person-id>`")
        else:
            person_id = data[2]
            search = people.search(where('id') == person_id)
            if search:
                people.remove(where('id') == person_id)
                print("Person removed successfully!")
            else:
                print("No such person exists!")

    elif data[1] == "assign":
        if len(data) != 4:
            print("Incorrect argument number! Expected `person assign <person-id> <card-id>`")
        else:
            person_id = data[2]
            search = people.search(where('id') == person_id)
            if search:
                card_id = data[3]
                card_search = db.table('cards').search(where('id') == card_id)
                if card_search:
                    people.update({ 'card_id': card_id }, where('id') == person_id)
                    print("Person got the card assigned successfully!")
                else:
                    print("No such card exists!")
            else:
                print("No such person exists!")

    else:
        print("No such command!")



def command():
    print("> ", end="")
    data = input().split()

    if len(data) == 0 or data[0] == "exit":
        return

    elif data[0] == "terminal":
        terminal(data)

    elif data[0] == "card":
        cards(data)

    elif data[0] == "person":
        person(data)

    else:
        print("Available commands:", "terminal", "card",
                "person", "logins", "exit", sep="\n\t")

    command()
