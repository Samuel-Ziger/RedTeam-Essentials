# 17 — Tempo, volume e adversário global

Criptografia protege conteúdo, mas pacotes ainda têm tempo, direção e tamanho.
Um observador capaz de ver entrada e saída pode comparar padrões: início de
sessão, rajadas, pausas, duração e volume. Essa é uma limitação conhecida de
redes de baixa latência como Tor.

## Modelo, não garantia

“Adversário global” é uma hipótese forte: visão ampla e capacidade de armazenar
e correlacionar. Um ISP local, um site e um invasor de endpoint são modelos
diferentes. Declare qual deles importa e não presuma que adicionar saltos
elimina correlação.

## Limites da análise defensiva

Similaridade temporal gera hipótese, não autoria. Eventos populares, atualizações
automáticas e relógios desalinhados produzem coincidências. Uma análise robusta
usa janelas justificadas, qualidade de relógio, múltiplas fontes, teste contra
baseline e taxa esperada de falso positivo.

## Padding e latência

Cobertura de tráfego, padding e atraso podem reduzir alguns sinais, com custo de
banda e usabilidade. Não existe uma configuração universal. Protocolos precisam
ser avaliados formalmente; improvisar ruído pode criar um padrão ainda mais
distintivo.

## Prática segura

Use apenas os horários sintéticos da fixture. Compare duas sequências parecidas
e liste três explicações alternativas. Não capture comunicações de outras
pessoas.

