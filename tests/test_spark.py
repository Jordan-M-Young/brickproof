# from pyspark.sql import SparkSession, DataFrame
# from pyspark.sql.functions import col
# import pytest


# @pytest.fixture
# def spark() -> SparkSession:
#     # Create a SparkSession (the entry point to Spark functionality) on
#     # the cluster in the remote Databricks workspace. Unit tests do not
#     # have access to this SparkSession by default.

#     spark = SparkSession.builder.getOrCreate()

#     return spark


# def test_spark(spark):
#     data = spark.createDataFrame(
#         [(1, "a", "Ideal"), (2, "b", "Premium")], ["id", "name", "cut"]
#     )
#     assert data.collect()[0][2] == "Ideal"
