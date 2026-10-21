# Laboratórios Linux

Os seis laboratórios avaliativos conectam os capítulos a entregas observáveis.
Eles são progressivos: concluir a leitura não libera automaticamente o próximo;
é preciso satisfazer o critério de saída do laboratório anterior.

## Classes de risco

| Classe | Ambiente | Regra |
|--------|----------|-------|
| A | usuário comum e diretório temporário | sem privilégio e teardown automático |
| B | VM principal com snapshot | mudança administrativa limitada e reversível |
| C | clone descartável com console | disco, boot, módulo ou kernel |

Container não substitui a VM nas práticas de classe C porque compartilha o
kernel e pode receber dispositivos do host.

## Rota avaliativa

| Marco | Conteúdo exigido | Produto |
|-------|------------------|---------|
| [Lab 01](lab-01-shell-arquivos-permissoes.md) | capítulos 00–08 | árvore segura, pipeline e política de acesso |
| [Lab 02](lab-02-identidades-processos-memoria.md) | capítulos 09–12 + Lab 01 | identidade, processo, sinais e relatório de memória |
| [Lab 03](lab-03-armazenamento-boot-systemd.md) | capítulos 13–16 + Lab 02 | pilha loop, recuperação de boot, unit e timer |
| [Lab 04](lab-04-operacao-hardening-isolamento.md) | capítulos 17–23 + Lab 03 | serviço local operável, backup e hardening |
| [Lab 05](lab-05-kernel-desempenho-servicos.md) | capítulos 24–29 + Lab 04 | trace, kernel, desempenho e runbook |
| [Lab 06](lab-06-capstone-linux.md) | capítulo 30 + todos os marcos | sistema reproduzido, incidentes e restore |

O [Host Observer](../projetos/host-observer/README.md) é a implementação de
referência para contrato, teste, staging, systemd, backup e operação do capstone.

## Roteiros de risco específico

Estes roteiros complementam os marcos e só devem ser usados quando a etapa
correspondente pedir:

- [armazenamento em arquivo loop](armazenamento-loop.md);
- [boot e recuperação](boot-recovery.md);
- [módulo, tracing e fallback de kernel](kernel.md);
- [integração do projeto](projeto.md).

Eles não são atalhos nem laboratórios independentes no aplicativo. O marco
avaliativo agrega pré-condições, evidências, falhas e teardown.

## Regra de mudança

Preencha antes de cada prática B ou C:

~~~text
VM confirmada:
Snapshot:
Console alternativo:
Alvo exato:
Estado antes:
Mudança:
Validação:
Rollback:
Teardown:
~~~

Pare se o alvo estiver vazio, resolver para raiz, home inteira, dispositivo
raiz ou disco não criado no próprio laboratório. Um comando destrutivo nunca
depende apenas de glob ou variável não validada.

## Padrão de evidência

Cada entrega contém:

1. objetivo e comportamento esperado;
2. versões e diagrama das camadas;
3. previsão antes dos comandos;
4. saídas textuais saneadas;
5. falha provocada e hipótese;
6. correção e teste funcional;
7. rollback ou teardown;
8. reflexão sobre o que a prática não provou.

Screenshot sozinho não demonstra mecanismo. Inclua texto pesquisável e ligue
cada conclusão à linha, estado ou teste correspondente.

## Reprovação automática

- execução de prática C no host pessoal;
- segredo, chave privada, token, serial ou dado real na entrega;
- permissão universal ou controle de segurança desativado como correção;
- backup nunca restaurado;
- única via de recuperação dependente do serviço em alteração;
- afirmação de sucesso sem teste funcional;
- alvo destrutivo não associado ao arquivo-imagem do próprio lab.
