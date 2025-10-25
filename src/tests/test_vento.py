import unittest
import sys
import os

# Adicionar o diretório raiz do projeto ao Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.vento import GerenciadorVento

class TestVento(unittest.TestCase):
    
    def setUp(self):
        self.vento = GerenciadorVento()
    
    def test_carregar_previsao(self):
        """Testa se a previsão foi carregada corretamente"""
        previsao = self.vento.previsao
        
        # Verifica se tem os dias esperados
        self.assertIn(1, previsao)
        self.assertIn(2, previsao)
        self.assertIn(3, previsao)
        self.assertIn(4, previsao)
        self.assertIn(5, previsao)
        self.assertIn(6, previsao)
        self.assertIn(7, previsao)
    
    def test_get_vento(self):
        """Testa obtenção de vento por dia e hora"""
        # Teste com hora que existe
        vento = self.vento.get_vento(1, 7 * 60)  # 07:00 -> faixa 06h
        self.assertIsInstance(vento, dict)
        self.assertIn('velocidade', vento)
        self.assertIn('direcao', vento)
        
    def test_hora_para_faixa(self):
        """Testa conversão de hora para faixa"""
        self.assertEqual(self.vento._hora_para_faixa(7 * 60), '06h')   # 07:00 -> 06h
        self.assertEqual(self.vento._hora_para_faixa(10 * 60), '09h')  # 10:00 -> 09h
        self.assertEqual(self.vento._hora_para_faixa(13 * 60), '12h')  # 13:00 -> 12h
        self.assertEqual(self.vento._hora_para_faixa(16 * 60), '15h')  # 16:00 -> 15h
        self.assertEqual(self.vento._hora_para_faixa(19 * 60), '18h')  # 19:00 -> 18h
        self.assertEqual(self.vento._hora_para_faixa(22 * 60), '21h')  # 22:00 -> 21h

if __name__ == '__main__':
    unittest.main()