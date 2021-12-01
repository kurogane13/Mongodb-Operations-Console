import pymongo
from pymongo import MongoClient
import getpass
import json

loop = 0
while True:

    def main_program():

        global client, mydb, mycol, DDATABASE_NAME, DATABASE_USERNAME, DATABASE_PASSWORD
        client = MongoClient()
        db = client.this_mongo
        print("\n################################################################")
        print("                ***  PYMONGO CUSTOM CLIENT ***                  \n")
        print("In order to start using the program, you will need to provide:\n")
        print("- A valid existing Mongo database")
        print("- Validate access to the database with username, and password")
        print("\n--------------------------------------------------------------------------------------")
        print("\nATTENTION: If no valid database, and credentials are provided, the connection will fail and you will be redirected to this prompt.\n")
        print("--------------------------------------------------------------------------------------")
        input("\nPress enter to start using the program: ")
        DATABASE_NAME = input("\nEnter the name of an existing Mongo database to connect to: ")
        DATABASE_HOST = "127.0.0.1"
        DATABASE_USERNAME = input("\nUsername for database "+DATABASE_NAME+"?: ")
        DATABASE_PASSWORD = getpass.getpass(prompt="\nPassword for database "+DATABASE_NAME+"?: ")

        try:
            client = MongoClient(DATABASE_HOST, username=DATABASE_USERNAME, password=DATABASE_PASSWORD, authSource=DATABASE_NAME)

            print("\nShowing Databases: "+str(client.list_database_names()))#lists databases

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
                    main_program()

                else:
                    print("\nERROR!. Only type an option from the menu and press enter")
                    mongo_operations()

            mongo_operations()


        except:
            print("\n[!] Database connection error!. Unable to connect to to database: "+DATABASE_NAME)
            input("\nNo valid Database with valid credentials matched. Press enter to be redirected to re-start the program... ")
            main_program()

    main_program()








