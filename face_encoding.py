# usage
# python face_encoding.py --dataset dataset --encodings encodings.pickle

# importing required packages
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

# handling the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-d', '--dataset', required=True, help='path of dataset')
ap.add_argument('-e', '--encodings', required=True, help='path to output serialized database of face encodings')
ap.add_argument('-m', '--detection_method', type=str, default='hog', help='face detection model to use: hog or cnn')
args = vars(ap.parse_args())

# initializing empty list of encodings and names
knownEncodings = []
knownNames = []

# forming image paths from dataset
imagePaths = list(paths.list_images(args['dataset']))

print("[INFO] starting face encoding for dataset...")
print("[INFO] This might take a while...")

# loop over image paths
for (i, imagePath) in enumerate(imagePaths):
    # extracting person's name form image path
    name = imagePath.split(os.path.sep)[-2]

    # loading input image and converting it from BGR(OpenCV) to RGB(dlib)
    image = cv2.imread(imagePath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # detecting bounding boxes for each face
    boxes = face_recognition.face_locations(rgb, model=args['detection_method'])

    # computing the face embedding
    encodings = face_recognition.face_encodings(rgb, boxes)

    # loop over encodings
    for encoding in encodings:
        knownEncodings.append(encoding)
        knownNames.append(name)

print("[INFO] face encoding done...")
# dumping facial encodings + names to disk
print("[INFO] saving encodings")
data = {"encodings": knownEncodings, "names": knownNames}
f = open(args['encodings'], 'wb')
f.write(pickle.dumps(data))
f.close()