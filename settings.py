"""
    settings.py, author: Lukas Klescinec <lukas.klescinec@gmail.com>
    FIIT Slovak University of Technology 2016

    This file is part of school project on lesson Advanced Databases.
"""

# Database settings
HOSTNAME = 'localhost'
USERNAME = 'postgres'
PASSWORD = ''
DB_NAME = 'pdt_map'

# Info string for info call
infos = [
    {
        'id': 1,
        'title': u'PubMap',
        'description': u'This is map server project for PDT lesson, which displays something.',
        'done': False
    }
]