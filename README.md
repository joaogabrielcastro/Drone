# Drone

APS faculdade.

## Heurística de escolha de velocidade (alpha / beta)

O simulador/algoritmo usa uma heurística simples para escolher a velocidade de cada trecho. O custo usado para comparar opções é:

    custo = alpha * tempo_em_minutos + beta * consumo_em_percentual

Onde:

- `tempo_em_minutos` é o tempo estimado do trecho em minutos na velocidade testada.
- `consumo_em_percentual` é a porcentagem da autonomia do drone que o trecho consumiría na velocidade testada (por exemplo, 10.0 significa 10% da bateria).

Interpretação prática:

- `alpha` controla quanto o tempo importa. Valores maiores favorecem rotas/velocidades mais rápidas.
- `beta` controla quanto a economia de bateria importa. Valores maiores favorecem velocidades que consomem menos porcentagem da autonomia.

Exemplos:

- `alpha=1, beta=0` (padrão) — prioriza minimizar tempo; o consumo não é penalizado.
- `alpha=1, beta=1` — 1 minuto de voo tem o mesmo peso que 1% de bateria consumida.
- `alpha=1, beta=100` — penaliza fortemente o consumo; o algoritmo tenderá a escolher velocidades mais econômicas.

Como ajustar:

- Você pode alterar os valores em `src/config/settings.py` (campos `HEURISTICA_ALPHA` e `HEURISTICA_BETA`).
- Ou usar o script `run_simulacao.py` que demonstra duas simulações com diferentes configurações.

Recomenda-se experimentar alguns pares (alpha,beta) e observar o trade-off tempo vs recargas para escolher uma configuração adequada ao seu objetivo.
