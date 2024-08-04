import duckdb
import sys
import os

csv_directory = os.path.join(os.getcwd(), "src/data/permit_csvs")

# Connect to the DuckDB database (create a new file if it doesn't exist)
conn = duckdb.connect("permit_data_temp.duckdb")
c = conn.cursor()

create_table_query = """CREATE TABLE IF NOT EXISTS permit (
    pparsID TEXT,
    planningScheme TEXT,
    applicationType TEXT,
    dateApplicationReceived TEXT,
    dateOfRAOutcome TEXT,
    dateOfFinalOutcome TEXT,
    responsibleAuthorityOutcome TEXT,
    finalOutcome TEXT,
    applicationCategory TEXT,
    currentLandUse TEXT,
    proposedLandUse TEXT,
    estimatedCostOfWorks TEXT,
    fees TEXT,
    submissions INTEGER,
    publicNotice TEXT,
    referralIssued TEXT,
    furtherInformationRequested TEXT,
    vicSmart TEXT,
    sixtyDayTimeframe TEXT,
    vicSmartTimeframe TEXT,
    vcatGroundsForAppeal TEXT,
    vcatLodgementDate TEXT,
    vcatOutcomeDate TEXT,
    vcatOutcome TEXT,
    numberOfNewLots INTEGER,
    numberOfNewDwellings INTEGER
);
"""

# Create the table
c.execute(create_table_query)

# Function to load data from a CSV file into the table
def load_csv(file_path, table_name):
    # Read and format CSV file directly to DuckDB
    c.execute(f"COPY {table_name} FROM '{file_path}' (HEADER TRUE, DELIMITER ',');")


for filename in os.listdir(csv_directory):
    if filename.endswith(".csv"):
        file_path = os.path.join(csv_directory, filename)
        load_csv(file_path, "permit")

# Commit the changes (for DuckDB, this is done automatically)
conn.commit()
# Closing the connection
conn.close()

with open("permit_data_temp.duckdb", "rb") as db_file:
    sys.stdout.buffer.write(db_file.read())
    # now delete the file
    os.remove("permit_data_temp.duckdb")
