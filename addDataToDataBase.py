import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime


cred = credentials.Certificate(r"K:\schl\Attendance\serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendancescl-default-rtdb.firebaseio.com/'
})

ref = db.reference('Students')

data = {
    '12GA146':
            {
                'name':"shaswath",
                'id':'12GA146',
                'class':'XII-Curium',
                'standing':'-',
                'year':'-',
                'starting_year':2012,
                'total_attendance':1,
                'last_attendance_time': '2000-01-01  00:00:00'

            },
    '963852':
            {
                'name': "elon musk",
                'id': '001',
                'class': 'XII-Nihonium',
            'standing': '-',
            'year': '-',
            'starting_year': 2012,
            'total_attendance': 1,
            'last_attendance_time': '2000-01-01  00:00:00'

        },
    '852741':
        {
            'name': "emily blunt",
            'id': '248',
            'class': 'XII-sonnet',
            'standing': '-',
            'year': '-',
            'starting_year': 2022,
            'total_attendance': 1,
            'last_attendance_time': '2000-01-01  00:00:00'

        },
    '007':
        {
            'name': "Bhama",
            'id': '007',
            'class': 'pharmacy',
            'standing': '-',
            'year': '-',
            'starting_year': 2022,
            'total_attendance': 1,
            'last_attendance_time': '2000-01-01  00:00:00'

        },





}

for key,value in data.items():
    ref.child(key).set(value)