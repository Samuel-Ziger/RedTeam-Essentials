# 17 — Containers Windows e configuração como código

Container compartilha kernel do host ou usa Hyper-V isolation. Compatibilidade
entre host e image, base image e runtime é central. O curso estuda lifecycle e
filesystem local; conectividade/orquestração virão depois de redes.

## Imagem responsável

- base oficial por digest quando possível;
- menor conjunto de componentes;
- usuário/privilégio compatível com workload;
- nada de segredo na layer;
- SBOM, scan, assinatura e rebuild regular;
- dados persistentes fora da camada gravável;
- cleanup do lab.

## DSC e estado desejado

Desired State Configuration descreve recursos e convergência. Versões
PowerShell DSC 1.1/2/3 diferem; confirme documentação do ambiente. Comece com
recurso local simples e modo de teste.

Um padrão menor pode ser implementado pelo script `Set-RteLocalState.ps1` do
curso: manifesto JSON, `-WhatIf`, criação idempotente e validação.

## Exercício

Converja duas vezes um diretório de fixture; a segunda execução não deve mudar
estado. Modele uma imagem container sem executá-la se o runtime não estiver local.

