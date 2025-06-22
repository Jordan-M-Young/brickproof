# Brickproof

Testing suite for integrating Databricks tests into CI/CD workflows.


# Installation

```sh
pip install brickproof
```

# Use

## Initialize Project

To initialize a brickproof project, run:

```sh
python3 brickproof init
```

This will create a new `brickproof.toml` file, which you will edit for your own usecase. Running the `init` command multiple times will not overwrite your `brickproof.toml` file.


## Configre Databricks Connection

To configure connection credentials to your Databricks workspace, run:

```sh

python3 brickproof configure

```

## Run Brickproof

To run a brickproof testing event, run:

```sh
python3 brickproof run
```

To run with a specific configured profile, run:

```sh
python3 brickproof run --p <MY_PROFILE>
```

## Version

To get the version of your brickproof instance, run:

```sh
python3 brickproof version

```

This command will prompt you to enter your databricks workspace url, personal access token, and profile name. These
will be written out to a `.bprc` file in your local directory. 


## Contributing

See the Contributing doc for more details!


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