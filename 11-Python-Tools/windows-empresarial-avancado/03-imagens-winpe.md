# 03 — Engenharia de imagens WIM, VHDX e WinPE

WIM armazena uma ou mais imagens baseadas em arquivos com single-instance
storage; VHDX representa disco/blocos; WinPE é ambiente mínimo de setup/reparo.

## Thin image

Prefira imagem Microsoft limpa + atualizações + automação de aplicativos e
políticas. Imagem "golden" espessa envelhece rapidamente e esconde procedência.

## Pipeline

1. fixe ISO/ADK/WinPE por versão e hash;
2. monte cópia da imagem, nunca o original;
3. aplique updates/drivers/features suportados;
4. examine pending actions e component health;
5. desmonte com commit somente após validação;
6. teste boot/Setup/OOBE/rollback em VM;
7. gere manifesto, hashes, SBOM quando possível e changelog;
8. assine/promova o release.

## WinPE

Inclua apenas componentes/drivers necessários. Mídia de boot é privilegiada:
controle acesso, versão, assinatura, expiração e descarte.

## Exercício

Desenhe o pipeline e a proveniência. Não armazene ISO/WIM no repositório.

