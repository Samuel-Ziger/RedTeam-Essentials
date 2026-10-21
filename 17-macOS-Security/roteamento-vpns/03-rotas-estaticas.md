# 03 — Rotas estáticas, default e sumarização

Rotas conectadas surgem de interfaces; estáticas são declaradas pelo operador;
default cobre destinos sem rota mais específica. Uma rota estática flutuante
tem preferência pior e serve como backup, mas precisa de detecção adequada:
interface up não prova que o destino remoto está acessível.

Sumarização agrega prefixos contíguos alinhados e reduz estado/instabilidade.
Anunciar resumo sem possuir todos os componentes pode criar blackhole. Uma rota
para null no agregador impede loop, enquanto rotas específicas encaminham partes
existentes.

Rotas estáticas são previsíveis em redes pequenas, default de stub e caminhos
fixos. Escalam mal com muitas mudanças e não carregam sozinhas informação de
falha ponta a ponta.

## Exercício

Resuma `10.20.0.0/24` a `10.20.3.0/24`; depois mostre por que incluir apenas
`.0/24` e `.2/24` no mesmo resumo pode descartar destinos inexistentes.
