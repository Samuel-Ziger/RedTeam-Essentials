# Lab 06 — Capstone de recuperação local

**Classe: C — integração e falha cega reversível.**

Este é o gate final. Ele não repete comandos isolados: outra pessoa deve usar o
runbook para operar e recuperar a VM sem conhecimento oral. O cenário permanece
local, doméstico e sem dados reais.

## Pré-requisitos e equipe

Conclua os cinco gates, os 18 capítulos, o caderno, o guia e o projeto de
referência. Forme dois papéis: operador documenta a baseline; revisor escolhe e
injeta uma falha permitida, guardando o gabarito até a conclusão.

Tenha snapshots `capstone-limpo` e `capstone-pronto`, segundo disco de dados,
backup separado, manifests e recovery key armazenada fora da evidência quando
aplicável. Pare se qualquer pré-condição não puder ser demonstrada.

## Contrato de serviço

Defina usuário fictício, documentos, dois aplicativos confiáveis, necessidades
de acessibilidade, RPO, RTO e critérios de aceite. O contrato deve declarar que
contas pessoais, compartilhamentos, domínio, administração remota e configuração
de conectividade não fazem parte do projeto.

## Construção da baseline

1. Execute e valide o inventário sanitizado.
2. Registre boot confiável, TPM e BitLocker com distinção de estados.
3. Prove uso cotidiano com conta comum e elevação pontual.
4. Manifeste arquivos e documente ACL efetiva da fixture.
5. Inventarie aplicativos, procedência, assinatura e rollback.
6. Registre Update e Defender sem reduzir proteção.
7. Execute backup, restaure em caminho novo e meça RPO/RTO.
8. Entregue runbook com critérios de parada e árvore de recuperação.

O revisor compara entregáveis à rubrica do capítulo 17 e só então autoriza a
injeção.

## Falha cega permitida

O revisor sorteia uma opção: arquivo de fixture excluído/alterado, ACE incorreta
na pasta de fixture, segundo volume abaixo do limiar por arquivo sintético ou
entrada inválida que impeça a fixture de abrir. A alteração deve ser única,
reversível e não tocar arquivos do sistema.

O revisor registra comando/ação, hora UTC, hash antes/depois e rollback em arquivo
separado. Não escolhe crash, serviço central, Registro real, malware, exclusão do
Defender, disco do sistema ou perda deliberada da recovery key.

## Diagnóstico pelo operador

1. Receba apenas a descrição do sintoma.
2. Marque estado inicial e preserve logs.
3. Escreva ao menos três hipóteses e testes discriminadores.
4. Execute primeiro o teste de menor impacto.
5. Atualize probabilidades sem apagar previsões anteriores.
6. Identifique a causa ou declare incerteza com próximo teste.
7. Corrija somente a fixture afetada.
8. Valide por função, hash, acesso e comparação com baseline.
9. Peça ao revisor para revelar e comparar o gabarito.

Acertar por acaso não aprova. A linha de raciocínio precisa permitir que outra
pessoa repita a conclusão.

## Teste do runbook

Uma terceira pessoa, ou o revisor em sessão limpa, restaura um arquivo e valida
o sistema usando somente documentação. O operador não pode explicar verbalmente.
Toda ambiguidade vira melhoria no runbook e nova execução. Registre tempo real e
compare com RTO.

## Evidências e aprovação

Entregue contrato, diagrama, três inventários, manifests, matriz de ACL,
aplicativos, baseline de proteção, restore, timeline, hipóteses, gabarito da
injeção, runbook revisado e cleanup. Assine hashes do pacote de evidência apenas
como verificação de integridade, sem segredos.

Nota mínima é 80% na rubrica do capítulo 17, sem falha automática. Reprova se
usar privilégio administrativo continuamente, operar fora de fixture, reduzir
proteção, apagar logs, expor segredo, declarar restore não testado ou receber
ajuda oral no teste do runbook.

## Cleanup final

Remova contas, ACEs, chaves e fixtures temporárias, valide preferências de
segurança e restaure `capstone-limpo`. Compare inventário final ao inicial. Guarde
somente documentação sanitizada. O gabarito registra cada remoção e qualquer
diferença residual.

## Questões de defesa

1. Qual evidência sustenta a causa e qual apenas se correlaciona?
2. Que falha compartilhada ainda existe na estratégia de backup?
3. Por que o runbook funcionou ou falhou sem explicação oral?
4. Qual ação teve maior risco e como foi contida?
5. O que você mudaria antes de operar um computador real?
