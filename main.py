import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
import csv



cred = credentials.Certificate(r"K:\schl\Attendance\serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendancescl-default-rtdb.firebaseio.com/',
    'storageBucket': 'faceattendancescl.appspot.com'
})

bucket = storage.bucket()
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
imgBackground = cv2.imread(r'K:\schl\Attendance\Resources\background.png')

folderModePath = r'K:\schl\Attendance\Resources\Modes'
modePathList= os.listdir(folderModePath)
imgModList= []
for path in modePathList:
    imgModList.append(cv2.imread(os.path.join(folderModePath,path)))

print('loading encode files......')
file = open('EncodeFile.p','rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown , studentIds = encodeListKnownWithIds
# print(studentIds)
print('encode file loaded')
currentdate = datetime.now().strftime('%Y-%m-%d')

fp = open(currentdate+'.csv','w+',newline='')
lnwriter = csv.writer(fp)
lnwriter.writerow(['NAME','Time','Class','Reg.NO'])
modeType = 0
counter = 0
id = -1
imgStudent = []
while True:
    success , img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame= face_recognition.face_encodings(imgS,faceCurFrame)

    imgBackground[162:162 + 480,55:55+640]= img
    imgBackground[44:44 + 633,808:808+414]= imgModList[modeType]
    if faceCurFrame:
        for encodeFace , faceloc in zip(encodeCurFrame,faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            facedis = face_recognition.face_distance(encodeListKnown,encodeFace)

            # print('matches',matches)
            # print('facedis',facedis)

            matchindex = np.argmin(facedis)
            # print('match index', matchindex)

            if matches[matchindex]:
                # print('known face detected')
                #print(studentIds[matchindex])
                y1 ,x2,y2,x1 = faceloc
                y1, x2, y2, x1 = y1*4 ,x2*4,y2*4,x1*4
                bbox = 55 + x1, 162 + y1 , x2 - x1 , y2 - y1
                imgBackground= cvzone.cornerRect(imgBackground,bbox,rt=0)
                id = studentIds[matchindex]
                if counter ==0:
                    cvzone.putTextRect(imgBackground,'Loading',(275,400))
                    cv2.imshow('face detector',imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1
            if counter!= 0 :

                if counter==1:
                    studentInfo =  db.reference(f'Students/{id}').get()
                    print(studentInfo)
                    blob = bucket.get_blob(f'K:\schl\Attendance\Images/{id}.png')
                    # print(blob)

                    try:
                        array = np.frombuffer(blob.download_as_string(),np.uint8)

                    except AttributeError:

                        pass

                    imgStudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)

                    try:
                        datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                      '%Y-%m-%d %H:%M:%S')

                    except TypeError:
                        pass

                    secondsElapsed = (datetime.now()-datetimeObject).total_seconds()
                    print(secondsElapsed)

                    if secondsElapsed > 30:
                        try:
                            ref = db.reference(f'Students/{id}')
                            studentInfo['total_attendance'] +=1
                            ref.child('total_attendance').set(studentInfo['total_attendance'])
                            ref.child('last_attendance_time').set(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                            currentTime=datetime.now().strftime('%H:%M:%S')

                            lnwriter.writerow([studentInfo['name'],currentTime,studentInfo['class'],studentInfo['id']])
                        except TypeError:
                            pass


                    else :
                        modeType=3
                        counter = 0
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModList[modeType]

                if modeType!= 3:

                    if 10<counter<20:
                        modeType = 2
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModList[modeType]


                    if counter<=10:
                        cv2.putText(imgBackground,str(studentInfo['total_attendance']),(861,125),
                                    cv2.FONT_HERSHEY_COMPLEX,1,(225,225,225),1)

                        cv2.putText(imgBackground, str(studentInfo['id']), (1006, 550),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (225, 225, 225), 1)
                        cv2.putText(imgBackground, str(studentInfo['class']), (1006, 493),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (225, 225, 225), 1)
                        # cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                        #             cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        # cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                        #             cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        # cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                        #             cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)


                        imgBackground[175:175+216,909:909+216] = imgStudent



                        (w,h),_ =cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
                        offset = (414-w)//2

                        cv2.putText(imgBackground, str(studentInfo['name']), (808+offset, 445),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)


                    counter +=1
                    if counter >=20:
                        counter = 0
                        modeType = 0
                        studentInfo = []
                        imgStudent = []
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModList[modeType]
    else:
        modeType=0
        counter=0




    cv2.imshow('face detector',imgBackground)
    cv2.waitKey(1)

