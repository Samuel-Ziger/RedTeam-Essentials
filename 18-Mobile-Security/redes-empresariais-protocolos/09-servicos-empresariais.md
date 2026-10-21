# 09 — E-mail, arquivos, voz e vídeo

SMTP transfere mensagens; submission autenticado é separado de relay entre
servidores. IMAP acessa caixas. SPF, DKIM e DMARC ajudam autenticar domínio e
política, mas não tornam toda mensagem verdadeira. TLS, antispam, retenção e
resposta a abuso completam o serviço.

SMB/NFS oferecem arquivos com modelos de identidade/locking diferentes. Controle
share/export e permissão de filesystem, assinatura/cifragem, backup imutável e
capacidade. Não exponha protocolos de arquivo diretamente à Internet.

SIP sinaliza voz; RTP/RTCP transporta mídia/qualidade. NAT, portas dinâmicas,
latência, jitter e perda exigem desenho; SBC estabelece fronteira. SRTP protege
mídia quando negociado corretamente.

## Matriz

Documente plano de controle e dados separadamente. Permitir SIP sem RTP produz
chamada sem áudio; permitir sinalização excessiva aumenta superfície.
