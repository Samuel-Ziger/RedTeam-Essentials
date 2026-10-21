# Cheatsheet de modelagem de privacidade

## Perguntas antes de escolher uma ferramenta

1. Qual ativo quero proteger: conteúdo, identidade, localização ou relação?
2. De qual observador: rede local, ISP, serviço, provedor VPN, empregador ou
   atacante no dispositivo?
3. Por quanto tempo e com qual impacto se houver correlação?
4. Qual metadado continua visível apesar da criptografia?
5. O endpoint e as contas estão confiáveis?
6. Como verificarei o controle e registrarei suas limitações?

## O que cada opção normalmente muda

| Controle | Ajuda a proteger | Não resolve sozinho |
|---|---|---|
| HTTPS/TLS | conteúdo e integridade até o destino | conta, dados entregues ao site, endpoint |
| VPN | enlace local/ISP até o gateway; IP visto pelo destino | confiança no gateway, cookies, conta, fingerprint |
| Proxy | tráfego da aplicação configurada | demais aplicações, conteúdo sem TLS, endpoint |
| Tor Browser | rota distribuída e padronização do navegador | login identificável, malware local, observador global forte |
| Modo privativo | estado local após fechar a sessão | IP, ISP, site, empregador, fingerprint |
| Minimização | quantidade e poder de correlação dos dados | falhas técnicas ou compromissos do endpoint |

## Regra de evidência

`observação → hipótese → explicações alternativas → teste → confiança → limite`

Nunca converta “mesmo IP” em “mesma pessoa”. Documente porta, protocolo,
horário com fuso, origem do log, NAT/CGNAT possível e autoridade para analisar.

