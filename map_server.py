"""
    map_server, author: Lukas Klescinec <lukas.klescinec@gmail.com>
    FIIT Slovak University of Technology 2016

    This module is part of school project on lesson Advanced Databases.
"""

import db_connection
import settings
from string import replace

from flask import Flask, request, jsonify, json

app = Flask(__name__)


@app.route('/info', methods=['GET'])
def info():
    if request.method == 'GET':
        query = 'SELECT PostGIS_full_version();'
        postgis_ver = db_connection.execute_query(conn, query)
        settings.infos[0]['postgis_ver'] = str(postgis_ver)
        return jsonify({'infos': settings.infos})


@app.route('/pubs_info', methods=['GET'])
def pubs_info():
    if request.method == 'GET':
        # query = 'SELECT name AS description, ST_AsGeoJSON(way) AS geometry FROM planet_osm_point WHERE amenity = \'pub\';'
        query = 'SELECT row_to_json(fc) FROM ( SELECT \'FeatureCollection\' AS type, array_to_json(array_agg(f)) AS features FROM (SELECT \'Feature\' AS type , ST_AsGeoJSON(way)::json AS geometry, row_to_json((name, amenity)) AS properties FROM planet_osm_point WHERE amenity = \'pub\'   ) AS f )  AS fc;'
        pubs = db_connection.execute_query(conn, query)
        pubs = str(pubs)
        new_pubs = replace(pubs, "f1", "description")
        final_pubs = replace(new_pubs, "f2", "icon")
        return json.dumps(final_pubs)
        # return jsonify({'places': str(pubs)})

if __name__ == '__main__':
    # connect database
    conn = db_connection.open_connection()
    print "Database connected."
    # start API server
    app.run(debug=True)

