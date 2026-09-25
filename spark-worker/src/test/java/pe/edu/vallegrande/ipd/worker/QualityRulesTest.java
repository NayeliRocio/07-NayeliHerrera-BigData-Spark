package pe.edu.vallegrande.ipd.worker;

import org.junit.jupiter.api.Test;
import pe.edu.vallegrande.ipd.contracts.Deportista;
import static org.junit.jupiter.api.Assertions.*;

class QualityRulesTest {
    @Test void aceptaRegistroCompleto() {
        assertTrue(QualityRules.valido(new Deportista(1, "Ana", "Voley", 20)));
    }
    @Test void rechazaCamposVaciosYEdadesInvalidas() {
        assertFalse(QualityRules.valido(new Deportista(1, "", "Voley", 20)));
        assertFalse(QualityRules.valido(new Deportista(1, "Ana", " ", 20)));
        assertFalse(QualityRules.valido(new Deportista(1, "Ana", "Voley", 5)));
    }
}
