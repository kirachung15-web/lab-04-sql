"""Read, clean, and upload mock CSV data to MySQL."""

import logging
import os

import mysql.connector
import pandas as pd


# Configure logging so the script reports its progress.
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


def read_data(filename):
    """Read a CSV file and return it as a pandas DataFrame."""
    logging.info("Reading data from %s", filename)
    data = pd.read_csv(filename)
    logging.info("Read %d rows", len(data))
    return data


def clean_data(data):
    """Remove rows containing missing values and return cleaned data."""
    logging.info("Cleaning data")

    # Remove any row that contains a missing value.
    cleaned_data = data.dropna().copy()

    logging.info(
        "Removed %d rows with missing values; %d rows remain",
        len(data) - len(cleaned_data),
        len(cleaned_data),
    )

    return cleaned_data


def load_data(data, table):
    """Create a MySQL table if needed and upload the DataFrame rows."""
    # Read database credentials from environment variables.
    db_config = {
        "host": os.environ["DBHOST"],
        "user": os.environ["DBUSER"],
        "password": os.environ["DBPASS"],
        "database": os.environ["DBNAME"],
    }

    connection = None
    cursor = None

    try:
        logging.info("Connecting to MySQL")
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # The schema matches the columns in MOCK_DATA.csv.
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS `{table}` (
            id BIGINT PRIMARY KEY,
            `group` VARCHAR(255),
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            email VARCHAR(255),
            ip_address VARCHAR(255)
        )
        """

        cursor.execute(create_table_query)

        # Clear old rows so rerunning the script does not create duplicates.
        cursor.execute(f"DELETE FROM `{table}`")

        # Values are supplied separately using placeholders to avoid
        # constructing INSERT statements from the data itself.
        insert_query = f"""
        INSERT INTO `{table}`
            (id, `group`, first_name, last_name, email, ip_address)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        for row in data.itertuples(index=False, name=None):
            cursor.execute(insert_query, tuple(row))

        connection.commit()
        logging.info(
            "Successfully uploaded %d rows to %s",
            len(data),
            table,
        )

    except mysql.connector.Error as error:
        logging.error("Database error: %s", error)

        if connection is not None:
            connection.rollback()

        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()
            logging.info("Database connection closed")


def main():
    """Read, clean, and upload MOCK_DATA.csv to the mock table."""
    data = read_data("MOCK_DATA.csv")
    cleaned_data = clean_data(data)
    load_data(cleaned_data, "mock")


if __name__ == "__main__":
    main()
    