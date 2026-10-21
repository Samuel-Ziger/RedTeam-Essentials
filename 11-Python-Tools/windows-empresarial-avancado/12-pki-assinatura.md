# 12 — PKI, certificados e assinatura de código

PKI liga identidades a chaves públicas por certificados. Confiança depende de
chain building, finalidade/EKU, validade, revogação, nome e proteção da chave.

## Ciclo

Key generation → request → validação → issuance → distribuição → uso →
monitoramento → renewal/revocation → archival/destruction conforme finalidade.

## AD CS

Enterprise CA, templates e autoenrollment integram AD. Uma CA raiz offline,
issuing CAs e HSM podem compor desenho, mas custo/complexidade devem ser
justificados. Template com enrollment/subject/EKU permissivos pode delegar mais
confiança que o pretendido.

Implantação, CRL/AIA e protocolos dependem de redes; aqui fazemos threat model,
template review e assinatura local com certificado de laboratório.

## PowerShell/code signing

Proteja private key, separe code signing de TLS/usuário, use timestamp confiável
e publique cadeia/política. `Set-AuthenticodeSignature` assina o conteúdo; toda
alteração posterior invalida.

## Exercício

Em VM, crie certificado self-signed apenas para lab, assine script fixture,
valide, altere um byte e observe a assinatura quebrar. Remova chave/certificado.

