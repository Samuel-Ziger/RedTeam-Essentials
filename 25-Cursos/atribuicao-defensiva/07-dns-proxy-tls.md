# 07 — DNS, proxy e TLS

DNS mostra intenção de resolver um nome, não necessariamente conexão. Cache,
prefetch, processo de segurança e outro cliente atrás do mesmo resolvedor podem
gerar consulta. Relacione resposta, TTL, cliente, processo e fluxo.

## Proxy

Proxy corporativo conhece cliente autenticado, URL conforme protocolo/política,
destino, decisão e volume. O destino vê o proxy. Preserve `X-Forwarded-For` ou
equivalente somente entre proxies confiáveis; cabeçalho recebido diretamente do
cliente é falsificável.

## TLS

Sem inspeção, sensores podem observar IP, porta, versão/handshake e metadados
permitidos pelo protocolo. Certificado e SNI não devem ser presumidos visíveis
em todas as versões/configurações. Fingerprints TLS são probabilísticos e mudam
com biblioteca, proxy e atualização.

## DNS cifrado

DoH/DoT muda a visibilidade da rede e concentra consulta no resolvedor. Em
empresa, política deve equilibrar segurança, privacidade e necessidade. Detectar
resolver não autorizado é diferente de descriptografar dados pessoais sem base.

## Prática

Correlacione consulta sintética, resposta, fluxo e request ID. Escreva uma
alternativa em que a consulta não levou à conexão.

