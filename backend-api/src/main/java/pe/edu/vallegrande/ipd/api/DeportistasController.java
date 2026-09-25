package pe.edu.vallegrande.ipd.api;

import java.util.List;
import java.util.Map;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import pe.edu.vallegrande.ipd.contracts.Deportista;

/** Endpoints de demostracion de arquitectura; no representan datos oficiales del IPD. */
@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "http://localhost:8081")
public class DeportistasController {
    @GetMapping("/status")
    public Map<String, String> estado() {
        return Map.of("proyecto", "IPD Inteligencia Deportiva", "version", "2.0.0", "status", "OK");
    }
    @GetMapping("/deportistas/demo")
    public List<Deportista> ejemplo() {
        return List.of(
            new Deportista(1, "Ana", "Voley", 20),
            new Deportista(2, "Luis", "Atletismo", 22)
        );
    }
}
