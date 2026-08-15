# 20 - Laboratórios ofensivos integrados

> Prática ofensiva segura e mensurável contra fixtures, localhost ou ambientes
> explicitamente autorizados. Não inclui malware, credential theft, phishing
> weaponizado, bypass de EDR ou exploração automática de terceiros.

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | Estudantes intermediários/avançados que concluíram as trilhas-base. |
| Pré-requisitos | Módulos 00, 01, 03, 07, 08, 10, 13 e 14. |
| Tempo estimado | 24 horas, divididas em cinco operações curtas. |
| Ambiente | Fixtures versionadas, localhost, docker-lab ou sandbox autorizado. |
| Evidência final | Attack path, matriz de autorização, canário e relatório sanitizado. |
| Critério de conclusão | Cinco operações com scope guard, telemetria e cleanup. |

## Ferramentas seguras incluídas

| Ferramenta | Finalidade | Restrição |
|------------|------------|----------|
| [`roe_scope_guard.py`](tools/roe_scope_guard.py) | Validar alvo contra allowlist antes de outra ferramenta. | Não conecta à rede. |
| [`recon_correlator.py`](tools/recon_correlator.py) | Correlacionar DNS/CT/IP/ASN a partir de JSON offline. | Não consulta APIs. |
| [`api_auth_matrix.py`](tools/api_auth_matrix.py) | Encontrar BOLA/BFLA em resultados HTTP fornecidos. | Não envia requests. |

## Operação 1 — Recon e attack surface

Use a fixture [`fixtures/recon.json`](fixtures/recon.json). Correlacione host,
IP, ASN, certificado e tecnologia:

```bash
python3 20-Offensive-Labs/tools/recon_correlator.py \
  20-Offensive-Labs/fixtures/recon.json
```

O resultado deve priorizar ativos com múltiplas exposições sem inferir uma
vulnerabilidade apenas pela tecnologia observada.

## Operação 2 — Web/API authorization

Analise a matriz sintética [`fixtures/api-auth-results.json`](fixtures/api-auth-results.json):

```bash
python3 20-Offensive-Labs/tools/api_auth_matrix.py \
  20-Offensive-Labs/fixtures/api-auth-results.json
```

Um `2xx` para `user-a` em objeto de `user-b` é um candidato BOLA; acesso de
usuário comum a função administrativa é candidato BFLA. Confirme contexto antes
de classificar impacto.

## Operação 3 — AD, cloud e identidade híbrida

Desenhe um grafo usando o módulo 15 e as fixtures IAM do módulo 08. Para cada
aresta, registre precondição, evidência, privilégio alcançado, log e revogação.
Não crie credenciais ou assignments reais.

## Operação 4 — Containers e CI/CD

Compare manifests/pipelines conceituais dos módulos 10 e 16. Procure trust
excessivo, token alcançável por código não confiável, pod privilegiado, secrets
em artifact/cache e ausência de approval. A prova deve ser análise ou teste
local, nunca execução em runner de terceiros.

## Operação 5 — Pós-exploração controlada

Use somente um arquivo canário. Registre foothold simulado, objetivo de coleta,
staging local, evidência, kill list e remoção. Não copie PII, credenciais ou
dados reais e não implemente persistência oculta.

## Gate obrigatório de escopo

Antes de qualquer comando ativo, crie uma allowlist e valide o alvo:

```bash
printf '127.0.0.1\nlocalhost\n*.lab.local\n' > /tmp/rte-scope.txt
python3 20-Offensive-Labs/tools/roe_scope_guard.py \
  --scope /tmp/rte-scope.txt --target 127.0.0.1
```

Falha no gate significa **parar**, não contornar a validação.

## Critérios de conclusão

- [ ] Alvos ativos passaram por allowlist explícita.
- [ ] Recon separou observação, correlação e hipótese.
- [ ] Matriz API diferenciou objeto próprio, alheio e função administrativa.
- [ ] Attack path híbrido registrou precondições e revogação.
- [ ] Canário provou impacto sem coletar dado real.
- [ ] Telemetria e falso positivo foram documentados.
- [ ] Kill list e cleanup foram verificados.

## Vídeos em português

Use estes materiais como complemento à leitura e aos exercícios do módulo. Execute demonstrações somente no laboratório ou em ativos formalmente autorizados.

1. [Estabelecendo Conexão VPN no TryHackMe de Forma Rápida e Sem Complicação!!!](https://www.youtube.com/watch?v=EMH5dL3KoAQ) — **Cybersecurity With Mateus Novaes**.
2. [Qual plataforma é melhor: TryHackMe ou Hack The Box?](https://www.youtube.com/watch?v=fu10bMuNHKw) — **Tyler Ramsbey - Hack Smarter**.
3. [Hack The Box vs TryHackMe - para INICIANTES](https://www.youtube.com/watch?v=84lDcEDP5_U) — **SkillsBuild Security**.
4. [Pentest básico - Passo a passo completo | TryHackMe | CTF para hackers](https://www.youtube.com/watch?v=iaCfgtUF9-o) — **HackHunt**.
5. [TryHackMe vs Hack The Box A melhor plataforma revelada!](https://www.youtube.com/watch?v=OTMZM_znVh8) — **InfoSec Pat**.
