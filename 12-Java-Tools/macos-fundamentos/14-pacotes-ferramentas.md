# 14 — Pacotes e ferramentas de desenvolvimento

Command Line Tools fornece compiladores e utilitários Apple. Xcode inclui SDKs,
simuladores, depurador e IDE. Gerenciadores de terceiros como Homebrew não fazem
parte do macOS e devem ser tratados como supply chain adicional.

```zsh
xcode-select -p
xcrun --find clang
clang --version
pkgutil --pkgs
```

Antes de adicionar uma dependência, responda: por que a ferramenta nativa não
basta, quem mantém, como a versão é fixada, quais scripts são executados, onde
arquivos são gravados e como remover. Não execute instaladores de rede no curso.

Rosetta pode ser requisito de uma ferramenta Intel, mas não é uma correção
universal. Prefira binários nativos ou universais e registre arquitetura.

## Prática

Inventarie somente as ferramentas já instaladas. Crie uma tabela com origem,
versão, arquitetura, licença, atualizador e dependentes. Não atualize durante o
inventário.
