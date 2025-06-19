#!/bin/sh

# chek if cicd-testing director exists
if databricks workspace list /Workspace/Users/jordan.m.young0@gmail.com | grep /cicd-testing; then
    #if so, do nothing
    echo "/cicd-testing directory found!"
else
    #if not, create the directory
    echo "/cicd-testing directory not found... creating directory now...."
    databricks workspace mkdirs /Workspace/Users/jordan.m.young0@gmail.com/cicd-testing
fi

# Load json payload from file
DB_JSON_BODY=$(cat git_folder.json)

#sanity check payload
echo $DB_JSON_BODY

# run create git repo command and save response in RESPONSE_JSON
RESPONSE_JSON=$(databricks repos create --json "$DB_JSON_BODY")

# get the id of the git folder from the saved response
GIT_FOLDER_ID=$(echo $RESPONSE_JSON | jq '.id')

#output the id
echo "Created Git Folder ID:" $GIT_FOLDER_ID 


#do some work....
sleep 20

echo "Deleting Git Folder ID:" $GIT_FOLDER_ID "....."

#delete git folder
databricks repos delete $GIT_FOLDER_ID

echo "Deleted Git Folder ID:" $GIT_FOLDER_ID




