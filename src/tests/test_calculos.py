import unittest
import sys
import os

# Adicionar o diretório raiz do projeto ao Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.utils.calculos import *

class TestCalculos(unittest.TestCase):
    
    def test_distancia_mesmo_ponto(self):
        """Distância entre o mesmo ponto deve ser zero"""
        dist = distancia_haversine(-25.423314, -49.216067, -25.423314, -49.216067)
        self.assertAlmostEqual(dist, 0.0, places=2)
    
    def test_distancia_pontos_diferentes(self):
        """Testa distância entre pontos conhecidos"""
        # Dois pontos próximos em Curitiba
        dist = distancia_haversine(-25.423314, -49.216067, -25.432100, -49.225000)
        self.assertGreater(dist, 0.5)
        self.assertLess(dist, 2.0)
    
    def test_direcao_cardinal(self):
        """Testa conversão de ângulo para cardinal"""
        self.assertEqual(direcao_para_cardinal(0), 'N')
        self.assertEqual(direcao_para_cardinal(90), 'E')
        self.assertEqual(direcao_para_cardinal(180), 'S')
        self.assertEqual(direcao_para_cardinal(270), 'W')
        self.assertEqual(direcao_para_cardinal(45), 'NE')
    
    def test_cardinal_para_angulo(self):
        """Testa conversão de cardinal para ângulo"""
        self.assertEqual(cardinal_para_angulo('N'), 0)
        self.assertEqual(cardinal_para_angulo('E'), 90)
        self.assertEqual(cardinal_para_angulo('S'), 180)
        self.assertEqual(cardinal_para_angulo('W'), 270)
        self.assertEqual(cardinal_para_angulo('NE'), 45)
    
    def test_calcular_direcao(self):
        """Testa cálculo de direção entre coordenadas"""
        # Norte (mesma longitude, latitude aumenta)
        direcao = calcular_direcao(-25.0, -49.0, -24.9, -49.0)
        self.assertAlmostEqual(direcao, 0, delta=10)  # Aproximadamente Norte
        
        # Leste (mesma latitude, longitude aumenta)
        direcao = calcular_direcao(-25.0, -49.0, -25.0, -48.9)
        self.assertAlmostEqual(direcao, 90, delta=10)  # Aproximadamente Leste
    
    def test_calcular_velocidade_efetiva(self):
        """Testa cálculo de velocidade com vento"""
        # Sem vento
        v_efetiva = calcular_velocidade_efetiva(36, 0, 0, 0)
        self.assertAlmostEqual(v_efetiva, 36.0, places=1)
        
        # Vento a favor
        v_efetiva = calcular_velocidade_efetiva(36, 0, 10, 0)  # Vento do Norte
        self.assertGreater(v_efetiva, 36.0)
        
        # Vento contra
        v_efetiva = calcular_velocidade_efetiva(36, 0, 10, 180)  # Vento do Sul
        self.assertLess(v_efetiva, 36.0)

if __name__ == '__main__':
    unittest.main()