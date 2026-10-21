# Laboratórios progressivos — engenharia de software

Estes cinco laboratórios convertem conceitos em evidência reproduzível. Eles
não pedem apenas uma implementação que produz a saída esperada: cada entrega
precisa declarar contrato, hipótese de custo, invariantes, testes, limitações e
uma decisão justificável.

| Laboratório | Pergunta central | Evidência principal |
|---|---|---|
| [01 — contrato e complexidade](lab-01-contrato-complexidade.md) | O que significa resolver corretamente e quanto custa? | especificação, oráculo e medição |
| [02 — estruturas, busca e grafos](lab-02-estruturas-grafos.md) | A representação escolhida sustenta as operações exigidas? | implementação comparada e propriedades |
| [03 — estratégias e design modular](lab-03-estrategias-design.md) | Como separar algoritmo, política e infraestrutura? | DP, contraexemplo guloso e portas |
| [04 — evolução segura](lab-04-evolucao-arquitetura-testes.md) | Como mudar um sistema sem perder comportamento? | characterization tests, ADR e refatoração |
| [05 — Dependency Planner](lab-05-dependency-planner.md) | A solução pode ser operada, explicada e evoluída? | capstone executável e defesa técnica |

## Regra de evidência

Para cada experimento, preserve um registro curto:

```text
pergunta:
previsão:
ambiente e versão:
entrada/fixture:
comando reproduzível:
resultado essencial:
explicação:
limitação:
teste permanente:
```

Uma captura de tela isolada não é suficiente. Outra pessoa deve conseguir
reproduzir a conclusão a partir do repositório e dos comandos registrados. Não
inclua nomes, credenciais ou dados reais nas fixtures.

## Linha de base executável

Na raiz do repositório:

```bash
bash 02-OSINT/engenharia-software/testar-curso.sh
```

O runner usa diretório temporário para builds e executa todas as toolchains
disponíveis. `SKIP` significa que uma ferramenta não está instalada; não
significa que aquela implementação foi validada. Para uma entrega formal,
execute em CI com todas as versões declaradas pelo curso.

## Definição global de concluído

- a linha de base passa antes e depois da mudança;
- casos válidos, limites e entradas inválidas estão cobertos;
- a complexidade declarada corresponde à representação real;
- a saída é determinística quando o contrato promete determinismo;
- erros esperados não aparecem como stack trace ou estado parcial;
- benchmark separa aquecimento, geração de entrada e região medida;
- commits e documentos registram o motivo, não apenas o que mudou;
- todo artefato temporário pode ser removido sem afetar outros projetos.

