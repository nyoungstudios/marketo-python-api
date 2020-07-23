# imports
import requests
import os

#base rest and base identity urls
baseCode = os.environ.get('baseCode')
baseUrl = "https://" + baseCode + ".mktorest.com/"
baseRest = baseUrl + "rest"
baseIdentity = baseUrl + "identity"
baseBulk = baseUrl + "bulk"

#client id and client secret strings
clientID = os.environ.get('marketoClientID')
clientSecret = os.environ.get('marketoClientSecret')

#function to create the marketo api access token
def createAccessToken():
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'grant_type': 'client_credentials', 'client_id': clientID, 'client_secret': clientSecret}

    # sending get request and saving the response as response object
    data = requests.get(url=baseIdentity + "/oauth/token", params=PARAMS).json()

    return data

#returns just the access token
def getAccessToken():
    return createAccessToken()['access_token']
