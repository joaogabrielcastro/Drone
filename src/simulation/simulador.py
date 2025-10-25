import datetime
from ..config.settings import Config

class Simulador:
    """Simula a execução completa de uma trajetória"""
    
    def __init__(self, drone, gerenciador_vento):
        self.drone = drone
        self.gerenciador_vento = gerenciador_vento
        self.log = []
    
    def simular_trajetoria(self, individuo):
        """Simula a trajetória completa do indivíduo"""
        self.log = []
        self._adicionar_log(f"=== SIMULAÇÃO DA ROTA ===")
        self._adicionar_log(f"Indivíduo: {len(individuo.coordenadas)} pontos")
        self._adicionar_log(f"Fitness: {individuo.fitness:.2f}")
        
        if not individuo.viabilidade:
            self._adicionar_log("❌ ROTA INVIÁVEL")
            return self.log
        
        # Executar simulação detalhada
        dia_atual = 1
        hora_atual = Config.HORA_INICIO
        bateria_atual = self.drone.calcular_autonomia(36)
        
        self._adicionar_log(f"📅 Dia {dia_atual} - Iniciando às {self._formatar_hora(hora_atual)}")
        
        for i, trecho in enumerate(individuo.trechos):
            # Verificar mudança de dia
            if trecho.dia != dia_atual:
                dia_atual = trecho.dia
                self._adicionar_log(f"📅 Dia {dia_atual} - Continuando às {self._formatar_hora(hora_atual)}")
            
            # Verificar recarga
            if trecho.precisa_recarregar(bateria_atual):
                self._adicionar_log(f"⚡ RECARGA em {trecho.origem.cep} - R$80,00")
                bateria_atual = self.drone.calcular_autonomia(36)
                individuo.numero_pousos += 1
            
            # Executar trecho
            self._adicionar_log(
                f"➡️  Trecho {i+1}: {trecho.origem.cep} → {trecho.destino.cep} | "
                f"Vel: {trecho.velocidade}km/h | "
                f"Dist: {trecho.distancia:.1f}km | "
                f"Tempo: {trecho.tempo_voo_segundos}s | "
                f"Bateria: {bateria_atual/60:.1f}min"
            )
            
            # Atualizar estado
            bateria_atual -= trecho.consumo_bateria
            hora_atual = trecho.get_hora_chegada()
            
            # Parada para fotos
            hora_atual += 1
            self._adicionar_log(f"   📸 Fotografando {trecho.destino.cep} (+72s)")
        
        self._adicionar_log(f"✅ SIMULAÇÃO CONCLUÍDA")
        self._adicionar_log(f"   Dias utilizados: {individuo.dias_utilizados}")
        self._adicionar_log(f"   Pousos para recarga: {individuo.numero_pousos}")
        self._adicionar_log(f"   Custo total: R$ {individuo.custo_total:.2f}")
        self._adicionar_log(f"   Tempo total: {individuo.tempo_total:.1f} min")
        
        return self.log
    
    def _adicionar_log(self, mensagem):
        """Adiciona mensagem ao log"""
        self.log.append(mensagem)
        print(mensagem)
    
    def _formatar_hora(self, minutos):
        """Formata minutos para string HH:MM"""
        horas = minutos // 60
        minutos_rest = minutos % 60
        return f"{horas:02d}:{minutos_rest:02d}"
    
    def salvar_log(self, arquivo="log_simulacao.txt"):
        """Salva log em arquivo"""
        with open(arquivo, 'w', encoding='utf-8') as f:
            for linha in self.log:
                f.write(linha + '\n')
        print(f"✅ Log salvo em: {arquivo}")