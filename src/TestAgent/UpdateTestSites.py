#region "Imports"
import traceback
import json
from WIMLib.Config import Config
import os
import requests
import time
from  WIMLib.WiMLogging import WiMLogging
from WIMLib import Shared

#Open config file and define workspace
config = json.load(open(os.path.join(os.path.dirname(__file__), 'config.json')))
Config (config)

class testCase(object):
        #region Constructor
    def __init__(self):
        try:
            self.gitUrl = Config()["TestCase"]["gitUrl"]
        except:
            self.gitUrl = None

        #self._sm("initialized StreamStatsServiceAgent")
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.gitUrl=None
    
    def LoadJson (self, url = None):
        try:
            if self.gitUrl != None and url == None: 
                url = self.gitUrl
            elif self.gitUrl == None and url == None:
                url = "https://raw.githubusercontent.com/USGS-WiM/StreamStats-Setup/master/batchTester/testSites.geojson"
            #try:
            if (os.path.exists(url)):
                with open(url) as fp:
                    response = json.load(fp)
                    return [response, '']
            else: 
                response = requests.get(url)
                return [response.json(), response.headers]
            #except:
            #    self._sm("Error: file " + os.path.basename(url) + "doesn't exist", "ERROR")
            #    return ''
        except:
            tb = traceback.format_exc()
            self._sm("StreamstatsService getBChar Error "+tb, "ERROR")
            return json

    def saveJson(self, url, data):
        try:
            with open(url, "w") as fp:
                json.dump(data[0], fp)
        except:
            tb = traceback.format_exc()
            self._sm("StreamstatsService getBChar Error "+tb, "ERROR")
            
    def FindString (self, name, userdict):
        for i in userdict:
            if (i.get("Label") == name):
                return (i.get("Value"))
            else:
                None

    def updateValue (self, name, userdict, value):
        for i in userdict:
            if (i.get("Label") == name):
                i["Value"] = value

    def _sm(self,msg,type="INFO", errorID=0):        
        WiMLogging().sm(msg,type="INFO", errorID=0)
        
        
# set url to wherever you want the updated site list to end up
url = './testSites.geojson'

# you can send the url in LoadJson() if you have the testSites file downloaded locally and want to read and update it there
response =  (testCase().LoadJson())
result = response[0]["features"]
bcharpath = config["referenceFolderBasinChar"]



workingDir = Shared.GetWorkspaceDirectory (config["workingdirectory"]) #initialize and create logging folder w file
sumPath = os.path.join (workingDir, 'TestCase.txt')
fSummary = open (sumPath, 'w+')
for i in result:
    mismatch = {}
    try:
        siteid = int(i.get("properties").get("siteid"))
        rcode = i.get("properties").get("state")
        jsonpath = (bcharpath + "/" + str(siteid) + ".json")    
        
        bcharvalues = i.get("properties").get("testData")
    

        with open(jsonpath, 'r') as f:
            bchar = json.load(f)    
        for item in bchar:
            for j in item:
                if list (j.keys())[0] == "code":
                    varname = list(j.values())[0]
                    myval = testCase().FindString ( varname, bcharvalues)
                elif list (j.keys())[0] == "value":
                    if (myval is None):
                        # value doesn't exist in geojson, add here
                        newobject = {'Label': varname, 'Value': float(list(j.values())[0])}
                        bcharvalues.append(newobject)
                    else:          
                        if (float(myval) == float(list(j.values())[0])):
                            print ("")
                        else:
                            # here, update geojson using varname and myval
                            mismatch["Attribute"] = varname
                            mismatch['Reference'] = float(myval)
                            mismatch['Server'] = float (list(j.values())[0])
                            testCase().updateValue (varname, bcharvalues, float(list(j.values())[0]))
                else:
                    None
              
        fSummary.write ("Results for site: " + rcode + ', ' + str(siteid) + '\n')
        fSummary.write (str(mismatch) + '\n')

    except:
        fSummary.write ("Exception error site: " + rcode + ', ' + str(siteid) + '\n')
        None
fSummary.close ()
#save geojson file here
testCase().saveJson(url, response)
