# 14 — Contas, contexto e correlação

Uma conta é um vínculo explícito. Se o objetivo é impedir que a aplicação saiba
quem é o usuário, autenticar com conta pessoal contradiz o objetivo, ainda que a
rede esteja protegida por VPN ou Tor. E-mail de recuperação, telefone, SSO,
pagamento e suporte também criam relações administrativas.

## Contexto técnico

Separar perfis de navegador pode reduzir mistura acidental entre trabalho e uso
pessoal. Isso é higiene e minimização, não licença para criar identidades falsas
ou violar termos. Ambientes corporativos devem preferir identidades gerenciadas,
MFA resistente a phishing, dispositivos conformes e sessões auditáveis.

## Correlação comportamental

Horário recorrente, idioma, padrões de navegação e relações sociais podem ligar
contextos. Esses sinais são ambíguos e sujeitos a viés. Blue Teams devem usá-los
somente como apoio, com fontes independentes e hipóteses alternativas.

## Recuperação e suporte

Controles extremos que impedem recuperação podem piorar segurança. Modele perda
de dispositivo, revogação de sessão, recuperação de conta e contato com suporte.
Proteção sustentável inclui disponibilidade.

## Prática segura

Mapeie fluxos de login, recuperação e encerramento de sessão de uma aplicação
própria. Identifique quais campos realmente precisam ser pessoais e quais podem
ser temporários ou removidos.

