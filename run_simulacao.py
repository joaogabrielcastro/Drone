from src.models.drone import Drone
from src.models.vento import GerenciadorVento
from src.models.coordenada import Coordenada
from src.models.individuo import Individuo
from src.simulation.simulador import Simulador
from src.config.settings import Config

# Montar uma rota curta: Unibrasil -> ponto1 -> Unibrasil
unibrasil = Coordenada(Config.CEP_INICIAL, -25.416, -49.273)
# Ponto a leste (~1 grau de longitude) para ter distância não trivial
ponto = Coordenada('00000002', -25.416, -49.150)
coordenadas = [unibrasil, ponto, unibrasil]

# Instanciar objetos
crane = Drone()
gerenciador = GerenciadorVento()

ind = Individuo(coordenadas, crane, gerenciador)

# Simular rota (gera trechos)
ind.simular_rota()

# Mostrar trechos escolhidos
for t in ind.trechos:
    print(f"Trecho: {t.origem.cep}->{t.destino.cep} Vel={t.velocidade} Vel_efetiva={t.velocidade_efetiva:.2f}km/h Tempo={t.tempo_voo_segundos}s")

# Rodar simulador detalhado
sim = Simulador(crane, gerenciador)
sim.simular_trajetoria(ind)

# Exemplo: alterar heurística e re-simular
print('\n-- Ajustando heurística: penalizar consumo (beta=1) --')
from src.config.settings import Config as Cfg
Cfg.HEURISTICA_ALPHA = 1.0
Cfg.HEURISTICA_BETA = 1000.0

ind2 = Individuo(coordenadas, crane, gerenciador)
ind2.simular_rota()
for t in ind2.trechos:
    print(f"Trecho: {t.origem.cep}->{t.destino.cep} Vel={t.velocidade} Vel_efetiva={t.velocidade_efetiva:.2f}km/h Tempo={t.tempo_voo_segundos}s")

sim.simular_trajetoria(ind2)
