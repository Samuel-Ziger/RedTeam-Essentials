# 07 — BGP e sistemas autônomos

BGP anuncia prefixos e atributos entre peers TCP. eBGP conecta ASes; iBGP
distribui rotas externas internamente. BGP é path-vector e orientado a política,
não simplesmente “o menor caminho”.

AS_PATH ajuda prevenir loops e expressa ASes atravessados. NEXT_HOP precisa ser
alcançável. LOCAL_PREF influencia saída dentro do AS; MED sugere entrada a um
vizinho conforme política; communities carregam marcações. A ordem exata de
best-path varia por implementação.

iBGP não readvertise rotas iBGP a outros peers iBGP no modelo básico, exigindo
full mesh, route reflectors ou confederações. Route reflector reduz sessões, mas
seu desenho afeta visibilidade/diversidade de caminhos.

## Primeiro princípio

Nunca aceite/anuncie “tudo” por padrão. Defina prefixos autorizados, máximo de
rotas, atributos esperados, sessão, responsável e resposta a incidente.
