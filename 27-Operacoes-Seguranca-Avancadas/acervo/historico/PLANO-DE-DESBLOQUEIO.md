# Plano de desbloqueio da trilha final

> **Registro histórico:** os portões necessários para a especialização de
> firewalls/WAF foram atendidos e o curso ativo está em
> `defesa-perimetro-aplicacoes/`. Este plano continua válido somente para a
> proposta mais ampla de malware/exploits simulados preservada em
> `LEGADO-OFENSIVO-DEFENSIVO.md`; ela não faz parte do módulo ativo.

## Portões curriculares

A implementação só deve começar quando houver cursos completos e testados de:

1. programação, estruturas, testes e engenharia de software;
2. APIs, bancos, aplicações e automação;
3. redes e protocolos;
4. Linux, Windows, processos, memória e permissões;
5. C e baixo nível com depuração e segurança de memória;
6. criptografia aplicada e identidade;
7. web, cloud, containers e cadeia de fornecimento;
8. logs, DFIR, threat intelligence e engenharia de detecção;
9. ética, regras de engajamento, laboratório e comunicação de risco.

## Formato obrigatório de cada unidade futura

```text
objetivo autorizado
  -> modelo de ameaça
  -> comportamento seguro/simulado
  -> telemetria esperada
  -> hipótese e regra de detecção
  -> prevenção e mitigação
  -> resposta e recuperação
  -> teste, falsos positivos e relatório
```

Nenhuma unidade ofensiva ficará sem contraparte defensiva. Toda prática deve ter
fixture sintética, limite técnico, procedimento de cleanup e critério de parada.

## Critério para iniciar

- todos os pré-requisitos possuem contrato, exercícios, respostas e CI;
- o laboratório impede egress e acesso acidental a ativos externos;
- os simuladores são incapazes de persistir, propagar ou coletar dados reais;
- cada atividade possui revisão ética e de segurança;
- existe mecanismo automatizado para validar escopo e cleanup.
