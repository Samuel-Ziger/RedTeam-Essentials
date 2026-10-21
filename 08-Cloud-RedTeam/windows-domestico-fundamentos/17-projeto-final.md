# 17 — Projeto final: computador local recuperável

O projeto integra instalação, inventário, identidade, armazenamento, proteção,
backup, automação e diagnóstico. O resultado não é uma VM “bonita”, mas um
sistema cujo estado pode ser explicado, alterado com controle e recuperado por
outra pessoa.

## Objetivos

- transformar requisitos de uma pessoa em configuração local justificável;
- entregar baseline sanitizada e reproduzível;
- provar backup e recuperação por exercício independente;
- diagnosticar uma falha sintética sem conhecer sua causa;
- defender decisões, limites e riscos com evidência.

## Cenário

Prepare uma VM Windows suportada para uma pessoa fictícia que trabalha com
documentos locais e dois aplicativos confiáveis. Ela precisa usar conta cotidiana
com privilégio mínimo, recuperar um arquivo alterado dentro do RPO e voltar a
trabalhar dentro do RTO. O ambiente não usa compartilhamentos, domínio,
administração remota ou configuração de conectividade.

Defina perfil, acessibilidade, tipos de documento, capacidade, RPO, RTO e
restrições antes de configurar. Não use dados reais nem credenciais pessoais.

## Fase 1 — arquitetura e baseline

Crie diagrama de firmware, discos/volumes, contas e locais de dados. Registre
origem da mídia, edição, versão/build, arquitetura, requisitos e ciclo de suporte
consultado. Explique cada partição sem publicar identificadores.

Execute `Get-RteLocalInventory.ps1`, valide o JSON com `ConvertFrom-Json` e
confirme a ausência de hostname, usuário, serial, endereços e chaves. Guarde hash
do inventário e nome do snapshot.

## Fase 2 — operação segura

Configure uma conta comum para uso cotidiano e mantenha elevação separada.
Construa a pasta de fixtures com ACL mínima e manifeste os arquivos. Inventarie
aplicativos por editor, versão, origem, assinatura e método de remoção. Registre
estado de Update, Defender, Secure Boot, TPM e BitLocker quando suportados,
distinguindo ausente, não consultável e desativado.

Não altere serviço do sistema, Registro fora da chave de laboratório nem
proteção para “otimizar”. Preferências de acessibilidade devem derivar do perfil
da pessoa e ser testadas naquela conta.

## Fase 3 — continuidade

Desenhe estratégia 3-2-1 simulada com mídias virtuais independentes, retenção,
RPO/RTO e localização da recovery key. Execute `Backup-RteFixture.ps1` com
`-WhatIf`, depois faça a cópia real. Altere e exclua fixtures de trabalho e
restaure em um terceiro caminho.

Compare manifests, abra amostras, meça tempo e registre divergências. O backup
não é aprovado se a restauração depender de explicação oral ou sobrescrever a
única cópia.

## Fase 4 — falha cega

Uma segunda pessoa escolhe uma falha reversível:

- arquivo de fixture excluído ou alterado;
- ACL incorreta apenas na pasta de fixture;
- segundo volume abaixo do limiar de espaço;
- aplicativo nativo/fixture que falha ao abrir por entrada controlada.

Ela registra a injeção separadamente. Você recebe apenas o sintoma. Marque hora,
preserve evidência, construa ao menos três hipóteses e teste a mais barata que
as distingue. Corrija somente a causa, valide função e execute rollback da
injeção. Não provoque crash, toque arquivo do sistema, limpe log ou desative
proteção.

## Entregáveis

1. contrato do cenário, escopo e critérios de aceite;
2. ficha de edição/build/hardware e fonte de suporte;
3. diagrama de boot, volumes, contas e dados;
4. inventário JSON sanitizado e schema explicado;
5. matriz de aplicativos, procedência e rollback;
6. baseline de Update, Defender, Secure Boot/TPM e BitLocker;
7. plano 3-2-1 com RPO/RTO e restauração validada;
8. linha do tempo e relatório da falha cega;
9. runbook do estado normal até WinRE/reinstalação;
10. prova de cleanup e snapshot final.

O runbook deve dizer o que observar, quando parar, como identificar alvos e como
validar. Uma sequência de comandos sem decisões não é runbook.

## Rubrica

| Critério | Peso | Evidência mínima |
|---|---:|---|
| segurança e reversibilidade | 20% | alvos, classes de risco, snapshots e cleanup |
| modelo técnico | 20% | explicações corretas de boot, identidade e armazenamento |
| diagnóstico | 20% | hipóteses refutáveis, timeline e causa demonstrada ou incerteza explícita |
| backup e recuperação | 20% | restore independente, hashes, RPO e RTO medidos |
| automação | 10% | scripts legíveis, saída sanitizada e testes |
| comunicação | 10% | outra pessoa executa o runbook sem ajuda oral |

Nota mínima sugerida: 80%, sem falha automática.

## Falhas automáticas

O projeto é reprovado se usar dados reais; operar no disco errado; expor segredo;
desativar Defender, Update ou UAC; usar imagem/licença não autorizada; manter uso
administrativo cotidiano; declarar backup sem restaurar; apagar logs; ou afirmar
causa sem evidência. Corrija o processo e repita o gate afetado.

## Exercícios

1. Faça uma revisão de projeto antes da injeção e liste riscos residuais.
2. Entregue o runbook a alguém que não acompanhou a construção e observe sem ajudar.
3. Compare inventário inicial, pós-configuração e pós-recuperação.
4. Apresente uma decisão que você rejeitou e a evidência usada.
5. Grave uma defesa de dez minutos separando fato, inferência e limitação.

## Checklist de domínio

- [ ] Requisitos e critérios de aceite antecedem configuração.
- [ ] Baseline é completa, sanitizada e versionada.
- [ ] Conta cotidiana, ACL e aplicativos seguem privilégio mínimo e procedência.
- [ ] Backup foi restaurado em caminho novo por outra pessoa.
- [ ] Falha cega foi diagnosticada por hipóteses, sem tentativa aleatória.
- [ ] Runbook cobre parada segura, rollback e validação independente.
- [ ] Todos os recursos temporários foram removidos ou revertidos.
- [ ] Consigo defender limites e incertezas do projeto.
