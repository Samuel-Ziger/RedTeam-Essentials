# Arquitetura executável do Dependency Planner

## Contexto

Um usuário ou automação fornece um documento local e recebe um plano. O sistema
não acessa rede nem banco e não modifica o arquivo de entrada.

```text
[pessoa/CI] -- argv + arquivo --> [processo dependency-planner]
             <-- stdout/stderr + status --
```

## Componentes e dependências

```text
cli.py  ------------------------------ interface e composition root
  |                         |
  |                         `---------- apresentação text/JSON
  v
service.py --------------------------- caso de uso PlanProject
  |                  |
  v                  v
ports.py             graph.py -------- algoritmos puros
  ^                   |
  |                   v
repository.py       domain.py -------- invariantes e resultado
JSON adapter
```

As setas representam dependências de código. O núcleo não conhece terminal,
arquivo ou JSON. A porta estrutural vive em `ports.py`; o caso de uso e o adapter
dependem dela, enquanto somente `repository.py` conhece `Path` e JSON.

## Contratos por fronteira

| Fronteira | Entrada | Saída/erro | Garantia |
|---|---|---|---|
| CLI | argumentos | status + canais | resultado nunca mistura com erro |
| JSON adapter | bytes UTF-8 limitados | snapshot de `WorkItem` | schema estrito, sem campo ignorado |
| caso de uso | `WorkItemRepository` | `Plan` | orquestra sem conhecer formato |
| domínio | valores tipados | objetos imutáveis | invariantes locais |
| grafo | iterável de itens | plano ou erro tipado | ordem, lotes e caminho determinísticos |

## Fluxo válido

1. CLI interpreta argumentos.
2. Adapter lê no máximo o limite de bytes e decodifica UTF-8.
3. Schema raiz e cada item são validados.
4. Caso de uso obtém snapshot imutável.
5. Grafo rejeita IDs duplicados/referências ausentes.
6. Kahn produz ordem e lotes; ciclo gera `CycleError` com caminho fechado no
   sentido pré-requisito → dependente.
7. DP em ordem topológica calcula caminho crítico.
8. CLI serializa e escreve somente em `stdout`.

## Atributos de qualidade relevantes

- **correção:** propriedades topológicas e invariantes testadas;
- **determinismo:** IDs ordinais desempatarão resultados;
- **modificabilidade:** adapters dependem do núcleo por uma porta;
- **segurança de recursos:** limites de bytes, itens, strings e dependências;
- **diagnosticabilidade:** erros esperados têm categoria, contexto e status 2;
- **portabilidade:** biblioteca padrão Python, sem serviço externo.

O projeto não promete scheduling com recursos, calendário real, persistência,
concorrência entre processos ou execução distribuída. Essas capacidades exigem
novos contratos e decisões.
