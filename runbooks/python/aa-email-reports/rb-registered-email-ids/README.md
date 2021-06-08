# Runbook: rb_organisation_hierarchy

## Overview

This runbook queries the CSRS database for the organisational hierarchy - the hierarchy is then saved to a virtual CSV file and emailed to recipients via GOV.UK notify.

## Automation Assets

|Name|Description|
|-|-|
|MYSQL_HOST|Host for the database|
|CSRS_DATABASE|Name of the CSRS database|
|MYSQL_USER|Database username|
|MYSQL_PASSWORD|Database password|
|MYSQL_PORT|Database port|
|GOVUK_NOTIFY_API_KEY|API key for GOV.UK notify service|
|ORG_HIERARCHY_EMAIL_TEMPLATE_ID|Template ID for the organisation hierarchy email (GOV.UK notify)|

## Arguments

|Position|Name|Description|Example|
|-|-|-|-|
|1|Recipients|A **comma separated** list of email addresses to send the CSV to.|example1@example.com,example2@example.com