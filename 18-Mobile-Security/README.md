# 18 - Segurança mobile

> Fundamentos defensivos para Android e iOS alinhados a armazenamento, tráfego,
> identidade e privacidade. Use somente apps deliberadamente vulneráveis.

## Contrato do módulo

| Campo | Definição |
|-------|-----------|
| Público | AppSec e desenvolvedores mobile intermediários. |
| Pré-requisitos | Módulos 00 e 07; HTTP/TLS e autenticação. |
| Tempo estimado | 8 horas de leitura e 6 horas em emulador descartável. |
| Ambiente | Emulador/simulador e aplicação própria ou vulnerável de treinamento. |
| Evidência final | Threat model, três achados sanitizados e correções testáveis. |
| Critério de conclusão | Cobrir armazenamento, transporte e identidade com cleanup. |

## Checklist por superfície

1. **Dados locais:** preferências, bancos, backups, screenshots, clipboard, logs
   e Keychain/Keystore; segredos não devem ficar em texto claro.
2. **Transporte:** TLS, trust configuration, cleartext, hostname validation e
   tratamento de falhas; pinning é defesa adicional, não substituto para TLS.
3. **Identidade:** OAuth/OIDC, PKCE, biometria como desbloqueio local, expiração,
   revogação e autorização sempre validada no servidor.
4. **Plataforma:** permissions, intents/deep links, exported components, URL
   schemes, WebViews e atualizações.
5. **Privacidade:** minimização, consentimento, retenção e exclusão verificável.

## Exercício seguro

Use dados canário em um emulador. Mapeie onde o app armazena o canário, quais
requests o transportam e qual identidade o acessa. Não tente interceptar apps de
terceiros nem contornar proteções de dispositivo real.

## Referência metodológica

Use OWASP MASVS/MASTG como catálogo de requisitos e testes, registrando a versão
consultada durante o exercício. Um checklist sem modelo de ameaça não determina
risco de negócio.

## Cleanup

Apague dados do app, destrua o emulador/snapshot, revogue tokens de laboratório
e confirme que nenhum proxy ou certificado de teste permaneceu instalado.

