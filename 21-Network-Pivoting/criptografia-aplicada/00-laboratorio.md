# 00 — Laboratório e fronteiras de confiança

A mini-PKI usa somente `localhost` e o domínio reservado `example.test`,
diretório temporário e certificados de curta duração. A raiz de laboratório não
deve ser instalada no trust store do sistema ou navegador.

Desenhe fronteiras entre CA offline, emissora, serviço, cliente, DNS, relógio,
logs e operador. O laboratório valida estrutura e assinatura; confiança real
também exige política, custódia, auditoria e procedimento de incidente.

## Cleanup

Apague diretório temporário, confirme que nenhuma chave entrou no shell history
ou Git e remova qualquer configuração de trust criada manualmente.
