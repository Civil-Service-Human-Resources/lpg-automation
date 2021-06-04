# Runbook: rb_organisation_hierarchy

## Overview

This runbook queries the CSRS database for the organisational hierarchy - the hierarchy is then saved to a virtual CSV file and emailed to recipients via GOV.UK notify.

## Arguments

|Position|Name|Description|Example|
|-|-|-|-|
|1|Recipients|A **comma separated** list of email addresses to send the CSV to.|example1@example.com,example2@example.com