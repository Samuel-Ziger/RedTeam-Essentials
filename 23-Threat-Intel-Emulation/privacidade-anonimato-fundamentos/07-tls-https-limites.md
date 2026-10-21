# 07 — TLS, HTTPS e seus limites

TLS autentica o servidor por certificados e protege confidencialidade e
integridade do transporte. HTTPS é HTTP sobre TLS. Ele evita que um observador
passivo leia ou altere o corpo da requisição entre os pontos onde TLS começa e
termina, mas não elimina todos os metadados.

## O que continua existindo

- endereços e portas necessários ao roteamento;
- horários, duração, direção e volume aproximado;
- informação exposta pela aplicação antes ou depois do túnel;
- conta, cookie e dados fornecidos ao serviço;
- logs no endpoint, CDN, reverse proxy e aplicação;
- confiança na autoridade certificadora e no dispositivo local.

TLS pode terminar em uma CDN ou balanceador e ser iniciado novamente até o
backend. Em ambiente corporativo autorizado, inspeção TLS instala uma CA de
confiança e cria novo ponto de terminação; isso exige governança, minimização,
exceções para dados sensíveis e transparência.

## VPN não substitui HTTPS

Ao sair do gateway VPN, tráfego sem TLS volta a ser legível no caminho. O
destino também precisa ser autenticado; um túnel até “algum gateway” não prova
qual site recebeu os dados.

## Prática segura

Desenhe HTTPS direto e HTTPS dentro de VPN. Marque as duas camadas de
criptografia e seus pontos de terminação. Explique por que o gateway VPN não
deveria receber a senha do site em claro.

