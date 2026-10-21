# Laboratórios do módulo 03

Os cinco laboratórios transformam decisões de produto em evidência executável.
Eles são cumulativos: cada etapa reutiliza contratos da anterior, mas a entrega
deve continuar compreensível fora do seu computador e sem explicação oral.

## Regras comuns

- trabalhe somente com dados sintéticos e sem credenciais reais;
- fixe versões de toolchain e registre sistema, runtime e navegador usados;
- mantenha `stdout` para resultados e `stderr` para diagnóstico em CLIs;
- execute primeiro o caminho feliz e depois ao menos três falhas deliberadas;
- não apague o dado anterior para “resolver” migração, importação ou upgrade;
- produza instruções reproduzíveis de execução, teste e recuperação;
- preserve evidências em `evidencias/lab-0N/`, sem binários grandes no Git.

Uma evidência válida contém comando, entrada sintética, resultado esperado,
resultado observado e interpretação. Captura de tela isolada não substitui
teste, log textual ou descrição do cenário.

## Percurso e portas de entrada

| Laboratório | Conteúdo necessário | Produto observado |
|---|---|---|
| [01](lab-01-contrato-cli-configuracao.md) | capítulos 00–03 e exemplos | contrato de produto, CLI, configuração e erros |
| [02](lab-02-dados-estado-gui.md) | Lab 01 e capítulos 04–06 | documento versionado, estado e fronteira de GUI |
| [03](lab-03-web-acessivel-offline-i18n.md) | Lab 02 e capítulos 07–10 | interface web acessível, resiliência e localização |
| [04](lab-04-diagnostico-distribuicao-desempenho.md) | Lab 03 e capítulos 11–15 | diagnóstico, extensão, pacote, perfil e release |
| [05](lab-05-capstone-aplicacao-profissional.md) | percurso completo | aplicação profissional defendida por evidências |

## Convenção de entrega

Use esta estrutura ou uma equivalente explicada no README:

```text
evidencias/lab-0N/
├── README.md              # ambiente, hipóteses, comandos e conclusão
├── casos/                 # entradas pequenas e não sensíveis
├── resultados/            # saídas estáveis ou relatórios
└── decisoes/              # ADRs e trade-offs
```

O arquivo de evidência deve responder: qual contrato foi testado, como a falha
foi provocada, que estado permaneceu válido e como outra pessoa reproduz o
resultado? Use o [guia de diagnóstico](../GUIA-DIAGNOSTICO.md) quando algo não
se comportar como previsto.

## Avaliação transversal

Cada laboratório vale 20 pontos:

- 5: contrato e critérios de aceite verificáveis;
- 5: implementação separa domínio de entrada, apresentação e adaptadores;
- 4: testes cobrem sucesso, fronteiras e falhas sem depender de ordem;
- 3: acessibilidade, privacidade e recuperação foram verificadas;
- 3: documentação permite execução e diagnóstico por outra pessoa.

Resultado abaixo de 15 pede correção antes do próximo laboratório. Não é uma
penalidade: a porta existe para evitar carregar um contrato frágil para etapas
mais caras.
