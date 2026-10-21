# 29 — Operação de serviços Linux

## Objetivos

- transformar um processo em serviço instalável, observável e recuperável;
- controlar configuração, identidade, dados, segredos e diretórios de runtime;
- desenhar saúde, deploy, atualização e rollback com critérios objetivos;
- entregar runbook que outra pessoa consegue executar.

## Serviço é mais que um processo

Um serviço operável possui:

- requisitos e dono;
- pacote/artefato autenticado;
- configuração validável;
- identidade e permissões mínimas;
- dados e segredos com ciclo de vida;
- supervisão e limites;
- health/readiness significativos;
- logs, métricas e alertas;
- backup e restauração;
- atualização, rollback e runbook.

## Layout previsível

Uma aplicação local pode usar:

```text
/usr/local/bin/app                 executável administrado localmente
/etc/app/app.conf                  configuração
/var/lib/app/                      estado persistente
/var/cache/app/                    cache reconstruível
/var/log/app/                      logs, se não usar journal
/run/app/                          PID/socket/estado volátil
```

Pacotes da distro usam `/usr`, não `/usr/local`. systemd oferece
`StateDirectory=`, `CacheDirectory=`, `LogsDirectory=` e `RuntimeDirectory=`
para criar diretórios com ownership e ciclo corretos.

## Configuração como mudança controlada

Fluxo:

1. registrar ticket/objetivo;
2. capturar configuração efetiva e saúde;
3. preparar arquivo novo com ownership/mode;
4. validar sintaxe e semântica offline;
5. criar backup ou manter versão anterior;
6. trocar atomicamente quando suportado;
7. reload se seguro, restart se necessário;
8. validar readiness e comportamento;
9. observar janela e reverter se falhar.

Exemplos de validadores:

```bash
nginx -t 2>/dev/null
sshd -t
visudo -c
systemd-analyze verify arquivo.service
```

Um teste de sintaxe não prova conectividade, permissões, certificado ou regra de
negócio.

## Bind, proxy e TLS

Serviço interno deve ouvir apenas onde necessário. Um reverse proxy pode
terminar TLS, aplicar limites e rotear, mas acrescenta headers e trust boundary.
Defina quais proxies são confiáveis antes de aceitar `X-Forwarded-For` ou
equivalentes.

Para TLS:

- chave privada com acesso mínimo;
- cadeia completa e nomes corretos;
- renovação automatizada e monitorada;
- reload após renovação;
- protocolos/cifras segundo biblioteca e política atuais;
- teste externo e local de expiração.

## Bancos e filas

Não exponha banco por conveniência. Use identidade de serviço, privilégios por
schema/operação, TLS quando atravessa fronteira, pool limitado, timeout e
backup nativo consistente. Migração deve ser compatível com versão anterior
durante rollout ou ter janela/rollback planejados.

## Saúde

- liveness: processo deve ser reiniciado?
- readiness: instância pode receber trabalho?
- dependency health: dependência está acessível, sem tornar toda falha transitória
  em restart storm;
- synthetic check: comportamento importante funciona de fora?

Um endpoint que sempre retorna 200 não mede saúde. Um endpoint que consulta
todas as dependências pode amplificar falha.

## Deploy e rollback

Artefato deve ser versionado e imutável. Separe código de estado. Implante em
staging, depois canário/parte da frota, observe e amplie. Rollback de binário
pode não reverter migração de dados; desenhe expand/migrate/contract.

## Atualização do sistema

Agrupe hosts por ondas. Antes:

- confirme backup e console;
- leia advisories e pacotes afetados;
- verifique espaço;
- drene tráfego quando necessário;
- defina saúde e tempo de rollback.

Depois: confirme kernel/processos atualizados, units, listeners, logs, SLO e
capacidade. Automatização sem observação apenas falha mais rápido.

## Runbook mínimo

```text
Serviço e proprietário:
SLO e dependências:
Como verificar saúde:
Como localizar logs/métricas:
Como iniciar/parar/recarregar:
Como validar configuração:
Como implantar e reverter:
Onde está o backup e como restaurar:
Alertas e primeira resposta:
Escalonamento:
```

## Laboratório

Instale a unit didática apenas na VM ou use `systemd-run --user`. Demonstre:

1. conta sem login;
2. diretórios administrados pela unit;
3. serviço em foreground;
4. hardening incremental;
5. timer com atraso aleatório;
6. logs estruturados;
7. falha deliberada e diagnóstico;
8. backup e restauração da configuração.

## Exercícios

1. Empacote a unit didática em uma árvore de staging sem instalar no host e
   valide caminhos, modos e ownership pretendidos.
2. Provoque uma configuração inválida, prove que o validador impede a troca e
   preserve a versão funcional.
3. Defina liveness e readiness diferentes para um serviço local; explique por
   que reiniciar não resolve toda falha de dependência.
4. Entregue seu runbook a outra pessoa ou execute-o em VM limpa sem recorrer à
   memória; transforme cada pergunta não respondida em correção documental.

## Checklist de domínio

Consigo operar um serviço durante instalação, mudança, falha, atualização e
recuperação, sem depender da memória de quem o criou.
