class Config:
    """Configurações baseadas no PDF do projeto"""
    
    # Drone
    VELOCIDADE_REFERENCIA = 36  # km/h
    AUTONOMIA_REFERENCIA = 5000  # segundos
    FATOR_CORRECAO = 0.93
    VELOCIDADE_MINIMA = 36  # km/h (10 m/s)
    VELOCIDADE_MAXIMA = 96  # km/h
    TEMPO_PARADA = 72  # segundos por parada
    TEMPO_RECARGA = 30  # minutos
    
    # Horários
    HORA_INICIO = 6 * 60  # 06:00 em minutos
    HORA_FIM = 19 * 60    # 19:00 em minutos
    HORA_TAXA_EXTRA = 17 * 60  # 17:00 para taxa adicional
    
    # Custos
    CUSTO_RECARGA = 0  # R$
    CUSTO_TAXA_TARDE = 80.0  # R$ adicional após 17:00
    # Custo por minuto de operação (opcional). Se não houver custo por tempo,
    # deixar 0.0. Anteriormente o código esperava esta constante e sua
    # ausência causava uma exceção que zerava o custo final.
    CUSTO_POR_MINUTO = 0.0
    # Como a taxa tardia é aplicada: 'start' -> baseada no início da recarga;
    # 'end' -> baseada no término da recarga (start + TEMPO_RECARGA)
    TAXA_BASEADA_EM = 'start'  # 'start' or 'end'
    
    # Projeto
    DIAS_MAXIMOS = 7
    CEP_INICIAL = "82821020"  # Unibrasil
    # Heurística para escolha de velocidade: custo = ALPHA * tempo + BETA * consumo
    # Ajuste BETA para >0 para equilibrar tempo vs consumo e permitir velocidades
    # intermediárias (múltiplos de 4). Valor padrão anterior era 0.0 (favorecia
    # sempre a velocidade mais rápida). Pequeno valor como 0.1 promove variação.
    HEURISTICA_ALPHA = 3.0
    # Aumentamos BETA para 1.0 para dar mais peso ao consumo na heurística.
    # Isso deve reduzir a preferência por velocidades extremas altas (96 km/h)
    # e incentivar escolhas intermediárias quando o consumo relativo é alto.
    HEURISTICA_BETA = 1.0
    # Como tratar rota que excede DIAS_MAXIMOS
    # Se HARD_DIAS_MAX for True, rotas que ultrapassam o limite serão marcadas
    # inviáveis imediatamente (comportamento antigo). Se False, uma penalidade
    # por dia excedido será aplicada (soft-penalty), permitindo que o otimizador
    # avalie rotas próximas da viabilidade e encontre um meio-termo.
    HARD_DIAS_MAX = False
    # Penalidade aplicada por cada dia que ultrapassar DIAS_MAXIMOS (valor em
    # unidades de custo, somado a self.penalidades). Ajuste para controlar o
    # trade-off entre viabilidade e economia. Ex: 10000 é severo; 1000 é leve.
    PENALIDADE_POR_DIA_EXCEDIDO = 10000