package pe.edu.vallegrande.ipd.worker;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;
import static org.apache.spark.sql.functions.*;

/**
 * Ejemplo local: lectura, limpieza y resumen de deportistas IPD con Java + Spark.
 * Desde la raiz, argumento opcional: ruta CSV de entrada.
 */
public final class SparkWorkerApplication {
    private SparkWorkerApplication() {}

    public static void main(String[] args) {
        String entrada = args.length > 0 ? args[0] : "data/sample/deportistas.csv";
        SparkSession spark = SparkSession.builder()
                .appName("IPD-Inteligencia-Deportiva")
                .master("local[*]")
                .getOrCreate();
        try {
            Dataset<Row> origen = spark.read()
                    .option("header", "true")
                    .option("inferSchema", "true")
                    .csv(entrada);

            Dataset<Row> validos = origen
                    .withColumn("nombre", trim(col("nombre")))
                    .withColumn("disciplina", trim(col("disciplina")))
                    .withColumn("edad", col("edad").cast("integer"))
                    .filter(col("id").isNotNull()
                            .and(col("nombre").isNotNull())
                            .and(length(col("nombre")).gt(0))
                            .and(col("disciplina").isNotNull())
                            .and(length(col("disciplina")).gt(0))
                            .and(col("edad").between(10, 100)))
                    .dropDuplicates("id");

            Dataset<Row> resumen = validos
                    .groupBy("disciplina")
                    .count()
                    .withColumnRenamed("count", "total_deportistas")
                    .orderBy("disciplina");

            validos.show(false);
            resumen.show(false);
        } finally {
            spark.stop();
        }
    }
}
