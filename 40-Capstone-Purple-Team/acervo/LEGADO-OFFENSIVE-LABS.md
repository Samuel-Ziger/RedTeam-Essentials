# Acervo legado — laboratórios ofensivos integrados

O módulo 20 contém Criptografia II. As ferramentas seguras, fixtures e o
conteúdo integrado anterior agora estão consolidados fisicamente no módulo 40.

## Ferramentas preservadas

| Ferramenta | Finalidade | Restrição |
|---|---|---|
| [`roe_scope_guard.py`](../../27-Operacoes-Seguranca-Avancadas/acervo/ferramentas/roe_scope_guard.py) | Validar alvo contra allowlist. | Não conecta à rede. |
| [`recon_correlator.py`](tools/recon_correlator.py) | Correlacionar dados de reconhecimento em JSON. | Não consulta APIs. |
| [`api_auth_matrix.py`](tools/api_auth_matrix.py) | Avaliar resultados HTTP fornecidos. | Não envia requests. |

As práticas originais continuam limitadas a fixtures, `localhost`,
`docker-lab` ou ambientes explicitamente autorizados, sempre com telemetria,
canários, kill list e cleanup.

## Operações originais

1. Correlacionar host, IP, ASN, certificado e tecnologia na fixture
   [recon.json](fixtures/recon.json), separando observação de hipótese.
2. Avaliar BOLA/BFLA na matriz
   [api-auth-results.json](fixtures/api-auth-results.json), sem enviar requests.
3. Desenhar grafo AD/cloud com precondição, evidência, privilégio, log e
   revogação, sem criar assignments reais.
4. Revisar manifests e pipelines locais por trust, tokens, privilégios, secrets
   em artifacts/cache e ausência de approval.
5. Simular pós-exploração somente com arquivo canário, staging local, kill list
   e remoção, sem PII, credencial real ou persistência oculta.

## Gate de escopo e conclusão

Antes de qualquer ação ativa, o alvo deve estar em allowlist explícita validada
por `roe_scope_guard.py`. Falha significa parar. A entrega registra telemetria,
falso positivo, canário, relatório sanitizado e cleanup verificado.

---

## Registro histórico integral

> A seção abaixo conserva o conteúdo substantivo do README anterior, com seus
> contratos, sequência, referências e avisos éticos. Ela é um registro de
> preservação e não substitui o currículo atual descrito no [README do módulo 40](../README.md).

> Prática ofensiva segura e mensurável contra fixtures, localhost ou ambientes
> explicitamente autorizados. Não inclui malware, credential theft, phishing
> weaponizado, bypass de EDR ou exploração automática de terceiros.

## Histórico — Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Estudantes intermediários/avançados que concluíram as trilhas-base. |
| Pré-requisitos | Módulos 00, 01, 03, 07, 08, 10, 13 e 14. |
| Tempo estimado | 24 horas, divididas em cinco operações curtas. |
| Ambiente | Fixtures versionadas, localhost, docker-lab ou sandbox autorizado. |
| Evidência final | Attack path, matriz de autorização, canário e relatório sanitizado. |
| Critério de conclusão | Cinco operações com scope guard, telemetria e cleanup. |

## Histórico — Ferramentas seguras incluídas

| Ferramenta | Finalidade | Restrição |
|------------|------------|----------|
| [`roe_scope_guard.py`](../../27-Operacoes-Seguranca-Avancadas/acervo/ferramentas/roe_scope_guard.py) | Validar alvo contra allowlist antes de outra ferramenta. | Não conecta à rede. |
| [`recon_correlator.py`](tools/recon_correlator.py) | Correlacionar DNS/CT/IP/ASN a partir de JSON offline. | Não consulta APIs. |
| [`api_auth_matrix.py`](tools/api_auth_matrix.py) | Encontrar BOLA/BFLA em resultados HTTP fornecidos. | Não envia requests. |

## Histórico — Operação 1 — Recon e attack surface

Use a fixture [`fixtures/recon.json`](fixtures/recon.json). Correlacione host,
IP, ASN, certificado e tecnologia:

```bash
python3 40-Capstone-Purple-Team/acervo/tools/recon_correlator.py \
  40-Capstone-Purple-Team/acervo/fixtures/recon.json
```

O resultado deve priorizar ativos com múltiplas exposições sem inferir uma
vulnerabilidade apenas pela tecnologia observada.

## Histórico — Operação 2 — Web/API authorization

Analise a matriz sintética [`fixtures/api-auth-results.json`](fixtures/api-auth-results.json):

```bash
python3 40-Capstone-Purple-Team/acervo/tools/api_auth_matrix.py \
  40-Capstone-Purple-Team/acervo/fixtures/api-auth-results.json
```

Um `2xx` para `user-a` em objeto de `user-b` é um candidato BOLA; acesso de
usuário comum a função administrativa é candidato BFLA. Confirme contexto antes
de classificar impacto.

## Histórico — Operação 3 — AD, cloud e identidade híbrida

Desenhe um grafo usando o módulo 15 e as fixtures IAM do módulo 08. Para cada
aresta, registre precondição, evidência, privilégio alcançado, log e revogação.
Não crie credenciais ou assignments reais.

## Histórico — Operação 4 — Containers e CI/CD

Compare manifests/pipelines conceituais dos módulos 10 e 16. Procure trust
excessivo, token alcançável por código não confiável, pod privilegiado, secrets
em artifact/cache e ausência de approval. A prova deve ser análise ou teste
local, nunca execução em runner de terceiros.

## Histórico — Operação 5 — Pós-exploração controlada

Use somente um arquivo canário. Registre foothold simulado, objetivo de coleta,
staging local, evidência, kill list e remoção. Não copie PII, credenciais ou
dados reais e não implemente persistência oculta.

## Histórico — Gate obrigatório de escopo

Antes de qualquer comando ativo, crie uma allowlist e valide o alvo:

```bash
printf '127.0.0.1\nlocalhost\n*.lab.local\n' > /tmp/rte-scope.txt
python3 27-Operacoes-Seguranca-Avancadas/acervo/ferramentas/roe_scope_guard.py \
  --scope /tmp/rte-scope.txt --target 127.0.0.1
```

Falha no gate significa **parar**, não contornar a validação.

## Histórico — Critérios de conclusão

- [ ] Alvos ativos passaram por allowlist explícita.
- [ ] Recon separou observação, correlação e hipótese.
- [ ] Matriz API diferenciou objeto próprio, alheio e função administrativa.
- [ ] Attack path híbrido registrou precondições e revogação.
- [ ] Canário provou impacto sem coletar dado real.
- [ ] Telemetria e falso positivo foram documentados.
- [ ] Kill list e cleanup foram verificados.

## Histórico — Vídeos em português

Use estes materiais como complemento à leitura e aos exercícios do módulo. Execute demonstrações somente no laboratório ou em ativos formalmente autorizados.

1. [Estabelecendo Conexão VPN no TryHackMe de Forma Rápida e Sem Complicação!!!](https://www.youtube.com/watch?v=EMH5dL3KoAQ) — **Cybersecurity With Mateus Novaes**.
2. [Qual plataforma é melhor: TryHackMe ou Hack The Box?](https://www.youtube.com/watch?v=fu10bMuNHKw) — **Tyler Ramsbey - Hack Smarter**.
3. [Hack The Box vs TryHackMe - para INICIANTES](https://www.youtube.com/watch?v=84lDcEDP5_U) — **SkillsBuild Security**.
4. [Pentest básico - Passo a passo completo | TryHackMe | CTF para hackers](https://www.youtube.com/watch?v=iaCfgtUF9-o) — **HackHunt**.
5. [TryHackMe vs Hack The Box A melhor plataforma revelada!](https://www.youtube.com/watch?v=OTMZM_znVh8) — **InfoSec Pat**.
