# AVEVA Data Hub Event Store Python Sample

| :loudspeaker: **Notice**: This sample uses the AVEVA Data Hub Event Store, which is currently in preview. To get access to this feature, please reach out to your account manager. |
| -----------------------------------------------------------------------------------------------|

**Version:** 1.0.1

[![Build Status](https://dev.azure.com/AVEVA-VSTS/Cloud%20Platform/_apis/build/status%2Fproduct-readiness%2FCloud%20Operations%2FAVEVA.sample-adh-event_store-python?repoName=AVEVA%2Fsample-adh-event_store-python&branchName=main)](https://dev.azure.com/AVEVA-VSTS/Cloud%20Platform/_build/latest?definitionId=14923&repoName=AVEVA%2Fsample-adh-event_store-python&branchName=main)

Developed against Python 3.11.3.

## Requirements

- AVEVA Data Hub with the Event Store feature enabled
- Python 3.7+
- Register a [Client-Credentials Client](https://datahub.connect.aveva.com/clients) in your AVEVA Data Hub tenant and create a client secret to use in the configuration of this sample. ([Video Walkthrough](https://www.youtube.com/watch?v=JPWy0ZX9niU)). Please note that a client is a different authentication method from using your user account to login.
- The client that is registered must have "Manage Permissions" access on all collections and collection items that you intend to set security for. Generally, the Tenant Administrator role will have manage access unless a custom configuration has been set.
- Install required modules: `pip install -r requirements.txt`

## About this sample

This sample uses the sample python library, which makes REST API calls to ADH, to show usage of the AVEVA Data Hub events store. The steps are as follows

1. Create an AVEVA Data Hub client
1. Get or create authorization tag
1. Get or create enumeration
1. Get or create reference data type
1. Get or create an Asset to reference
1. Upsert reference data
1. Get or Create event type
1. Upsert events
1. Get authorization tags
1. Get Enumerations
1. Get reference data types
1. Get reference data
1. Get event types
1. Get events
1. Use a graphQL query to retrieve events, refernce data, and assets
1. Clean up the created events and reference data

## Configuring the sample

The sample is configured by modifying the file [appsettings.placeholder.json](appsettings.placeholder.json). Details on how to configure it can be found in the sections below. Before editing appsettings.placeholder.json, rename this file to `appsettings.json`. This repository's `.gitignore` rules should prevent the file from ever being checked in to any fork or branch, to ensure credentials are not compromised.

### Configuring appsettings.json

AVEVA Data Hub is secured by obtaining tokens from its identity endpoint. Client credentials clients provide a client application identifier and an associated secret (or key) that are authenticated against the token endpoint. You must replace the placeholders in your `appsettings.json` file with the authentication-related values from your tenant and a client-credentials client created in your ADH tenant.

```json
{
  "Resource": "https://uswe.datahub.connect.aveva.com",
  "ApiVersion": "v1",
  "TenantId": "PLACEHOLDER_REPLACE_WITH_TENANT_ID",
  "NamespaceId": "PLACEHOLDER_REPLACE_WITH_NAMESPACE_ID",
  "ClientId": "PLACEHOLDER_REPLACE_WITH_APPLICATION_IDENTIFIER",
  "ClientSecret": "PLACEHOLDER_REPLACE_WITH_APPLICATION_SECRET",
}
```

## Running the sample

To run this example from the command line once the `appsettings.json` is configured, run

```shell
python program.py
```

## Running the automated test

To test the sample, run

```shell
pip install pytest
python -m pytest test.py
```

Note: Example ids for event types, reference data types, etc. are hardcoded, and will need to be updated if they are changed in program.py

---

Tested against Python 3.11.1

For the main ADH samples page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS)  
For the main AVEVA samples page [ReadMe](https://github.com/osisoft/OSI-Samples)
