# Runbook: rb-registered-email-ids

## Overview

This runbook queries the IDENTITY database for the registered email ids - the email ids are then saved to a virtual CSV file and emailed to recipients via GOV.UK notify.

## Automation Assets

|Name|Description|
|-|-|
|MYSQL_HOST|Host for the database|
|IDENTITY_DATABASE|Name of the IDENTITY database|
|MYSQL_USER|Database username|
|MYSQL_PASSWORD|Database password|
|MYSQL_PORT|Database port|
|GOVUK_NOTIFY_API_KEY|API key for GOV.UK notify service|
|REGISTERED_EMAIL_IDS_EMAIL_TEMPLATE_ID|Template ID for the registered email ids email (GOV.UK notify)|

## Arguments

|Position|Name|Description|Example|
|-|-|-|-|
|1|Recipients|A **comma separated** list of email addresses to send the CSV to.|example1@example.com,example2@example.com