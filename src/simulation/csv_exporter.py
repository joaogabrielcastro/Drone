import csv
import os
from datetime import datetime
from ..config.settings import Config

class CSVExporter:
    """Exporta resultados no formato CSV - SOBRESCREVE arquivos existentes"""
    
    def __init__(self, diretorio_saida="data/output"):
        self.diretorio_saida = diretorio_saida
        self._criar_diretorio()
    
    def _criar_diretorio(self):
        """Cria diretório de saída se não existir"""
        if not os.path.exists(self.diretorio_saida):
            os.makedirs(self.diretorio_saida)
    
    def exportar_rota_completa(self, individuo):
        """
        Exporta rota completa - SOBRESCREVE rota_otimizada.csv se existir
        """
        caminho_completo = os.path.join(self.diretorio_saida, "rota_otimizada.csv")
        
        # Verificar se arquivo já existe
        if os.path.exists(caminho_completo):
            print(f"📝 Sobrescrevendo arquivo existente: rota_otimizada.csv")
        else:
            print(f"✅ Criando novo arquivo: rota_otimizada.csv")
        
        # SOBRESCRITA DIRETA - modo 'w' sempre limpa o arquivo
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
            
            # Dados dos trechos - SOBRESCREVE todo o conteúdo
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
        
        print(f"✅ Arquivo atualizado: {caminho_completo}")
        print(f"   📊 {len(individuo.trechos)} trechos exportados")
        return caminho_completo
    
    def exportar_resumo(self, individuo, historico_metricas):
        """Exporta resumo - SOBRESCREVE resumo_execucao.csv se existir"""
        caminho_completo = os.path.join(self.diretorio_saida, "resumo_execucao.csv")
        
        # Verificar se arquivo já existe
        if os.path.exists(caminho_completo):
            print(f"📝 Sobrescrevendo arquivo existente: resumo_execucao.csv")
        else:
            print(f"✅ Criando novo arquivo: resumo_execucao.csv")
        
        # SOBRESCRITA DIRETA
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
            
            # Adicionar métricas da evolução
            if historico_metricas:
                melhor_inicial = historico_metricas[0]['melhor_fitness']
                melhor_final = individuo.fitness
                melhoria = ((melhor_inicial - melhor_final) / melhor_inicial * 100) if melhor_inicial > 0 else 0
                writer.writerow(['Melhoria (%)', f"{melhoria:.1f}"])
                writer.writerow(['Gerações executadas', len(historico_metricas)])
        
        print(f"✅ Arquivo atualizado: {caminho_completo}")
        return caminho_completo
    
    def exportar_metricas_evolucao(self, historico_metricas):
        """Exporta métricas de evolução - SOBRESCREVE metricas_evolucao.csv se existir"""
        caminho_completo = os.path.join(self.diretorio_saida, "metricas_evolucao.csv")
        
        # Verificar se arquivo já existe
        if os.path.exists(caminho_completo):
            print(f"📝 Sobrescrevendo arquivo existente: metricas_evolucao.csv")
        else:
            print(f"✅ Criando novo arquivo: metricas_evolucao.csv")
        
        # SOBRESCRITA DIRETA
        with open(caminho_completo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Cabeçalho
            writer.writerow(['geracao', 'melhor_fitness', 'pior_fitness', 'fitness_medio', 
                           'melhor_distancia', 'melhor_tempo', 'taxa_viabilidade'])
            
            # Dados - SOBRESCREVE todo o histórico
            for i, metrica in enumerate(historico_metricas):
                writer.writerow([
                    i + 1,
                    metrica['melhor_fitness'],
                    metrica['pior_fitness'],
                    metrica['fitness_medio'],
                    metrica.get('melhor_distancia', 0),
                    metrica.get('melhor_tempo', 0),
                    metrica.get('taxa_viabilidade', 0)
                ])
        
        print(f"✅ Arquivo atualizado: {caminho_completo}")
        print(f"   📈 {len(historico_metricas)} gerações registradas")
        return caminho_completo
    
    def _formatar_hora_csv(self, minutos):
        """Formata minutos para string HH:MM:SS"""
        horas = minutos // 60
        minutos_rest = minutos % 60
        return f"{horas:02d}:{minutos_rest:02d}:00"
    
    def verificar_arquivos_existentes(self):
        """Mostra quais arquivos existem no diretório"""
        try:
            arquivos = [f for f in os.listdir(self.diretorio_saida) if f.endswith('.csv')]
            if arquivos:
                print(f"📁 Arquivos existentes em {self.diretorio_saida}:")
                for arquivo in arquivos:
                    caminho = os.path.join(self.diretorio_saida, arquivo)
                    tamanho = os.path.getsize(caminho)
                    print(f"   • {arquivo} ({tamanho} bytes)")
            return arquivos
        except Exception as e:
            print(f"❌ Erro ao verificar arquivos: {e}")
            return []