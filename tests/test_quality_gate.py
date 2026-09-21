from src.domain.quality_gate import QualityGate


def test_quality_gate_detects_invalid_rows():
    rows = [
        {"id": 1, "nombre": "Ana", "disciplina": "Atletismo"},
        {"id": 2, "nombre": "", "disciplina": "Natacion"},
    ]

    result = QualityGate().evaluate(rows)

    assert result.total_rows == 2
    assert result.valid_rows == 1
    assert result.invalid_rows == 1
    assert result.is_valid is False
