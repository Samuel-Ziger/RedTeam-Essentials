# 06 — DNS e visibilidade

DNS traduz nomes em registros. Uma consulta tradicional pode ficar visível à
rede local, ao ISP e ao resolvedor escolhido. O resolvedor recursivo também vê
consultas e origem, salvo mecanismos de minimização ou intermediação.

## Transporte cifrado

DNS over TLS e DNS over HTTPS protegem a consulta no trecho entre cliente e
resolvedor. Isso muda quem observa o conteúdo da consulta, mas não torna o
destino invisível por si só: conexões subsequentes usam endereços, e outros
metadados de TLS ou tráfego podem contribuir para inferências.

## Dentro de uma VPN

O DNS deve seguir a política definida. Um “vazamento DNS” ocorre quando a
consulta sai por outro caminho que não o pretendido, por exemplo pelo resolvedor
da rede física. Split DNS é diferente: pode ser desenho intencional para nomes
corporativos, desde que rotas, confiança e fallback estejam documentados.

## Defesa e privacidade

Logs DNS ajudam a detectar domínios maliciosos, mas também são dados sensíveis.
Colete com propósito, retenção limitada, acesso auditado e transparência. Para
investigação, diferencie consulta, resposta, cache e conexão efetiva.

## Prática segura

Crie uma tabela com três desenhos: DNS tradicional, DoH direto e DNS dentro de
VPN. Liste rede local, ISP, resolvedor, gateway e destino; marque observação e
confiança em cada um.

