# 13 — DNS pelo túnel

Escolha uma política, não apenas um endereço de DNS:

- resolvedor público alcançado pelo gateway;
- resolvedor local na VPN;
- resolvedor corporativo para zonas internas;
- split DNS com domínios explícitos.

O campo `DNS` de `wg-quick` depende de integração do sistema (`resolvconf` ou
equivalente). Em desktops, NetworkManager/systemd-resolved podem gerir rotas de
DNS. Verifique o estado real:

```bash
resolvectl status
resolvectl query example.test
```

## Resolver local

Se operar seu próprio resolvedor, limite escuta e recursão aos clientes
autorizados; não crie um resolvedor aberto. Atualize, monitore e defina política
de cache/logs com minimização.

## Bootstrap

Um endpoint por hostname precisa de DNS antes do túnel subir. Registre esse
fluxo. Fixar IP remove a consulta, mas exige processo para mudança de endereço.

## Falha

Decida se ausência do resolvedor deve bloquear consultas ou recorrer à rede
física. Em cenário sensível, fallback silencioso contradiz a política; em
continuidade, bloqueio total pode ser inadequado. Documente a escolha.

## Prática

Teste estado antes, durante e após o túnel em seu próprio cliente. Não conclua
“vazamento” sem comparar com a política declarada.

