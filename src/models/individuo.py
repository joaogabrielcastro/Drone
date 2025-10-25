import random
from ..models.trecho import Trecho
from ..config.settings import Config

class Individuo:
    """Representa uma solução (rota completa) para o problema"""
    
    def __init__(self, coordenadas, drone, gerenciador_vento):
        self.coordenadas = coordenadas
        self.drone = drone
        self.gerenciador_vento = gerenciador_vento
        self.trechos = []
        self.fitness = float('inf')
        self.viabilidade = True
        self.penalidades = 0
        
        # Métricas
        self.distancia_total = 0
        self.tempo_total = 0
        self.custo_total = 0
        self.numero_pousos = 0
        self.dias_utilizados = 0
        
        self._validar_rota()
    
    def _validar_rota(self):
        """Valida restrições básicas da rota"""
        # Deve começar e terminar no Unibrasil
        if not self.coordenadas[0].eh_unibrasil():
            self.viabilidade = False
            self.penalidades += 10000
        
        if not self.coordenadas[-1].eh_unibrasil():
            self.viabilidade = False
            self.penalidades += 10000
        
        # Não pode ter CEPs repetidos (exceto Unibrasil no início/fim)
        ceps_vistos = set()
        for coord in self.coordenadas[1:-1]:  # Excluir início e fim
            if coord.cep in ceps_vistos:
                self.viabilidade = False
                self.penalidades += 5000
            ceps_vistos.add(coord.cep)
    
    def simular_rota(self):
        """Simula a execução completa da rota"""
        if not self.viabilidade:
            return
        
        dia_atual = 1
        hora_atual = Config.HORA_INICIO
        bateria_atual = self.drone.calcular_autonomia(36)
        self.trechos = []
        self.numero_pousos = 0
        self.custo_total = 0
        
        for i in range(len(self.coordenadas) - 1):
            origem = self.coordenadas[i]
            destino = self.coordenadas[i + 1]
            
            # Verificar se precisa dormir (após 19:00)
            if hora_atual >= Config.HORA_FIM and dia_atual < Config.DIAS_MAXIMOS:
                dia_atual += 1
                hora_atual = Config.HORA_INICIO
                print(f"   ⏰ Dia {dia_atual} - Recarregando durante a noite")
            
            # Escolher velocidade para este trecho
            velocidade = self._escolher_velocidade_otima(origem, destino, bateria_atual)
            
            # Obter vento atual
            vento = self.gerenciador_vento.get_vento(dia_atual, hora_atual)
            
            # Criar trecho
            trecho = Trecho(origem, destino, velocidade, dia_atual, hora_atual, 
                           vento['velocidade'], vento['direcao'])
            
            # Verificar se precisa recarregar
            if trecho.precisa_recarregar(bateria_atual):
                self._processar_recarga(origem, dia_atual, hora_atual)
                bateria_atual = self.drone.calcular_autonomia(36)
                self.numero_pousos += 1
            
            # Executar trecho
            bateria_atual -= trecho.consumo_bateria
            hora_atual = trecho.get_hora_chegada()
            
            # Adicionar tempo de parada para fotos (72 segundos)
            hora_atual += 1  # Aproximação de 72 segundos = 1.2 minutos
            
            # Aplicar penalidades
            self._aplicar_penalidades(trecho, hora_atual)
            
            # Atualizar métricas
            self.trechos.append(trecho)
            self.distancia_total += trecho.distancia
            self.tempo_total += trecho.tempo_voo_segundos / 60  # Converter para minutos
        
        self.dias_utilizados = dia_atual
    
    def _escolher_velocidade_otima(self, origem, destino, bateria_atual):
        """Escolhe velocidade que minimize tempo dentro das restrições de bateria"""
        velocidades_validas = self.drone.get_velocidades_validas()
        
        # Por enquanto, usa velocidade mínima (mais econômica)
        # Futuramente implementar lógica de otimização
        return 36
    
    def _processar_recarga(self, coordenada, dia, hora):
        """Processa recarga da bateria"""
        custo_recarga = Config.CUSTO_RECARGA
        
        # Verificar se é após 17:00
        if hora >= Config.HORA_TAXA_EXTRA:
            custo_recarga += Config.CUSTO_TAXA_TARDE
        
        self.custo_total += custo_recarga
        
        # Tempo de recarga (30 minutos)
        # hora += Config.TEMPO_RECARGA  # Será aplicado na simulação
    
    def _aplicar_penalidades(self, trecho, hora_chegada):
        """Aplica penalidades por violação de restrições"""
        # Penalidade por voo após 19:00
        if hora_chegada > Config.HORA_FIM:
            self.penalidades += 1000
        
        # Penalidade por exceder 7 dias
        if self.dias_utilizados > Config.DIAS_MAXIMOS:
            self.penalidades += 5000
    
    def calcular_fitness(self):
        """Calcula fitness baseado no custo total e penalidades"""
        if not self.viabilidade:
            return float('inf')
        
        # Fitness = custo total + tempo total (convertido para custo) + penalidades
        custo_tempo = self.tempo_total * 0.1  # Converter tempo para custo aproximado
        self.fitness = self.custo_total + custo_tempo + self.penalidades
        
        return self.fitness
    
    def __repr__(self):
        return (f"Individuo({len(self.coordenadas)} pontos, "
                f"fit={self.fitness:.2f}, "
                f"viavel={self.viabilidade})")
    
    def __len__(self):
        return len(self.coordenadas)