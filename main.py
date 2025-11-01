import os
from src.utils.file_handlers import carregar_coordenadas
from src.models.drone import Drone
from src.models.vento import GerenciadorVento
from src.models.populacao import Populacao
from src.algorithms.genetico import AlgoritmoGenetico
from src.simulation.simulador import Simulador
from src.simulation.csv_exporter import CSVExporter

def main():
    print("🚀 UNIBRASIL SURVEYOR - Etapa 2")
    print("=" * 50)
    
    # Configurações
    ARQUIVO_COORDENADAS = "data/coordenadas.csv"
    TAMANHO_POPULACAO = 30
    NUMERO_GERACOES = 50
    
    # Carregar dados
    coordenadas = carregar_coordenadas(ARQUIVO_COORDENADAS)
    if not coordenadas:
        return
    
    # Inicializar componentes
    drone = Drone()
    vento = GerenciadorVento()
    populacao = Populacao(coordenadas, drone, vento, TAMANHO_POPULACAO)
    algoritmo = AlgoritmoGenetico(populacao)
    simulador = Simulador(drone, vento)
    exporter = CSVExporter()
    
    print(f"🧬 Executando algoritmo genético...")
    print(f"📊 {NUMERO_GERACOES} gerações | {TAMANHO_POPULACAO} indivíduos por geração")
    print(f"🌬️  Sistema de vento carregado")
    
    print("=" * 50)
    
    # Executar algoritmo genético
    for geracao in range(NUMERO_GERACOES):
        stats = algoritmo.executar_geracao()
        
        # Mostrar progresso a cada geração
        print(f"📍 Geração {geracao + 1:02d}/{NUMERO_GERACOES} - "
              f"Melhor: {stats['melhor_fitness']:.2f} | "
              f"Médio: {stats['fitness_medio']:.2f} | "
              f"Viáveis: {stats['taxa_viabilidade']:.1f}%")
    
    # Resultados
    melhor = algoritmo.get_melhor_individuo()
    historico = algoritmo.get_historico()
    
    print("\n" + "=" * 50)
    print("🎯 RESULTADOS FINAIS:")
    print("=" * 50)
    print(f"   • Fitness: {melhor.fitness:.2f}")
    print(f"   • Distância: {melhor.distancia_total:.1f} km")
    print(f"   • Tempo: {melhor.tempo_total:.1f} min")
    print(f"   • Custo: R$ {melhor.custo_total:.2f}")
    print(f"   • Dias: {melhor.dias_utilizados}")
    print(f"   • Pousos: {melhor.numero_pousos}")
    print(f"   • Viável: {'SIM' if melhor.viabilidade else 'NÃO'}")
    
    # Simular trajetória
    print(f"\n🔄 Simulando trajetória...")
    simulador.simular_trajetoria(melhor)
    simulador.salvar_log()
    
    # Exportar resultados
    print(f"\n💾 Exportando resultados...")
    exporter.exportar_rota_completa(melhor)
    exporter.exportar_resumo(melhor, historico)
    # Exportar detalhamento de recargas (cada recarga: dia, hora, cep, taxa_bool, pouso_atrasado)
    try:
        exporter.exportar_recargas_detalhadas(melhor)
    except Exception:
        print("⚠️ Falha ao exportar recargas detalhadas")
    
    print(f"\n✅ Execução concluída com sucesso!")

if __name__ == "__main__":
    main()