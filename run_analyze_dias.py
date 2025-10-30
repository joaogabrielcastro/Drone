from src.utils.file_handlers import carregar_coordenadas
from src.models.drone import Drone
from src.models.vento import GerenciadorVento
from src.models.individuo import Individuo
from src.simulation.simulador import Simulador
from src.config.settings import Config


def main():
    coords = carregar_coordenadas('data/coordenadas.csv')
    if not coords:
        return

    drone = Drone()
    vento = GerenciadorVento()

    # Garantir que a rota comece e termine no Unibrasil;
    # se o CSV não terminar com o Unibrasil, constrói uma rota de exemplo com
    # os primeiros pontos e fecha no Unibrasil.
    if not coords[0].eh_unibrasil() or not coords[-1].eh_unibrasil():
        # Construir rota curta de exemplo (30 pontos no máximo)
        n = min(30, len(coords) - 1)
        rota_coordenadas = [coords[0]] + coords[1:n+1] + [coords[0]]
    else:
        rota_coordenadas = coords

    ind = Individuo(rota_coordenadas, drone, vento)
    ind.simular_rota()

    print('\n=== Resumo da Rota (ordem do CSV) ===')
    print(f'Dias utilizados (simulação): {ind.dias_utilizados}')
    print(f'Tempo total (min): {ind.tempo_total:.1f}')
    print(f'Distância total (km): {ind.distancia_total:.1f}')
    print(f'Número de pousos para recarga: {ind.numero_pousos}')
    print(f'Penalidades: {ind.penalidades}')

    # Calcular tempo agregado (voo + paradas fotos + recargas)
    tempo_voo_min = ind.tempo_total
    num_paradas = len(ind.trechos)
    tempo_fotos_min = (Config.TEMPO_PARADA * num_paradas) / 60.0
    tempo_recargas_min = ind.numero_pousos * Config.TEMPO_RECARGA

    total_min = tempo_voo_min + tempo_fotos_min + tempo_recargas_min
    minutos_por_dia = (Config.HORA_FIM - Config.HORA_INICIO)
    dias_necessarios = int((total_min + minutos_por_dia - 1) // minutos_por_dia)

    print('\nEstimativa baseada em soma de tempos:')
    print(f'  Tempo de voo (min): {tempo_voo_min:.1f}')
    print(f'  Tempo fotos (min): {tempo_fotos_min:.1f}')
    print(f'  Tempo recargas (min): {tempo_recargas_min:.1f}')
    print(f'  Total (min): {total_min:.1f}')
    print(f'  Minutos por dia úteis: {minutos_por_dia}')
    print(f'  Dias necessários (arredondado pra cima): {dias_necessarios}')

    # Simulação detalhada
    simulador = Simulador(drone, vento)
    simulador.simular_trajetoria(ind)


if __name__ == '__main__':
    main()
