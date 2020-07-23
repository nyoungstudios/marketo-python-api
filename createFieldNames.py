import leads

# copy and paste this output into fieldNames.py so that you can access all your
# field names in your Marketo instance through code completion in your IDE

data = leads.describe2Lead()
firstLower = lambda s: s[:1].lower() + s[1:] if s else ''

allValues = set()

for apiNameList in data['result'][0]['fields']:
    apiName = apiNameList['name']
    apiName = apiName.strip()
    if apiName[-3:] == "__c":
        varName = apiName.replace("__c", "").replace("_", "").replace("-", "") + "c"
    else:
        varName = apiName.replace("_", "").replace("-", "")

    # lower camel case unless acronym
    if len(varName) > 1 and (varName[1].islower() or varName[1].isnumeric()):
        varName = firstLower(varName)

    # if there are duplicates
    if varName in allValues:
        varName += '2'
    allValues.add(varName)

    print(varName + " = " + "'" + apiName + "'")
