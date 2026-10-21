# 16 — CAPTCHA, Turnstile e step-up

Desafio é uma resposta de risco, não autenticação nem autorização. Ele adiciona
custo à automação, mas também fricção, dependência, coleta de sinais e barreiras
de acessibilidade. Use apenas em jornadas humanas e quando controles menos
intrusivos não bastarem.

## Fluxo correto do Turnstile

```text
browser recebe widget/sitekey → obtém token curto
browser envia token junto da operação → servidor chama Siteverify
servidor valida success + hostname + action + idade + uso único
servidor decide sobre a operação; token não vira sessão
```

Validação no servidor é obrigatória. A documentação atual informa tokens de
uso único e validade de cinco minutos. O segredo fica no backend; a sitekey é
pública. Use chaves oficiais de teste no desenvolvimento e nunca versione o
segredo real.

## Anti-replay e binding

Verifique `hostname` e `action` esperados e rejeite token usado ou velho. Uma
resposta `success` sem binding pode ser aceita no fluxo errado. Associe a
validação à operação de curta duração, sem transformar fingerprint em identidade.

## UX, privacidade e falha

Forneça alternativa acessível e suporte. Defina comportamento quando o provedor
está indisponível: rotas de baixo risco podem degradar; recuperação de conta ou
pagamento pedem outra camada. Não coloque CAPTCHA em toda API.

## Purple Team

Red testa localmente token ausente, expirado, repetido, hostname e action
incorretos usando respostas sintéticas. Blue verifica motivo sem registrar o
token. Purple mede abandono, solve rate, acessibilidade e falso positivo antes
de ampliar o rollout.
