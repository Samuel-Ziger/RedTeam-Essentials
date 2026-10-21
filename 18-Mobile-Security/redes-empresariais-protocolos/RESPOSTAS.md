# Respostas orientativas

## Capítulo 05

Use endereços estáticos/anycast documentados para NTP/DNS de bootstrap e evite
que resolução inicial dependa do próprio serviço quebrado. Certificados exigem
tempo aproximado correto; RTC/bootstrap seguro antecede sincronização fina.

## Capítulo 11

Dois links de 10 Gbit/s fornecem 20 Gbit/s agregados apenas se hashes/fluxos
distribuírem; no estado N-1 restam 10 Gbit/s. Pico de 12 Gbit/s exige limitar,
degradar classe ou aumentar capacidade para cumprir o objetivo durante falha.

## Projeto

Uma entrega forte conecta requisito a controle e a SLI, calcula falha, evita
dependências circulares e testa rollback. A extensão RNP/1 preserva parsing de
versão anterior ou negocia nova versão; não reutiliza tipo com nova semântica.
