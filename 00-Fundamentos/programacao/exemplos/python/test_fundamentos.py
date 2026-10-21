from __future__ import annotations

import json
import math
import subprocess
import sys
import unittest
from pathlib import Path

from fundamentos import analisar, conceito, converter_argumentos, resumir, validar_nota


SCRIPT = Path(__file__).with_name("fundamentos.py")


class FundamentosTests(unittest.TestCase):
    def test_limites_dos_conceitos(self) -> None:
        casos = {9: "A", 7: "B", 5: "C", 0: "D", 10: "A", 4.999: "D"}
        for nota, esperado in casos.items():
            with self.subTest(nota=nota):
                self.assertEqual(conceito(nota), esperado)

    def test_resumo_preserva_contrato_publico(self) -> None:
        self.assertEqual(
            resumir([10, 8, 4]),
            {"quantidade": 3, "media": 7.33, "conceitos": {"A": 1, "B": 1, "C": 0, "D": 1}},
        )

    def test_analisar_aceita_gerador_e_calcula_extremos(self) -> None:
        resultado = analisar(nota for nota in (3, 7, 10))
        self.assertEqual(resultado.quantidade, 3)
        self.assertEqual(resultado.media, 6.67)
        self.assertEqual((resultado.menor, resultado.maior), (3.0, 10.0))

    def test_resultado_nao_permite_mutar_frequencias(self) -> None:
        resultado = analisar([10, 8, 4])
        with self.assertRaises(TypeError):
            resultado.conceitos["A"] = 99  # type: ignore[index]

        # A cópia de fronteira continua sendo JSON serializável e independente.
        serializavel = resultado.como_dict()
        self.assertEqual(json.loads(json.dumps(serializavel))["conceitos"]["A"], 1)

    def test_rejeita_fora_do_intervalo_e_nao_finitos(self) -> None:
        for nota in (-0.1, 10.1, math.inf, -math.inf, math.nan):
            with self.subTest(nota=nota), self.assertRaises(ValueError):
                validar_nota(nota)

    def test_rejeita_tipos_incorretos_inclusive_bool(self) -> None:
        for nota in (True, False, "8", None, object()):
            with self.subTest(nota=nota), self.assertRaises(TypeError):
                validar_nota(nota)

    def test_rejeita_colecao_vazia(self) -> None:
        with self.assertRaisesRegex(ValueError, "ao menos uma"):
            analisar([])

    def test_conversao_indica_posicao_e_preserva_causa(self) -> None:
        with self.assertRaisesRegex(ValueError, "argumento 2") as contexto:
            converter_argumentos(["8", "oito"])
        self.assertIsInstance(contexto.exception.__cause__, ValueError)

    def test_cli_emite_json_deterministico(self) -> None:
        processo = subprocess.run(
            [sys.executable, str(SCRIPT), "10", "8", "4"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(processo.returncode, 0, processo.stderr)
        self.assertEqual(json.loads(processo.stdout)["media"], 7.33)

    def test_cli_invalida_retorna_codigo_dois(self) -> None:
        processo = subprocess.run(
            [sys.executable, str(SCRIPT), "11"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(processo.returncode, 2)
        self.assertIn("entre 0 e 10", processo.stderr)


if __name__ == "__main__":
    unittest.main()
