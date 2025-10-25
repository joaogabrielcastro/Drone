class FitnessFunction:
    """Função de fitness especializada para o problema do drone"""
    
    def __init__(self, peso_tempo=1.0, peso_custo=1.0, peso_penalidades=10.0):
        self.peso_tempo = peso_tempo
        self.peso_custo = peso_custo
        self.peso_penalidades = peso_penalidades
    
    def calcular(self, individuo):
        """
        Calcula fitness considerando:
        - Custo total (recargas + taxas)
        - Tempo total de voo
        - Penalidades por violações
        """
        if not individuo.viabilidade:
            return float('inf')
        
        # Simular rota se ainda não foi simulada
        if not individuo.trechos:
            individuo.simular_rota()
        
        # Componentes do fitness
        custo_componente = individuo.custo_total * self.peso_custo
        tempo_componente = individuo.tempo_total * self.peso_tempo
        penalidades_componente = individuo.penalidades * self.peso_penalidades
        
        fitness = custo_componente + tempo_componente + penalidades_componente
        
        # Bônus por usar menos dias
        if individuo.dias_utilizados <= 3:
            fitness *= 0.9  # 10% de desconto
        elif individuo.dias_utilizados >= 6:
            fitness *= 1.1  # 10% de acréscimo
        
        return fitness
    
    def __repr__(self):
        return f"FitnessFunction(peso_tempo={self.peso_tempo}, peso_custo={self.peso_custo})"