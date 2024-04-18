# BikePartPicker
College project coded from 1-24 to 3-24.

For this assignment, I was permitted to choose the objectives of my system. I chose to design a system which provides part selection and part pricing capabilities for bicycles. The requirements are as follows:
  - Users must log in to access the system. This is required so that part lists can be saved by the user.
  - Users can log in to an existing account and create an account.
  - The 'Builder' webpage permits users to add and delete parts from the selected part list.
  - All parts have pricing information retrieved using bs4 and checked for validity using Jaro-Winkler.
  - The 'My Part Lists' webpage permits users to create and delete part lists, as well as modify part list details.

Ensure Flask, pyodbc, openpyxl, requests and bs4 are installed.
Python, HTML, JS, CSS and Transact-SQL required to run the program.
Ensure all database tables have been created and test data has been inserted.
Modify the SQL connection string (ReadSpreadsheet.py, line 19 and Bike_Part_Picker_Functions.py, line 8).

Run Read_Spreadsheet.py to insert pricing data into the database table. This can be run multiple times, on different days, so that price changes can be recorded on the database.
Run Bike_Part_Picker_Main.py to run the program.

Note: Only test data for the categories 'Frameset', 'Frame', 'Fork', 'Stem', 'Handlebar' and 'Handlebar tape' is being inserted from the SQL file 'Create Tables.sql'.
