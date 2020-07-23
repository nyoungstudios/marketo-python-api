# imports
import requests
import identity
import json
import fieldNames
import formatTime

# variables parameters for creating leads
createOnly = 'createOnly'
updateOnly = 'updateOnly'
createDuplicate = 'createDuplicate'

# variables for bulk exports
bulkStatusCreated = 'created'
bulkStatusQueued = 'queued'
bulkStatusProcessing = 'processing'
bulkStatusCancelled = 'cancelled'
bulkStatusCompleted = 'completed'
bulkStatusFailed = 'failed'
bulkStatusAll = [bulkStatusCreated, bulkStatusQueued, bulkStatusProcessing, bulkStatusCancelled, bulkStatusCompleted, bulkStatusFailed]

# function to get leads. Type is how to filter it by and value is the value of the type. Pass parameters that we want to return though the fields array
def getLeads(type, value, fields=[]):
    # defining a params dict for the parameters to be sent to the API.
    PARAMS = {'access_token': identity.getAccessToken(), 'filterType': type, 'filterValues': value, 'fields': fields}

    # sending get request
    data = requests.get(url=identity.baseRest + "/v1/leads.json", params=PARAMS).json()

    return data

# function to get leads by id. id is the id value. Pass parameters that we want to return though the fields array
def getLeadsById(id, fields=[]):
    return getLeads(fieldNames.id, id, fields)

# function to get leads by email. Email is the email value. Pass parameters that we want to return though the fields array
def getLeadsByEmail(email, fields=[]):
    return getLeads(fieldNames.email, email, fields)

# function to create a new lead. Default is to create or update lead, but can pass variable string to change action. Pass array of dictionaries in the input.
def createLead(type, input, action='createOrUpdate'):
    # defining a data json for the parameters to be sent to the API
    data = json.dumps({'action': action, 'lookupField': type, 'input': input})

    # sending post request.
    r = requests.post(url=identity.baseRest + "/v1/leads.json", headers={'Content-type': 'application/json', 'Authorization': 'Bearer ' + str(identity.getAccessToken())}, data=data).json()

    return r

# function to create new lead by id
def createLeadById(input, action='createOrUpdate'):
    return createLead(fieldNames.id, input, action)

# function to create new lead by email
def createLeadByEmail(input, action='createOrUpdate'):
    return createLead(fieldNames.email, input, action)

# function to delete a lead. Pass the id in the function.
def deleteLead(id):
    # defining a data json for the parameters to be sent to the API
    data = json.dumps({'input': [{fieldNames.id: id}]})

    # sending delete request
    r = requests.delete(url=identity.baseRest + "/v1/leads.json", headers={'Content-type': 'application/json', 'Authorization': 'Bearer ' + str(identity.getAccessToken())}, data=data).json()

    return r

# function to get the api names for the leads
def describe2Lead():
    # defining a params dict for the parameters to be sent to the API.
    PARAMS = {'access_token': identity.getAccessToken()}

    # sending get request
    data = requests.get(url=identity.baseRest + "/v1/leads/describe2.json", params=PARAMS).json()

    return data

# function to list all custom objects available. No parameters needed.
def listCustomObjects():
    # defining a params dict for the parameters to be sent to the API.
    PARAMS = {'access_token': identity.getAccessToken()}

    # sending get request
    data = requests.get(url=identity.baseRest + "/v1/customobjects.json", params=PARAMS).json()

    return data


# function to get custom objects. value is a list type containing the dedupe field values. Fields is optional but useful to specify which data you want to be returned. Usage: getCustomObjects('utm_c', [395944])
def getCustomObjects(apiName, value, fields=[]):
    # defining a params dict for the parameters to be sent to the API.
    PARAMS = {'access_token': identity.getAccessToken(), 'filterType': 'dedupeFields', 'filterValues': value, 'fields': fields}

    # sending get request
    data = requests.get(url=identity.baseRest + "/v1/customobjects/" + apiName + ".json", params=PARAMS).json()

    return data


# function to create/update custom object. Action field is optional. Usage: createCustomObjects('utm_c', [{'linker': 395944, 'data': 'test'}])
def createCustomObjects(apiName, input, action='createOrUpdate'):
    # defining a data json for the parameters to be sent to the API
    data = json.dumps({'action': action, 'dedupeBy': 'dedupeFields', 'input': input, 'seq': 2})

    # sending post request.
    r = requests.post(url=identity.baseRest + "/v1/customobjects/" + apiName + ".json", headers={'Content-type': 'application/json', 'Authorization': 'Bearer ' + str(identity.getAccessToken())}, data=data).json()


    return r

# function to delete custom objects. Input is an array of dictionaries which contain the dedupe field. Usage: deleteCustomObjects('utm_c', [{'linker': 395944}])
def deleteCustomObjects(apiName, input):
    # defining a data json for the parameters to be sent to the API
    data = json.dumps({'deleteBy': 'dedupeFields', 'input': input})

    # sending post request.
    r = requests.post(url=identity.baseRest + "/v1/customobjects/" + apiName + "/delete.json", headers={'Content-type': 'application/json', 'Authorization': 'Bearer ' + str(identity.getAccessToken())}, data=data).json()

    return r

# fields is a list of fields that we want to export. format can be: CSV, SSV, or TSV.
def createBulkExtractJob(fields, filter, format='CSV'):
    # defining a data json for the parameters to be sent to the API
    data = json.dumps({'fields': fields, 'format': format, 'filter': filter})

    # sending post request.
    r = requests.post(url=identity.baseBulk + "/v1/leads/export/create.json", headers={'Content-type': 'application/json', 'Authorization': 'Bearer ' + str(identity.getAccessToken())}, data=data).json()

    return r

# creates bulk extract job with static list id
def createBulkExtractJobStaticListId(fields, id, format='CSV'):
    return createBulkExtractJob(fields, {'staticListId': id}, format)

# creates bulk extract job with smart list id
def createBulkExtractJobSmartListId(fields, id, format='CSV'):
    return createBulkExtractJob(fields, {'smartListId': id}, format)

# creates bulk extract job with static list name
def createBulkExtractJobStaticListName(fields, name, format='CSV'):
    return createBulkExtractJob(fields, {'staticListName': name}, format)

# creates bulk extract job with smart list name
def createBulkExtractJobSmartListName(fields, name, format='CSV'):
    return createBulkExtractJob(fields, {'smartListName': name}, format)

# creates bulk extract job with lead creation date
def createBulkExtractJobSmartListCreatedAt(fields, startNdaysAgo, endNdaysAgo, format='CSV'):
    return createBulkExtractJob(fields, {'createdAt': {'startAt': formatTime.formattedDateNDaysAgo(startNdaysAgo), 'endAt': formatTime.formattedDateNDaysAgo(endNdaysAgo)}}, format)

# gets bulk extract jobs. status is a list of strings defining the progress
def getBulkExtractJobs(status=bulkStatusAll):
    # defining a params dict for the parameters to be sent to the API.
    PARAMS = {'access_token': identity.getAccessToken(), 'status': status}

    # sending get request
    data = requests.get(url=identity.baseBulk + "/v1/leads/export.json", params=PARAMS).json()

    return data

def startBulkExtractJob(exportId):
    # defining a data json for the parameters to be sent to the API
    data = json.dumps({})

    # sending post request.
    r = requests.post(url=identity.baseBulk + "/v1/leads/export/" + exportId + "/enqueue.json", headers={'Content-type': 'application/json', 'Authorization': 'Bearer ' + str(identity.getAccessToken())}, data=data).json()

    return r

def pollBulkExtractJob(exportId):
    # defining a params dict for the parameters to be sent to the API.
    PARAMS = {'access_token': identity.getAccessToken()}

    # sending get request
    data = requests.get(url=identity.baseBulk + "/v1/leads/export/" + exportId + "/status.json", params=PARAMS).json()

    return data

def retrieveBulkExtractData(exportId):
    # defining a params dict for the parameters to be sent to the API.
    PARAMS = {'access_token': identity.getAccessToken()}

    # sending get request. Doesn't return json as it returns csv which is parsed with .text
    data = requests.get(url=identity.baseBulk + "/v1/leads/export/" + exportId + "/file.json", params=PARAMS).text

    return data

def cancelBulkExtractJob(exportId):
    # defining a data json for the parameters to be sent to the API
    data = json.dumps({})

    # sending post request
    r = requests.post(url=identity.baseBulk + "/v1/leads/export/" + exportId + "/cancel.json", headers={'Content-type': 'application/json', 'Authorization': 'Bearer ' + str(identity.getAccessToken())}, data=data).json()

    return r

# this function doesn't work yet, use createLeadById/createLeadByEmail instead with the input list of 300 records max
def createBulkImportJob(file, partitionName=None, listId=None, format='csv', lookupField=fieldNames.id):

    # creates dictionary to pass with csv file to API call
    files = {'file': ('leads.' + format, file)}

    # defining a data json for the parameters to be sent to the API
    data = {'access_token': identity.getAccessToken(), 'format': format, 'lookupField': lookupField}

    #checks to add values to request if not none type
    if listId is not None:
        data['listId'] = listId

    if partitionName is not None:
        data['partitionName'] = partitionName

    # sending post request.
    r = requests.post(url=identity.baseBulk + "/v1/leads.json", files=files, data=data).json()

    return r

def pollBulkImportJob(batchId):
    # defining a params dict for the parameters to be sent to the API.
    PARAMS = {'access_token': identity.getAccessToken()}

    # sending get request
    data = requests.get(url=identity.baseBulk + "/v1/leads/batch/" + batchId + ".json", params=PARAMS).json()

    return data

def getBulkImportFailures(batchId):
    # defining a params dict for the parameters to be sent to the API.
    PARAMS = {'access_token': identity.getAccessToken()}

    # sending get request
    data = requests.get(url=identity.baseBulk + "/v1/leads/batch/" + batchId + "/failures.json", params=PARAMS).json()

    return data

def getBulkImportWarnings(batchId):
    # defining a params dict for the parameters to be sent to the API.
    PARAMS = {'access_token': identity.getAccessToken()}

    # sending get request
    data = requests.get(url=identity.baseBulk + "/v1/leads/batch/" + batchId + "/warnings.json", params=PARAMS).json()

    return data

def getStaticList(id):
    # defining a params dict for the parameters to be sent to the API.
    PARAMS = {'access_token': identity.getAccessToken()}

    # sending get request
    data = requests.get(url=identity.baseRest + "/asset/v1/staticList/{:d}.json".format(id), params=PARAMS).json()

    return data
