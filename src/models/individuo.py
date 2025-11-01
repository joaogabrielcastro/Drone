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
        self.pousos_taxa_tarde = 0
        self.dias_utilizados = 0
        # Alertas e detalhes de pousos atrasados
        self.alertas = []  # Lista de strings com avisos gerados durante a simulação
        self.pousos_atrasados = []  # Lista detalhada de pousos que ocorreram fora do horário

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
        
        # Relógio absoluto (minutos desde o início da simulação)
        dia_atual = 1
        minutos_abs = 0  # minutos decorridos desde o início (0 = início em HORA_INICIO do dia 1)
        hora_atual = (Config.HORA_INICIO + minutos_abs) % (24 * 60)
        bateria_atual = self.drone.calcular_autonomia(36)
        # Reset acumuladores/métricas antes de simular para evitar acumular
        # resultados de simulações anteriores (bug: antes não zerávamos
        # distancia_total/tempo_total/pousos_taxa_tarde etc.)
        self.trechos = []
        self.distancia_total = 0
        self.tempo_total = 0
        self.numero_pousos = 0
        self.custo_total = 0
        self.pousos_taxa_tarde = 0
        self.dias_utilizados = 0
        # Reset de alertas/detalhes
        self.alertas = []
        self.pousos_atrasados = []
        # Lista detalhada de recargas: tuplas (dia, hora_minutos, cep, taxa_tarde_bool)
        self.lista_recargas = []
        
        for i in range(len(self.coordenadas) - 1):
            origem = self.coordenadas[i]
            destino = self.coordenadas[i + 1]
            
            # Verificar se precisa dormir (após HORA_FIM)
            if hora_atual >= Config.HORA_FIM and dia_atual < Config.DIAS_MAXIMOS:
                # Avança o relógio até o próximo dia útil (HORA_INICIO)
                minutos_ate_fim_dia = (24 * 60) - hora_atual
                minutos_ate_reinicio = minutos_ate_fim_dia + Config.HORA_INICIO
                minutos_abs += minutos_ate_reinicio
                dia_atual += 1
                hora_atual = (Config.HORA_INICIO + minutos_abs) % (24 * 60)
                print(f"   ⏰ Dia {dia_atual} - Recarregando durante a noite")
            
            # Escolher velocidade para este trecho (considera vento e bateria)
            velocidade = self._escolher_velocidade_otima(origem, destino, bateria_atual, dia_atual, hora_atual)
            
            # Obter vento atual
            vento = self.gerenciador_vento.get_vento(dia_atual, hora_atual)
            
            # Criar trecho
            trecho = Trecho(origem, destino, velocidade, dia_atual, hora_atual, 
                           vento['velocidade'], vento['direcao'])

            # Verificar se precisa recarregar
            if trecho.precisa_recarregar(bateria_atual):
                # Processar recarga (registra se há taxa tarde) - usamos minutos_abs
                taxa = self._processar_recarga(origem, minutos_abs)
                # Recarregar via Drone (fonte de verdade)
                try:
                    self.drone.recarregar()
                    bateria_atual = self.drone.bateria_atual
                except Exception:
                    # fallback: recomputar autonomia manualmente
                    bateria_atual = self.drone.calcular_autonomia(36)

                self.numero_pousos += 1
                # Obter dia/hora formatados para registro
                from ..utils.time_utils import abs_to_day_and_minuto
                rec_dia, rec_hora = abs_to_day_and_minuto(minutos_abs)
                # Registrar detalhe da recarga (dia, hora_minutos, cep, taxa_bool)
                self.lista_recargas.append((rec_dia, rec_hora, origem.cep, taxa))
                # Registrar pouso atrasado se fora do horário de operação
                if rec_hora >= Config.HORA_FIM:
                    aviso = f"Pouso atrasado: dia {rec_dia}, hora {rec_hora} min, CEP {origem.cep}"
                    self.alertas.append(aviso)
                    self.pousos_atrasados.append((rec_dia, rec_hora, origem.cep, 'fora_horario'))
                    print(f"   ⚠️ {aviso}")
                # Registrar pouso que teve taxa extra (após HORA_TAXA_EXTRA)
                if taxa:
                    aviso_taxa = f"Pouso com taxa tarde: dia {rec_dia}, hora {rec_hora} min, CEP {origem.cep}"
                    self.alertas.append(aviso_taxa)
                    print(f"   ⚠️ {aviso_taxa}")
                # Avançar o tempo pela duração da recarga (em minutos)
                minutos_abs += Config.TEMPO_RECARGA
                # Atualizar hora_atual com base no relógio absoluto
                hora_atual = (Config.HORA_INICIO + minutos_abs) % (24 * 60)

                # Se a recarga empurrar além do horário de operação, dormir até o próximo dia
                if hora_atual >= Config.HORA_FIM and dia_atual < Config.DIAS_MAXIMOS:
                    minutos_ate_fim_dia = (24 * 60) - hora_atual
                    minutos_abs += minutos_ate_fim_dia + Config.HORA_INICIO
                    dia_atual += 1
                    hora_atual = (Config.HORA_INICIO + minutos_abs) % (24 * 60)
                    print(f"   ⏰ Dia {dia_atual} - Recarregando durante a noite (após recarga)")
            
            # Executar trecho: avançar tempo absoluto e reduzir bateria
            bateria_atual -= trecho.consumo_bateria
            minutos_voo = trecho.tempo_voo_segundos // 60
            minutos_abs += minutos_voo
            # Atualizar hora_atual com base no relógio absoluto
            hora_atual = (Config.HORA_INICIO + minutos_abs) % (24 * 60)

            # Adicionar tempo de parada para fotos (72 segundos ~= 1.2 minutos)
            minutos_abs += 1
            hora_atual = (Config.HORA_INICIO + minutos_abs) % (24 * 60)
            
            # Aplicar penalidades
            # Recalcular dias utilizados até este ponto para penalidades e avisos
            dias_ate_agora = 1 + ((Config.HORA_INICIO + minutos_abs) // (24 * 60))
            # Se ultrapassou o número máximo de dias permitidos, aplicar política
            # configurável: hard-invalidade ou penalidade suave por dia excedido.
            if dias_ate_agora > Config.DIAS_MAXIMOS:
                # Registrar alerta apenas uma vez
                if 'dias_excedidos' not in [a.split(':')[0] for a in self.alertas]:
                    aviso_dias = f"Dias utilizados excederam o máximo: {dias_ate_agora} dias (limite {Config.DIAS_MAXIMOS})"
                    self.alertas.append('dias_excedidos: ' + aviso_dias)
                    print(f"   🚨 {aviso_dias}")

                # Se modo hard estiver ativado, manter comportamento antigo
                if getattr(Config, 'HARD_DIAS_MAX', False):
                    self.viabilidade = False
                    self.penalidades += 100000
                    return

                # Caso contrário, aplicar penalidade suave proporcional aos dias
                # excedidos e continuar a simulação para permitir comparar
                # soluções próximas da viabilidade.
                excess_days = dias_ate_agora - Config.DIAS_MAXIMOS
                try:
                    self.penalidades += Config.PENALIDADE_POR_DIA_EXCEDIDO * excess_days
                except Exception:
                    # Se a constante não existir por algum motivo, aplicar um valor padrão
                    self.penalidades += 10000 * excess_days

            # Aplicar penalidades normais (sem checagem rígida de dias aqui)
            self._aplicar_penalidades(trecho, hora_atual, dias_ate_agora)
            
            # Atualizar métricas
            self.trechos.append(trecho)
            self.distancia_total += trecho.distancia
            self.tempo_total += trecho.tempo_voo_segundos / 60  # Converter para minutos
        
        # Ao final da simulação, calcular custo total com base em tempo e recargas
        # Ao final da simulação, calcular custo total com base em tempo e recargas
        try:
            custo_tempo = self.tempo_total * Config.CUSTO_POR_MINUTO
            custo_recargas = self.numero_pousos * Config.CUSTO_RECARGA
            custo_taxa = self.pousos_taxa_tarde * Config.CUSTO_TAXA_TARDE
            self.custo_total = custo_tempo + custo_recargas + custo_taxa
        except Exception:
            # fallback: manter valor atual
            pass

        # Ao final, calcular dias utilizados considerando dias de 24h (calendário)
        minutos_totais_desde_inicio = minutos_abs
        # O dia final é 1 + número de vezes que cruzamos 1440 minutos desde o início
        dias_passados = (Config.HORA_INICIO + minutos_totais_desde_inicio) // (24 * 60)
        self.dias_utilizados = int(dias_passados) + 1

    
    
    def _escolher_velocidade_otima(self, origem, destino, bateria_atual, dia, hora):
        """Escolhe velocidade que minimize tempo dentro das restrições de bateria.

        A estratégia atual é testar todas as velocidades válidas e escolher a
        que produz o menor tempo de voo (considerando vento) sem exigir
        recarga antes do trecho. Se nenhuma velocidade for viável, retorna
        a velocidade mínima (forçando a recarga depois).
        """
        from ..models.trecho import Trecho

        # Gera lista de velocidades válidas (múltiplos de 4 entre min/max)
        velocidades_validas = sorted(self.drone.get_velocidades_validas(), reverse=True)

        # Obter vento no momento (mesma chamada que será usada ao criar o trecho)
        vento = self.gerenciador_vento.get_vento(dia, hora)

        melhor_velocidade = None
        menor_custo = float('inf')
        # Pequena tolerância para desempate: se dois custos forem muito próximos,
        # preferimos a velocidade maior (mais rápida) para cumprir a rota antes.
        EPS_DESEMPATE = 0.01  # unidades de custo (aprox 0.01 minuto)

        # Heurística: custo = alpha * tempo + beta * consumo
        alpha = Config.HEURISTICA_ALPHA
        beta = Config.HEURISTICA_BETA

        for v in velocidades_validas:
            try:
                trecho = Trecho(origem, destino, v, dia, hora, vento['velocidade'], vento['direcao'])
            except Exception:
                # Se cálculo do trecho falhar (ex: divisão por zero), pular essa velocidade
                continue

            # Se precisa recarregar antes do trecho, não é viável nessa velocidade
            if trecho.precisa_recarregar(bateria_atual):
                continue

            # Normalizar termos:
            # - tempo em minutos (mais intuitivo que segundos)
            # - consumo em porcentagem da autonomia disponível na velocidade v
            tempo_min = trecho.tempo_voo_segundos / 60.0
            try:
                autonomia_v = self.drone.calcular_autonomia(v)
                consumo_percent = (trecho.consumo_bateria / autonomia_v) * 100.0
            except Exception:
                consumo_percent = float('inf')

            # Custo linear com termos normalizados
            custo = alpha * tempo_min + beta * consumo_percent

            # Se o custo for claramente melhor, escolhe; em caso de empate
            # dentro de EPS_DESEMPATE, escolhe a velocidade maior (já que
            # iteramos em ordem decrescente, isso favorece velocidades maiores).
            if custo < menor_custo - EPS_DESEMPATE:
                menor_custo = custo
                melhor_velocidade = v
            elif abs(custo - menor_custo) <= EPS_DESEMPATE:
                # desempate: preferir velocidade maior
                if melhor_velocidade is None or v > melhor_velocidade:
                    melhor_velocidade = v

        # Se nenhuma velocidade foi viável, retorna velocidade mínima (forçar recarga)
        if melhor_velocidade is None:
            return self.drone.config.VELOCIDADE_MINIMA

        return melhor_velocidade
    
    def _processar_recarga(self, coordenada, minutos_abs):
        """Processa recarga da bateria usando o relógio absoluto (minutos_abs).

        Decide se a recarga incorrerá em taxa tardia com base em
        Config.TAXA_BASEADA_EM ('start' ou 'end'). Retorna True se taxa.
        """
        from ..utils.time_utils import abs_to_day_and_minuto

        taxa_flag = False
        # Obter hora de início da recarga (minuto do dia)
        dia_rec, hora_inicio = abs_to_day_and_minuto(minutos_abs)

        # Determinar hora para avaliar taxa (início ou fim)
        if Config.TAXA_BASEADA_EM == 'end':
            hora_avaliacao = (hora_inicio + Config.TEMPO_RECARGA) % (24 * 60)
        else:
            hora_avaliacao = hora_inicio

        # Contabilizar taxa se a hora de avaliação >= HORA_TAXA_EXTRA
        if hora_avaliacao >= Config.HORA_TAXA_EXTRA:
            taxa_flag = True
            try:
                self.pousos_taxa_tarde += 1
            except Exception:
                self.pousos_taxa_tarde = 1

        return taxa_flag
    
    def _aplicar_penalidades(self, trecho, hora_chegada, dias_ate_agora=None):
        """Aplica penalidades por violação de restrições"""
        # Penalidade por voo após 19:00
        if hora_chegada > Config.HORA_FIM:
            self.penalidades += 1000
        # Observação: penalidade por dias excedidos é aplicada na simulação
        # principal (simular_rota) como soft-penalty configurável.
    
    def calcular_fitness(self):
        """Calcula fitness baseado no custo total e penalidades"""
        if not self.viabilidade:
            return float('inf')
        # Agora que custo_total já representa o custo monetário (inclui tempo
        # convertido em custo), fitness baseia-se apenas nisso + penalidades.
        self.fitness = self.custo_total + self.penalidades
        
        return self.fitness
    
    def __repr__(self):
        return (f"Individuo({len(self.coordenadas)} pontos, "
                f"fit={self.fitness:.2f}, "
                f"viavel={self.viabilidade})")
    
    def __len__(self):
        return len(self.coordenadas)