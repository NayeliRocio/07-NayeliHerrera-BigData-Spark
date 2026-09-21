from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class QualityResult:
    total_rows: int
    valid_rows: int
    invalid_rows: int

    @property
    def is_valid(self) -> bool:
        return self.invalid_rows == 0


class QualityGate:
    """Valida reglas mínimas de calidad para datos deportivos."""

    REQUIRED_FIELDS = ("id", "nombre", "disciplina")

    def evaluate(self, rows: Iterable[dict]) -> QualityResult:
        total = 0
        invalid = 0

        for row in rows:
            total += 1
            if any(not str(row.get(field, "")).strip() for field in self.REQUIRED_FIELDS):
                invalid += 1

        return QualityResult(
            total_rows=total,
            valid_rows=total - invalid,
            invalid_rows=invalid,
        )
