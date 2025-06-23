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

