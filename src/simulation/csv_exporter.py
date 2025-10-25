import csv
import os
from datetime import datetime
from ..config.settings import Config

class CSVExporter:
    """Exporta resultados no formato CSV especificado"""
    
    def __init__(self, diretorio_saida="data/output"):
        self.diretorio_saida = diretorio_saida
        self._criar_diretorio()
    
    def _criar_diretorio(self):
        """Cria diretório de saída se não existir"""
        if not os.path.exists(self.diretorio_saida):
            os.makedirs(self.diretorio_saida)
    
    def exportar_rota_completa(self, individuo, nome_arquivo=None):
        """
        Exporta rota completa no formato especificado no PDF
        """
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"rota_otimizada_{timestamp}.csv"
        
        caminho_completo = os.path.join(self.diretorio_saida, nome_arquivo)
        
        with open(caminho_completo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Cabeçalho conforme especificação
            cabecalho = [
                'CEP inicial', 'Latitude inicial', 'Longitude inicial',
                'Dia do vôo', 'Hora inicial', 'Velocidade',
                'CEP final', 'Latitude final', 'Longitude final',
                'Pouso', 'Hora final'
            ]
            writer.writerow(cabecalho)
            
            # Dados dos trechos
            for trecho in individuo.trechos:
                pouso = "SIM" if trecho.precisa_recarregar(0) else "NÃO"
                
                linha = [
                    trecho.origem.cep,
                    trecho.origem.latitude,
                    trecho.origem.longitude,
                    trecho.dia,
                    self._formatar_hora_csv(trecho.hora_partida),
                    trecho.velocidade,
                    trecho.destino.cep,
                    trecho.destino.latitude,
                    trecho.destino.longitude,
                    pouso,
                    self._formatar_hora_csv(trecho.get_hora_chegada())
                ]
                writer.writerow(linha)
        
        print(f"✅ Rota exportada: {caminho_completo}")
        return caminho_completo
    
    def _formatar_hora_csv(self, minutos):
        """Formata minutos para string HH:MM:SS"""
        horas = minutos // 60
        minutos_rest = minutos % 60
        return f"{horas:02d}:{minutos_rest:02d}:00"
    
    def exportar_resumo(self, individuo, historico_metricas, nome_arquivo=None):
        """Exporta resumo da execução"""
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"resumo_execucao_{timestamp}.csv"
        
        caminho_completo = os.path.join(self.diretorio_saida, nome_arquivo)
        
        with open(caminho_completo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            writer.writerow(['PARÂMETRO', 'VALOR'])
            writer.writerow(['Data execução', datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            writer.writerow(['Total pontos', len(individuo.coordenadas)])
            writer.writerow(['Distância total (km)', f"{individuo.distancia_total:.2f}"])
            writer.writerow(['Tempo total (min)', f"{individuo.tempo_total:.2f}"])
            writer.writerow(['Custo total (R$)', f"{individuo.custo_total:.2f}"])
            writer.writerow(['Número de pousos', individuo.numero_pousos])
            writer.writerow(['Dias utilizados', individuo.dias_utilizados])
            writer.writerow(['Fitness final', f"{individuo.fitness:.2f}"])
            writer.writerow(['Viabilidade', 'SIM' if individuo.viabilidade else 'NÃO'])
        
        print(f"✅ Resumo exportado: {caminho_completo}")
        return caminho_completo