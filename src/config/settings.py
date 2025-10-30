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
    CUSTO_RECARGA = 80.0  # R$
    CUSTO_TAXA_TARDE = 80.0  # R$ adicional após 17:00
    
    # Projeto
    DIAS_MAXIMOS = 7
    CEP_INICIAL = "82821020"  # Unibrasil
    # Heurística para escolha de velocidade: custo = ALPHA * tempo + BETA * consumo
    HEURISTICA_ALPHA = 1.0
    HEURISTICA_BETA = 0.0