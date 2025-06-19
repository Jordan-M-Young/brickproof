#!/bin/sh


if databricks workspace list <MY_WORKSPACE_URL> | grep /cicd-testing; then
    echo "/cicd-testing directory found!"
else
    echo "/cicd-testing directory not found... creating directory now...."
    databricks workspace mkdirs <MY_WORKSPACE_URL>/cicd-testing
fi