# 12 — E-mail e colaboração

Incidentes de e-mail exigem cabeçalhos, logs do provedor, autenticação, regras de
caixa, consentimentos OAuth, encaminhamentos, mensagens e ações do usuário.

## Cabeçalhos

Preserve mensagem original no formato apropriado. `Received` forma uma cadeia,
mas campos adicionados por remetente podem ser falsificados; interprete a partir
dos servidores confiáveis. SPF, DKIM e DMARC avaliam domínio/caminho e assinatura,
não garantem intenção ou segurança do conteúdo.

## Comprometimento de conta

Procure login, emissão de sessão, criação de regra, delegação, consentimento de
aplicativo, envio, exclusão e mudança de MFA. Um e-mail enviado pela conta pode
resultar de token roubado.

## Colaboração

Links, compartilhamentos e aplicativos integrados geram audit logs. Preserve ID
do objeto, tenant, principal e ação; evite baixar conteúdo pessoal além do
necessário.

## Prática

Com fixture fictícia, construa timeline de login → regra de encaminhamento →
mensagem. Defina contenção e comunicação sem expor destinatários.

