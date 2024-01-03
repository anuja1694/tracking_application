import shutil
import os
import datetime
import sqlite3

# Set the path to the database file
db_path = 'C:/Users/anuja/PycharmProjects/logisticstracking/tracking.db'
# Set the path to the backup directory
backup_dir = 'C:/Users/anuja/PycharmProjects/logisticstracking'
# Create the backup directory if it doesn't exist
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)
# Set the backup file name with timestamp
backup_file = backup_dir + 'backup_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + 'tracking.db'
# Connect to the database
conn = sqlite3.connect(db_path)

# Create a cursor object
cursor = conn.cursor()

# Make a copy of the database file
shutil.copyfile(db_path, backup_file)

# Close the database connection
conn.close()
