import pymongo
from pymongo import MongoClient
import getpass
import json
import netrc
import os

loop = 0
while True:

    def main_program():

        def get_credentials_from_netrc():
            netrc_path = ".netrc"  # Read from the current directory

            if not os.path.exists(netrc_path):
                print("\n[!] Error: .netrc file not found in the current directory.")
                return None, None, None

            host, username, password = None, None, None

            try:
                with open(netrc_path, "r") as file:
                    lines = file.readlines()

                for line in lines:
                    parts = line.strip().split(maxsplit=1)  # Split into key and value

                    if len(parts) < 2:
                        continue
                    key, value = parts[0].lower(), parts[1]

                    if key == "host":
                        host = value
                    elif key == "username":
                        username = value
                    elif key == "password":
                        password = value

                # Validate all required fields are found
                if not all([host, username, password]):
                    print("\n[!] Error: Missing required fields in .netrc file.")
                    return None, None, None

                return host, username, password

            except Exception as e:
                print(f"\n[!] Error reading .netrc file: {e}")
                return None, None, None

        def get_mongo_client():
            global host, username, password
            print("\nAuthentication Method:")
            print("\n1 - Enter username and password manually")
            print("2 - Use credentials from .netrc file")
            print("\n    Example of valid .netrc file format: ")
            print("\n      host 127.0.0.1")
            print("      username john")
            print("      password doe")
            auth_option = input("\nChoose an option (1/2): ")

            if auth_option == "1":
                host= input("\nMongoDB Host IP: ")
                username = input("\nMongoDB Username: ")
                password = getpass.getpass("MongoDB Password: ")
                print("\nAttempting to connect to: ")
                print(f"\nHost: {host}")
                print(f"Username: {username}")
                print(f"Password: ")
                print("\n Connecting to MongoDB with provided data...")
            elif auth_option == "2":
                credentials = get_credentials_from_netrc()
                if credentials is None:
                    return None
                host, username, password = credentials

            else:
                print("\n[!] Invalid option. Please try again.")
                return None

            try:
                client = MongoClient(host=host, username=username, password=password)
                client.admin.command("ping")
                print("\n[+] Authentication successful.")
                return client
            except Exception as e:
                print(f"\n[!] Authentication failed: {e}")
                input("\nPress enter to return to the main menu: ")
                mongodb_main_menu()

        def create_a_mongodb_database():
            client = get_mongo_client()
            if not client:
                return

            db_name = input("\nEnter new database name: ")
            db = client[db_name]

            try:
                db.command("ping")
                print(f"\n[+] Database '{db_name}' is ready.")
                print(
                    "\nIMPORTANT: In order to view the database in the available databases list, you MUST create a collection name for it. ")
            except Exception as e:
                print(f"\n[!] Error creating database '{db_name}': {e}")

            input("\nPress enter to return to the main menu: ")
            mongodb_main_menu()

        def create_a_mongo_db_collection():
            client = get_mongo_client()
            if not client:
                return

            db_name = input("\nEnter database name: ")
            db = client[db_name]

            collection_name = input("\nEnter new collection name: ")

            try:
                if collection_name not in db.list_collection_names():
                    db.create_collection(collection_name)
                    print(f"\n[+] Collection '{collection_name}' created successfully in database '{db_name}'.")
                else:
                    print(f"\n[!] Collection '{collection_name}' already exists in database '{db_name}'.")
            except Exception as e:
                print(f"\n[!] Error creating collection '{collection_name}': {e}")

            input("\nPress enter to return to the main menu: ")
            mongodb_main_menu()

        def delete_a_mongodb_database():
            client = get_mongo_client()
            if not client:
                return

            db_name = input("\nEnter the database name to delete: ")
            confirmation = input(f"\nAre you sure you want to delete the database '{db_name}'? (yes/no): ")

            if confirmation.lower() == "yes":
                client.drop_database(db_name)
                print(f"\n[+] Database '{db_name}' deleted successfully.")
            else:
                print("\n[-] Operation canceled.")

            input("\nPress enter to return to the main menu: ")

        def delete_a_mongo_db_collection():
            client = get_mongo_client()
            if not client:
                return

            db_name = input("\nEnter database name: ")
            db = client[db_name]

            collection_name = input("\nEnter collection name to delete: ")

            if collection_name in db.list_collection_names():
                confirmation = input(
                    f"\nAre you sure you want to delete the collection '{collection_name}'? (yes/no): ")
                if confirmation.lower() == "yes":
                    db[collection_name].drop()
                    print(f"\n[+] Collection '{collection_name}' deleted successfully from database '{db_name}'.")
                else:
                    print("\n[-] Operation canceled.")
            else:
                print(f"\n[-] Collection '{collection_name}' does not exist in database '{db_name}'.")

            input("\nPress enter to return to the main menu: ")

        def show_mongodb_databases():
            client = get_mongo_client()
            if not client:
                return

            try:
                databases = client.list_database_names()
                print("\nAvailable Databases:\n")
                for db in databases:
                    print(f" - {db}")
            except Exception as e:
                print(f"\n[!] Error retrieving databases: {e}")

            input("\nPress enter to return to the main menu: ")
            mongodb_main_menu()

        def connect_to_a_mongodb_database():
            global client, mydb, mycol, DATABASE_HOST, DATABASE_NAME, DATABASE_USERNAME, DATABASE_PASSWORD

            try:
                get_mongo_client()

                client = MongoClient(host=host, username=username, password=password)

                print("\nShowing Databases: " + str(client.list_database_names()))  # lists databases

                DATABASE_NAME=input("\nType the name of the database you want to connect to, and press enter: ")

                client = MongoClient(host=host, username=username, password=password, authSource=DATABASE_NAME)

                print("\n[+] Connected to Database "+DATABASE_NAME)

                global mydb
                mydb = client[DATABASE_NAME]

                def mongo_operations():
                    print("\n###############################################")
                    print("       MONGO DB OPERATIONS MENU CONSOLE\n")
                    print("\n THIS CONSOLE IS NOW OPERATING WITH DATABASE: "+DATABASE_NAME+"\n")
                    print("1 - Show Databases in connected session")
                    print("2 - Show Collections")
                    print("3 - View amount of Documents in a collection")
                    print("4 - Show Documents of a specific Collection")
                    print("5 - Find a record (key and value) in a specific collection")
                    print("6 - Insert a new record")
                    print("7 - Delete an existing record")
                    print("8 - Insert many records (json file)")
                    print("9 - Delete many records (json file)")
                    print("10 - Connect to a different database - Returns to main program\n")
                    print("11 - <--- Go back to main program\n")
                    options=input("Type a number for the menu and press enter: ")

                    if options == "1":
                        print("\nShowing Databases: "+str(client.list_database_names()))#lists databases
                        input("\nQuery executed. Press enter to get back to main menu...")
                        mongo_operations()

                    if options == "2":

                        print("\nShowing Collections in connected Database "+DATABASE_NAME+":\n")
                        for col in mydb.list_collection_names():
                            print(col)
                        input("\nQuery executed. Press enter to get back to main menu...")
                        mongo_operations()

                    if options == "3":

                        COLLECTION_NAME=input("\nType the name of a collection to view the amount of documents it has, and press enter: ")

                        for col in mydb.list_collection_names():
                            if COLLECTION_NAME in mydb.list_collection_names():

                                mycol = mydb[COLLECTION_NAME]

                                print("\n[+] Success: Collection name "+COLLECTION_NAME+ " in database "+DATABASE_NAME+" was found\n")
                                print(mycol.name, " - Amount of documnents :", mycol.count_documents({}))

                                input("\nQuery executed. Press enter to get back to main menu...")
                                mongo_operations()

                            else:
                                print("\nERROR!: No collection found by the name of "+COLLECTION_NAME)
                                input("\nPress enter to get back to main menu...")
                                mongo_operations()

                    if options == "4":

                        COLLECTION_NAME=input("\nType the name of a collection to view its documents, and press enter: ")

                        for col in mydb.list_collection_names():
                            if COLLECTION_NAME in mydb.list_collection_names():

                                mycol = mydb[COLLECTION_NAME]

                                print("\nShowing documents for collection "+COLLECTION_NAME+" in database "+DATABASE_NAME+":\n")
                                print(mycol.name, " - Amount of documnents :", mycol.count_documents({}))
                                print("\n")
                                mydoc = mycol.find()
                                for x in mydoc:
                                    print(x)

                                input("\nQuery executed. Press enter to get back to main menu...")
                                mongo_operations()

                            else:
                                print("\nERROR!: No collection found by the name of "+COLLECTION_NAME)
                                input("\nPress enter to get back to main menu...")
                                mongo_operations()

                    if options == "5":

                        def find_record():
                            COLLECTION_NAME=input("\nType the name of the collection in which you want to find a specific record: ")
                            for col in mydb.list_collection_names():
                                if COLLECTION_NAME in mydb.list_collection_names():
                                    mycol = mydb[COLLECTION_NAME]
                                    print("\n[+] Success: Collection name "+COLLECTION_NAME+ " in database "+DATABASE_NAME+" was found")
                                    key=input("\nType a key name and press enter: ")
                                    value=input("\nEnter a key value for the key "+'"'+key+'"'+" and press enter: ")
                                    record_to_find = { key : value }
                                    query_record = mycol.find(record_to_find)
                                    for record in query_record:
                                        print("\n")
                                        print(record)
                                    input("\nQuery executed. Press enter to get back to the menu console...")
                                    mongo_operations()

                                else:
                                    print("\nERROR: Unable to find the record in collection name "+COLLECTION_NAME+" in database "+DATABASE_NAME)
                                    input("\nPress enter to get back to the menu console...")
                                    mongo_operations()

                        find_record()

                    if options == "6":

                        try:
                            def insert_new_record():
                                COLLECTION_NAME=input("\nType the name of the collection in which you want to insert a new record, and press enter: ")
                                for col in mydb.list_collection_names():
                                    if COLLECTION_NAME in mydb.list_collection_names():
                                        mycol = mydb[COLLECTION_NAME]
                                        print("\n[+] Success: Collection name "+COLLECTION_NAME+ " in database "+DATABASE_NAME+" was found")
                                        def insert_record():
                                            try:

                                                key=input("\nType new key and press enter: ")
                                                value=input("\nEnter a value for the key: ")
                                                new_record = { key : value }
                                                new_record_value = mycol.insert_one(new_record)
                                                def insert_other():

                                                    other_record = input("\nInsert another record in collection "+COLLECTION_NAME+"?: y/n... ")
                                                    if other_record == "y":
                                                        insert_record()

                                                    if other_record == "n":
                                                        input("\nYou decided not to enter a new record. Press enter to get back to main console... ")
                                                        mongo_operations()

                                                    else:
                                                        print("\nOnly type either y or n and press enter.")
                                                        insert_other()

                                                insert_other()
                                            except:
                                                def retry_inserting():
                                                    retry_insert = input("\nTo retry providing json file press 'r', to get back to main menu, press 'm': ")
                                                    if retry_insert == "r":
                                                        insert_record()
                                                    if retry_insert == "m":
                                                        mongo_operations()
                                                    else:
                                                        print("\nOnly enter either r, or m please.")
                                                        retry_inserting()
                                                    retry_inserting()

                                        insert_record()

                                    else:
                                        print("\nERROR!: No collection found by the name of "+COLLECTION_NAME)
                                        input("\nPress enter to get back to the console menu...")
                                        mongo_operations()

                            insert_new_record()
                        except:
                            print("\nERROR: Unable to insert new record to collection "+COLLECTION_NAME+" in database "+DATABASE_NAME)
                            input("\nPress enter to get back to the menu console...")
                            mongo_operations()

                    if options == "7":

                        def delete_record():
                            COLLECTION_NAME=input("\nType the name of the collection for which you want to delete a record, and press enter: ")
                            for col in mydb.list_collection_names():
                                if COLLECTION_NAME in mydb.list_collection_names():
                                    mycol = mydb[COLLECTION_NAME]
                                    print("\n[+] Success: Collection name "+COLLECTION_NAME+ " in database "+DATABASE_NAME+" was found")
                                    def input_key_value():

                                        try:

                                            key=input("\nType an existing key name and press enter: ")
                                            value=input("\nEnter an existing value for "+'"'+key+'"'+" and press enter: ")
                                            delete_record = { key : value }
                                            def confirm_deletion():

                                                delete_or_not = input("\nConfirm you want to proceed with deletion: y/n... ")
                                                if delete_or_not == "y":
                                                    delete_record_value = mycol.delete_one(delete_record)
                                                    input("\nCommand executed. To validate that the record was deleted, the key and values provided must match in the collection. Press enter to get back to the operations menu, and check if it was deleted...")
                                                    mongo_operations()
                                                if delete_or_not == "n":
                                                    input("\nAborted record deletion, press enter to get back to main menu... ")
                                                    mongo_operations()

                                                else:
                                                    print("\nPlease only type either 'y' or 'n'.")
                                                    confirm_deletion()

                                            confirm_deletion()
                                        except:
                                            def retry_deleting():
                                                retry_deletion = input("\nTo retry providing json file press 'r', to get back to main menu, press 'm': ")
                                                if retry_deletion == "r":
                                                    input_key_value()
                                                if retry_deletion == "m":
                                                    mongo_operations()
                                                else:
                                                    print("\nOnly enter either r, or m please.")
                                                    retry_deleting()
                                            retry_deleting()

                                    input_key_value()

                                else:
                                    print("\nERROR!: No collection found by the name of "+COLLECTION_NAME)
                                    input("\nPress enter to get back to the menu console...")
                                    mongo_operations()

                        delete_record()

                    if options == "8":

                        def insert_many_records():
                            COLLECTION_NAME=input("\nType the name of the collection for which you want to insert multiple records, and press enter: ")
                            for col in mydb.list_collection_names():
                                if COLLECTION_NAME in mydb.list_collection_names():
                                    mycol = mydb[COLLECTION_NAME]
                                    print("\n[+] Success: Collection name "+COLLECTION_NAME+ " in database "+DATABASE_NAME+" was found")
                                    def json_file_data():

                                        json_data = input("\nProvide the data from a .json format file, specifying the full path to it and press enter: ")
                                        try:

                                            with open(json_data) as file:

                                                file_data = json.load(file)

                                            def insert_more_records():
                                                    continue_inserting = input("\nInsert more records in collection "+COLLECTION_NAME+"? y/n: ")
                                                    if continue_inserting == "y":
                                                        json_file_data()

                                                    if continue_inserting == "n":
                                                        input("\nYou decided not to insert more record in collection "+COLLECTION_NAME+" for now. Press enter to get back to main console... ")
                                                        mongo_operations()

                                                    else:
                                                        print("\nPlease only type either 'y' or 'n'.")
                                                        insert_more_records()

                                            if isinstance(file_data, list):
                                                mycol.insert_many(file_data)
                                                print("\n[+] Success: Inserted data in "+COLLECTION_NAME)
                                                insert_more_records()

                                            else:
                                                mycol.insert_one(file_data)
                                                print("\n[+] Success: Inserted data in "+COLLECTION_NAME)
                                                insert_more_records()
                                        except:
                                            print("\nERROR: Cannot insert provided data. Invalid format provided.")
                                            def retry_Insert():
                                                retry_insertion = input("\nTo retry providing json file press 'r', to get back to main menu, press 'm': ")
                                                if retry_insertion == "r":
                                                    json_file_data()
                                                if retry_insertion == "m":
                                                    mongo_operations()
                                                else:
                                                    print("\nOnly enter either r, or m please.")
                                                    retry_Insert()
                                            retry_Insert()


                                    json_file_data()

                                else:
                                    print("\nERROR!: No collection found by the name of "+COLLECTION_NAME)
                                    input("\nPress enter to get back to the menu console...")
                                    mongo_operations()

                        insert_many_records()

                    if options == "9":

                        def delete_many_records():
                            COLLECTION_NAME=input("\nType the name of the collection for which you want to delete multiple records, and press enter: ")
                            for col in mydb.list_collection_names():
                                if COLLECTION_NAME in mydb.list_collection_names():
                                    mycol = mydb[COLLECTION_NAME]
                                    print("\n[+] Success: Collection name "+COLLECTION_NAME+ " in database "+DATABASE_NAME+" was found")
                                    def data_key_and_value():

                                        delete_data = input("\nProvide the data from a .json format file, specifying the full path to it, and press enter: ")
                                        with open(delete_data) as file:
                                            file_data = json.load(file)
                                        def confirm_deletion():
                                            confirmation = input("\nDo you confirm the deletion of the provided data? y/n: ")
                                            if confirmation == "y":
                                                try:

                                                    mycol.delete_many(file_data)
                                                    print("\nOperation executed.")
                                                    def delete_more_records():
                                                        continue_deleting = input("\nDelete more records in collection "+COLLECTION_NAME+"? y/n: ")
                                                        if continue_deleting == "y":
                                                            data_key_and_value()

                                                        if continue_deleting == "n":
                                                            input("\nYou decided not to delete more record in collection "+COLLECTION_NAME+" for now. Press enter to get back to main console... ")
                                                            mongo_operations()

                                                        else:
                                                            print("\nPlease only type either 'y' or 'n'.")
                                                            delete_more_records()
                                                    delete_more_records()

                                                except:
                                                    print("\nERROR: Cannot delete provided data. Invalid format provided.")
                                                    def retry_delete():
                                                        retry_deletion = input("\nTo retry providing json file press 'r', to get back to main menu, press 'm': ")
                                                        if retry_deletion == "r":
                                                            data_key_and_value()
                                                        if retry_deletion == "m":
                                                            mongo_operations()
                                                        else:
                                                            print("\nOnly enter either r, or m please.")
                                                            retry_delete()
                                                    retry_delete()

                                            if confirmation == "n":
                                                input("\nYou decided not to delete the data provided. Press enter to get back to main console...")
                                                mongo_operations()
                                            else:
                                                print("\nPlease only type either y or n, and press enter")
                                                confirm_deletion()
                                        confirm_deletion()

                                    data_key_and_value()

                                else:
                                    print("\nERROR!: No collection found by the name of "+COLLECTION_NAME)
                                    input("\nPress enter to get back to the menu console...")
                                    mongo_operations()
                        delete_many_records()

                    if options == "10":
                        connect_to_a_mongodb_database()
                    if options == "11":
                        mongodb_main_menu()

                    else:
                        print("\nERROR!. Only type an option from the menu and press enter")
                        input("\nPress enter to get back to the menu console...")
                        mongo_operations()

                mongo_operations()


            except:
                print("\n[!] Database connection error!. Unable to connect to to database: "+DATABASE_NAME)
                input("\nNo valid Database with valid credentials matched. Press enter to be redirected to re-start the program... ")
                main_program()

        def mongodb_main_menu():

            print("\n###############################################")
            print("       MONGO DB MAIN OPERATIONS MENU CONSOLE\n")
            print("\n1 - Show available mongodb databases")
            print("2 - Create a new mongodb database")
            print("3 - Create a new collection in a mongodb database")
            print("4 - Delete a mongodb database")
            print("5 - Delete a collection in a mongodb database")
            print("6 - Connect to a mongodb database")
            options = input("\nType a number for the menu and press enter: ")

            if options == "1":
                show_mongodb_databases()
            elif options == "2":
                create_a_mongodb_database()
            elif options == "3":
                create_a_mongo_db_collection()
            elif options == "4":
                delete_a_mongodb_database()
            elif options == "5":
                delete_a_mongo_db_collection()
            elif options == "6":
                connect_to_a_mongodb_database()
            else:
                print("\nInvalid option, please try again.")
                mongodb_main_menu()

        mongodb_main_menu()

    main_program()