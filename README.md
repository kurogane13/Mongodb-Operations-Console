# Mongodb-Operations-Console
Pymongo based CLI client, to run operation on existing databases and collections

Program developed by Gustavo Wydler Azuaga - 12-01-2021
--------------------------------------------------------------------------------------------
NEW VERSION RELEASED: 3 - 02-17-2025
--------------------------------------------------------------------------------------------

NOTE: Program screenshots can be viewed in the Screenshots folder
--------------------------------------------------------------------------------------------


Program description: 

The program is a command line interface client developed in python, which uses the pymongo libraries to connect to existing databases, and run operations and queries. It is an interactive program based on numbered options.

--------------------------------------------------------------------------------------------

Version 3 includes:

- Manual login option. The user manually provides:
  
  - Host ip
  - username
  - password

- Automatic database login option via netrc file, validating credentials.
  ```bash
  #Provide credentials in the following format example
     
  host 127.0.0.1
  username john
  password doe
  
  ```
- Creation and deletion of mongodb databases
- Creation and deletion of mongodb collections in databases

--------------------------------------------------------------------------------------------


Requirements to operate the program:

- Mongo server running on localhost
- At least one Database created
- At least one collection created

--------------------------------------------------------------------------------------------

How to run the program:

- Download the python_mongo3.py file
- Install and import the following libraries:
  - import pymongo
  - from pymongo import MongoClient
  - import getpass
  - import json

- Run the program: python3.x python_mongo3.py




