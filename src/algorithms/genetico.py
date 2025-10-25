import random
import copy
from ..models.populacao import Populacao
from ..models.individuo import Individuo

class AlgoritmoGenetico:
    """Implementa o algoritmo genético para otimização de rotas"""
    
    def __init__(self, populacao, taxa_mutacao=0.05, taxa_crossover=0.8, elitismo=True):
        self.populacao = populacao
        self.taxa_mutacao = taxa_mutacao
        self.taxa_crossover = taxa_crossover
        self.elitismo = elitismo
        self.historico = []
    
    def executar_geracao(self):
        """Executa uma geração completa do algoritmo genético"""
        # Avaliar população atual
        self.populacao.avaliar_populacao()
        
        # Registrar métricas
        self._registrar_metricas()
        
        # Criar nova população
        nova_populacao = self._criar_nova_populacao()
        self.populacao.individuos = nova_populacao
        
        return self.populacao.get_estatisticas()
    
    def _criar_nova_populacao(self):
        """Cria nova população através de seleção, crossover e mutação"""
        nova_populacao = []
        
        # Elitismo: mantém o melhor indivíduo
        if self.elitismo and self.populacao.melhor_individuo:
            nova_populacao.append(copy.deepcopy(self.populacao.melhor_individuo))
        
        # Preenche o resto da população
        while len(nova_populacao) < self.populacao.tamanho:
            # Seleção
            pai1 = self._selecao_torneio()
            pai2 = self._selecao_torneio()
            
            # Crossover
            if random.random() < self.taxa_crossover:
                filho = self._crossover_ox(pai1, pai2)
            else:
                filho = copy.deepcopy(pai1)
            
            # Mutação
            if random.random() < self.taxa_mutacao:
                filho = self._mutacao_troca(filho)
            
            nova_populacao.append(filho)
        
        return nova_populacao[:self.populacao.tamanho]
    
    def _selecao_torneio(self, k=3):
        """Seleção por torneio com tamanho k"""
        participantes = random.sample(
            self.populacao.individuos, 
            min(k, len(self.populacao.individuos))
        )
        return min(participantes, key=lambda x: x.fitness)
    
    def _crossover_ox(self, pai1, pai2):
        """Order Crossover (OX) para rotas"""
        size = len(pai1.coordenadas)
        
        # Garantir que não mexe no Unibrasil do início e fim
        start = 1  # Começa após o Unibrasil inicial
        end = size - 2  # Termina antes do Unibrasil final
        
        if end <= start:
            return copy.deepcopy(pai1)
        
        start, end = sorted(random.sample(range(start, end + 1), 2))
        
        # Cria filho com segmento do pai1
        filho_coords = [None] * size
        filho_coords[0] = pai1.coordenadas[0]  # Unibrasil inicial
        filho_coords[-1] = pai1.coordenadas[-1]  # Unibrasil final
        filho_coords[start:end] = pai1.coordenadas[start:end]
        
        # Preenche com genes do pai2
        pos = end
        for gene in pai2.coordenadas:
            if gene.eh_unibrasil():
                continue  # Pula Unibrasil (já está fixo)
            
            if gene not in filho_coords:
                if pos >= size - 1:
                    pos = 1  # Começa após Unibrasil inicial
                
                # Encontra próxima posição vazia
                while filho_coords[pos] is not None and pos < size - 1:
                    pos += 1
                    if pos == end:  # Volta ao início se necessário
                        pos = 1
                
                if pos < size - 1:  # Não mexe no Unibrasil final
                    filho_coords[pos] = gene
                    pos += 1
        
        return Individuo(filho_coords, self.populacao.drone, self.populacao.gerenciador_vento)
    
    def _mutacao_troca(self, individuo):
        """Mutação por troca de dois pontos (exceto Unibrasil)"""
        coords = individuo.coordenadas.copy()
        
        # Encontrar índices que não são Unibrasil
        indices_validos = [i for i, coord in enumerate(coords) 
                          if not coord.eh_unibrasil() and i != 0 and i != len(coords)-1]
        
        if len(indices_validos) >= 2:
            i, j = random.sample(indices_validos, 2)
            coords[i], coords[j] = coords[j], coords[i]
        
        return Individuo(coords, self.populacao.drone, self.populacao.gerenciador_vento)
    
    def _registrar_metricas(self):
        """Registra métricas da geração atual"""
        stats = self.populacao.get_estatisticas()
        self.historico.append(stats)
    
    def get_historico(self):
        return self.historico
    
    def get_melhor_individuo(self):
        return self.populacao.melhor_individuo