# Example Github Action

`docs/github-action-example.yml` is an example of a valid github action pipeline that integrates brickproof testing.


The first portion of the yml file is fairly standard. Decide when this particular action should run.

```yaml
#example brickproof test cicd pipeline for github actions
name: Brickproof Tests

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]
permissions:
  contents: read
  ```


The next section is more brickproof specific.

```yaml

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python 3.10
      uses: actions/setup-python@v3
      with:
        python-version: "3.10"
    - name: Install Dependencies
      run: |
        python3 -m pip install --upgrade pip
        python3 -m pip install -r requirements.txt
        python3 -m pip install brickproof
    - name: Run Brickproof
      env: # add your workspace and token secrets to repo secrets in your repo settings
        TOKEN: ${{ secrets.TOKEN }}
        WORKSPACE_URL: ${{ secrets.WORKSPACE_URL }}

      run: |
        brickproof version
        brickproof edit-config -v repo.branch=$GITHUB_HEAD_REF
        cat ./brickproof.toml
        touch .bprc
        echo [default] >> .bprc
        echo workspace=$WORKSPACE_URL >> .bprc
        echo token=$TOKEN >> .bprc
        cat .bprc
        set +e
        python3 brickproof run
        if [ $? -eq 1 ]; then
          echo "Command failed with exit code 1"
          exit 1
        fi
```

Lets look at the `Run Brickproof` step more closely.

```yaml

    - name: Run Brickproof
      env: # add your workspace and token secrets to repo secrets in your repo settings
        TOKEN: ${{ secrets.TOKEN }}
        WORKSPACE_URL: ${{ secrets.WORKSPACE_URL }}

      run: |
        brickproof version
        brickproof edit-config -v repo.branch=$GITHUB_HEAD_REF
        cat ./brickproof.toml
        touch .bprc
        echo [default] >> .bprc
        echo workspace=$WORKSPACE_URL >> .bprc
        echo token=$TOKEN >> .bprc
        cat .bprc
        set +e
        brickproof run
        if [ $? -eq 1 ]; then
          echo "Command failed with exit code 1"
          exit 1
        fi
```

There are a few main things that are happening here. First we're pulling in our databricks PAT token secret as `TOKEN` and our workspace url as `WORKSPACE_URL` and adding them to our job's env vars. To do this, go to your repo's settings and add them as repo secrets.

Next we're running the job. The first consequential item we run `brickproof edit-config -v repo.branch=$GITHUB_HEAD_REF`. This sets the 
`repo.branch` field of our brickproof.toml file to the branch we're looking to test and merge.

The next step is to populate our .bprc file using the following lines:

```
echo [default] >> .bprc
echo workspace=$WORKSPACE_URL >> .bprc
echo token=$TOKEN >> .bprc
```

Then we run brickproof, if your unit tests pass you'll see something like the following pop up in the logs:

```
============================= test session starts ==============================
platform linux -- Python 3.11.10, pytest-8.4.1, pluggy-1.6.0
rootdir: /Workspace/Users/jordan.m.young0@gmail.com/.brickproof_testing
plugins: typeguard-4.3.0
collected 6 items

brickproof/tests/test_dummies.py .                                       [ 16%]
brickproof/tests/test_utils.py .....                                     [100%]

============================== 6 passed in 7.37s ===============================
```

Looks like a pytest report! If a test fails you'll see an analagous failure report.
