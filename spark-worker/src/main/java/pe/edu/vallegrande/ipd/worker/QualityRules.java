package pe.edu.vallegrande.ipd.worker;

import pe.edu.vallegrande.ipd.contracts.Deportista;

/** Reglas de calidad del dominio deportivo, sin dependencia de Spark. */
public final class QualityRules {
    private QualityRules() {}
    public static boolean valido(Deportista deportista) {
        return deportista != null
            && deportista.id() > 0
            && deportista.nombre() != null && !deportista.nombre().isBlank()
            && deportista.disciplina() != null && !deportista.disciplina().isBlank()
            && deportista.edad() >= 10 && deportista.edad() <= 100;
    }
}
