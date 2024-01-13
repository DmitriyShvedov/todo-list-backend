import json
import os
from typing import List


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries: List[Entry] = []

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        file_names = os.listdir(self.data_path)
        for file_name in file_names:
            file_path = os.path.join(self.data_path, file_name)
            if file_name.endswith(".json"):
                entry = Entry.load(file_path)
                self.entries.append(entry)

    def add_entry(self, title: str):
        entry = Entry(title)
        self.entries.append(entry)


class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def __str__(self):
        return self.title

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, level=0):
        print_with_indent(str(self), level)
        for entry in self.entries:
            entry.print_entries(level + 1)

    def json(self):
        my_dict = {
            "title": self.title,
            "entries": [entry.json() for entry in self.entries]
        }
        return my_dict

    @classmethod
    def from_json(cls, json_to_object: dict):
        new_entry = cls(json_to_object["title"])
        for item in json_to_object.get("entries", []):
            new_entry.add_entry(cls.from_json(item))
        return new_entry

    def save(self, path):
        with open(os.path.join(path, f'{self.title}.json'), 'w', encoding='utf-8') as f:
            json.dump(self.json(), f)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = json.load(f)
            return Entry.from_json(content)


def print_with_indent(value, level):
    indent = '\t' * level
    print(indent + value)
