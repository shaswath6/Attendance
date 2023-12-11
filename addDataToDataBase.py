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

    '006':
        {
            'name': "test",
            'id': '008',
            'class': 'pharmacy',
            'standing': '-',
            'year': '-',
            'starting_year': 2022,
            'total_attendance': 1,
            'last_attendance_time': '2000-01-01  00:00:00'

        }






}

for key,value in data.items():
    ref.child(key).set(value)