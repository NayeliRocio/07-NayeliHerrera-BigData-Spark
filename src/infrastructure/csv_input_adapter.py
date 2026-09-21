from pathlib import Path
from pyspark.sql import DataFrame, SparkSession


class CsvInputAdapter:
    """Adaptador de entrada para fuentes CSV del proyecto IPD."""

    def __init__(self, spark: SparkSession) -> None:
        self.spark = spark

    def read(self, path: str | Path) -> DataFrame:
        return (
            self.spark.read
            .option("header", True)
            .option("inferSchema", True)
            .csv(str(path))
        )
