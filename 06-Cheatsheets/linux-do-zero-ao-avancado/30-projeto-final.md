# 30 — Projeto final e avaliação

## Objetivos

- integrar instalação, operação, segurança, diagnóstico e recuperação;
- entregar estado reproduzível e evidência saneada, não apenas screenshots;
- responder a falhas sintéticas com hipótese, correção e validação;
- defender decisões, limites e risco residual com base em requisitos.

## Missão

Entregar duas VMs reproduzíveis:

1. **estação:** Ubuntu LTS com desktop, ferramentas e diagnóstico;
2. **servidor:** Debian stable minimal, executando sob systemd um serviço
   acessível por loopback ou console da VM.

Uma terceira VM descartável é usada para armazenamento, boot e kernel. Nada é
publicado na Internet.

## Requisitos do servidor

### Instalação e inventário

- imagem oficial com hash/assinatura verificados;
- UEFI/GPT, layout documentado e volume criptografado se suportado pelo lab;
- hostname, fuso e sincronização corretos;
- inventário de hardware virtual, pacotes, mounts e serviços;
- snapshot inicial e console de recuperação testado.

### Contas e acesso

- uma conta humana administrativa sem login direto de root;
- uma conta de serviço sem shell interativo;
- SSH local por chave, host key validada e senha desabilitada somente após teste;
- sudo mínimo e revisado;
- ciclo de entrada e remoção documentado.

### Serviço

- aplicação local simples ou servidor HTTP estático;
- unit systemd validada, restart limitado e shutdown limpo;
- diretórios declarados e filesystem de runtime read-only quando possível;
- `systemd-analyze security` analisado e controles compatíveis aplicados;
- listener somente em loopback ou socket Unix;
- endpoint ou teste de readiness significativo.

### Armazenamento e dados

- volume de dados separado ou arquivo-imagem seguro;
- montagem persistente por UUID em clone descartável;
- uso e inodes monitorados;
- backup versionado de configuração e dados;
- restauração realizada em caminho/VM vazio;
- RPO e RTO medidos.

### Segurança e operação

- pacotes e serviços mínimos;
- atualização e reboot testados;
- exposição entre hosts explicitamente adiada para os módulos 14 a 18;
- AppArmor/SELinux em enforcement conforme distro;
- logs persistentes ou centralizados e retenção definida;
- alertas para serviço, espaço, backup e autenticação;
- runbook de deploy, rollback, incidente e recuperação.

## Provas práticas

Sem consultar comandos prontos, realize:

1. encontrar arquivo por dono, tamanho e data preservando nomes estranhos;
2. corrigir acesso por grupo sem conceder `777`;
3. identificar processo, descritores, cgroup e consumo de memória;
4. explicar `MemAvailable`, RSS, PSS, cache, swap e PSI do host;
5. recuperar uma unit que falha por usuário, caminho ou permissão;
6. diagnosticar ausência de processo versus listener versus readiness;
7. validar configuração, fazer reload e comprovar comportamento;
8. restaurar arquivo e aplicação a partir do backup;
9. iniciar kernel anterior ou modo de resgate na VM descartável;
10. explicar uma syscall observada e o caminho pelo kernel.

## Incidentes simulados seguros

O avaliador escolhe três:

- filesystem a 90% por arquivo sintético;
- arquivo apagado ainda aberto;
- unit com variável/caminho ausente;
- permissão ou contexto MAC incorreto;
- socket local já ocupado por outro processo sintético;
- arquivo de resolução local com entrada fictícia incorreta;
- chave SSH local revogada;
- backup mais recente corrompido, exigindo versão anterior;
- regressão de configuração com rollback;
- memória limitada por cgroup, sem provocar OOM no host.

Cada incidente exige linha do tempo, hipóteses, evidência, correção,
validação e prevenção.

## Entregáveis

```text
projeto-linux/
├── README.md
├── arquitetura.md
├── inventario/
├── configuracao/             # sem segredos
├── scripts/
├── systemd/
├── testes/
├── runbooks/
│   ├── deploy.md
│   ├── rollback.md
│   ├── backup-restore.md
│   └── recovery.md
└── evidencias/              # saídas saneadas
```

## Rubrica (100 pontos)

| Critério | Pontos |
|----------|-------:|
| Instalação, inventário e arquitetura | 10 |
| Arquivos, permissões e identidades | 10 |
| Pacotes, processos, memória e systemd | 15 |
| Armazenamento, boot e recuperação | 15 |
| SSH local, systemd e serviço | 15 |
| Hardening proporcional e comprovado | 10 |
| Observabilidade e troubleshooting | 10 |
| Backup restaurado com RPO/RTO | 10 |
| Clareza, testes e reversibilidade | 5 |

**Aprovação:** 75 pontos, nenhum segredo no repositório, restauração
demonstrada e nenhum requisito crítico executado no host pessoal.

## Defesa oral

Em 20 minutos, explique:

1. por que escolheu a distro e o filesystem;
2. o caminho do boot ao serviço;
3. o caminho de uma requisição e de uma leitura de arquivo;
4. como o serviço é limitado e observado;
5. qual falha seu backup não cobre;
6. como recuperaria acesso sem reinstalar;
7. qual decisão mudaria em produção.

## Exercícios de preparação

1. Faça uma revisão cruzada dos entregáveis e associe cada requisito a um
   arquivo, teste ou evidência concreta.
2. Sorteie três incidentes, limite cada diagnóstico a trinta minutos e registre
   em que ponto faltou telemetria ou documentação.
3. Recrie o servidor a partir de uma VM vazia usando somente os artefatos
   entregues e meça o tempo até o teste funcional passar.
4. Apresente a defesa oral sem comandos prontos; toda afirmação deve apontar
   para requisito, decisão, evidência e consequência.

## Checklist de conclusão

- [ ] As duas VMs podem ser recriadas e o serviço local passa no teste.
- [ ] Backup foi restaurado em destino vazio e RPO/RTO foram medidos.
- [ ] Nenhum segredo, identificador pessoal ou dado real foi versionado.
- [ ] Mudanças de boot, armazenamento e kernel ocorreram somente na VM.
- [ ] Outra pessoa executou ao menos um runbook sem ajuda informal.
- [ ] A rubrica atingiu 75 pontos sem falha crítica de recuperação.

## Conclusão real

O módulo termina quando você consegue descobrir comandos pela documentação,
explicar o mecanismo e recuperar uma falha. Memorizar uma lista extensa não é
o objetivo.
