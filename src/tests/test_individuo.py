import unittest
import sys
import os

# Ajustar path para importar pacote
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.individuo import Individuo
from src.models.drone import Drone
from src.models.vento import GerenciadorVento
from src.models.coordenada import Coordenada
from src.config.settings import Config


class TestIndividuo(unittest.TestCase):
    def setUp(self):
        self.drone = Drone()
        self.gerenciador = GerenciadorVento()

        # Coordenada do Unibrasil (início/fim exigido pelo validador)
        self.unibrasil = Coordenada(Config.CEP_INICIAL, 0.0, 0.0)
        # Um ponto distante para forçar tempos de voo não triviais
        self.ponto = Coordenada('00000001', 0.0, 1.0)

        self.coordenadas = [self.unibrasil, self.ponto, self.unibrasil]

    def test_escolher_velocidade_sem_vento_retorna_maxima(self):
        """Sem vento, a estratégia de menor tempo deve escolher a velocidade máxima"""
        ind = Individuo(self.coordenadas, self.drone, self.gerenciador)

        # Forçar vento nulo
        ind.gerenciador_vento.get_vento = lambda dia, hora: {'velocidade': 0, 'direcao': 'N'}

        bateria = self.drone.calcular_autonomia(36)
        velocidade = ind._escolher_velocidade_otima(self.unibrasil, self.ponto, bateria, 1, Config.HORA_INICIO)

        self.assertIn(velocidade, self.drone.get_velocidades_validas())
        # Deve escolher a velocidade máxima (menor tempo)
        self.assertEqual(velocidade, self.drone.get_velocidades_validas()[-1])

    def test_escolher_velocidade_com_bateria_baixa_retorna_minima(self):
        """Se a bateria for insuficiente para qualquer trecho, retorna a mínima"""
        ind = Individuo(self.coordenadas, self.drone, self.gerenciador)

        # Forçar vento nulo
        ind.gerenciador_vento.get_vento = lambda dia, hora: {'velocidade': 0, 'direcao': 'N'}

        # Bateria muito baixa para qualquer trecho realista
        bateria_baixa = 1  # segundo
        velocidade = ind._escolher_velocidade_otima(self.unibrasil, self.ponto, bateria_baixa, 1, Config.HORA_INICIO)

        self.assertEqual(velocidade, self.drone.config.VELOCIDADE_MINIMA)

    def test_escolher_velocidade_retorna_valida(self):
        """Verifica que a velocidade retornada está dentro das válidas"""
        ind = Individuo(self.coordenadas, self.drone, self.gerenciador)

        # Simular vento a favor
        ind.gerenciador_vento.get_vento = lambda dia, hora: {'velocidade': 20, 'direcao': 'E'}

        bateria = self.drone.calcular_autonomia(36)
        velocidade = ind._escolher_velocidade_otima(self.unibrasil, self.ponto, bateria, 1, Config.HORA_INICIO)

        self.assertIn(velocidade, self.drone.get_velocidades_validas())


if __name__ == '__main__':
    unittest.main()
