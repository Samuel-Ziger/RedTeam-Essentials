# 12 — Diffie–Hellman e sigilo futuro

Diffie–Hellman permite combinar segredo local e valor público para obter um
segredo compartilhado. Sem autenticação, não identifica o outro participante e
permanece vulnerável a um intermediário ativo. Protocolos assinam o transcript
ou autenticam por certificado/chave prévia.

Chaves efêmeras de sessão e exclusão posterior podem fornecer forward secrecy:
comprometer a chave de identidade não recupera sessões antigas gravadas.
Valide grupos/valores e passe o segredo bruto por KDF com transcript e papéis.

## Verificação

Separe no diagrama as chaves de identidade, efêmeras, segredo DH e chaves
derivadas de tráfego.
