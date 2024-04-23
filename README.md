# IndividualProject

All data from the research can be found the in the ResultData directory.

Prerequisites to run the project ->

The commands executed in project are soecific to MacOS

Languages and versions 

JDK 1.8 https://docs.aws.amazon.com/corretto/latest/corretto-8-ug/downloads-list.html

JDK 11 https://docs.aws.amazon.com/corretto/latest/corretto-11-ug/downloads-list.html

You can check the versions install through this command `/usr/libexec/java_home -V`

Python3.5+ https://www.python.org/downloads/

You can check the versions install through this command `python3 --version`

To get started, clone the project using the address below. HTTPS and SSH has been provided

HTTPS 
command `git clone https://github.com/Nyall-Livett/IndividualProject.git`

SSH
command `git clone git@github.com:Nyall-Livett/IndividualProject.git`

Change to directory to the recently cloned project.

command `cd IndividualProject`


Create and activate python environment so the libraries needed to run the proeject can be installed.

command `python3 -m venv myenv`

command `source myenv/bin/activate`

Install the libraries.

command `pip install -r requirements.txt`

Create the directory to hold the projects in the research.

command `mkdir projects-used-for-data`

command `cd projects-used-for-data`

Add the sample project to directory.

HTTPS
command `git clone https://github.com/Nyall-Livett/Nyall-Livett-IndividualProject-sample.git`

SSH
command `git clone git@github.com:Nyall-Livett/Nyall-Livett-IndividualProject-sample.git`

Go back to root

command `cd ..`

Add Api key to ./Config.py

Create directory to hold the processed files.

command `mkdir processed_files`

Initiate Dataprocessing stage. This traverse the project, finds test class pairs.
Follow prompts on screen. I would advise not to say yes to starting training a model on the data. 

command `python3 DataProcessor.py`

Download Evosuite 1.20 standalone runtime jar from 
`https://github.com/EvoSuite/evosuite/releases/tag/v1.2.0`

Inside the directory where the Evosuite 1.20 standalone runtime jar file is, run this
command. This allows the runtime jar to be referenced inside the project where it is set as a dependency.

`mvn install:install-file -Dfile=./evosuite-standalone-runtime-1.2.0.jar -DgroupId=org.evosuite -DartifactId=evosuite-runtime -Dversion=1.2.0 -Dpackaging=jar`

Download Evosuite 1.20 jar

`https://github.com/EvoSuite/evosuite/releases/tag/v1.2.0`

and copy to the root of the project

Start generating and evalating the tests

command `python3 TestCaseGenerator.py`

This will create a CSV file class `results.csv` in root directory and will append the results from the generation
