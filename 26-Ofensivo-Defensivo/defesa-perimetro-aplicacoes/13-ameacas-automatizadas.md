# 13 — Ameaças automatizadas e bots

Automação não é sinônimo de ataque. Search crawlers, monitores, integrações,
leitores de acessibilidade e clientes de API podem ser legítimos. O problema é
o comportamento abusivo e seu impacto no processo de negócio.

## Categorias orientadas ao impacto

- credential stuffing e tentativa distribuída de conta;
- criação de contas, spam e fraude promocional;
- scraping que viola contrato, privacidade ou capacidade;
- scalping/inventory hoarding e automação de checkout;
- carding e abuso de pagamento;
- enumeração de conteúdo ou de identificadores;
- negação de inventário, busca cara e abuso de API.

## Modele a jornada

Uma requisição isolada pode parecer normal. Observe sequência: listar item,
reservar, iniciar pagamento, falhar, trocar conta e repetir. Defina o recurso
escasso e a unidade de abuso: conta, sessão, dispositivo, tenant, token,
endereço, cartão tokenizado ou combinação.

## Bots bons e verificação

User-agent é declaração, não prova. Use mecanismo oficial de verified bots,
identidade de API, assinatura ou allowlist com owner e revisão. Não permita um
crawler em todas as rotas apenas pelo nome.

## Resposta gradual

Observar → atrasar/limitar → exigir step-up → restringir função → bloquear.
A ação depende de confiança e impacto. Uma decisão irreversível por sinal fraco
prejudica usuários sob NAT, VPN corporativa ou rede móvel.

## Exercício Purple

Red descreve uma jornada abusiva com eventos sintéticos e um budget pequeno.
Blue escolhe sinais em três camadas e uma resposta progressiva. Purple adiciona
dois fluxos legítimos parecidos para medir falso positivo.
