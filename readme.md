![WiM](wimlogo.png)

# StreamStats Integration test

This project contains scripts used for computing StreamStats values for test sites and comparing to previous runs or values stored on GitHub.

### Purpose:
* testing that StreamStats functions work together properly
* supporting *temporal* accuracy of results.

### Method:

This script delineates various locations across the Contiguous United States and computes basin characteristics and flow statistics from the StreamStats REST API services. A list of values on GitHub also provides a means to check the outputs from a list of known values, and a script allows you to produce an updated list of known values to update on GitHub.

  If no data exists for a site in the BasinChar, BasinDel and FlowStats folders, new json files are added with that information.

  If data does exist for a site, subsequent runs are compared against those existing json files.
  
  Each cycle, a summary file is generated inside the StreamStatsIntegrationTest/Test folder. The summary file notifies you if (a) an output failed to come back, (b) an output succeeded and a new json was added, (c) if it compared the output with an existing file and it was an equal json or (d) if it compared the output with an existing file and there were differences. If (d), the differences will be displayed in the summary file.


### Core Functions:

There are 3 python scripts:
1. IntegrationWrapperV2.py
    
    a. This contains the main functionality to get the delination, basin chars and flow stats for each point and populate the BasinChar, BasinDel and FlowStats folders.
2. TestCaseGithub.py
    
    a. This file runs a quick comparison of the jsons in the BasinChar folder with the stored values [here](https://raw.githubusercontent.com/USGS-WiM/StreamStats-Setup/master/batchTester/testSites.geojson).
3. UpdateTestSites.py
   
    a. This file creates a new testSites.geojson you can copy to GitHub to update the geojson [here](https://raw.githubusercontent.com/USGS-WiM/StreamStats-Setup/master/batchTester/testSites.geojson).
    
    b. If your geojsons are not being read as jsons in VSCode, you can open the geojson file, click the button on the bottom right hand nav bar that says "Plain Text", select "Configure file association for .geojson", and select json. This will allow you to format geojson documents and view with the typical json coloring.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Installing
### Dependencies
[ python WIMLib package](https://pypi.org/project/WIMLib/): `pip install WIMLib`

### How to run
1. Make sure you are running right version of [python](https://www.python.org/downloads/) (3+)
2. Open /StreamStatsIntegrationTest/src/IntegrationWrapperV2.py in Python
    
    a. Note that you can also run this in an IDE such as Visual Studio Code.
3. Make sure all dependencies and modules are installed.
4. If you get an error stating "ModuleNotFoundError", make sure to add the folder path to the [sys](https://docs.python.org/3.7/library/sys.html) of Python 3.

```{python}
import sys
sys.path.append ('C:\\path\\to\\StreamStatsIntegrationTest\\src')
```

5. If you get an error finding the config.json file, setup a working directory as following, change line 25

```{python}
os.chdir ('D:\\Work\\Integration\\StreamStatsIntegrationTest\\src\\')
config = json.load(open('config.json'))
```

6. Run

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on the process for submitting pull requests to us. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details on adhering by the [USGS Code of Scientific Conduct](https://www2.usgs.gov/fsp/fsp_code_of_scientific_conduct.asp).

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](../../tags). 

Advance the version when adding features, fixing bugs or making minor enhancement. Follow semver principles. To add tag in git, type git tag v{major}.{minor}.{patch}. Example: git tag v2.0.5

To push tags to remote origin: `git push origin --tags`

*Note that your alias for the remote origin may differ.

## Authors

* **[Timur Sabitov](https://github.com/tim7en)**  - *Developer* - [USGS Maryland Water Science Center](https://www.usgs.gov/centers/md-de-dc-water)
* **[Katrin Jacobsen](https://www.usgs.gov/staff-profiles/katrin-jacobsen)**  - *Developer* - [USGS Web Informatics and Mapping](https://wim.usgs.gov)

See also the list of [contributors](../../graphs/contributors) who participated in this project.

## License

This project is licensed under the Creative Commons CC0 1.0 Universal License - see the [LICENSE.md](LICENSE.md) file for details

## Suggested Citation

In the spirit of open source, please cite any re-use of the source code stored in this repository. Below is the suggested citation:

`This project contains code produced by the Web Informatics and Mapping (WIM) team at the United States Geological Survey (USGS). As a work of the United States Government, this project is in the public domain within the United States. https://wim.usgs.gov`


## About WIM

* This project authored by the [USGS WIM team](https://wim.usgs.gov)
* WIM is a team of developers and technologists who build and manage tools, software, web services, and databases to support USGS science and other federal government cooperators.
* WiM is a part of the [Upper Midwest Water Science Center](https://www.usgs.gov/centers/wisconsin-water-science-center).
