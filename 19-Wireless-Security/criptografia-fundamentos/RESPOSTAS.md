# Respostas orientativas

## Pontos essenciais

- Base64 é codificação reversível; não usa chave nem esconde conteúdo.
- O inverso modular existe quando os operandos são coprimos.
- Nonce normalmente é público, mas sua unicidade pode ser requisito crítico.
- Hash sem chave detecta alteração apenas quando o digest chega por canal confiável.
- HMAC autentica entre detentores da chave e não prova qual deles criou a tag.
- Hash ideal de 256 bits oferece aproximadamente 128 bits contra colisões.
- Salt separa registros; não precisa ser secreto e não substitui custo de KDF.
- OTP exige chave uniforme, secreta, do tamanho da mensagem e usada uma vez.

As respostas dos projetos são critérios, não um arquivo pronto: compare modelo
de ameaça, serialização e testes negativos, não somente o digest final.
