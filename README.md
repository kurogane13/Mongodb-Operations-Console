# Mongodb-Operations-Console
Pymongo based CLI client, to run operations on existing databases and collections.

Program developed by Gustavo Wydler Azuaga 

Version 1 released in: 12-01-2021
--------------------------------------------------------------------------------------------
Version 2 released in: 02-17-2025
--------------------------------------------------------------------------------------------
NEW VERSION RELEASED: 3 - 02-18-2025
--------------------------------------------------------------------------------------------

NOTE: Program screenshots can be viewed in the Screenshots folder
--------------------------------------------------------------------------------------------


Program description: 

The program is a command line interface client developed in python, which uses the pymongo libraries to connect to existing databases, and run operations and queries. It is an interactive program based on numbered options.

--------------------------------------------------------------------------------------------

Version 2 and 3 includes:

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
  
Version 3 now includes:

- New creation and deletion features
	- Users in pymongo client (and mongo shell in linux)
	- Users in databases 
	- Mongodb databases
	- Collections in databases
	
- New permissions features

	- View user permissions
	- Grant user permissions
	- Revoke user permissions

--------------------------------------------------------------------------------------------


Requirements to operate the program:

- Mongo server running on localhost
- At least one Database created
- At least one collection created

- Tested with mongodb shell version:

  ```bash
  MongoDB shell version v3.6.8
  git version: 8e540c0b6db93ce994cc548f000900bdc740f80a
  OpenSSL version: OpenSSL 1.1.1f  31 Mar 2020
  allocator: tcmalloc
  modules: none
  build environment:
  distarch: x86_64
  target_arch: x86_64
  
  ```

--------------------------------------------------------------------------------------------

How to run the program:

- Download the python_mongo3.py file
- Install and import the following libraries:
  - import pymongo
  - from pymongo import MongoClient
  - import getpass
  - import json

- Run the program: python3.x python_mongo3.py




