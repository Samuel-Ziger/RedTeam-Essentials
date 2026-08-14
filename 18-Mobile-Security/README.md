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

## Vídeos em português

Use estes materiais como complemento à leitura e aos exercícios do módulo. Execute demonstrações somente no laboratório ou em ativos formalmente autorizados.

1. [iPhone vs Android: Qual é o mais seguro? #hardwarehacking](https://www.youtube.com/watch?v=0tAamNaPGAg) — **Cortes TecMundo [OFICIAL]**.
2. [Android ou iPhone (iOS): Qual é o MAIS SEGURO?](https://www.youtube.com/watch?v=T4lLXfJLIew) — **Cyber Novas**.
3. [Android ou iPhone: qual é mais seguro? Hacker responde](https://www.youtube.com/watch?v=vpKMEg-Nja4) — **Cortes TecMundo [OFICIAL]**.
4. [Como Proteger seu Celular de Hackers – 10 Dicas Essenciais para Android e iPhone](https://www.youtube.com/watch?v=t_EMKgIoGx8) — **Cyber Alerta**.
5. [🤔É Realmente NECESSÁRIO usar Antivírus no Celular? (Android e iOS)](https://www.youtube.com/watch?v=bZVr2m6cj4o) — **Mestres da Informática**.
