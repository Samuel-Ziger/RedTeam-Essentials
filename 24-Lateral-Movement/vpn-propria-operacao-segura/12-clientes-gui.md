# 12 — Windows, macOS e dispositivos móveis

Instale o cliente oficial pela loja ou site oficial indicado na documentação do
WireGuard. Verifique editor, assinatura e versão. Cada dispositivo gera a
própria chave; não envie uma configuração com chave privada por e-mail ou chat.

## Importação

O formato INI é semelhante em todas as plataformas. Antes de importar:

- confirme endpoint e chave pública do servidor por canal autenticado;
- atribua endereço exclusivo;
- revise `AllowedIPs` e DNS;
- proteja o arquivo e apague a cópia de transporte;
- nomeie o peer pelo dispositivo, não apenas pela pessoa.

QR code contém a configuração e, portanto, a chave privada do cliente. Gere e
exiba localmente em ambiente controlado; não fotografe, grave ou inclua em
documentação.

## Comportamento do sistema

Suspensão, troca de Wi-Fi/rede móvel, economia de bateria e políticas MDM podem
alterar o túnel. Teste reconexão, DNS e tráfego de fallback. Em empresa, use
distribuição gerenciada e revogação no offboarding.

## Prática

Sem expor chaves, produza um checklist específico para uma plataforma: origem
do aplicativo, armazenamento, ativação, teste, logs, revogação e desinstalação.

