# 05 — Proxy reverso, CDN e origem

O proxy reverso recebe a conexão do cliente e inicia outra até a origem. Pode
terminar TLS, balancear, cachear, normalizar cabeçalhos e aplicar política. CDN
aproxima conteúdo e absorve parte do volume. WAF inspeciona HTTP. Esses papéis
podem estar no mesmo produto, mas continuam controles diferentes.

## Proteja a origem

Se o endereço da origem for acessível diretamente, regras da borda podem ser
irrelevantes. Combine:

- firewall permitindo somente a borda ou túnel privado;
- TLS entre edge e origem, com validação correta;
- autenticação da borda na origem quando suportada;
- segredo/certificado rotacionável, nunca como única defesa;
- nenhum DNS histórico ou serviço alternativo desnecessário;
- monitoramento de conexão que não veio do caminho esperado.

## Cabeçalhos confiáveis

A aplicação não deve aceitar `X-Forwarded-For`, `Forwarded`, host ou esquema de
qualquer cliente. O primeiro proxy confiável remove valores externos e escreve
o formato canônico. Documente a cadeia para evitar registrar o proxy como
usuário ou confiar em IP forjado.

## Cache e dados

Defina chave de cache e respostas que jamais podem ser compartilhadas. Cookies,
`Authorization`, variação por idioma e dados pessoais exigem cuidado. Purge é
operação privilegiada e precisa de auditoria.

## Exercício Purple

Red testa localmente o hostname público, a origem e uma rota alternativa
inventariada; envia cabeçalhos duplicados apenas à fixture. Blue prova qual
componente reescreveu cada campo e detecta acesso direto. Purple transforma o
resultado em teste de arquitetura executado após toda mudança de borda.
