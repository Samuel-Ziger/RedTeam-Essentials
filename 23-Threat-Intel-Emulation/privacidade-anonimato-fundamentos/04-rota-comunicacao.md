# 04 — A rota de uma comunicação

Uma requisição web comum atravessa mais componentes do que “cliente e site”:

```text
aplicação → sistema operacional → rede local → roteador/NAT → ISP
          → trânsito/peering → CDN/reverse proxy → aplicação → identidade
```

Antes da conexão pode haver DNS. Durante a sessão, sistemas de endpoint,
firewall, proxy corporativo, balanceador e aplicação podem gerar eventos. O
caminho de resposta pode não coincidir exatamente com o de ida.

## Endereço não é rota completa

IP escolhe o próximo encaminhamento; BGP troca alcançabilidade entre sistemas
autônomos. `traceroute` oferece uma observação parcial: respostas ICMP podem ser
filtradas, roteadores podem não responder e túneis escondem saltos internos.
Ausência de um salto na saída não significa ausência do componente.

## Onde a criptografia começa e termina

TLS geralmente termina no serviço, CDN ou proxy reverso. Uma VPN começa no
cliente e termina no gateway. Se ambos são usados, são camadas diferentes:
HTTPS ainda deve proteger o trecho do gateway ao destino.

## Matriz de observadores

Desenhe colunas para `origem`, `destino`, `DNS`, `conteúdo`, `tempo`, `volume`
e `identidade de aplicação`. Marque apenas o que cada ponto realmente vê; não
confunda acesso potencial com coleta comprovada.

## Prática segura

Desenhe a rota de um acesso HTTPS feito por seu computador. Depois insira uma
VPN e destaque quais linhas mudaram de observador e quais permaneceram iguais.

