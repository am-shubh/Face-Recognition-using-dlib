# usage
# python dataset.py --query "Jon Snow" --output dataset/Jon_Snow

# importing the required packages
from requests import exceptions
import argparse
import requests
import cv2
import os


# handling the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-q', '--query', required=True, help='search query')
ap.add_argument('-o', '--output', required=True, help='path to output directory of images')
args = vars(ap.parse_args())


API_KEY = '--------------------------------'    # Write your BING SEARCH API KEY
MAX_RESULTS = 50                                # maximum no. of images to be downloaded
GROUP_SIZE = 10                                 # group size, images will be downloaded in group of 10

# url end point for image
URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"


# exception lists
EXCEPTIONS = set([IOError, FileNotFoundError, exceptions.RequestException, exceptions.HTTPError, exceptions.ConnectionError, exceptions.Timeout])

# setting header and search parameter
query_term = args["query"]
headers = {"Ocp-Apim-Subscription-Key" : API_KEY}
params = {"q": query_term, "offset": 0, "count": GROUP_SIZE}

# performing the search
print("[INFO] searching Bing API for '{}'".format(query_term))
search = requests.get(URL, headers=headers, params=params)
search.raise_for_status()

# grab the results from the search, including the total number of estimated results returned by the Bing API
results = search.json()
estNumResults = min(results["totalEstimatedMatches"], MAX_RESULTS)
print("[INFO] {} total results for '{}'".format(estNumResults, query_term))

# initializing total number of images downloaded so far
total = 0

for offset in range(0, estNumResults, GROUP_SIZE):
	# make the request to fetch the results
	params["offset"] = offset
	search = requests.get(URL, headers=headers, params=params)
	search.raise_for_status()
	results = search.json()

    # loop over the results
	for v in results["value"]:
		# try to download the image
		try:
			# make a request to download the image
			print("[INFO] fetching: {}".format(v["contentUrl"]))
			r = requests.get(v["contentUrl"], timeout=30)
 
			# build the path to the output image
			ext = v["contentUrl"][v["contentUrl"].rfind("."):]
			p = os.path.sep.join([args["output"], "{}{}".format(
				str(total).zfill(8), ext)])
 
			# write the image to disk
			f = open(p, "wb")
			f.write(r.content)
			f.close()
 
		# catch any errors that would not unable us to download the image
		except Exception as e:
			# checking for exceptions list
			if type(e) in EXCEPTIONS:
				print("[INFO] skipping: {}".format(v["contentUrl"]))
				continue

        # try to load the image from disk
		image = cv2.imread(p)
 
		# if the image is `None`, we should delete it.
		if image is None:
			print("[INFO] deleting: {}".format(p))
			os.remove(p)
			continue
 
		# update the counter
		total += 1