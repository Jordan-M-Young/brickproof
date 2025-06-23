# Databricks notebook source
!pip install pytest

# COMMAND ----------

dbutils.library.restartPython()


# COMMAND ----------

import pytest
import os
import sys

# COMMAND ----------

# Run all tests in the repository root.
notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
repo_root = os.path.dirname(os.path.dirname(notebook_path))
os.chdir(f'/Workspace/{repo_root}')
%pwd

# Skip writing pyc files on a readonly filesystem.
sys.dont_write_bytecode = True

retcode = pytest.main(["-p", "no:cacheprovider"])

# Fail the cell execution if we have any test failures.
assert retcode == 0, 'The pytest invocation failed. See the log above for details.'

# COMMAND ----------
#Exits notebook run with a value we can use for determining success or failure.
dbutils.notebook.exit(retcode)

# COMMAND ----------

# !PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider