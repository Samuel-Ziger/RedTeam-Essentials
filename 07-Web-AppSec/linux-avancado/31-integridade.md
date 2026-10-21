# 31 — Assinatura, IMA/EVM, fs-verity e dm-verity

## Objetivos

- separar autenticidade, integridade, medição e confidencialidade;
- entender assinatura de módulo e lockdown;
- comparar IMA appraisal/measurement, EVM, fs-verity e dm-verity;
- desenhar rotação e revogação de chaves.

## Quatro perguntas

- **integridade:** bytes mudaram?
- **autenticidade:** uma chave autorizada aprovou o artefato?
- **medição:** qual hash foi registrado e onde?
- **confidencialidade:** quem consegue ler?

Uma assinatura não cifra. Um hash sem origem confiável detecta acidente, mas um
atacante que troca dados e hash pode enganar o consumidor.

## Módulos

O kernel pode verificar assinatura anexada a módulos. Em modo permissivo, módulo
não confiável pode carregar e marcar taint; em modo restritivo, é rejeitado.
Chaves embutidas e keyrings secundários definem confiança. Revogação precisa
alcançar máquinas que ainda confiam na chave comprometida.

## IMA e EVM

IMA pode medir arquivos em log associado a PCR, verificar hashes/assinaturas e
aplicar appraisal conforme política. EVM protege metadados de segurança, como
xattrs, contra alteração offline. A política define cobertura; habilitar a feature
sem política adequada não protege todo arquivo.

```bash
cat /sys/kernel/security/ima/policy 2>/dev/null | head
head /sys/kernel/security/ima/ascii_runtime_measurements 2>/dev/null
```

## fs-verity e dm-verity

fs-verity protege arquivos individuais somente leitura com Merkle tree, opcional
assinatura e verificação sob demanda. dm-verity protege uma imagem de bloco
somente leitura. Ambos precisam de digest/root hash autenticado externamente.

Use fs-verity para artefatos dentro de filesystem mutável quando apropriado;
dm-verity para raiz/imagem imutável. Atualização normalmente cria novo artefato,
não modifica o verificado no lugar.

## Cadeia e recuperação

Documente root of trust, chaves intermediárias, signer, verifier, validade,
revogação, modo de falha e acesso de recuperação. Se a única chave for perdida,
uma política perfeita pode tornar o sistema irrecuperável.

## Âncora e política

Toda verificação termina numa âncora aceita sem outra prova naquele contexto:
chave embutida, firmware, política de boot ou segredo provisionado. Documente
como entrou, quem pode atualizá-la e como revogar. Assinar com chave desconhecida
não cria confiança; comparar hash recebido do mesmo canal da imagem não impede
substituição coordenada.

IMA measurement registra eventos; appraisal decide permitir com base em hash ou
assinatura e política. Audit-only ajuda implantação, mas não bloqueia. EVM protege
xattrs relevantes contra alteração offline e depende de chave/modo corretos.
Defina quais hooks, máscaras e paths a política cobre; uma exceção ampla pode
virar caminho não verificado.

## Granularidade e atualização

fs-verity verifica páginas lidas de arquivo habilitado e imutável; não protege
nomes de diretório nem arquivos não habilitados. dm-verity cobre blocos de uma
imagem somente leitura a partir de root hash. Nenhum fornece confidencialidade.
Use novo arquivo ou novo slot para atualização e autentique metadados que apontam
para a versão esperada.

Assinatura de módulo depende de keyrings, config e modo de enforcement. Lockdown
pode restringir interfaces que permitiriam alterar ou ler kernel, mas seu modo e
gatilho variam. Registre a política real em runtime.

## Falhas comuns

- confundir hash, assinatura, medição e cifragem;
- habilitar IMA sem revisar a política efetiva;
- proteger conteúdo e deixar seleção de versão mutável;
- perder chave de recuperação ou não testar revogação;
- acreditar que fs-verity cobre o diretório inteiro;
- aceitar módulo não confiável em modo permissivo sem perceber o taint.

## Prática B/C

1. Gere uma chave descartável na VM.
2. Assine um pequeno módulo sem carregá-lo e inspecione trailer.
3. Crie arquivo fs-verity em filesystem descartável.
4. Confirme leitura e rejeição de modificação.
5. Revogue a confiança no roteiro e descreva recuperação.

## Exercícios

1. Desenhe âncora, signer, assinatura, verifier, artefato e revogação para módulo
   e imagem dm-verity.
2. Compare IMA measurement, appraisal e EVM em uma tabela de decisão.
3. Habilite fs-verity apenas em imagem descartável, valide leitura e documente o
   que nome, diretório e metadata ainda permitem mudar.
4. Modele troca conjunta de imagem e root hash e mostre onde autenticação externa
   interrompe o ataque.

## Checklist de domínio

- [ ] Distingo integridade, autenticidade, medição e confidencialidade.
- [ ] Identifico a âncora de confiança e o caminho de revogação.
- [ ] Explico cobertura e limites de IMA, EVM, fs-verity e dm-verity.
- [ ] Projeto update criando novo artefato verificável.
- [ ] Mantenho recovery testado sem desativar a política normal.

Fontes: [module signing](https://docs.kernel.org/admin-guide/module-signing.html),
[fs-verity](https://docs.kernel.org/filesystems/fsverity.html) e
[dm-verity](https://docs.kernel.org/admin-guide/device-mapper/verity.html).
