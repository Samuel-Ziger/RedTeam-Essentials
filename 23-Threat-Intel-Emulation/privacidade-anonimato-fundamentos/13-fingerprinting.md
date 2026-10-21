# 13 — Fingerprinting e padronização

Fingerprinting combina sinais suficientes para distinguir um cliente mesmo sem
cookie. Exemplos incluem versão do navegador, sistema, idioma, fuso, tela,
renderização gráfica, fontes, áudio, APIs disponíveis e padrão de interação.

Nenhum campo precisa ser único sozinho. A combinação, sua estabilidade e o
contexto do serviço determinam o poder de identificação. Fingerprints também
mudam com atualizações e podem gerar colisões; não são prova infalível.

## Duas estratégias

- **reduzir superfície:** limitar APIs e permissões desnecessárias;
- **misturar-se ao conjunto:** padronizar atributos para se parecer com muitos
  outros usuários.

O Tor Browser enfatiza padronização e isolamento por site. Personalizá-lo com
extensões, janela incomum ou opções raras pode desfazer parte do benefício.
Spoofar valores individualmente também cria combinações incoerentes e quebra
sites.

## Uso defensivo responsável

Fraude e proteção de conta podem usar sinais do dispositivo, mas devem considerar
consentimento, proporcionalidade, vieses, retenção e explicabilidade. Trate o
fingerprint como sinal probabilístico, não identidade civil.

## Prática segura

Liste dez atributos possíveis e classifique estabilidade, sensibilidade e
necessidade para sua própria aplicação. Remova três cuja coleta não se justifica.

