# usage
# python recognize_faces.py --image test/pic1.jpg

# importing the required packages
import face_recognition
import argparse
import pickle
import cv2

# handling the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='path to input image')
ap.add_argument('-m', '--detection_method', type=str, default='hog', help='face detection model: hog or cnn')
args = vars(ap.parse_args())

encodingsFile = 'encodings.pickle'

# loading known faces and known encodings
print("[INFO] loding encodings..")
data = pickle.loads(open(encodingsFile, 'rb').read())

# loading the input image and converting it to RGB
image = cv2.imread(args['image'])
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# detecting bounding boxes for each face in input image and computing facial encodings
print('[INFO] recognizing faces...')
boxes = face_recognition.face_locations(rgb, model=args["detection_method"])
encodings = face_recognition.face_encodings(rgb, boxes)

# initialize the list of names for each face detected
names = []

# looping over facial embeddings
for encoding in encodings:
    # attemting to match face in input image to the known encodings
    matches = face_recognition.compare_faces(data['encodings'], encoding)
    name = 'unknown'

    # check to see, if any match is found
    if True in matches:

        # find the indexes of all matched faces then initialize a dictionary to count total
        # number of times each face was matched
        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
        counts = {}

        # loop ver matched indexes and maintian a count for each recognized faces
        for i in matchedIdxs:
            name = data['names'][i]
            counts[name] = counts.get(name, 0) + 1

        # determine the recognized face with largest number of count
        name = max(counts, key=counts.get)

    names.append(name)


# loop over recognized faces
for ((top, right, bottom, left), name) in zip(boxes, names):
    # drawing names over faces
    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
    y = top - 15 if top - 15 > 15 else top + 15
    cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)


# saving recognized images in results directory
print("[INFO] Saving recognized image in results directory...")
cv2.imwrite('results/'+args['image'].split('/')[-1],image)

# showing the output image
cv2.imshow("Image", image)
cv2.waitKey(0)

    