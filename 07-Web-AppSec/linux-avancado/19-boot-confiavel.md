# 19 — UEFI, initramfs, UKI, TPM e boot medido

## Objetivos

- detalhar a cadeia firmware → kernel → initramfs → raiz → PID 1;
- separar Secure Boot de measured boot;
- entender Unified Kernel Image e rollback;
- recuperar uma falha sem substituir o único boot funcional.

## Cadeia de inicialização

UEFI executa binários PE na EFI System Partition conforme entradas e política.
Um boot manager pode carregar kernel e initramfs. O kernel inicializa memória,
scheduler, drivers e monta uma raiz inicial. O `/init` do initramfs encontra e
prepara a raiz real, executa `switch_root`, e o PID 1 inicia o user space.

```bash
bootctl status 2>/dev/null || true
efibootmgr -v 2>/dev/null || true
lsinitramfs /boot/initrd.img-"$(uname -r)" 2>/dev/null | head
cat /proc/cmdline
```

## Secure Boot

Secure Boot verifica assinaturas antes de executar componentes. Ele controla
**quem foi autorizado a iniciar**, desde que chaves, revogações e política sejam
corretas. Não cifra disco nem prova que o sistema permaneceu íntegro após boot.

## Measured boot e TPM

Measured boot estende hashes em PCRs do TPM. O TPM registra medidas; um verifier
ou uma política decide se elas são aceitáveis. Medir código malicioso conhecido
não impede sua execução por si só. Sealing pode liberar segredo somente sob
estado esperado, mas precisa de recuperação para atualizações legítimas.

## UKI

Uma UKI pode reunir stub UEFI, kernel, initrd, linha de comando e metadados em um
artefato PE assinável. Isso reduz combinações desencontradas, mas a atualização
continua precisando de slots, atomicidade e rollback.

Modelo A/B:

```text
slot A: conhecido e funcional
slot B: candidato
boot once B → health check → marcar bom
falha/timeout → firmware/boot manager retorna A
```

## Initramfs

Inclua apenas drivers, regras, ferramentas e credenciais indispensáveis. Secrets
embutidos podem ficar expostos no artefato. Use mecanismos de credencial e TPM
adequados, e considere que prompt de recuperação precisa de console funcional.

## Confiança, medição e decisão

Verificação responde se um artefato foi aprovado por uma chave confiável.
Medição registra o que foi carregado. Attestation combina medidas com identidade
e freshness para um verificador decidir. Nenhuma dessas propriedades cifra o
volume. Para cada elo, documente produtor, chave, local da verificação, política
de falha e como uma chave comprometida é revogada.

PCR é estendido, não simplesmente sobrescrito: ordem e valores anteriores
participam do resultado. Selar segredo a PCRs rígidos pode impedir boot legítimo
após update. Política precisa aceitar conjuntos versionados, controlar rollback
e oferecer recovery autenticado que não anule a proteção cotidiana.

## Boot transacional

Update seguro grava o slot inativo, verifica antes de marcar candidato, tenta-o
com contador finito e só promove após health check. O health check deve avaliar
função essencial, não apenas PID vivo. Dados mutáveis e schemas precisam ser
compatíveis com retorno ao slot anterior; caso contrário o binário volta, mas o
sistema não.

Initramfs é parte crítica porque descobre storage, desbloqueia volume e monta a
raiz. Construa-o a partir de dependências declaradas, inspecione conteúdo e evite
segredos permanentes. Uma entrada paralela conhecida e console testado são
pré-requisitos para qualquer mudança.

## Falhas comuns

- dizer apenas “o boot é assinado” sem mapear a cadeia;
- confundir Secure Boot, measured boot e disco cifrado;
- colocar root hash ou chave de confiança no mesmo estado mutável;
- promover slot antes de health check completo;
- fazer migração irreversível de dados antes da confirmação;
- testar recovery somente depois da falha real.

## Laboratório C/D

1. Extraia o initramfs em diretório temporário e desenhe `/init`.
2. Construa uma imagem alternativa com mensagem visível.
3. Crie entrada de boot **adicional** e uma tentativa única.
4. Simule falha no slot B.
5. Demonstre retorno ao slot A e documente tempo de recuperação.

## Exercícios

1. Desenhe firmware, bootloader ou UKI, kernel, initramfs, raiz e PID 1, marcando
   assinatura, medida e chave em cada elo.
2. Proponha política de PCR que aceite update autorizado e rejeite rollback sem
   bloquear recovery legítimo.
3. Modele A/B com contador, health check, promoção e três pontos de queda.
4. Inspecione initramfs e classifique cada arquivo como essencial, derivado ou
   segredo indevido.

## Checklist de domínio

- [ ] Distingo verificação, medição, attestation e confidencialidade.
- [ ] Explico extensão de PCR e risco de política rígida.
- [ ] Projeto update A/B com promoção tardia e rollback testado.
- [ ] Mantenho entrada conhecida e console antes de alterar boot.
- [ ] Respondo quem assina, quem confia, onde verifica e como revoga.

Fonte: [systemd UKI](https://uapi-group.org/specifications/specs/unified_kernel_image/).
