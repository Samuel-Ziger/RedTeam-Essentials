# 16 - Segurança de CI/CD e supply chain

> Auditoria defensiva de pipelines, artefatos, dependências e identidades OIDC.
> Não inclua segredos reais nem execute workflows de repositórios terceiros.

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | DevSecOps, AppSec e Red/Purple Team avançado. |
| Pré-requisitos | Módulos 00, 07 e 08; Git e CI básicos. |
| Tempo estimado | 8 horas de leitura e 4 horas de auditoria local. |
| Ambiente | Fork/lab próprio e fixtures sem secrets. |
| Evidência final | Threat model do pipeline e patch de hardening validado. |
| Critério de conclusão | Identificar trust boundaries, aplicar três controles e testar regressão. |

## Superfícies

- eventos de PR/fork e diferença entre código confiável e não confiável;
- permissões do token do workflow e ambientes protegidos;
- actions/plugins mutáveis versus commits imutáveis;
- OIDC para cloud, audience/subject e políticas de trust;
- runners persistentes, caches, artifacts e logs;
- lockfiles, provenance, SBOM, assinatura e promoção de artefatos.

## Auditoria segura

1. Faça inventário de `on`, `permissions`, `uses`, `secrets` e runners.
2. Marque onde código não confiável alcança token, cache, artifact ou rede.
3. Reduza `permissions` para read por padrão e eleve por job.
4. Fixe actions por SHA **verificado** e automatize atualização.
5. Prefira OIDC de curta duração a chaves cloud estáticas.
6. Separe build de PR da publicação/deploy com approval e ambiente protegido.
7. Gere SBOM/provenance e verifique antes da promoção.

## Critério de parada

Pare se um teste imprimir secret, atingir cloud real, modificar branch protegida
ou executar código não confiável em runner persistente. Revogue o segredo
exposto, preserve logs mínimos e siga resposta a incidente.

## Cleanup

Remova environments, tokens, artifacts e caches de teste; destrua runner
descartável e confirme que nenhuma credencial de longa duração foi criada.


## Vídeos em português

Use estes materiais como complemento à leitura e aos exercícios do módulo. Execute demonstrações somente no laboratório ou em ativos formalmente autorizados.

1. [DevSecOps (Segurança no Ciclo de Desenvolvimento de Software) // Dicionário do Programador](https://www.youtube.com/watch?v=CCp30BD9uRo) — **Código Fonte TV**.
2. [Top 10 CI/CD Security - Protegendo a Cadeia de Suprimentos de Software](https://www.youtube.com/watch?v=GzxTiLYY69Y) — **GoHacking**.
3. [DevSecOps: Aplicando segurança em seu CI/CD com Gitlab e Horusec](https://www.youtube.com/watch?v=TuDaEBGSACs) — **Samuel Gonçalves**.
4. [Aulão de DevSecOps (Segurança em DevOps) na prática](https://www.youtube.com/watch?v=5yyy1TGvcpQ) — **TBX Tech**.
5. [CI/CD, deploy automatizado e DevSecOps: como estruturamos isso na UEEK](https://www.youtube.com/watch?v=sc3LVX3E7RI) — **UEEK Soluções Digitais**.
=======

