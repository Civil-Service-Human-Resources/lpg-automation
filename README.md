# LPG-Automation

## Overview
This repository contains various automation scripts used by LPG. These are intended to be hosted within Azure via the Automation Account / Runbook services. For more information regarding Azure Automation please visit: https://docs.microsoft.com/en-us/azure/automation/automation-intro

Right now, this repository is purely for storing runbook code. There is scope in the future for adding Terraform support in order to deploy code changes to Azure.

The current preferred language for runbooks is **Python 3**. More information about Python 3 runbooks can be found here: https://docs.microsoft.com/en-us/azure/automation/learn/automation-tutorial-runbook-textual-python-3

## Usage

Runbooks can be developed / tested locally using the `automationassets` Python module, provided here: https://github.com/azureautomation/python_emulated_assets. The package is written in Python 2 but has been altered slightly to work with Python 3.

### Structure

Runbooks in the `runbooks` repository are stored in the following directory structure:

`<language>/<automation-account>/<runbook-name>`

So, for exmaple, a Python runbook called `rb-organisation-hierarchy` in the automation account `email-reports` would be in the `runbooks/python/email-reports/rb-organisation-hierarchy` directory.

The runbook name should simply be `code.py`, with accompanying `README.md` and `requirements.txt` files. This structure is important for both consistency and potential Terraform implementation.

### Requirements

Python 3 is required to develop and test Python runbooks locally.

Additionally, the requirements for the runbook (found in the `requirements.txt` within the runbook's directory) should be installed; it is recommended to use a virtual Python environment for this to avoid cluttering the base install.

### Automation Assets

As previously mentioned, the python runbooks in this repository make use of a local module called `automationassets.py`. This module simulates the automation assets found in the Azure Runbook environment.

To populate the necessary variables for automation assets locally, they must be added to the `localassets.json` file. An example of this file can be found here: https://github.com/azureautomation/python_emulated_assets/blob/master/automationassets/localassets.json

**Important**: the `localassets.json` file has been removed from the git index for this repository - this means that any changes made to the file **will not** be tracked. This is to prevent accidentally committing sensitive variables.

### Running the runbook

To execute the runbook localy, use the provided `run_runbook.sh` script. It's important to use this script as it sets the `PYTHONPATH` environment variable correctly (this allows `automationassets` to be referenced in the same way that it is in Azure, despite being a few levels up from the scripts directory-wise)

The script takes 1 argument, which is `<automation-account-name>/<runbook-name>`.

### Uploading the runbook

Until Terraform support is implemented into this repository, runbooks will need to be manually uploaded to the Automation Account.

To do this:
1. navigate to the Automation account in Azure
1. Click `runbooks`
1. Click `Import runbook`
1. Select the relevant `code.py` file from the runbooks directory
1. Enter the name of the runbook (The name of the containing folder)
1. The type should be Python 3
1. Enter a description
1. Click `Create`