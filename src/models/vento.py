class GerenciadorVento:
    def __init__(self):
        self.previsao = self._carregar_previsao()
    
    def _carregar_previsao(self):
        """Carrega previsão de vento dos 7 dias conforme tabela do PDF"""
        return {
            1: {  # Dia 1
                '06h': {'velocidade': 17, 'direcao': 'ENE'},
                '09h': {'velocidade': 18, 'direcao': 'E'},
                '12h': {'velocidade': 19, 'direcao': 'E'},
                '15h': {'velocidade': 19, 'direcao': 'E'},
                '18h': {'velocidade': 20, 'direcao': 'E'},
                '21h': {'velocidade': 20, 'direcao': 'E'}
            },
            2: {  # Dia 2
                '06h': {'velocidade': 20, 'direcao': 'E'},
                '09h': {'velocidade': 19, 'direcao': 'E'},
                '12h': {'velocidade': 16, 'direcao': 'E'},
                '15h': {'velocidade': 19, 'direcao': 'E'},
                '18h': {'velocidade': 21, 'direcao': 'E'},
                '21h': {'velocidade': 21, 'direcao': 'E'}
            },
            # Dias 3-7 seguindo a mesma estrutura...
            # Por enquanto vou simplificar, depois completamos
            3: {  # Dia 3 (exemplo)
                '06h': {'velocidade': 15, 'direcao': 'ENE'},
                '09h': {'velocidade': 17, 'direcao': 'NE'},
                '12h': {'velocidade': 8, 'direcao': 'NE'},
                '15h': {'velocidade': 20, 'direcao': 'E'},
                '18h': {'velocidade': 16, 'direcao': 'E'},
                '21h': {'velocidade': 15, 'direcao': 'ENE'}
            },
             4: {  # Dia 4
        '06h': {'velocidade': 8, 'direcao': 'ENE'},
        '09h': {'velocidade': 11, 'direcao': 'ENE'},
        '12h': {'velocidade': 8, 'direcao': 'NE'},
        '15h': {'velocidade': 11, 'direcao': 'E'},
        '18h': {'velocidade': 11, 'direcao': 'E'},
        '21h': {'velocidade': 11, 'direcao': 'E'}
    },
    5: {  # Dia 5
        '06h': {'velocidade': 3, 'direcao': 'WSW'},
        '09h': {'velocidade': 3, 'direcao': 'WSW'},
        '12h': {'velocidade': 7, 'direcao': 'WSW'},
        '15h': {'velocidade': 7, 'direcao': 'SSW'},
        '18h': {'velocidade': 10, 'direcao': 'E'},
        '21h': {'velocidade': 11, 'direcao': 'E'}
    },
    6: {  # Dia 6
        '06h': {'velocidade': 4, 'direcao': 'NE'},
        '09h': {'velocidade': 5, 'direcao': 'ENE'},
        '12h': {'velocidade': 4, 'direcao': 'NE'},
        '15h': {'velocidade': 8, 'direcao': 'E'},
        '18h': {'velocidade': 15, 'direcao': 'E'},
        '21h': {'velocidade': 15, 'direcao': 'E'}
    },
    7: {  # Dia 7
        '06h': {'velocidade': 6, 'direcao': 'NE'},
        '09h': {'velocidade': 8, 'direcao': 'NE'},
        '12h': {'velocidade': 14, 'direcao': 'NE'},
        '15h': {'velocidade': 16, 'direcao': 'NE'},
        '18h': {'velocidade': 13, 'direcao': 'ENE'},
        '21h': {'velocidade': 10, 'direcao': 'ENE'}
    }
}
    
    def get_vento(self, dia, hora_minutos):
        """
        Retorna vento para dia e hora específicos
        hora_minutos: minutos desde 00:00
        """
        if dia not in self.previsao:
            # Retorna vento neutro se dia não existir
            return {'velocidade': 0, 'direcao': 'N'}
        
        hora_str = self._hora_para_faixa(hora_minutos)
        return self.previsao[dia].get(hora_str, {'velocidade': 0, 'direcao': 'N'})
    
    def _hora_para_faixa(self, hora_minutos):
        """Converte hora em minutos para faixa (06h, 09h, etc.)"""
        horas = hora_minutos // 60
        if horas < 9: return '06h'
        elif horas < 12: return '09h'
        elif horas < 15: return '12h'
        elif horas < 18: return '15h'
        elif horas < 21: return '18h'
        else: return '21h'
    
    def __repr__(self):
        return f"GerenciadorVento({len(self.previsao)} dias)"