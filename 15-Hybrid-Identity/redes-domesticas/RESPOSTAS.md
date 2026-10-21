# Respostas orientativas

## Capítulo 04

O plano proposto separa infraestrutura, reservas e dinâmicos, tornando conflitos
e inventário mais simples. Não é obrigatório e desperdiça endereços se aplicado
sem necessidade; a documentação é mais importante que a numeração escolhida.

## Capítulo 09

Todo port forward precisa de serviço/dono, origem, porta externa/interna,
autenticação, atualização, logs, data de revisão e alternativa. UPnP sem
inventário e administração WAN elevam o risco.

## Projeto

Uma boa resposta não presume que “guest” isola IPv6/cliente. Ela define fluxos,
testa os dois protocolos e prevê descoberta controlada quando um controlador
precisa encontrar IoT. CGNAT impede entrada IPv4 simples; não justifica expor
serviço por IPv6 sem firewall/autenticação.
