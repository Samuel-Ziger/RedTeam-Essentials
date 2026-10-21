# 06 — Chaves, peers e ciclo de vida

Gere chaves no dispositivo que as usará:

```bash
umask 077
wg genkey | tee private.key | wg pubkey > public.key
chmod 600 private.key
```

A chave privada nunca sai do peer. Envie apenas a chave pública pelo processo de
provisionamento autenticado. Identifique o peer por proprietário, dispositivo,
data, finalidade, endereço de túnel e data de revisão — nunca armazene a chave
privada no inventário.

## Um dispositivo, uma chave

Compartilhar chave impede revogar apenas um dispositivo e confunde
responsabilização. Ao perder um aparelho, remova sua chave pública do servidor,
aplique a configuração e confirme que novo handshake não ocorre.

## Rotação

WireGuard não impõe calendário universal. Rotacione diante de suspeita,
offboarding, exposição, mudança de custódia ou política organizacional. Planeje
sobreposição curta entre peer antigo e novo quando disponibilidade exigir.

## Preshared key

Uma PSK opcional pode ser misturada ao protocolo. Ela é segredo adicional e
exige distribuição/rotação segura; não corrige endpoint comprometido nem gestão
ruim de chaves.

## Prática

Crie inventário fictício com dois peers e simule a revogação de um. Evidencie a
remoção da chave pública e do endereço, sem usar segredo real.

