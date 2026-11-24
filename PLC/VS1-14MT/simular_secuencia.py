"""Ejecuta el listado publicado por redes, con entradas y reloj simulados.

Modelo de las instrucciones utilizadas. Las salidas representan bits, no
movimientos hidráulicos. Ejecutar con Python 3.10+ sin dependencias externas.
"""
from collections import defaultdict
from pathlib import Path
import unittest


class ScanVigor:
    def __init__(self):
        path = Path(__file__).with_name('secuencia-vigor.txt')
        self.program = [line.split() for line in path.read_text(encoding='utf-8').splitlines()
                        if line.strip() and not line.lstrip().startswith('#')]
        self.bits = defaultdict(bool, {'M9000': True})
        self.words = defaultdict(int)
        self.elapsed = defaultdict(int)
        self.first = True

    def value(self, operand):
        if operand.startswith('K'):
            return int(operand[1:])
        return self.words[operand]

    def scan(self, ms=10, **inputs):
        for address, value in inputs.items():
            self.bits[address] = bool(value)
        self.bits['M9002'] = self.first
        self.first = False
        power = False
        for ins, *args in self.program:
            if ins == 'END':
                break
            address = args[0]
            if ins == 'LD':
                power = self.bits[address]
            elif ins == 'LDI':
                power = not self.bits[address]
            elif ins == 'AND':
                power = power and self.bits[address]
            elif ins == 'ANI':
                power = power and not self.bits[address]
            elif ins == 'OR':
                power = power or self.bits[address]
            elif ins == 'SET':
                if power:
                    self.bits[address] = True
            elif ins == 'RST':
                if power:
                    self.bits[address] = False
            elif ins == 'OUT':
                if address.startswith('T'):
                    self.elapsed[address] = self.elapsed[address] + ms if power else 0
                    self.bits[address] = power and self.elapsed[address] >= 100 * self.value(args[1])
                else:
                    self.bits[address] = power
            elif ins == 'CMP':
                if power:
                    lhs, rhs, start = self.value(address), self.value(args[1]), int(args[2][1:])
                    for index, result in enumerate((lhs > rhs, lhs == rhs, lhs < rhs)):
                        self.bits[f'M{start + index}'] = result
            else:
                raise ValueError(f'Instrucción sin modelo: {ins}')
        return {f'Y{i}' for i in range(6) if self.bits[f'Y{i}']}

    def fixture(self):
        # Datos sintéticos para el reloj del simulador. Solo se escriben en memoria local.
        self.words.update(dict(zip((f'D{7000+i}' for i in range(7)), (8, 4, 30, 8, 8, 10, 1))))


class TestSecuencia(unittest.TestCase):
    def setUp(self):
        self.plc = ScanVigor()
        self.plc.fixture()
        self.scan(X0=1, X2=1, X3=1, expect=set())

    def scan(self, expect=None, ms=10, **signals):
        active = self.plc.scan(ms, **signals)
        self.assertLessEqual(len(active & {'Y0', 'Y1', 'Y2', 'Y3'}), 1)
        if 'Y5' in active:
            self.assertEqual(active, {'Y5'})
            self.assertTrue(self.plc.bits['X0'] and self.plc.bits['X2'])
        if expect is not None:
            self.assertEqual(active, expect)
        return active

    def salida(self):
        self.scan(X4=1, expect={'Y0', 'Y4'})
        self.scan(X0=0, X4=0, expect={'Y0', 'Y4'})
        self.scan(X1=1, expect={'Y3', 'Y4'})

    def volver_noyo(self):
        self.salida()
        self.scan(X2=0, expect={'Y3', 'Y4'})
        self.scan(X5=1, expect={'Y1', 'Y4'})
        self.scan(X1=0, X5=0, expect={'Y1', 'Y4'})

    def terminar(self):
        self.volver_noyo()
        self.scan(X0=1, expect={'Y2', 'Y4'})
        self.scan(X2=1, expect={'Y5'})

    def test_ciclo_y_siguiente_apertura_con_x4_en_el_mismo_scan(self):
        self.terminar()
        self.scan(X3=0, expect={'Y5'})
        self.scan(X3=1, X4=1, expect={'Y0', 'Y4'})

    def test_pulso_x5_corto_se_consume_una_vez(self):
        self.volver_noyo()
        self.scan(expect={'Y1', 'Y4'})
        self.scan(X0=1, expect={'Y2', 'Y4'})
        self.scan(X2=1, expect={'Y5'})

    def test_descarga_en_espera_mantiene_k6(self):
        self.salida()
        self.scan(X2=0, expect={'Y3', 'Y4'})
        self.scan(ms=1000, expect={'Y3'})
        self.scan(X5=1, expect={'Y1', 'Y4'})

    def test_x2_pegada_impide_retorno_y_cierre(self):
        self.salida()
        self.scan(ms=400, expect=set())
        self.assertTrue(self.plc.bits['M94'])
        self.scan(X5=1, expect=set())

    def test_x5_prematura_impide_movimiento(self):
        self.salida()
        self.scan(X5=1, expect=set())
        self.assertTrue(self.plc.bits['M93'])

    def test_x2_vuelve_antes_de_confirmar_el_noyo_dentro(self):
        self.volver_noyo()
        self.scan(X2=1, expect=set())
        self.assertTrue(self.plc.bits['M92'])

    def test_perder_noyo_fuera_durante_avance(self):
        self.salida()
        self.scan(X1=0, X2=0, expect=set())
        self.assertTrue(self.plc.bits['M92'])

    def test_perder_molde_abierto_y_rearme_en_base(self):
        self.salida()
        self.scan(X3=0, expect=set())
        self.assertTrue(self.plc.bits['M90'])
        self.scan(M99=1, expect=set())
        self.assertTrue(self.plc.bits['M90'])
        self.scan(X0=1, X1=0, X3=1, M99=1, expect=set())
        self.assertFalse(self.plc.bits['M90'])
        self.scan(X4=1, expect={'Y0', 'Y4'})

    def test_quitar_x2_durante_permiso_cierre(self):
        self.terminar()
        self.scan(X2=0, expect=set())
        self.assertTrue(self.plc.bits['M90'])

    def test_sin_habilitacion_no_mueve(self):
        self.plc.words['D7006'] = 0
        self.scan(X4=1, expect=set())
        self.assertFalse(self.plc.bits['M50'])

    def test_tiempos_con_orden_invalido_no_habilitan(self):
        self.plc.words['D7005'] = self.plc.words['D7001']
        self.scan(X4=1, expect=set())
        self.assertFalse(self.plc.bits['M50'])

    def test_x4_alto_al_arranque_exige_un_pulso_nuevo(self):
        self.plc = ScanVigor()
        self.plc.fixture()
        self.scan(X0=1, X2=1, X3=1, X4=1, expect=set())
        self.scan(expect=set())
        self.scan(X4=0, expect=set())
        self.scan(X4=1, expect={'Y0', 'Y4'})

    def test_faltan_micros_de_base_al_arranque(self):
        self.scan(X0=0, X4=1, expect=set())
        self.scan(X0=1, expect=set())
        self.scan(X4=0, expect=set())
        self.scan(X4=1, expect={'Y0', 'Y4'})

    def test_micro_del_noyo_contradictorio_bloquea(self):
        self.scan(X0=1, X1=1, X4=1, expect=set())
        self.assertTrue(self.plc.bits['M91'])

    def test_expira_recogida_y_corta_k6(self):
        self.salida()
        self.scan(X2=0, ms=3000, expect=set())
        self.assertTrue(self.plc.bits['M94'])

    def test_no_termina_retorno_de_expulsion(self):
        self.volver_noyo()
        self.scan(X0=1, expect={'Y2', 'Y4'})
        self.scan(ms=800, expect=set())
        self.assertTrue(self.plc.bits['M94'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
