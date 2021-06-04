import mysql.connector
from notifications_python_client.notifications import NotificationsAPIClient
from notifications_python_client import prepare_upload
import automationassets
import csv
import re
import tempfile
import sys

class Config:

    MYSQL_HOST = None
    CSRS_DATABASE = None
    MYSQL_USER = None
    MYSQL_PASSWORD = None
    MYSQL_PORT = None
    MYSQL_CERT = None

    GOVUK_NOTIFY_API_KEY = None

    EMAIL_TEMPLATE_ID = None

    def __init__(self) -> None:

        self.MYSQL_HOST = automationassets.get_automation_variable("MYSQL_HOST")
        self.CSRS_DATABASE = automationassets.get_automation_variable("CSRS_DATABASE")
        self.MYSQL_USER = automationassets.get_automation_variable("MYSQL_USER")
        self.MYSQL_PASSWORD = automationassets.get_automation_variable("MYSQL_PASSWORD")
        self.MYSQL_PORT = automationassets.get_automation_variable("MYSQL_PORT")

        self.GOVUK_NOTIFY_API_KEY = automationassets.get_automation_variable("GOVUK_NOTIFY_API_KEY")

        self.EMAIL_TEMPLATE_ID = automationassets.get_automation_variable("ORG_HIERARCHY_EMAIL_TEMPLATE_ID")

ORGANISATION_HIERARCHY_SQL = """
    select ou.id, ou.name, ou.abbreviation, ou.code, ou.agency_token_id, ou.payment_methods, ou.parent_id, pou.name as "parent_name"
    from csrs.organisational_unit ou 
    left outer join csrs.organisational_unit pou on ou.parent_id = pou.id
    order by pou.name asc, ou.name asc;
"""

EMAIL_REGEX = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


def info(msg):
    print(f"VERBOSE: - {msg}")


def error(msg):
    print(f"ERROR: - {msg}")


def get_sql_connection(sql_user, sql_password, sql_host, sql_port, sql_database):
    try:
        return mysql.connector.connect(user=sql_user, password=sql_password, host=sql_host, port=sql_port, database=sql_database)
    except Exception as e:
        error(f"Error connecting to database: {e}")


def fetch_org_hierarchy(sql_connection):

    cursor = sql_connection.cursor()
    cursor.execute(ORGANISATION_HIERARCHY_SQL)
    results = cursor.fetchall()

    info(f"found {len(results)} DB rows")

    if results:

        table_data = list()

        # Headers
        table_data.append([description[0] for description in cursor.description])

        # Rows
        for row in results:
            table_data.append(row)

        return table_data

    else:
        return None


def create_csv_file(table_data):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as file:
    
        csv_writer = csv.writer(file, delimiter=",", quotechar="\"", quoting=csv.QUOTE_ALL)
        csv_writer.writerows(table_data)
    
    return file


def send_file_to_recipients(csv_file, recipients, gov_uk_notify_key, email_template_id):

    with open(csv_file.name, "rb") as csv_file:

        notifications_client = NotificationsAPIClient(gov_uk_notify_key)

        personalisation = {
            "link_to_file": prepare_upload(csv_file, is_csv=True)
        }

        info(f"Sending csv file to {len(recipients)} recipients")
        for recipient in recipients:

            response = notifications_client.send_email_notification(
                email_address=recipient,
                template_id=email_template_id,
                personalisation=personalisation
            )


def run(args, config: Config):

    recipients = get_recipients(args)
    sql_conn = get_sql_connection(config.MYSQL_USER,
                                    config.MYSQL_PASSWORD,
                                    config.MYSQL_HOST,
                                    config.MYSQL_PORT,
                                    config.CSRS_DATABASE)

    table_data = fetch_org_hierarchy(sql_conn)

    if table_data:
        csv_file = create_csv_file(table_data)
        send_file_to_recipients(csv_file, recipients, config.GOVUK_NOTIFY_API_KEY, config.EMAIL_TEMPLATE_ID)

    if sql_conn.is_connected():
        info("Closing SQL connection")
        sql_conn.close()


def get_recipients(args):

    if len(args) <= 1:
        raise ValueError("1 argument required: comma separated email recipients")

    emails = args[1]
    separated_emails = emails.split(",")

    invalid_emails = []
    for email in separated_emails:
        if not re.search(EMAIL_REGEX, email):
            invalid_emails.append(email)
    
    if invalid_emails:
        invalid_emails_str = ", ".join(invalid_emails)
        raise ValueError(f"The following email addresses are invalid: {invalid_emails_str}")

    return separated_emails

try:
    config = Config()
    run(sys.argv, config)
except Exception as e:
    error(e)