import pyodbc

drivers = pyodbc.drivers()

print("Available ODBC Drivers:")
if drivers:
    for driver in drivers:
        print(f" - {driver}")
else:
    print("No ODBC drivers found.")