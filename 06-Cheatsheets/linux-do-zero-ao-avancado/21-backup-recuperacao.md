# 21 — Backup, restauração e recuperação

## Objetivos

- traduzir risco de perda em escopo, RPO, RTO, retenção e responsáveis;
- separar cópia, sincronização, snapshot, archive e backup recuperável;
- preservar consistência de aplicação, integridade, metadados e confidencialidade;
- provar restauração em destino vazio e registrar o tempo observado.

## Backup é capacidade de restaurar

Uma cópia sem teste de restauração é apenas uma esperança. Defina:

- **RPO:** quanto dado no tempo pode ser perdido;
- **RTO:** quanto tempo a recuperação pode levar;
- escopo: dados, metadados, configuração, segredos e software;
- consistência: crash-consistent ou application-consistent;
- retenção e imutabilidade;
- onde chaves e credenciais de restauração ficam;
- quem pode apagar origem e backups.

## Regra 3-2-1 como ponto de partida

Três cópias, dois tipos/meios e uma fora do domínio local reduzem falhas
comuns. Ambientes de maior risco acrescentam cópia offline/imutável e verificação
sem erros. A regra não substitui requisitos nem teste.

## O que precisa ser reconstruído

Classifique:

| Classe | Exemplo | Estratégia |
|--------|---------|------------|
| fonte | Git e IaC | remoto autenticado + backup |
| configuração | `/etc`, units, inventário | versionar sem segredos |
| estado | banco, uploads, filas | backup consistente da aplicação |
| segredos | chaves, certificados | cofre e recuperação separada |
| derivados | cache, artefato reproduzível | geralmente reconstruir |

Uma imagem de disco captura estado amplo, mas pode ser grande e inconsistente.
Backup de arquivos é granular, mas pode omitir boot, ACL, xattrs e dados de
aplicação. Combine conforme o objetivo.

## `tar`, `rsync` e ferramentas dedicadas

`tar` cria arquivo; `rsync` sincroniza árvores; nenhum fornece sozinho
catálogo, retenção, criptografia, imutabilidade e teste. Restic, Borg e soluções
corporativas adicionam recursos, mas ainda precisam de política e credenciais.

```bash
tar --xattrs --acls -C /caminho/fonte -cpf backup.tar .
tar -tf backup.tar | less
rsync -aHAXn --itemize-changes -- /fonte/ /destino/
```

As opções exigem suporte nos dois lados. Não use `--delete` até validar dry-run,
caminhos, retenção e backup anterior.

## Consistência de aplicação

Copiar arquivos de um banco em execução pode produzir conjunto inconsistente.
Use dump, API de backup, snapshot coordenado ou pausa/quiesce documentado.
Depois restaure em instância isolada e execute verificadores do banco.

Snapshot reduz a janela para coletar dados consistentes, mas continua no mesmo
domínio de falha e pode depender do volume original. Exporte-o para armazenamento
independente.

## Integridade e confidencialidade

- autentique o repositório e transporte;
- criptografe dados sensíveis em trânsito e repouso;
- guarde chaves fora do backup que elas destravam;
- registre hashes/MACs ou use formato autenticado;
- restrinja exclusão e altere credenciais comprometidas;
- monitore falha, duração, tamanho anômalo e idade do último sucesso.

Hash confirma igualdade com a referência, não que o conteúdo capturado já era
correto.

## Restauração em camadas

1. declare incidente e preserve evidência se necessário;
2. escolha ponto de recuperação anterior à corrupção;
3. prepare ambiente isolado e versões compatíveis;
4. restaure configuração, dados e metadados;
5. valide permissões, ownership, ACL, xattrs e contexto MAC;
6. execute verificação de integridade da aplicação;
7. teste funcionalmente;
8. reconecte tráfego de forma controlada;
9. monitore e documente RPO/RTO reais.

## Recuperação do sistema

Tenha mídia de instalação/resgate, inventário de partições, header LUKS,
metadados LVM/RAID, cópia de `/etc`, lista de pacotes, bootloader e credenciais
de emergência. Teste reconstruir uma VM vazia; isso encontra dependências
implícitas melhor que restaurar sempre sobre o mesmo sistema.

## Laboratório

O arquivo `exemplos/backup_versionado.sh` cria backup versionado de uma árvore
sintética sem apagar snapshots anteriores. O teste:

1. gera dados e metadados;
2. executa duas versões;
3. remove a origem;
4. restaura em outro diretório;
5. compara conteúdo;
6. mede RPO e RTO observados.

## Exercícios

1. Execute o exemplo duas vezes, restaure a versão escolhida em diretório vazio
   e compare conteúdo, permissões e checksum.
2. Modele RPO e RTO para configuração, banco e cache; explique por que as três
   classes não precisam da mesma estratégia.
3. Simule archive corrompido e demonstre que o processo recusa a cópia antes de
   substituir dados válidos.
4. Desenhe credenciais e poderes de exclusão: comprometimento da origem não
   deve permitir apagar todas as cópias.

## Checklist de domínio

Consigo explicar qual falha cada cópia tolera, provar restauração em ambiente
vazio e demonstrar que segredos e capacidade de apagar backup estão separados.
