# 00 — Escopo, segurança e preflight

Implante somente em VPS/VM pertencente a você ou coberta por autorização. Leia
os termos do provedor e a legislação aplicável. Uma VPN própria não autoriza
acesso a terceiros, evasão de controles ou abuso.

## Antes da primeira mudança

- console web/serial fora de banda testado;
- snapshot ou backup e procedimento de restauração;
- usuário administrativo com chave SSH e `sudo`;
- relógio sincronizado;
- sistema suportado e atualizado;
- interface de saída identificada, sem copiar `ens3` às cegas;
- UDP escolhido permitido no firewall do provedor;
- plano de endereçamento sem sobreposição;
- janela, observador, critério de sucesso e rollback.

Execute os primeiros labs em VM local. Regras de firewall e roteamento podem
interromper SSH. Mantenha a sessão atual aberta e valide em uma segunda sessão
antes de encerrar.

## Segredos

Chaves privadas ficam com permissão `0600`, fora do Git, tickets, chat, capturas
e backups não cifrados. O curso fornece placeholders. Scanner de segredos não
substitui disciplina.

## Critério de parada

Interrompa se perder console, detectar chave exposta, observar tráfego fora do
escopo, não conseguir explicar uma regra ou encontrar configuração preexistente
que conflite com o guia.

## Prática

Preencha o checklist e escreva os comandos exatos de verificação e rollback do
seu sistema, sem executá-los ainda.

