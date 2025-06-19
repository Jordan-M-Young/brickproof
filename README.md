# Brickproof

Testing suite for integrating Databricks tests into CI/CD workflows.

# Setup 

To setup, run the following:

```sh
./utility_scripts/dev_setup.sh
```

This will copy template json assets into the root for your personal use case, and install dependencies.


# CICD

Currently the functionality of brickproof is limited to creating and then tearing down a git folder in databricks. Before running you'll need to make sure you've 
 edited `git_folder.json` for your own personal use case. Once thats completed, to run this functionality try the following:


```sh

./cicd.sh <MY_WORKSPACE_FULL_PATH>

```

This script will download the git repository you specified in your `git_folder.json` file to a `cicd-testing` directory in the workspace path you specified. The script will wait 20 seconds before tearing down your git repository. This functionality simulates the opening and final steps of the final-idealized cicd pipeline.