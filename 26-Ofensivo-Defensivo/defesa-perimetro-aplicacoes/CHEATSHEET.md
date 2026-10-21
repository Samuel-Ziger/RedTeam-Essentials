# Cheatsheet operacional

## Antes da mudança

- [ ] autoridade, escopo, janela, owner e parada registrados;
- [ ] diagrama e origem real confirmados;
- [ ] baseline funcional, de segurança e latência salvo;
- [ ] regra/política versionada e revisada;
- [ ] canário, rollback e observabilidade prontos;
- [ ] IPv4, IPv6, API, browser, mobile e bots legítimos considerados.

## Firewall

```text
default deny | estado | direção | origem | destino | serviço
IPv4 + IPv6 | entrada + saída | gestão | expiração | log | owner
```

## WAF

```text
host + rota + método + campo + regra + ação + versão
detectar → medir → excluir estreito → canário → bloquear → retestar
```

## Bots e rate limiting

```text
impacto de negócio > user-agent
conta/tenant/token/sessão + rede > IP isolado
volume + sequência + estado + identidade + contexto
observe → rate limit → challenge → restringir → bloquear
```

## Turnstile

```text
Siteverify no servidor | uso único | <= 300 s | hostname | action
segredo fora do cliente/repo | chaves de teste no ambiente de teste
```

## Identidade

```text
WebAuthn/passkeys para admins | TOTP não é phishing-resistant
step-up para cadastrar/remover fator | recovery code de uso único
break-glass monitorado | sessões antigas revogadas quando necessário
```

## Evidência

Registre `request_id`, tempo UTC, rota, regra, ação, razões, versão e resultado.
Não registre senha, cookie, token ou corpo completo por padrão.
