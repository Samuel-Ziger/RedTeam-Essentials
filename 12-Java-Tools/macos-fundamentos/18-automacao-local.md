# 18 — Automação local segura

Automatização confiável é determinística, idempotente, observável e reversível.
zsh/Bash compõem ferramentas; Python trata dados; Shortcuts integra ações de
usuário; AppleScript/Apple events automatizam apps que expõem essa interface.

## Contrato de script

- entradas validadas e caminhos explícitos;
- modo de simulação para mudanças;
- saída estruturada e erros em canal separado;
- nenhum segredo em argumento ou log;
- pós-condição verificável;
- rollback ou falha antes da mutação.

O coletor do curso possui modo fixture: a mesma transformação recebe saídas
sintéticas nos testes e comandos reais no Mac. Isso separa coleta dependente da
plataforma da lógica verificável.

## Prática

Execute os exemplos, leia os testes e introduza uma fixture com FileVault
desativado. Confirme que o resultado muda sem alterar o computador.
