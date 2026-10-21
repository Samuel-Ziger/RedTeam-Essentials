# 14 — Sinais e classificação de automação

Ferramentas automatizadas são inferidas por combinação de sinais. Nenhum campo
isolado prova intenção ou autoria.

## Famílias de sinais

| Família | Exemplos | Limitação |
|---|---|---|
| volume | taxa, burst, concorrência | NAT agrupa pessoas; bot pode ser lento |
| sequência | ordem, profundidade, transições | usuário avançado foge do padrão |
| estado | cookie, sessão, idade, continuidade | privacidade e falhas de storage |
| cliente | JS, headers, TLS/HTTP fingerprint | versões mudam; fingerprints colidem |
| identidade | conta, token, dispositivo, tenant | credencial pode ser comprometida |
| rede | ASN, reputação, geografia | proxies corporativos e redes móveis |
| negócio | falhas, inventário, custo, conversão | requer contexto da aplicação |

JA3/JA4, user-agent e IP ajudam a agrupar, mas não devem ser tratados como
identidade forte. Sinais que perseguem unicidade também criam risco de
privacidade; aplique minimização e retenção.

## Score explicável

A ferramenta do curso soma razões transparentes e retorna `observe`,
`challenge`, `rate_limit` ou `block`. Em produção, use score para priorizar e
combinar contexto, não como verdade matemática.

```text
risco = velocidade + falhas + enumeração + anomalia de estado
        - identidade verificada - desafio recente válido
```

Separe browser de API. Ausência de JavaScript é normal para integração
autenticada; exigir cookie de navegador quebraria clientes legítimos.

## Validação

Meça precision/recall por caso de negócio, falso positivo por segmento, tempo
até decisão e impacto de latência. Reavalie drift após release de browser,
campanha, parceiro ou mudança de rota.

## Purple Team

Red altera ritmo e sequência apenas nas fixtures. Blue explica cada razão do
score. Purple rejeita classificador que não permita contestar e reproduzir uma
decisão.
