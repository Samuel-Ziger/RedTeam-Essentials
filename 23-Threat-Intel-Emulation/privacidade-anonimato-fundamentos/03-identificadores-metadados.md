# 03 — Identificadores e metadados

O endereço IP é apenas um identificador entre muitos. Serviços podem receber ou
derivar:

- conta, e-mail, telefone, chave pública e identificador de sessão;
- cookies, local storage, tokens e IDs de publicidade;
- IP/porta, ASN, horário, volume e sequência de requisições;
- user-agent, idioma, fuso, tamanho de tela, fontes e capacidades gráficas;
- modelo do dispositivo, versão do aplicativo e notificações push;
- padrões de uso, contatos, deslocamentos e relações entre contas.

Metadados podem revelar mais quando combinados. Um evento isolado em um IP VPN
tem baixa força identificadora. A mesma sessão com conta autenticada, cookie
persistente e dispositivo conhecido sustenta uma hipótese muito mais forte.

## Ciclo de vida

Classifique cada dado como coletado, transmitido, armazenado, compartilhado e
eliminado. Pergunte finalidade, base legal, retenção, acesso e possibilidade de
correção. Hash não anonimiza automaticamente: valores estáveis continuam
ligáveis e dados com pouco espaço de busca podem ser reidentificados.

## Minimização prática

- não colete o que não é necessário;
- use identificadores de curta duração quando o negócio permitir;
- separe telemetria operacional de identidade;
- agregue antes de reter;
- limite acesso e registre consultas;
- expire dados e valide a expiração.

## Prática segura

Faça um inventário de uma aplicação que você controla. Para cada campo,
registre origem, finalidade, retenção e poder de correlação.

