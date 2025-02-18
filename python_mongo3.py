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
            netrc_path = ".netrc_mongodb"  # Read from the current directory

            if not os.path.exists(netrc_path):
                print("\n[!] Error: .netrc_mongodb file not found in the current directory.")
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
                input("\nPress enter to return to the main menu: ")
                mongodb_main_menu()

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

            db_name = input("\nEnter database name to create a collection in it: ")
            db = client[db_name]

            collection_name = input("\nEnter new collection name for database "+db_name+": ")

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

            databases = list_mongodb_databases(client)
            if not databases:
                return

            while True:
                db_name = input("\nEnter the database name to delete (or type '0' to return): ").strip()
                if db_name == "0":
                    mongodb_main_menu()
                    return
                if db_name not in databases:
                    print("\n[!] Database not found. Try again.")
                    continue
                break

            confirmation = input(
                f"\nAre you sure you want to delete the database '{db_name}'? (yes/no): ").strip().lower()
            if confirmation == "yes":
                client.drop_database(db_name)
                print(f"\n[+] Database '{db_name}' deleted successfully.")
            else:
                print("\n[-] Operation canceled.")

            input("\nPress Enter to return to the main menu: ")
            mongodb_main_menu()

        def delete_a_mongo_db_collection():
            client = get_mongo_client()
            if not client:
                return

            databases = list_mongodb_databases(client)
            if not databases:
                return

            while True:
                db_name = input("\nEnter the database name (or type '0' to return): ").strip()
                if db_name == "0":
                    mongodb_main_menu()
                    return
                if db_name not in databases:
                    print("\n[!] Database not found. Try again.")
                    continue
                break

            db = client[db_name]
            collections = db.list_collection_names()

            if not collections:
                print(f"\n[-] No collections found in database '{db_name}'.")
                input("\nPress Enter to return to the main menu: ")
                mongodb_main_menu()
                return

            while True:
                collection_name = input("\nEnter the collection name to delete (or type '0' to return): ").strip()
                if collection_name == "0":
                    mongodb_main_menu()
                    return
                if collection_name not in collections:
                    print(f"\n[!] Collection '{collection_name}' not found in database '{db_name}'. Try again.")
                    continue
                break

            confirmation = input(
                f"\nAre you sure you want to delete the collection '{collection_name}'? (yes/no): ").strip().lower()
            if confirmation == "yes":
                db[collection_name].drop()
                print(f"\n[+] Collection '{collection_name}' deleted successfully from database '{db_name}'.")
            else:
                print("\n[-] Operation canceled.")

            input("\nPress Enter to return to the main menu: ")
            mongodb_main_menu()

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

        def list_mongodb_databases(client):
            try:
                databases = client.list_database_names()
                print("\nAvailable Databases:\n")
                for db in databases:
                    print(f"- {db}")
                return databases
            except Exception as e:
                print(f"\n[!] Error retrieving databases: {e}")
                return []

            input("\nPress enter to return to the main menu: ")
            mongodb_main_menu()

        import getpass

        def create_mongodb_user():
            client = get_mongo_client()
            if not client:
                return

            databases = list_mongodb_databases(client)
            if not databases:
                return

            while True:
                db_name = input(
                    "\nEnter the database name where the user will be created (or type '0' to return): ").strip()
                if db_name == "0":
                    mongodb_main_menu()
                    return
                if db_name not in databases:
                    print("\n[!] Database not found. Try again.")
                    continue
                break

            db = client[db_name]

            # Retrieve the currently authenticated user
            try:
                connection_status = client.admin.command("connectionStatus")
                auth_info = connection_status.get("authInfo", {})
                authenticated_users = auth_info.get("authenticatedUsers", [])

                if not authenticated_users:
                    print("\n[!] No authenticated users found. Make sure you are logged in with admin credentials.")
                    return

                admin_user = authenticated_users[0].get("user")
                if not admin_user:
                    print("\n[!] Unable to determine the authenticated user.")
                    return
            except Exception as e:
                print(f"\n[!] Error retrieving the authenticated user: {e}")
                return

            # Check if the current user has privileges to create users
            try:
                user_info = client.admin.command("usersInfo", admin_user)
                user_roles = user_info.get("users", [{}])[0].get("roles", [])

                # Extract roles that grant user creation rights
                admin_privileges = [
                    role for role in user_roles if
                    (role["db"] == db_name and role["role"] in ["dbOwner", "userAdmin"]) or
                    (role["db"] == "admin" and role["role"] == "userAdminAnyDatabase")
                ]

                if not admin_privileges:
                    print("\n[!] You do not have sufficient privileges to create users in this database.")
                    input("\nPress Enter to return to the main menu: ")
                    mongodb_main_menu()
                    return
            except Exception as e:
                print(f"\n[!] Error checking user privileges: {e}")
                return

            while True:
                new_username = input("\nEnter the new username (or type '0' to return): ").strip()
                if new_username == "0":
                    mongodb_main_menu()
                    return
                if new_username:
                    break

            while True:
                new_password = getpass.getpass(
                    "\nEnter the password for the new user (or type '0' to return): ").strip()
                if new_password == "0":
                    mongodb_main_menu()
                    return
                if new_password:
                    break

            print("\nChoose a role for the new user:\n")
            print("[1] Read-only")
            print("[2] Read-Write")
            print("[3] Database Owner")
            print("[0] Return to main menu")

            while True:
                role_choice = input("\nEnter your choice (1/2/3/0): ").strip()
                if role_choice == "0":
                    mongodb_main_menu()
                    return
                if role_choice in ["1", "2", "3"]:
                    break

            role_mapping = {
                "1": "read",
                "2": "readWrite",
                "3": "dbOwner"
            }
            role = role_mapping[role_choice]

            try:
                db.command("createUser", new_username, pwd=new_password, roles=[{"role": role, "db": db_name}])
                print(f"\n[+] User '{new_username}' created successfully with '{role}' role in database '{db_name}'.")
            except Exception as e:
                print(f"\n[!] Error creating user: {e}")

            input("\nPress Enter to return to the main menu: ")
            mongodb_main_menu()

        def delete_mongodb_user():
            client = get_mongo_client()
            if not client:
                return

            databases = list_mongodb_databases(client)
            if not databases:
                return

            while True:
                db_name = input(
                    "\nEnter the database name where the user will be deleted (or type '0' to return): ").strip()
                if db_name == "0":
                    mongodb_main_menu()
                    return
                if db_name not in databases:
                    print("\n[!] Database not found. Try again.")
                    continue
                break

            db = client[db_name]

            # Retrieve the currently authenticated user
            try:
                connection_status = client.admin.command("connectionStatus")
                auth_info = connection_status.get("authInfo", {})
                authenticated_users = auth_info.get("authenticatedUsers", [])

                if not authenticated_users:
                    print("\n[!] No authenticated users found. Make sure you are logged in with admin credentials.")
                    return

                admin_user = authenticated_users[0].get("user")
                if not admin_user:
                    print("\n[!] Unable to determine the authenticated user.")
                    return
            except Exception as e:
                print(f"\n[!] Error retrieving the authenticated user: {e}")
                return

            # Check if the current user has privileges to delete users
            try:
                user_info = client.admin.command("usersInfo", admin_user)
                user_roles = user_info.get("users", [{}])[0].get("roles", [])

                # Extract roles that grant user deletion rights
                admin_privileges = [
                    role for role in user_roles if
                    (role["db"] == db_name and role["role"] in ["dbOwner", "userAdmin"]) or
                    (role["db"] == "admin" and role["role"] == "userAdminAnyDatabase")
                ]

                if not admin_privileges:
                    print("\n[!] You do not have sufficient privileges to delete users in this database.")
                    input("\nPress Enter to return to the main menu: ")
                    mongodb_main_menu()
                    return
            except Exception as e:
                print(f"\n[!] Error checking user privileges: {e}")
                return

            users = db.command("usersInfo")["users"]
            if not users:
                print(f"\n[!] No users found in database '{db_name}'.")
                input("\nPress Enter to return to the main menu: ")
                mongodb_main_menu()
                return

            print("\nAvailable Users in Database: "+db_name+"\n")
            for user in users:
                print(f"- {user['user']}")

            while True:
                user_to_delete = input("\nEnter the username to delete from database: "+db_name+" (or type '0' to return): ").strip()
                if user_to_delete == "0":
                    mongodb_main_menu()
                    return
                if user_to_delete in [u["user"] for u in users]:
                    break
                print("\n[!] Invalid username. Try again.")

            try:
                db.command("dropUser", user_to_delete)
                print(f"\n[+] User '{user_to_delete}' deleted successfully from database '{db_name}'.")
            except Exception as e:
                print(f"\n[!] Error deleting user: {e}")

            input("\nPress Enter to return to the main menu: ")
            mongodb_main_menu()

        def show_user_permissions():
            client = get_mongo_client()

            if not client:  # Ensure we received a valid client connection
                return

            databases = list_mongodb_databases(client)
            if not databases:
                return

            db_name = input("\nEnter the database to check permissions: ").strip()
            if db_name not in databases:
                print("\n[!] Database not found.")
                return

            try:
                db = client[db_name]

                # Retrieve authenticated username from MongoDB session
                user_info = db.command("connectionStatus")
                username = user_info.get("authInfo", {}).get("authenticatedUsers", [{}])[0].get("user")

                if not username:
                    print("\n[!] No authenticated user found.")
                    return

                user_info = db.command("usersInfo", username)

                if "users" in user_info and user_info["users"]:
                    roles = user_info["users"][0].get("roles", [])
                    print(f"\nPermissions for {username} on {db_name}:\n")
                    for role in roles:
                        print(f"- Role: {role['role']}, Database: {role['db']}")
                else:
                    print("\n[!] No specific permissions found for this user in database: "+db_name)

            except Exception as e:
                print(f"\n[!] Error retrieving user permissions: {e}")

            input("\nPress enter to return to the main menu: ")
            mongodb_main_menu()

        def create_mongo_client_user():
            client = get_mongo_client()
            if not client:
                return

            admin_db = client["admin"]

            # Retrieve the currently authenticated user
            try:
                connection_status = client.admin.command("connectionStatus")
                auth_info = connection_status.get("authInfo", {})
                authenticated_users = auth_info.get("authenticatedUsers", [])

                if not authenticated_users:
                    print("\n[!] No authenticated users found. Make sure you are logged in with admin credentials.")
                    return

                admin_user = authenticated_users[0].get("user")
                if not admin_user:
                    print("\n[!] Unable to determine the authenticated user.")
                    return
            except Exception as e:
                print(f"\n[!] Error retrieving the authenticated user: {e}")
                return

            # Check if the current user has admin privileges
            try:
                user_info = client.admin.command("usersInfo", admin_user)
                user_roles = user_info.get("users", [{}])[0].get("roles", [])

                admin_privileges = [
                    role for role in user_roles if
                    role["db"] == "admin" and role["role"] in ["root", "userAdminAnyDatabase"]
                ]

                if not admin_privileges:
                    print("\n[!] You do not have sufficient privileges to create client users.")
                    input("\nPress Enter to return to the main menu: ")
                    mongodb_main_menu()
                    return
            except Exception as e:
                print(f"\n[!] Error checking user privileges: {e}")
                return

            while True:
                new_username = input("\nEnter the new client username (or type '0' to return): ").strip()
                if new_username == "0":
                    mongodb_main_menu()
                    return
                if new_username:
                    break

            while True:
                new_password = getpass.getpass(
                    "\nEnter the password for the new user (or type '0' to return): ").strip()
                if new_password == "0":
                    mongodb_main_menu()
                    return
                if new_password:
                    break

            print("\nChoose a role for the new client user:\n")
            print("[1] Read-only access to all databases")
            print("[2] Read-Write access to all databases")
            print("[3] Admin (can manage users & databases)")
            print("[0] Return to main menu")

            while True:
                role_choice = input("\nEnter your choice (1/2/3/0): ").strip()
                if role_choice == "0":
                    mongodb_main_menu()
                    return
                if role_choice in ["1", "2", "3"]:
                    break

            role_mapping = {
                "1": "readAnyDatabase",
                "2": "readWriteAnyDatabase",
                "3": "userAdminAnyDatabase"
            }
            role = role_mapping[role_choice]

            try:
                admin_db.command("createUser", new_username, pwd=new_password, roles=[{"role": role, "db": "admin"}])
                print(
                    f"\n[+] User '{new_username}' created successfully with '{role}' role at the MongoDB client level.")
            except Exception as e:
                print(f"\n[!] Error creating client user: {e}")

            input("\nPress Enter to return to the main menu: ")
            mongodb_main_menu()

        def delete_mongo_client_user():
            client = get_mongo_client()
            if not client:
                return

            admin_db = client["admin"]

            # Retrieve the currently authenticated user
            try:
                connection_status = client.admin.command("connectionStatus")
                auth_info = connection_status.get("authInfo", {})
                authenticated_users = auth_info.get("authenticatedUsers", [])

                if not authenticated_users:
                    print("\n[!] No authenticated users found. Make sure you are logged in with admin credentials.")
                    return

                admin_user = authenticated_users[0].get("user")
                if not admin_user:
                    print("\n[!] Unable to determine the authenticated user.")
                    return
            except Exception as e:
                print(f"\n[!] Error retrieving the authenticated user: {e}")
                return

            # Check if the current user has admin privileges
            try:
                user_info = client.admin.command("usersInfo", admin_user)
                user_roles = user_info.get("users", [{}])[0].get("roles", [])

                admin_privileges = [
                    role for role in user_roles if
                    role["db"] == "admin" and role["role"] in ["root", "userAdminAnyDatabase"]
                ]

                if not admin_privileges:
                    print("\n[!] You do not have sufficient privileges to delete client users.")
                    input("\nPress Enter to return to the main menu: ")
                    mongodb_main_menu()
                    return
            except Exception as e:
                print(f"\n[!] Error checking user privileges: {e}")
                return

            existing_users = []
            try:
                users_info = admin_db.command("usersInfo")
                existing_users = [user["user"] for user in users_info.get("users", [])]
            except Exception as e:
                print(f"\n[!] Error retrieving user list: {e}")
                return

            if not existing_users:
                print("\n[!] No users found in the MongoDB client.")
                input("\nPress Enter to return to the main menu: ")
                mongodb_main_menu()
                return

            print("\nExisting MongoDB Client Users:\n")
            for user in existing_users:
                print(f" - {user}")

            while True:
                username_to_delete = input("\nEnter the username to delete (or type '0' to return): ").strip()
                if username_to_delete == "0":
                    mongodb_main_menu()
                    return
                if username_to_delete in existing_users:
                    break
                print("\n[!] User not found. Try again.")

            try:
                admin_db.command("dropUser", username_to_delete)
                print(f"\n[+] User '{username_to_delete}' has been successfully deleted from the MongoDB client.")
            except Exception as e:
                print(f"\n[!] Error deleting user: {e}")

            input("\nPress Enter to return to the main menu: ")
            mongodb_main_menu()

        def grant_user_privileges():
            client = get_mongo_client()  # Get MongoDB client

            if not client:
                return

            databases = list_mongodb_databases(client)
            if not databases:
                return

            while True:
                db_name = input("\nEnter the database to grant privileges (or type '0' to return): ").strip()
                if db_name == "0":
                    mongodb_main_menu()
                    return
                if db_name not in databases:
                    print("\n[!] Database not found. Try again.")
                    continue
                break

            print("\nChoose privilege to grant:\n")
            print("1 - Read")
            print("2 - Read & Write")
            print("3 - Delete")
            print("4 - Database Owner")
            print("0 - Return to main menu")

            while True:
                choice = input("\nSelect an option (0-4): \n").strip()
                if choice == "0":
                    mongodb_main_menu()
                    return
                role_map = {
                    "1": "read",
                    "2": "readWrite",
                    "3": "dbAdmin",
                    "4": "dbOwner"
                }
                if choice not in role_map:
                    print("\n[!] Invalid option. Try again.")
                    continue
                role = role_map[choice]
                break

            try:
                db = client[db_name]

                # Retrieve authenticated username dynamically
                user_info = db.command("connectionStatus")
                username = user_info.get("authInfo", {}).get("authenticatedUsers", [{}])[0].get("user")

                if not username:
                    print("\n[!] No authenticated user found.")
                    return

                db.command("grantRolesToUser", username, roles=[{"role": role, "db": db_name}])
                print(f"\n[+] Granted '{role}' role to {username} on {db_name}.")

            except Exception as e:
                print(f"\n[!] Error granting privilege: {e}")

            mongodb_main_menu()  # Return to main menu after operation

        def revoke_user_privileges():
            client = get_mongo_client()  # Get MongoDB client

            if not client:
                return

            databases = list_mongodb_databases(client)
            if not databases:
                return

            while True:
                db_name = input("\nEnter the database to revoke privileges from (or type '0' to return): \n").strip()
                if db_name == "0":
                    mongodb_main_menu()
                    return
                if db_name not in databases:
                    print("\n[!] Database not found. Try again.")
                    continue
                break

            try:
                db = client[db_name]

                # Retrieve authenticated username dynamically
                user_info = db.command("connectionStatus")
                username = user_info.get("authInfo", {}).get("authenticatedUsers", [{}])[0].get("user")

                if not username:
                    print("\n[!] No authenticated user found.")
                    return

                user_info = db.command("usersInfo", username)

                if "users" in user_info and user_info["users"]:
                    roles = user_info["users"][0].get("roles", [])
                    if not roles:
                        print("\n[!] No roles assigned to this user.")
                        return

                    print("\nUser currently has the following roles:\n")
                    for idx, role in enumerate(roles, start=1):
                        print(f"{idx} - {role['role']} (DB: {role['db']})")
                    print("0 - Return to main menu")

                    while True:
                        choice = input("\nSelect the role number to revoke (or type '0' to return): ").strip()
                        if choice == "0":
                            mongodb_main_menu()
                            return
                        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(roles):
                            print("\n[!] Invalid selection. Try again.")
                            continue
                        role_to_remove = roles[int(choice) - 1]
                        break

                    db.command("revokeRolesFromUser", username, roles=[role_to_remove])
                    print(f"\n[+] Revoked '{role_to_remove['role']}' role from {username} on {db_name}.")

                else:
                    print("\n[!] No specific roles found for this user.")

            except Exception as e:
                print(f"\n[!] Error revoking privilege: {e}")

            input("\nPress enter to return to the main menu: ")
            mongodb_main_menu()  # Return to main menu after operation

        def connect_to_a_mongodb_database():
            global client, mydb, mycol, DATABASE_HOST, DATABASE_NAME, DATABASE_USERNAME, DATABASE_PASSWORD

            try:
                get_mongo_client()

                client = MongoClient(host=host, username=username, password=password)

                print("\nShowing Databases: " + str(client.list_database_names()))  # lists databases

                print("\nIMPORTANT!: CONNECTING TO THE CLIENT AND/OR A DATABASE, DOES NOT GUARANTEE ACCESS TO ALL OPERATIONS IN THE MENU.")
                print("VALIDATE THE USER PERMISSIONS FIRST, OR CONNECT WITH AN ADMIN USER TO HAVE FULL PRIVILIGES")

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
            print("2 - Connect to a mongodb database")
            print("--------------------------------------------------")
            print("\nCREATE OPERATIONS\n")
            print("3 - Create a new mongodb database")
            print("4 - Create a new collection in a mongodb database")
            print("--------------------------------------------------")
            print("\nDELETE OPERATIONS\n")
            print("5 - Delete a mongodb database")
            print("6 - Delete a collection in a mongodb database")
            print("--------------------------------------------------")
            print("\nUSER PERMISSION OPERATIONS\n")
            print("7-  View user permissions for a database")
            print("8-  Grant user permissions for a database")
            print("9-  Revoke user permissions for a database")
            print("--------------------------------------------------")
            print("\nUSER CREATION AND DELETION OPERATIONS\n")
            print("10 - Create a new mongoclient admin user")
            print("11 - Delete an admin mongoclient user")
            print("12 - Create a new user in a mongodb database")
            print("13 - Delete an existing user from a mongodb database")
            print("--------------------------------------------------")
            print("\nIMPORTANT!: CONNECTING TO THE CLIENT AND/OR A DATABASE, DOES NOT GUARANTEE ACCESS TO ALL OPERATIONS IN THE MENU.")
            print("VALIDATE THE USER PERMISSIONS FIRST, OR CONNECT WITH AN ADMIN USER TO HAVE FULL PRIVILIGES")
            options = input("\nType a number for the menu and press enter: ")

            if options == "1":
                show_mongodb_databases()
            elif options == "2":
                connect_to_a_mongodb_database()
            elif options == "3":
                create_a_mongodb_database()
            elif options == "4":
                create_a_mongo_db_collection()
            elif options == "5":
                delete_a_mongodb_database()
            elif options == "6":
                delete_a_mongo_db_collection()
            elif options == "7":
                show_user_permissions()
            elif options == "8":
                grant_user_privileges()
            elif options == "9":
                revoke_user_privileges()
            elif options == "10":
                create_mongo_client_user()
            elif options == "11":
                delete_mongo_client_user()
            elif options == "12":
                create_mongodb_user()
            elif options == "13":
                delete_mongodb_user()

            else:
                print("\nInvalid option, please try again.")
                mongodb_main_menu()

        mongodb_main_menu()

    main_program()