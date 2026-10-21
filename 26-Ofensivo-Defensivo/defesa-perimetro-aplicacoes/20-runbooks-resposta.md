# 20 — Runbooks e resposta a incidentes

WAF, firewall e bot management reduzem risco, mas também podem causar incidente
por regra incorreta. Runbook precisa tratar abuso real e falha do controle.

## Triagem

1. confirme impacto, SLO e rotas afetadas;
2. preserve request/rule IDs, versão e linha do tempo;
3. diferencie aumento legítimo, automação abusiva, erro de aplicação e mudança;
4. verifique edge, origem, identidade e dependências;
5. escolha resposta reversível e proporcional.

## Respostas possíveis

- ampliar cache ou modo degradado;
- limitar rota/operação e preservar clientes confiáveis;
- exigir step-up em jornada humana;
- revogar token/credencial comprometida;
- aplicar regra temporária com owner e expiração;
- restaurar ruleset anterior quando o controle causa impacto.

Bloquear país, ASN ou user-agent inteiro pode criar dano maior. Registre
hipótese, confiança, efeitos colaterais e critério de reversão.

## Comunicação

Separe fatos observados de inferências. Informe serviço, impacto, janela,
mitigação, próxima atualização e owner. Não atribua uma pessoa por IP ou
fingerprint.

## Pós-incidente

Remova exceção temporária, corrija a aplicação, atualize testes, revise retenção
e meça tempo de detectar/mitigar/recuperar. Um incidente bem contido ainda
pode revelar falta de proteção da origem ou de auditoria administrativa.

## Tabletop Purple

Simule, em papel, credential stuffing seguido de regra excessiva que bloqueia
usuários legítimos. Red fornece sinais, Blue opera o runbook e Purple injeta a
falha do provedor de desafio. Avalie decisões, não heroísmo.
