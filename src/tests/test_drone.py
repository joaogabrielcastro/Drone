import unittest
import sys
import os

# Adicionar o diretório raiz do projeto ao Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.drone import Drone

class TestDrone(unittest.TestCase):
    
    def setUp(self):
        self.drone = Drone()
    
    def test_autonomia_velocidade_referencia(self):
        """Testa autonomia na velocidade de referência (36 km/h)"""
        autonomia = self.drone.calcular_autonomia(36)
        esperado = 5000 * 0.93  # 5000s com fator de correção 0.93
        self.assertAlmostEqual(autonomia, esperado, delta=1)
    
    def test_autonomia_velocidade_maior(self):
        """Testa autonomia em velocidade maior (48 km/h)"""
        autonomia = self.drone.calcular_autonomia(48)
        esperado = 5000 * (36/48)**2 * 0.93
        self.assertAlmostEqual(autonomia, esperado, delta=1)
    
    def test_autonomia_velocidade_maxima(self):
        """Testa autonomia na velocidade máxima (96 km/h)"""
        autonomia = self.drone.calcular_autonomia(96)
        esperado = 5000 * (36/96)**2 * 0.93
        self.assertAlmostEqual(autonomia, esperado, delta=1)
    
    def test_velocidade_valida(self):
        """Testa validação de velocidades"""
        # Velocidades válidas
        self.assertTrue(self.drone.velocidade_valida(36))  # Mínima
        self.assertTrue(self.drone.velocidade_valida(40))  # Múltiplo de 4
        self.assertTrue(self.drone.velocidade_valida(96))  # Máxima
        
        # Velocidades inválidas
        self.assertFalse(self.drone.velocidade_valida(35))  # Abaixo do mínimo
        self.assertFalse(self.drone.velocidade_valida(97))  # Acima do máximo
        self.assertFalse(self.drone.velocidade_valida(37))  # Não múltiplo de 4
    
    def test_velocidades_validas(self):
        """Testa lista de velocidades válidas"""
        velocidades = self.drone.get_velocidades_validas()
        
        # Verifica algumas velocidades específicas
        self.assertIn(36, velocidades)
        self.assertIn(40, velocidades)
        self.assertIn(96, velocidades)
        
        # Verifica que velocidades inválidas não estão na lista
        self.assertNotIn(35, velocidades)
        self.assertNotIn(37, velocidades)
        self.assertNotIn(97, velocidades)
        
        # Verifica que todas são múltiplos de 4
        for velocidade in velocidades:
            self.assertEqual(velocidade % 4, 0)
    
    def test_consumo_bateria(self):
        """Testa consumo de bateria"""
        bateria_inicial = self.drone.bateria_atual
        
        # Consumir 1000 segundos de bateria
        resultado = self.drone.consumir_bateria(1000)
        
        self.assertTrue(resultado)  # Ainda tem bateria
        self.assertEqual(self.drone.bateria_atual, bateria_inicial - 1000)
    
    def test_recarregar(self):
        """Testa recarga completa da bateria"""
        # Consumir alguma bateria primeiro
        self.drone.consumir_bateria(2000)
        bateria_apos_consumo = self.drone.bateria_atual
        
        # Recarregar
        self.drone.recarregar()
        
        # Deve estar com bateria cheia (autonomia a 36 km/h)
        autonomia_cheia = self.drone.calcular_autonomia(36)
        self.assertEqual(self.drone.bateria_atual, autonomia_cheia)
        self.assertGreater(self.drone.bateria_atual, bateria_apos_consumo)

if __name__ == '__main__':
    unittest.main()