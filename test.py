RUNNER_DEF = """# Databricks notebook source
!pip install pytest
!pip install tomlkit
# COMMAND ----------

dbutils.library.restartPython()


# COMMAND ----------

import pytest
import os
import sys
from io import StringIO
# COMMAND ----------

# Run all tests in the repository root.
notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
repo_root = os.path.dirname(os.path.dirname(notebook_path))
os.chdir(f'/Workspace/{repo_root}')
%pwd
old_stdout = sys.stdout

# Skip writing pyc files on a readonly filesystem.
sys.dont_write_bytecode = True

captured_output = StringIO()
sys.stdout = captured_output
retcode = pytest.main(["-p", "no:cacheprovider","--capture=sys"{ignore}])
output_string = captured_output.getvalue()
sys.stdout = old_stdout

# COMMAND ----------
#Exits notebook run with a value we can use for determining success or failure.
dbutils.notebook.exit(f"BrickproofExitCode={retcode}@@@{output_string}")
"""


ignore = ["./tests/test_orchestrator.py", "./tests/test_databricks.py"]
ignore_statement = ""
if ignore:
    ignore_statement = [f'"--ignore={item}"' for item in ignore]
    ignore_statement = "," + ",".join(ignore_statement)


print(RUNNER_DEF.replace("{ignore}", ignore_statement))
