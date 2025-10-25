from dataclasses import dataclass
from ..config.settings import Config

@dataclass
class Trecho:
    """Representa um trecho entre duas coordenadas"""
    origem: object
    destino: object
    velocidade: int
    dia: int
    hora_partida: int  # minutos desde 00:00
    vento_velocidade: float
    vento_direcao: str
    
    def __post_init__(self):
        """Calcula automaticamente as métricas do trecho"""
        from ..utils.calculos import (
            distancia_haversine, calcular_direcao, 
            calcular_velocidade_efetiva, cardinal_para_angulo
        )
        
        # Distância em km
        self.distancia = distancia_haversine(
            self.origem.latitude, self.origem.longitude,
            self.destino.latitude, self.destino.longitude
        )
        
        # Direção do voo
        self.direcao_voo = calcular_direcao(
            self.origem.latitude, self.origem.longitude,
            self.destino.latitude, self.destino.longitude
        )
        
        # Velocidade efetiva com vento
        angulo_vento = cardinal_para_angulo(self.vento_direcao)
        self.velocidade_efetiva = calcular_velocidade_efetiva(
            self.velocidade, self.direcao_voo, 
            self.vento_velocidade, angulo_vento
        )
        
        # Tempo de voo em segundos (arredondado para cima)
        tempo_horas = self.distancia / self.velocidade_efetiva
        self.tempo_voo_segundos = int(tempo_horas * 3600) + 1  # +1 para arredondar para cima
        
        # Consumo de bateria (igual ao tempo de voo em segundos)
        self.consumo_bateria = self.tempo_voo_segundos
        
        # Custo do trecho
        self.custo = 0  # Será calculado durante a simulação
    
    def get_hora_chegada(self):
        """Retorna hora de chegada em minutos"""
        return self.hora_partida + (self.tempo_voo_segundos // 60)
    
    def precisa_recarregar(self, bateria_atual):
        """Verifica se precisa recarregar antes deste trecho"""
        return self.consumo_bateria > bateria_atual
    
    def __repr__(self):
        return (f"Trecho({self.origem.cep}→{self.destino.cep}: "
                f"{self.distancia:.1f}km, {self.tempo_voo_segundos}s)")