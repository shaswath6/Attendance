import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate(r"K:\schl\Attendance\serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendancescl-default-rtdb.firebaseio.com/',
    'storageBucket': 'faceattendancescl.appspot.com'
})


folder_path = r'K:\schl\Attendance\Images'
modePathList = os.listdir(folder_path)

imgList = []
studentIds = []
for path in modePathList:
    imgList.append(cv2.imread(os.path.join(folder_path,path)))
    studentIds.append(os.path.splitext(path)[0])

    fileName = f'{folder_path}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)




def findEncodings(imagesList):
    encodeList= []
    for img in imagesList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print('encoding started')
encodeListknown = findEncodings(imgList)
encodeListKnownIds = [encodeListknown,studentIds]

print('encoding completed')


file = open('EncodeFile.p','wb')
pickle.dump(encodeListKnownIds,file)
file.close()
print('file saved')
