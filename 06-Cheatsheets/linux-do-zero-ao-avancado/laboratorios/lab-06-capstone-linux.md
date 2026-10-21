# Laboratório 06 — capstone Linux reproduzível

## Missão

Construir, operar, quebrar e recuperar as duas VMs definidas no
[projeto final](../30-projeto-final.md). O capstone avalia domínio do sistema
operacional. Redes avançadas, ofensiva e exploração não fazem parte dele.
Use o [Host Observer](../projetos/host-observer/README.md) como referência de
contrato, teste, staging e operação; sua entrega pode ter implementação própria.

## Gates de entrada

- cinco laboratórios anteriores aprovados;
- caderno de práticas com evidências;
- snapshot e restauração testados;
- nenhuma credencial ou dado real no repositório;
- console independente de SSH;
- plano de oito a dezesseis horas dividido em fases.

## Fase 1 — design

Entregue requisitos, diagrama de camadas, escolha de distribuição, layout de
armazenamento, identidades, serviço local, RPO/RTO, ameaças e critérios de
aceitação. Toda escolha deve incluir alternativa rejeitada e consequência.

O serviço fica em loopback ou rede privada do laboratório. A avaliação limita-se
ao listener e à operação no host; arquitetura de endereçamento, firewall e
roteamento será desenvolvida nos módulos 14 a 18.

## Fase 2 — build reproduzível

Parta de VMs vazias e use apenas imagens oficiais verificadas. Construa:

- estação com desktop e ferramentas de diagnóstico;
- servidor mínimo com conta humana e conta de serviço;
- unidade systemd e timer validados;
- estado e configuração separados;
- volume ou imagem de dados documentado;
- automação idempotente sem segredos;
- backup versionado verificável.

Um procedimento que só funciona porque o ambiente já estava preparado não é
reproduzível.

## Fase 3 — operação

Demonstre inventário, atualização, saúde, logs, capacidade, retenção, backup e
restore. Execute o teste funcional após instalação, segunda execução, reboot,
mudança de configuração e restauração.

## Fase 4 — hardening

Mostre ameaça e evidência para cada controle. Inclua menor privilégio, superfície
mínima, sandbox da unit, proteção de arquivos, MAC suportado, atualização e
auditoria. Não é aprovado copiar uma baseline inteira sem verificar
aplicabilidade.

## Fase 5 — incidentes sorteados

Resolva quatro incidentes, um de cada grupo:

1. arquivo, permissão ou identidade;
2. processo, memória ou capacidade;
3. armazenamento, boot ou montagem;
4. unit, pacote, kernel ou dispositivo.

Use o [guia de diagnóstico](../GUIA-DIAGNOSTICO.md). Cada resposta contém
linha do tempo, hipóteses, evidência, menor correção, validação e prevenção.

## Fase 6 — reconstrução e defesa

Restaure configuração e dados em servidor vazio, meça RPO/RTO e execute o
teste funcional. Em seguida, faça a defesa oral de vinte minutos prevista no
projeto final.

## Entregáveis

~~~text
capstone-linux/
├── README.md
├── decisoes/
├── inventario/
├── configuracao/
├── scripts/
├── systemd/
├── testes/
├── runbooks/
├── backups/
└── evidencias/
~~~

Backups de entrega contêm somente dados sintéticos e não substituem o
repositório de backup da prática.

## Rubrica

| Critério | Pontos |
|----------|-------:|
| arquitetura e decisões | 10 |
| reprodução a partir do zero | 15 |
| arquivos, identidades e pacotes | 10 |
| processo, memória e capacidade | 10 |
| armazenamento, boot e recuperação | 15 |
| serviço, automação e observabilidade | 15 |
| hardening proporcional | 10 |
| backup e restauração medidos | 10 |
| documentação e defesa | 5 |

Aprovação exige 75 pontos, todos os critérios críticos de segurança, restauração
funcional e nenhuma mudança destrutiva no host pessoal.

## Checklist final

- [ ] Outra pessoa reproduziu o ambiente com os artefatos entregues.
- [ ] O serviço sobrevive a reboot e falha de configuração tem rollback.
- [ ] Restore em servidor vazio passou no teste funcional.
- [ ] Todos os comandos privilegiados possuem alvo e justificativa.
- [ ] Evidências estão saneadas e ligadas às conclusões.
- [ ] Risco residual e próximos módulos foram declarados.
