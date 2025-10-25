import random
from .individuo import Individuo

class Populacao:
    """Representa uma população de indivíduos (rotas)"""
    
    def __init__(self, coordenadas, drone, gerenciador_vento, tamanho=50):
        self.coordenadas = coordenadas
        self.drone = drone
        self.gerenciador_vento = gerenciador_vento
        self.tamanho = tamanho
        self.individuos = self._gerar_populacao_inicial()
        self.melhor_individuo = None
        self.pior_individuo = None
    
    def _gerar_populacao_inicial(self):
        """Gera população inicial com rotas aleatórias"""
        individuos = []
        
        for _ in range(self.tamanho):
            # Garantir que começa e termina no Unibrasil
            coordenadas_unibrasil = [c for c in self.coordenadas if c.eh_unibrasil()]
            outras_coordenadas = [c for c in self.coordenadas if not c.eh_unibrasil()]
            
            # Embaralhar outras coordenadas
            random.shuffle(outras_coordenadas)
            
            # Montar rota: Unibrasil + outras + Unibrasil
            rota_coordenadas = coordenadas_unibrasil + outras_coordenadas + coordenadas_unibrasil
            
            individuo = Individuo(rota_coordenadas, self.drone, self.gerenciador_vento)
            individuos.append(individuo)
        
        return individuos
    
    def avaliar_populacao(self):
        """Avalia todos os indivíduos da população"""
        for individuo in self.individuos:
            individuo.simular_rota()
            individuo.calcular_fitness()
        
        self._atualizar_melhores()
    
    def _atualizar_melhores(self):
        """Atualiza melhor e pior indivíduo"""
        if self.individuos:
            individuos_validos = [ind for ind in self.individuos if ind.viabilidade]
            
            if individuos_validos:
                self.melhor_individuo = min(individuos_validos, key=lambda x: x.fitness)
                self.pior_individuo = max(individuos_validos, key=lambda x: x.fitness)
            else:
                # Se não há indivíduos viáveis, pega o "menos pior"
                self.melhor_individuo = min(self.individuos, key=lambda x: x.fitness)
                self.pior_individuo = max(self.individuos, key=lambda x: x.fitness)
    
    def get_estatisticas(self):
        """Retorna estatísticas da população"""
        if not self.individuos:
            return {}
        
        fitness_values = [ind.fitness for ind in self.individuos]
        individuos_viaveis = sum(1 for ind in self.individuos if ind.viabilidade)
        
        return {
            'tamanho': len(self.individuos),
            'melhor_fitness': min(fitness_values),
            'pior_fitness': max(fitness_values),
            'fitness_medio': sum(fitness_values) / len(fitness_values),
            'individuos_viaveis': individuos_viaveis,
            'taxa_viabilidade': (individuos_viaveis / len(self.individuos)) * 100
        }
    
    def __len__(self):
        return len(self.individuos)
    
    def __getitem__(self, index):
        return self.individuos[index]
    
    def __iter__(self):
        return iter(self.individuos)