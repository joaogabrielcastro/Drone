import math
from ..config.settings import Config

class Drone:
    def __init__(self):
        self.config = Config
        self.bateria_atual = self.calcular_autonomia(36)  # Começa com bateria cheia na velocidade mínima
    
    def calcular_autonomia(self, velocidade):
        """
        Calcula autonomia baseada na fórmula: A(v) = 5000 * (36/v)² * 0.93
        Retorna autonomia em SEGUNDOS
        """
        if not self.velocidade_valida(velocidade):
            raise ValueError(f"Velocidade {velocidade} km/h inválida")
        
        autonomia = (self.config.AUTONOMIA_REFERENCIA * 
                    (self.config.VELOCIDADE_REFERENCIA / velocidade) ** 2 * 
                    self.config.FATOR_CORRECAO)
        return autonomia
    
    def velocidade_valida(self, velocidade):
        """Verifica se velocidade atende todas as restrições"""
        return (velocidade >= self.config.VELOCIDADE_MINIMA and 
                velocidade <= self.config.VELOCIDADE_MAXIMA and 
                velocidade % 4 == 0)
    
    def get_velocidades_validas(self):
        """Retorna lista de todas as velocidades válidas"""
        return [v for v in range(
            self.config.VELOCIDADE_MINIMA, 
            self.config.VELOCIDADE_MAXIMA + 1, 4
        )]
    
    def consumir_bateria(self, tempo_voo_segundos):
        """
        Consome bateria baseada no tempo de voo
        Retorna True se ainda tem bateria, False se acabou
        """
        self.bateria_atual -= tempo_voo_segundos
        return self.bateria_atual >= 0
    
    def recarregar(self):
        """Recarrega completamente a bateria"""
        self.bateria_atual = self.calcular_autonomia(36)  # Recarrega na velocidade mínima
    
    def get_bateria_porcentagem(self):
        """Retorna porcentagem da bateria"""
        bateria_cheia = self.calcular_autonomia(36)
        return (self.bateria_atual / bateria_cheia) * 100
    
    def __repr__(self):
        return f"Drone(bateria={self.get_bateria_porcentagem():.1f}%)"