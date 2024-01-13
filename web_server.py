from flask import Flask, request, jsonify
from resources import EntryManager, Entry

FOLDER = '/Users/dm.shvedov/Desktop'

app = Flask(__name__)

@app.route("/api/entries/")
def get_entries():
    my_list = []
    entry_manager = EntryManager(FOLDER)
    entry_manager.load()
    for entry in entry_manager.entries:
        my_list.append(entry.json())
    return my_list


@app.route('/api/save_entries/', methods=["POST"])
def save_entries():
        data = request.get_json()

        entry_manager = EntryManager(FOLDER)

        for entry_data in data:
            entry = Entry.from_json(entry_data)
            entry_manager.entries.append(entry)

        entry_manager.save()

        return {'status': 'success'}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)