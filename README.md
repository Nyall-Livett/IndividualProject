# IndividualProject

All data from the research can be found the in the ResultData directory.


Prerequisites to run the project ->

Must be on a Mac

download and install
JDK 1.8 https://docs.aws.amazon.com/corretto/latest/corretto-8-ug/downloads-list.html
JDK 11 https://docs.aws.amazon.com/corretto/latest/corretto-11-ug/downloads-list.html
Python3.5+ https://www.python.org/downloads/

command 'git clone https://github.com/Nyall-Livett/6CCS3PRJ'

command `cd 6CCS3PRJ`

Create and activate python environment where the libraries can be installed.

command `python3 -m venv myenv`
command `source myenv/bin/activate`

Install the libraries.
command `pip install -r requirements.txt`

command `cd projects-used-for-data`

command 'git clone https://github.com/Nyall-Livett/6CCS3PRJ-sample-project'

command 'cd ..'

Add Api key to ./Config.py

Initiate Dataprocessing stage. This traverse the project, finds test class pairs.
Follow prompts on screen.

command `python3 DataProcessor.py`

Start generating and evalating the tests

command `python3 TestCaseGenerator.py`

This will create a CSV file class `results.csv` in root directory and will append the results from the generation
