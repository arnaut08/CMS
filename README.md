# CMS
Credential Management System

Instructions to setup the application =>

1) Make a virtual environment to install all the required libraries. 
Command :- `virtualenv -p python3 venv`

2) Activate the environment.
Command :- `source venv/bin/activate`

3) Install the required libraries as mentioned in the **requirements.txt**.
Command :- `pip install -r requirements.txt`

4) Run the **tables.sql** file to create the tables in the database.


Instructions to run the application => 

1) Make sure the environment is activated and required libraries are installed.

2) Create **configurations.py** in the config directory. Use **sampleConfigurations.py** for the reference.

3) To run the application, use the following command :- 
`flask run`

4) The default host is localhost and the default port is 5000. To change the host and port, use the following command :-
`--host=HOST_NAME --port=PORT_NUMBER`
[*NOTE :- Use the aforementioned command together with the* `flask run`*command.*]