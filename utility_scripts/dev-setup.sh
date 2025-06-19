#!/bin/bash

#copy git folder template for use
if [-e "./git_folder.json"]; then
    echo "File exists."
else
    cp ./testing_assets/git_folder_template.json cp ./git_folder.json

fi

#copy job definition template for use
if [-e "./job_def.json"]; then
    echo "File exists."
else
    cp ./testing_assets/git_folder_template.json cp ./git_folder.json

fi


