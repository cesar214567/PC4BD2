# import the necessary packages
from imutils import paths
import face_recognition
import pickle
import cv2
import os

Collection = {}
SourcePath = "../dataset"
DestPath = "Algoritmos/encodings.pickle"

def getFeatures(imagePath):
	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	boxes = face_recognition.face_locations(rgb, model="cnn")

	encodings = face_recognition.face_encodings(rgb, boxes)
	return encodings[0]

def extract():

	print("[INFO] quantifying faces...")
	imagePaths = list(paths.list_images(SourcePath))

	knownEncodings = []
	knownNames = []

	with open(DestPath, "w+") as f:
		for (i, imagePath) in enumerate(imagePaths):
			# extract the person name from the image path
			print("[INFO] processing image {}/{}".format(i + 1,
				len(imagePaths)))

			name = imagePath.split(os.path.sep)[-2]
			encoding = getFeatures(imagePath)

			print(name)
			print(encoding)
			knownNames.append(name)
			knownEncodings.append(encoding)

	print("[INFO] serializing encodings...")
	data = {"encodings": knownEncodings, "names": knownNames}
	f = open(DestPath, "wb")
	f.write(pickle.dumps(data))
	f.close()

def initCollection():
	global Collection
	Collection = pickle.loads(open(DestPath, "rb").read())
	Collection['names'] = Collection['names']

initCollection()