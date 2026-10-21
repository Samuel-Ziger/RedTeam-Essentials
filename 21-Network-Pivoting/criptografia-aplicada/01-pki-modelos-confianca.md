# 01 — PKI e modelos de confiança

PKI liga nomes e atributos a chaves públicas por certificados assinados. O
modelo Web PKI usa várias raízes confiadas; organizações podem operar PKI
privada; SSH frequentemente usa trust on first use ou CA própria; pinning tem
trade-offs de recuperação e rotação.

Confiança não “vem do certificado”. Ela nasce de uma âncora distribuída com
segurança, regras de emissão, validação de caminho e política de aplicação.
Comprometer CA amplia impacto; hierarquia e restrições reduzem o raio.

## Prática

Compare Web PKI, CA interna e TOFU por bootstrap, rotação e revogação.
