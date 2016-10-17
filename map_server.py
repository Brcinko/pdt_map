"""
    map_server, author: Lukas Klescinec <lukas.klescinec@gmail.com>
    FIIT Slovak University of Technology 2016

    This module is part of school project on lesson Advanced Databases.
"""
from flask import Flask, request, jsonify
app = Flask(__name__)

infos = [
    {
        'id': 1,
        'title': u'PubMap',
        'description': u'This is map server project for PDT lesson, which displays something.',
        'done': False
    }
]


@app.route('/info', methods=['GET'])
def info():
    if request.method == 'GET':
        return jsonify({'infos': infos})

if __name__ == '__main__':
    app.run(debug=True)
