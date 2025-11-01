"""Helpers para conversão entre minutos absolutos e dia/hora do dia.

minutos_abs: minutos decorridos desde o início da simulação (0 = início em
Config.HORA_INICIO do dia 1).
"""
from ..config.settings import Config


def abs_to_day_and_minuto(minutos_abs: int):
    """Converte minutos_abs para (dia, minuto_do_dia).

    Retorna:
      (dia:int, minuto_do_dia:int)
    """
    absoluto = Config.HORA_INICIO + int(minutos_abs)
    dia = 1 + (absoluto // (24 * 60))
    minuto_do_dia = absoluto % (24 * 60)
    return int(dia), int(minuto_do_dia)


def formatar_hora_minutos(minutos: int):
    """Formata minutos (0-1439) como HH:MM"""
    horas = minutos // 60
    minutos_rest = minutos % 60
    return f"{horas:02d}:{minutos_rest:02d}"
