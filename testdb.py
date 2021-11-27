import sqlite3

# def deleteRecord():
#     try:
#         sqliteConnection = sqlite3.connect('db.sqlite3')
#         cursor = sqliteConnection.cursor()
#         print("Connected to SQLite")

#         # Deleting single record now
#         sql_delete_query = """DELETE from MedicalApp_billdetails"""
#         cursor.execute(sql_delete_query)
#         sqliteConnection.commit()
#         print("Record deleted successfully ")
#         cursor.close()

#     except sqlite3.Error as error:
#         print("Failed to delete record from sqlite table", error)
#     finally:
#         if sqliteConnection:
#             sqliteConnection.close()
#             print("the sqlite connection is closed")

# deleteRecord()


try:
    sqliteConnection = sqlite3.connect('db.sqlite3')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    # sqlite_insert_query = """INSERT INTO MedicalApp_customer
    #                       (name, address, contact, added_on) 
    #                        VALUES 
    #                       ('Thai','Nga 6','0238179834','2021-11-23 08:31:44.846726')"""
    # sqlite_insert_query = """INSERT INTO MedicalApp_bill
    #                       (added_on, customer_id_id) 
    #                        VALUES 
    #                       ('2021-11-23 08:31:44.846726','25')"""
    sqlite_insert_query = """INSERT INTO MedicalApp_billdetails
                          (qty, added_on, bill_id_id, medicine_id_id) 
                           VALUES 
                          ('4','2021-11-23 08:32:44.946726','25', '8')"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()
    print("Record inserted successfully into MedicalApp_customer table ", cursor.rowcount)
    cursor.close()

except sqlite3.Error as error:
    print("Failed to insert data into sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")