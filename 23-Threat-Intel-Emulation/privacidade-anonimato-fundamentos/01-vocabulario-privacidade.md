# 01 — Vocabulário de privacidade

Termos próximos descrevem propriedades diferentes:

- **segurança** reduz probabilidade e impacto de ações não autorizadas;
- **confidencialidade** protege o conteúdo contra leitura;
- **privacidade** dá governança sobre dados pessoais e relações;
- **anonimato** dificulta associar uma ação a uma identidade;
- **pseudonimato** substitui a identidade por um rótulo estável;
- **desvinculação** dificulta ligar duas ações entre si;
- **não observabilidade** tenta esconder que uma comunicação ocorreu.

Criptografia não cria todas essas propriedades. TLS pode esconder o corpo de
uma requisição no caminho e, ainda assim, o site conhece a conta, o horário, o
IP de saída, o user-agent e os dados enviados. Um pseudônimo também acumula
histórico: se for usado em contextos diferentes, esses contextos se tornam
correlacionáveis.

## Conjunto de anonimato

Anonimato depende de não ser distinguível dentro de um conjunto. Alterar muitas
configurações “para parecer diferente” pode reduzir o conjunto e criar um
fingerprint único. Em alguns sistemas, padronizar comportamentos é mais útil do
que personalizá-los.

## Privacidade por projeto

Priorize minimização, finalidade, retenção limitada, controle de acesso,
separação de funções, criptografia adequada e transparência. A tecnologia de
rede é apenas uma camada.

## Prática segura

Para uma conversa de suporte, classifique: conteúdo da mensagem, identidade da
conta, horário e relação cliente–empresa. Marque quais propriedades você quer
para cada item. Não use “anonimato” como resposta para todos.

