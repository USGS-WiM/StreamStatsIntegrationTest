
### Abstract

In this report, we illustrate the process of developing an integration testing tool for <https://streamstats.usgs.gov/ss/> project. All materials are open source and available through GitHub <https://github.com/USGS-WiM/StreamStatsIntegrationTest> page. Integration testing involves testing the functionality of some of the tools included in the computation of main basin parameters in the background. Such as watershed delineation and basin characteristics.


### Tools & Libraries

This part of the code includes importing essential libraries that contained in the source folder and downloaded from the online repositories. The python version used is 2.7.14, and it comes with arcpy library pre-installed with ESRI product ArcGIS 10.6.
Each library contains a predefined set of functions in the form of template available for a user.

```python
#Integration testing for watershed deliniation
import traceback
import datetime
import time
import os
import argparse
import fnmatch
import json
from WIMLib import WiMLogging
from WIMLib import Shared
from WIMLib.Config import Config
from StreamStatsServiceAgent import StreamStatsServiceAgent
from threading import Thread
import time
import random
from Queue import Queue

```

### Methods

#### Main
This part of the code is responsible for running the IntegrationTest class object. Also, we utilize a set of multiple threads available from using processors with multiple cores. A configuration file is supplemented with source code that sets default parameters available to the user. 
The input file for the current function is a .csv comma separated file with state identifier, x and y coordinates and a unique identifier generated by a user. A user has to generate unique identifier only once to populate "clean room" with reference files. These files are assumed to be an accurate representation of data.
As we mentioned, current class invokes threads and initialize them with .put instance into waiting thread within a query. Each instance calls for an object of class ThreadWorker.

```python
class IntigrationTest(object):
    def __init__(self):
        self.maxThreads = 5
        try:
            self.config = Config(json.load(open(os.path.join(os.path.dirname(__file__),
            'config.json'))))
            self.workingDir = Shared.GetWorkspaceDirectory(
            self.config["workingdirectory"])
            
            parser = argparse.ArgumentParser()
            #Use the following LAT/LON pour point
            parser.add_argument("-file", help="specifies csv file location including gage lat/long and comid's to estimate", type=str, default = './InputCoordinates.csv') #Change to the location of the csv file
            parser.add_argument("-inputEPSG_Code", help="Default WGS 84 (4326),see http://spatialreference.org/ref/epsg/ ", type=int, default = '4326')
            args = parser.parse_args()
            if not os.path.isfile(args.file): raise Exception("File does not exist")

            refDir = {"bdel":self.config["referenceFolderBasinDel"],"bchar":self.config
            ["referenceFolderBasinChar"]}

            file = Shared.readCSVFile(args.file)
            headers = file[0]
            rcode = headers.index("State") if "State" in headers else 0
            x = headers.index("dec_long") if "dec_long" in headers else 1
            y = headers.index("dec_lat") if "dec_lat" in headers else 2
            uniqueID = headers.index("GageID") if "GageID" in headers else 3
            file.pop(0)#removes the header
            startTime = time.time()
            WiMLogging.init(os.path.join(self.workingDir,"Temp"),"Integration.log")
            
            self._sm("Starting routine")
            queue= Queue()
            
            for thrd in range(self.maxThreads):
                worker = ThreadWorker(queue)
                worker.start()

            for row in file:
                queue.put((row[rcode],row[x],row[y],refDir,row[uniqueID], 
                self.workingDir))
                
            self._sm('Finished.  Total time elapsed:', str(round((time.time()- startTime)/60, 2)), 'minutes')

        except:
            tb = traceback.format_exc()
            self._sm("Error executing delineation wrapper "+tb)


    def _sm(self,msg,type="INFO", errorID=0):        
        WiMLogging.sm(msg,type, errorID)

```
#### Threading

Following the process of initialization of ThreadWorker in the queue, a ThreadWorker class object sends a call to the server to get an output with corresponding getBasin and getBChar functions. Function getBasin returns coordinates of basin boundaries for x,y coordinates that were put into thread and function getBChar returns basins characteristics for the workspaceID extracted from previous basin delineation step. Simultaneously, N-number of threads call get functions and "sleep" in the queue waiting for the echo of matching id. When the thread "wakes up" the next step is a comparison with the existing file in a library or creating a new one if reference file does not exist.

```python
class ThreadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
    
    
    def run(self):
        try:            
            while True:
                rcode,x,y,refdir,id,workspace = self.queue.get()
                try:
                    self._run(rcode,x,y,refdir,id,workspace)
                except:
                    tb = traceback.format_exc()
                    WiMLogging.sm("Error w/ run "+ tb)
                finally:
                    self.queue.task_done()
            #next
        except:
            tb = traceback.format_exc()
            WiMLogging.sm("Error running "+tb)

    
    
    def _run(self,rcode, x,y, path,siteIdentifier,workingDir):   
        try:
            result = None
            
            with StreamStatsServiceAgent() as sa: 
                try:
                    response = sa.getBasin(rcode,x,y,4326) #Get feature collection
                    responseBChar = sa.getBChar(rcode,response['workspaceID'])
                    resultBChar = responseBChar['parameters']
                    result = response['featurecollection'][1]['feature']['features'][0]['geometry']['coordinates']
                except:
                    pass                
    
            if result == None: raise Exception("{0} Failed to return from service"
            .format(siteIdentifier))
            if resultBChar == None: raise Exception ("{0} Failed to return from service Bchar".format(siteIdentifier))
            self._compare(result, path.get("bdel"),siteIdentifier,workingDir)
            self._compare(resultBChar, path.get("bchar"),siteIdentifier,workingDir)
        except:
            tb = traceback.format_exc()
            WiMLogging.sm("Error w/ station "+ tb)
```

#### Writing JSON file's 
Current function is responsible for writing .json files and was available from existing GitHub repository <https://gist.github.com/keithweaver/ae3c96086d1c439a49896094b5a59ed0>. As an input, it requires a path to the location of the working directory, the name of the file and an input file containing data.
```python
def _writeToJSONFile(self,path, fileName, data):  #Define function to write as json object
    try:
        filePathNameWExt = os.path.join(path,fileName+".json")
        with open(filePathNameWExt, 'w') as fp:
            json.dump(data, fp)
    except:
        tb=traceback.format_exc()
        WiMLogging.sm("Error writing json output "+tb)
```

#### Comparing JSON file's
Lastly, a comparison of JSON files is implemented. It requires an input object generated from current run, the path to the location of "clean room", unique identifier that defined by a user and a path to the location of the working directory where logs are stored for the current session. Each run, a new folder is generated in the "Temp" folder that collects logs and outputs of comparison.
In the first run, function populates reference folders and assigns unique identifier as a file name to the corresponding JSON output. In the consecutive runs returned output from the main function compared to the existing reference file using a unique identifier. A comparison is performed line by line as for string in the text file. Outputs that were identified as different from reference folders are stored in the upper level of the working directory of a current "Temp" log file.

```python
def _compare(self,inputObj,path,ID, workingDir):
    try:  
        refObj = None
        refFile = os.path.join(path, ID+".json") #Get the reference json file from 
        #existing root folder
        if os.path.isfile(refFile):
            with open (refFile) as f:
                refObj = json.load(f)

            if inputObj!= refObj:
                WiMLogging.sm("Not equal Json's"+" "+ID)
                self._writeToJSONFile(workingDir,ID+"_"+str(path.rsplit('/', 1)[-1]), inputObj) #Store in log folder
            else:
                tb = traceback.format_exc()
                WiMLogging.sm("Equal Json's"+" "+ID+" "+ tb) #Don't create file
        else:
            #file not in reference folder, Create it
            WiMLogging.sm("file not in reference folder, Creating it"+" "+refFile)
            self._writeToJSONFile(path, ID,inputObj)
    except:
        tb=traceback.format_exc()
        WiMLogging.sm("Error Comparing "+tb)
        self._writeToJSONFile(workingDir, ID+"_viaError",{'error':tb})

    #Create function to compare basin char
if __name__ == '__main__':
    IntigrationTest()
```


---


#### Credits:
This report is written in R Markdown.Markdown is a simple formatting syntax for authoring HTML, PDF, and MS Word documents. For more details on using R Markdown see <http://rmarkdown.rstudio.com>.
