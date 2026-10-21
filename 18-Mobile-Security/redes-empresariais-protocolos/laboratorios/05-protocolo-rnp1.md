# Lab 05 — Engenharia do RNP/1

1. derive uma tabela de testes de cada MUST da especificação;
2. execute demo e testes;
3. fragmente o vetor HELLO em todos os offsets possíveis;
4. teste length 4096 e 4097, UTF-8 inválido, flag reservada e mensagem fora de ordem;
5. proponha tipo `ACK` sem implementá-lo: valor, payload, estado e compatibilidade;
6. escreva threat model para uso hipotético sobre TLS.

**Aceite:** parser nunca aloca acima do limite, EOF parcial é erro e extensão
não muda semântica de tipos existentes.
