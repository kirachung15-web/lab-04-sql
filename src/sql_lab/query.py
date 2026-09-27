"""Query data from the mock MySQL table."""

import logging
import os

import mysql.connector


# Configure logging.
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


def get_connection():
    """Create and return a connection to the MySQL database."""
    return mysql.connector.connect(
        host=os.environ["DBHOST"],
        user=os.environ["DBUSER"],
        password=os.environ["DBPASS"],
        database=os.environ["DBNAME"],
    )


def get_data_by_group(value):
    """Return all rows where the `group` column equals the given value."""
    connection = None
    cursor = None

    try:
        logging.info("Getting rows for group %s", value)
        connection = get_connection()
        cursor = connection.cursor()

        # Use a parameterized query for the filter value.
        query = """
        SELECT id, `group`, first_name, last_name, email, ip_address
        FROM mock
        WHERE `group` = %s
        """

        cursor.execute(query, (value,))
        rows = cursor.fetchall()

        logging.info("Found %d rows for group %s", len(rows), value)
        return rows

    except mysql.connector.Error as error:
        logging.error("Database error: %s", error)
        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def plot_counts(groupby):
    """Return counts of rows grouped by the specified column."""
    connection = None
    cursor = None

    # Only allow columns that exist in our mock table.
    allowed_columns = {
        "id",
        "group",
        "first_name",
        "last_name",
        "email",
        "ip_address",
    }

    if groupby not in allowed_columns:
        raise ValueError("Invalid column name")

    try:
        logging.info("Counting rows grouped by %s", groupby)
        connection = get_connection()
        cursor = connection.cursor()

        # Column names cannot use %s placeholders, so validate the
        # column against the allowlist before inserting it into SQL.
        column = f"`{groupby}`"

        query = f"""
        SELECT {column}, COUNT(*)
        FROM mock
        GROUP BY {column}
        ORDER BY COUNT(*) DESC
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        logging.info("Finished counting rows by %s", groupby)
        return rows

    except mysql.connector.Error as error:
        logging.error("Database error: %s", error)
        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


def main():
    """Demonstrate the required database query functions."""
    # Show a few rows from one of our Mockaroo groups.
    group_rows = get_data_by_group("A")

    print("\nRows in group A:")
    for row in group_rows[:5]:
        print(row)

    # Count how many records belong to each group.
    counts = plot_counts("group")

    print("\nCounts by group:")
    for row in counts:
        print(row)


if __name__ == "__main__":
    main()