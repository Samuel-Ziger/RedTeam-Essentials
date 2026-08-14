# 22 - Code review ofensivo e análise de dados

> Identificação manual de trust boundaries, fontes, sinks e falhas de autorização
> em código próprio ou fornecido para treinamento. Não analise código vazado.

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | AppSec, desenvolvedores e pentesters intermediários. |
| Pré-requisitos | Módulos 00, 07, 11 e uma linguagem de programação. |
| Tempo estimado | 8 horas de leitura e 6 horas de exercícios. |
| Ambiente | Código deliberadamente vulnerável e sem segredos reais. |
| Evidência final | Data-flow, prova local, patch e teste de regressão. |
| Critério de conclusão | Revisar três classes e justificar severidade/limitações. |

## Método

1. Mapeie entrypoints, identidades, assets e trust boundaries.
2. Marque **sources** não confiáveis e transformações aplicadas.
3. Encontre **sinks**: SQL, shell, template, filesystem, URL, parser e logs.
4. Verifique autorização por função, objeto e tenant.
5. Revise erros, concorrência, limites, criptografia e secret management.
6. Confirme a hipótese em teste unitário/local, não em produção.
7. Corrija na causa e escreva teste negativo.

## Catálogo prático

| Classe | Source | Sink/decisão | Correção |
|--------|--------|---------------|----------|
| SQLi | parâmetro | query construída | parâmetros tipados |
| Command injection | input/job | shell | API sem shell + allowlist |
| SSRF | URL | cliente HTTP | allowlist + resolução/redirect seguros |
| Path traversal | filename | filesystem | raiz fixa + canonicalização |
| SSTI | template | render dinâmico | templates estáticos/dados separados |
| Deserialização | bytes | object construction | formato simples + schema |
| BOLA | object ID | policy | autorização por objeto/tenant |

## Evidência e severidade

Separe alcançabilidade, controle do atacante, impacto e controles compensatórios.
Um padrão perigoso não é automaticamente explorável. Redate segredos e forneça
somente o trecho mínimo, teste e patch necessários.

## Cleanup

Remova branches/fixtures temporárias, tokens canário e builds; confirme que o
teste vulnerável falha após o patch e que nenhuma credencial entrou no histórico.

## Vídeos em português

Use estes materiais como complemento à leitura e aos exercícios do módulo. Execute demonstrações somente no laboratório ou em ativos formalmente autorizados.

1. [Como Começar em AppSec do Zero | Guia Rápido de Segurança da Informação](https://www.youtube.com/watch?v=j6OKF3DFzi8) — **HackSafeBR**.
2. [Você confia nos seus logs? Código Seguro #082 | Cássio B. Pereira](https://www.youtube.com/watch?v=SvMTUKlKdsQ) — **Cássio Batista Pereira**.
3. [Tendências de AppSec para 2026 | AppSec Webinar](https://www.youtube.com/watch?v=5xgHsnhc7As) — **Conviso Application Security**.
4. [O profissional de appsec programa no dia a dia?](https://www.youtube.com/watch?v=IZjie0THS50) — **Ben-Hur Ott**.
5. [O que é AppSec?](https://www.youtube.com/watch?v=R49E7efhoDA) — **AppSecBR**.
