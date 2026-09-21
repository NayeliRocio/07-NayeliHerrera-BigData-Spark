from pathlib import Path
from pyspark.sql import SparkSession

from application.spark_pipeline import SparkPipeline
from infrastructure.csv_input_adapter import CsvInputAdapter


def build_spark_session() -> SparkSession:
    return (
        SparkSession.builder
        .appName("InteligenciaDeportivaIPD")
        .master("local[*]")
        .getOrCreate()
    )


def run(input_path: str) -> None:
    spark = build_spark_session()
    try:
        source = CsvInputAdapter(spark).read(Path(input_path))
        result = SparkPipeline().prepare(source)
        result.show(truncate=False)
    finally:
        spark.stop()


if __name__ == "__main__":
    run("data/sample/deportistas.csv")
