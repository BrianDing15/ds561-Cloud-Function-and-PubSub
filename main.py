import functions_framework
from google.cloud import storage
from google.cloud import pubsub_v1

@functions_framework.http

#Create Client
def createClient(projectName):
    #Create Client
    storage_client = storage.Client(project=projectName)
    return storage_client

#Return Info For Bucket
def returnBucket(storage_client, bucketName):
    bucket = storage_client.get_bucket(bucketName)
    return bucket

#Checks to see if request is a get request
def checkGet(request):
    print("checking if request is a GET request")
    if request.method == "GET":
        return True
    else:
        return False

#Returns the contents of the requested file
def returnContents(blob):
    contents = blob.open('r')
    return contents.read()

#List of banned countries
bannedCountries = ["North Korea", "Iran", "Cuba", "Myanmar", "Iraq", "Libya", "Sudan", "Zimbabwe", "Syria"]

#Main function
def get_file(request):

    projectId = 'ds561-project-435318'
    country = request.headers.get("X-country")

    print("COUNTRY ", country)
    if country in bannedCountries:
        message = b"There was a request from a forbidden country"

        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(projectId, 'DS561Project3PubSub')
        
        future = publisher.publish(topic_path, message)

        print("Request sent from forbidden country " + country)
        return "Permission Denied", 400
    
    #check if request is a GET request. If not, return 501
    if checkGet(request) == False:
        print("Requested method not implemented")
        return "Method not implemented", 501

    path = request.path.split("/")
    bucket = path[1]

    #Create storage client and locate bucket.
    storage_client = createClient(projectId)
    bucket = returnBucket(storage_client, path[1])

    #Get requested file from bucket
    blob = bucket.get_blob(path[2] + '/' + path[3])

    #If file not found, return 404
    if blob is None:
        print("Requested file not found")
        return "File not found", 404
    
    return returnContents(blob), 200