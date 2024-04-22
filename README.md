# IndividualProject

All data from the research can be found the in the ResultData directory.

Prerequisites to run the project ->

Must be on a Mac

download and install

JDK 1.8 https://docs.aws.amazon.com/corretto/latest/corretto-8-ug/downloads-list.html

JDK 11 https://docs.aws.amazon.com/corretto/latest/corretto-11-ug/downloads-list.html

You can check the versions install through this command `/usr/libexec/java_home -V`

Python3.5+ https://www.python.org/downloads/

command `git clone https://github.com/Nyall-Livett/IndividualProject.git`

or

command `git clone git@github.com:Nyall-Livett/IndividualProject.git`

command `cd IndividualProject`

Create and activate python environment where the libraries can be installed.

command `python3 -m venv myenv`

command `source myenv/bin/activate`

Install the libraries.

command `pip install -r requirements.txt`

Create the directory to hold the projects in the research

command `mkdir projects-used-for-data`

command `cd projects-used-for-data`

Add project to directory

command `git clone https://github.com/Nyall-Livett/Nyall-Livett-IndividualProject-sample.git`

or 

command `git clone git@github.com:Nyall-Livett/Nyall-Livett-IndividualProject-sample.git`

Go back to root

command `cd ..`

Add Api key to ./Config.py

Create directory to hold the processed files

command `mkdir processed_files`

Initiate Dataprocessing stage. This traverse the project, finds test class pairs.
Follow prompts on screen. I would advise not to say yes to starting training a model on the data. 

command `python3 DataProcessor.py`

Download Evosuite 1.20 standalone runtime jar from 
`https://github.com/EvoSuite/evosuite/releases/tag/v1.2.0`

Inside the directory where the Evosuite 1.20 standalone runtime jar file is, run this
command `mvn install:install-file -Dfile=./evosuite-standalone-runtime-1.2.0.jar -DgroupId=org.evosuite -DartifactId=evosuite-runtime -Dversion=1.2.0 -Dpackaging=jar`

Download Evosuite 1.20 jar

`https://github.com/EvoSuite/evosuite/releases/tag/v1.2.0`

and copy to the root of the project

Start generating and evalating the tests

command `python3 TestCaseGenerator.py`

This will create a CSV file class `results.csv` in root directory and will append the results from the generation
