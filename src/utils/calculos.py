import math

def distancia_haversine(lat1, lon1, lat2, lon2):
    """
    Calcula distância entre duas coordenadas usando fórmula Haversine
    Retorna distância em KILÔMETROS
    """
    R = 6371  # Raio da Terra em km
    
    # Converter para radianos
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Diferenças
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Fórmula Haversine
    a = (math.sin(dlat/2) ** 2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    distancia = R * c
    return distancia

def calcular_direcao(lat1, lon1, lat2, lon2):
    """
    Calcula direção do voo entre duas coordenadas
    Retorna ângulo em graus (0 = Norte, 90 = Leste)
    """
    # Converter para radianos
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Calcular diferenças
    dlon = lon2_rad - lon1_rad
    
    # Calcular ângulo
    x = math.sin(dlon) * math.cos(lat2_rad)
    y = (math.cos(lat1_rad) * math.sin(lat2_rad) - 
         math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon))
    
    direcao_rad = math.atan2(x, y)
    direcao_graus = math.degrees(direcao_rad)
    
    # Ajustar para 0-360
    return (direcao_graus + 360) % 360

def direcao_para_cardinal(angulo):
    """Converte ângulo em graus para direção cardinal"""
    direcoes = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    idx = int((angulo + 11.25) / 22.5) % 16
    return direcoes[idx]

def calcular_velocidade_efetiva(velocidade_drone, direcao_voo, vento_velocidade, vento_direcao):
    """
    Calcula velocidade efetiva considerando vento
    Implementação baseada no exemplo do PDF
    """
    # Converter direções para ângulos em radianos
    angulo_voo_rad = math.radians(direcao_voo)
    angulo_vento_rad = math.radians(vento_direcao)
    
    # Componentes do drone
    v_drone_x = velocidade_drone * math.sin(angulo_voo_rad)
    v_drone_y = velocidade_drone * math.cos(angulo_voo_rad)
    
    # Componentes do vento
    v_vento_x = vento_velocidade * math.sin(angulo_vento_rad)
    v_vento_y = vento_velocidade * math.cos(angulo_vento_rad)
    
    # Velocidade efetiva (solo)
    v_efetiva_x = v_drone_x + v_vento_x
    v_efetiva_y = v_drone_y + v_vento_y
    
    # Magnitude da velocidade efetiva
    v_efetiva = math.sqrt(v_efetiva_x**2 + v_efetiva_y**2)
    
    return v_efetiva

def cardinal_para_angulo(cardinal):
    """Converte direção cardinal para ângulo em graus"""
    direcoes = {
        'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5,
        'E': 90, 'ESE': 112.5, 'SE': 135, 'SSE': 157.5,
        'S': 180, 'SSW': 202.5, 'SW': 225, 'WSW': 247.5,
        'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5
    }
    return direcoes.get(cardinal, 0)