![WiM](wimlogo.png)

# StreamStats Integration test

StreamStats integration tests test the communication paths between different parts of the module to show that all modules/services are working correctly together.

### Purpose:
* testing that separately developed modules worked together properly
* test that a system of multiple modules worked as expected.
* supporting *temporal* accuracy of results.

### Method:

Script is accessing 44 reference sites from Contiguous United States and attributes from current streamstats REST API services. Reference sites contain information about sites basin characteristics, basin geometry information - defining basin area, and flow statistics. 

  Information returned from streamstats services, if is missing, in the local folders (BasinChar and BasinDel), are added.
  
  Following run returns from the rest api are compared against populated folders (BasinDel and BasinChar). 
  
  Each cycle a summary file generated inside of StreamStatsIntegrationTest/Test folder. If there any difference between outputs, it will display corresponding attribute and values from both files.


### Testing:

Information about reference sites can be obtained from [here](https://raw.githubusercontent.com/USGS-WiM/StreamStats-Setup/master/batchTester/testSites.geojson). 

To compare results from local with remote user can run StreamStatsIntegrationTest/src/TestAgent/TestCaseGithub.py script. 

To get a geojson to use to update the testSites on GitHub, run the StreamStatsIntegrationTest/src/TestAgent/UpdateTestSites.py script. This should then be used to update the geojson in the StreamStats-Setup repo. If your geojsons are not being read as jsons in VSCode, you can open the geojson file, click the button on the bottom right hand nav bar that says "Plain Text", select "Configure file association for .geojson", and select json. This will allow you to format geojson documents and view with the typical json coloring. 

Make sure to follow "How to Run" instructions same way as you would with main - IntegrationWrapperV2.py script. 

Results of test run are generated inside of the StreamStatsIntegrationTest/Test folder same way as in main run.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Installing
### Dependencies
[ python WIMLib package](https://pypi.org/project/WIMLib/): `pip install WIMLib`

### How to run
1. Make sure you are running right version of [python](https://www.python.org/downloads/) (3+)
2. Open /StreamStatsIntegrationTest/src/IntegrationWrapperV2.py in Python
3. Make sure all dependencies and modules are installed.
4. Change config.json from StreamStatsIntegrationTest/src folder to match path of your folders

Example:
```{python}
  "workingdirectory": "D:/Work/Integration/StreamStatsIntegrationTest/Test",
  "outputFile": "D:/Work/Integration/StreamStatsIntegrationTest/InputCoordinates.csv"
  ```
5. If error ModuleNotFoundError persists make sure to add folder path to the [sys](https://docs.python.org/3.7/library/sys.html) of Python 3.

```{python}
import sys
sys.path.append ('D:\\Work\\Integration\\StreamStatsIntegrationTest\\src')
```

6. If error finding config.json file persists - setup a working directory as following, change line 25

```{python}
os.chdir ('D:\\Work\\Integration\\StreamStatsIntegrationTest\\src\\')
config = json.load(open('config.json'))
```

7. Run

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on the process for submitting pull requests to us. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details on adhering by the [USGS Code of Scientific Conduct](https://www2.usgs.gov/fsp/fsp_code_of_scientific_conduct.asp).

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](../../tags). 

Advance the version when adding features, fixing bugs or making minor enhancement. Follow semver principles. To add tag in git, type git tag v{major}.{minor}.{patch}. Example: git tag v2.0.5

To push tags to remote origin: `git push origin --tags`

*Note that your alias for the remote origin may differ.

## Authors

* **[Jeremy Newson](https://www.usgs.gov/staff-profiles/jeremy-k-newson)**  - *Lead Developer* - [USGS Web Informatics & Mapping](https://wim.usgs.gov/)
* **[Timur Sabitov](https://github.com/tim7en)**  - *Developer* - [USGS Maryland Water Science Center](https://www.usgs.gov/centers/md-de-dc-water)

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
