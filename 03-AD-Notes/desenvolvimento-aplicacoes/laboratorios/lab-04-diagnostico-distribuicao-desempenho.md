# Laboratório 04 — Diagnóstico, distribuição e desempenho

## Objetivo

Preparar uma aplicação para existir fora do workspace do autor. A entrega terá
diagnóstico sanitizado, ponto de extensão controlado, artefato verificável,
orçamento de desempenho e procedimento de release/rollback.

## Etapa A — Eventos diagnósticos

Defina um pequeno catálogo de eventos. Cada evento precisa de nome estável,
versão, nível, timestamp, correlação e razão enumerada. Separe mensagem humana
de campos estruturados. Crie uma política que diga o que nunca registrar:
segredos, conteúdo livre, caminho pessoal completo e identificador sem propósito.

Implemente um logger injetável e testes que usem um canário como
`RTE_SECRET_CANARY_8472`. O canário pode entrar numa credencial falsa, mas não
pode aparecer em log, exceção, `stdout`, `stderr` ou pacote de diagnóstico.

Crie um pacote de suporte com prévia e seleção explícita. Inclua versão,
plataforma, configuração não sensível, eventos recentes limitados e resultado
de verificações. Nenhum envio de rede deve acontecer neste laboratório.

## Etapa B — Extensão controlada

Implemente um registry de exportadores, filtros ou presenters. Cada extensão
declara ID, versão, compatibilidade de API e capacidades. O host deve rejeitar
duplicata e incompatibilidade, ordenar descoberta de forma determinística e
conter falhas com contexto.

Evite carregar código arbitrário apenas para demonstrar plugin. Um registry de
objetos confiáveis já permite estudar o contrato. Se usar processo separado,
documente framing, timeout, tamanho e encerramento.

Teste:

- extensão compatível;
- ID duplicado;
- versão incompatível;
- capacidade não concedida;
- exceção durante execução;
- ordem diferente de descoberta com resultado determinístico.

## Etapa C — Artefato e proveniência

Escolha um formato apropriado: pacote de ecossistema, executável, bundle web ou
imagem de aplicação. Gere em diretório limpo e registre:

- toolchain e dependências travadas;
- comando exato;
- conteúdo esperado do artefato;
- hash SHA-256;
- SBOM ou inventário equivalente;
- instrução de instalação, atualização e remoção;
- dados preservados durante upgrade;
- assinatura/proveniência como etapa separada, se aplicável.

Teste o artefato, e não a árvore de fontes, em ambiente descartável. Não use
chave de assinatura real em laboratório local.

## Etapa D — Orçamento e profiling

Defina dispositivo/ambiente, volume, interação, percentil e limite antes de
medir. Exemplos: abrir 10 mil registros em p95 abaixo de 500 ms; filtro refletir
em até 100 ms; importação de 5 MB manter feedback e cancelamento.

Colete baseline, use profiler para localizar custo, altere uma coisa e repita.
Inclua correção funcional após otimizar. Não conclua “está rápido” com uma única
execução quente.

Provoque ao menos um problema controlado — renderização integral, serialização
repetida ou listener duplicado — e mostre como a medida aponta a causa. Remova a
falha antes da entrega.

## Etapa E — Release e rollback

Prepare uma release candidata com:

1. versão e changelog orientado ao usuário;
2. matriz app/schema/plugin/plataforma;
3. teste de instalação e smoke test;
4. migração e backup, quando houver;
5. verificação de acessibilidade essencial;
6. orçamento de desempenho;
7. hash e inventário;
8. rollout, critério de abortar e rollback;
9. canal de suporte e dados permitidos;
10. pós-verificação.

Simule uma falha depois do upgrade e execute o rollback. O dado de versão futura
não pode ser silenciosamente sobrescrito por software antigo.

## Evidências e aceite

- catálogo e exemplos de logs sanitizados;
- teste automático do canário;
- pacote de diagnóstico revisável;
- manifesto/registry de extensão e testes de isolamento;
- artefato, hash, inventário e comandos reproduzíveis;
- relatório de profiling antes/depois;
- runbook de release e transcrição de rollback.

A aprovação exige que uma máquina limpa execute o artefato, que a aplicação
continue diagnosticável sem revelar o canário, que o orçamento use medidas
repetíveis e que rollback preserve dados ou pare com instrução segura.

## Extensão avançada

Produza dois builds em ambientes limpos equivalentes e compare hashes. Quando
divergirem, investigue timestamp, ordem, locale, caminho e toolchain. Documente
o que falta para reprodutibilidade em vez de editar o hash.

## Checklist de domínio

- [ ] Eventos têm contrato e política de minimização.
- [ ] Pacote de suporte é local, pré-visualizável e sanitizado.
- [ ] Extensão incompatível falha sem derrubar o host.
- [ ] Artefato é testado fora da árvore de fontes.
- [ ] Otimização parte de baseline e termina com teste de correção.
- [ ] Release e rollback possuem critérios objetivos.
