#!/bin/sh

# Load json payload from file
DB_JSON_BODY=$(cat test.json)

#sanity check payload
echo $DB_JSON_BODY

# run create git repo command and save response in RESPONSE_JSON
RESPONSE_JSON=$(databricks repos create --json "$DB_JSON_BODY")

# get the id of the git folder from the saved response
GIT_FOLDER_ID=$(echo $RESPONSE_JSON | jq '.id')

#output the id
echo "Created Git Folder ID:" $GIT_FOLDER_ID 