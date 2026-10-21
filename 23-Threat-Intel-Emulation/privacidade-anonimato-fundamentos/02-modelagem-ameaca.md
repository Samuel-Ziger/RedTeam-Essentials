# 02 — Modelagem de ameaça para privacidade

Um modelo de ameaça evita recomendações universais. Use sete campos:

| Campo | Pergunta |
|---|---|
| Ativo | Qual dado, identidade ou relação precisa ser protegido? |
| Ação | O que o usuário fará e por quanto tempo? |
| Observador | Quem pode ver qual trecho ou endpoint? |
| Capacidade | Vê uma rede, controla um serviço ou correlaciona várias fontes? |
| Consequência | O que acontece se houver exposição ou vínculo? |
| Controle | Qual mecanismo reduz esse risco? |
| Validação | Que evidência demonstra funcionamento e limitação? |

Evite adversários vagos como “a internet”. Um administrador de Wi-Fi, um
provedor VPN, uma aplicação autenticada e um invasor com controle do endpoint
têm visões e capacidades diferentes.

## Premissas e dependências

Registre sistema atualizado, origem do software, integridade do dispositivo,
proteção da conta, relógio confiável e política do provedor. Se o endpoint está
comprometido, o tráfego pode ser capturado antes de entrar no túnel. Se a conta
é identificada, mudar o IP não desfaz a associação.

## Matriz simples

Para cada observador, marque `conteúdo`, `metadado`, `identidade`, `tempo` e
`controle sobre o endpoint` como nenhum, parcial ou amplo. A ferramenta
`privacy_model.py` transforma uma fixture dessa matriz em achados reproduzíveis.

## Prática segura

Modele dois cenários próprios: administração remota de uma VPS e leitura de um
site público. Não inclua pessoas reais nem destinos sensíveis.

