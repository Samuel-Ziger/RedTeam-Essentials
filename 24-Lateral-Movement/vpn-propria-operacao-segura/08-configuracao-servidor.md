# 08 — Configuração do servidor

Modelo de `/etc/wireguard/wg0.conf`:

```ini
[Interface]
Address = 10.66.0.1/24
ListenPort = 51820
PrivateKey = <CONTEUDO_DA_CHAVE_PRIVADA_DO_SERVIDOR>

[Peer]
# alice-laptop
PublicKey = <CHAVE_PUBLICA_ALICE>
AllowedIPs = 10.66.0.2/32
```

Não coloque `0.0.0.0/0` no `AllowedIPs` de um cliente road-warrior no servidor;
isso atribuiria a esse peer toda a rota. Cada cliente recebe endereço exclusivo.

Ative somente depois de revisar:

```bash
sudo wg-quick up wg0
sudo wg show
ip -brief address show dev wg0
```

Após teste, habilite no boot:

```bash
sudo systemctl enable wg-quick@wg0
```

## Aplicação sem interromper

`wg syncconf` pode atualizar peers sem derrubar a interface, mas configuração
persistida e runtime precisam permanecer coerentes. Em início de aprendizagem,
prefira mudança pequena, janela e validação explícita.

## Evidência

`wg show` pode revelar chaves públicas, endpoints e horários. Sanitize antes de
publicar. Nunca use `wg showconf` em relatório público sem revisão.

## Prática

Gere um template pelo planejador, compare campo a campo e explique cada
`AllowedIPs` antes de aplicar em VM.

