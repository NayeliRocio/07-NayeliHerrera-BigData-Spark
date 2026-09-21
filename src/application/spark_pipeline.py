from pyspark.sql import DataFrame
from pyspark.sql.functions import col, trim


class SparkPipeline:
    """Pipeline inicial de preparación de datos deportivos."""

    def prepare(self, dataframe: DataFrame) -> DataFrame:
        required = ("id", "nombre", "disciplina")
        missing = [field for field in required if field not in dataframe.columns]

        if missing:
            raise ValueError(f"Columnas requeridas ausentes: {', '.join(missing)}")

        return (
            dataframe
            .dropDuplicates(["id"])
            .filter(col("id").isNotNull())
            .filter(trim(col("nombre")) != "")
            .filter(trim(col("disciplina")) != "")
        )
