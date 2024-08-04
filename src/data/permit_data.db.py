# derived from https://github.com/yimbymelbourne/permit_analysis

import sqlite3
import csv
import os

csv_directory = os.path.join(os.getcwd(), "src/data/permit_csvs/")

# Connect to the SQLite database (create a new file if it doesn't exist)
conn = sqlite3.connect("permit_data.db")
c = conn.cursor()

create_table_query = """CREATE TABLE IF NOT EXISTS permit (
    pparsID	TEXT,
    planningScheme	TEXT,
    applicationType	TEXT,
    dateApplicationReceived	TEXT,
    dateOfRAOutcome	TEXT,
    dateOfFinalOutcome	TEXT,
    responsibleAuthorityOutcome	TEXT,
    finalOutcome	TEXT,
    applicationCategory	TEXT,
    currentLandUse	TEXT,
    proposedLandUse	TEXT,
    estimatedCostOfWorks	TEXT,
    fees	TEXT,
    submissions	INTEGER,
    publicNotice	TEXT,
    referralIssued	TEXT,
    furtherInformationRequested	TEXT,
    vicSmart	TEXT,
    sixtyDayTimeframe	TEXT,
    vicSmartTimeframe	TEXT,
    vcatGroundsForAppeal	TEXT,
    vcatLodgementDate	TEXT,
    vcatOutcomeDate	TEXT,
    vcatOutcome	TEXT,
    numberOfNewLots	INTEGER,
    numberOfNewDwellings INTEGER);
  """

# Create the table
c.execute(create_table_query)

# Function to load data from a CSV file into the table
def load_csv(file_path):
    with open(file_path, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        # Skip the header row
        next(csvreader)
        for row in csvreader:
            c.execute(
                f"INSERT INTO permit VALUES ({','.join(['?']*len(row))})",
                row,
            )


for filename in os.listdir(csv_directory):
    if filename.endswith(".csv"):
        file_path = os.path.join(csv_directory, filename)
        load_csv(file_path)

# Commit the changes and close the connection
conn.commit()

# now drop all columns except the one's were interested in from the database,
# so the generated db is a lot smaller and comes in under the 50MB Observable limit:
# finalOutcome
# numberOfNewDwellings
# estimatedCostOfWorks

c.execute(
    """
    CREATE TABLE permit_compressed AS
    SELECT finalOutcome, numberOfNewDwellings, estimatedCostOfWorks FROM permit
    """
)
# now force the deletion of the permit table such that permit_compress is the only table in the database
# and the data has been removed from the database
c.execute("DROP TABLE permit")

# VACUUM the database to reclaim free space
c.execute("VACUUM")

conn.commit()
conn.close()

# now output the created database to stdout so that Observable Framework can use it
with open("permit_data.db", "rb") as f:
    print(f.read(), end="")