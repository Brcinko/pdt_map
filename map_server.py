"""
    map_server, author: Lukas Klescinec <lukas.klescinec@gmail.com>
    FIIT Slovak University of Technology 2016

    This module is part of school project on lesson Advanced Databases.
"""

import db_connection
import settings

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/info', methods=['GET'])
def info():
    if request.method == 'GET':
        return jsonify({'infos': settings.infos})

if __name__ == '__main__':
    # connect database
    conn = db_connection.open_connection()
    print "Database connected."
    # start API server
    app.run(debug=True)

