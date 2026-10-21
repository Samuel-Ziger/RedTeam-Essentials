# 16 — Device Mapper, thin provisioning e verity

## Objetivos

- entender dispositivos de bloco empilháveis;
- relacionar LVM a targets do Device Mapper;
- explicar snapshot e thin provisioning;
- distinguir criptografia de integridade verificável.

## Tabelas e targets

Device Mapper cria um dispositivo virtual cuja tabela mapeia setores para um ou
mais targets. Targets incluem linear, stripe, mirror, snapshot, crypt, thin,
cache e verity. LVM automatiza metadados e composição; `dmsetup` expõe a camada.

```bash
lsblk -o NAME,TYPE,MAJ:MIN,SIZE,FSTYPE,MOUNTPOINTS
dmsetup ls --tree 2>/dev/null || true
dmsetup table --showkeys 2>/dev/null || true
```

`--showkeys` pode expor material sensível em certos targets; use apenas em VM
sem dados reais e não publique a saída.

## Snapshots clássicos

Ao preservar blocos antigos antes da primeira sobrescrita, copy-on-write permite
uma visão congelada. A área de exceções pode encher; quando isso ocorre, o
snapshot pode invalidar. Monitore metadados e dados, não apenas tamanho virtual.

## Thin provisioning

Volumes virtuais compartilham um pool e alocam blocos sob demanda. Overprovision
é intencional, mas exige alertas antes de esgotar data ou metadata. Falta de
metadata pode ser mais grave que falta de blocos de dados. Descarte precisa
atravessar filesystem, target e backing device.

## dm-crypt e dm-verity

`dm-crypt` fornece confidencialidade de blocos; não autentica automaticamente o
conteúdo. `dm-verity` verifica blocos somente leitura por uma Merkle tree e root
hash confiável. Um sistema pode combinar disco criptografado gravável para dados
e raiz imutável verificada, mas são ameaças diferentes.

O root hash precisa vir de uma cadeia confiável. Guardá-lo no mesmo local
mutável sem assinatura apenas move o problema.

## Composição e dependências

Cada target transforma um intervalo de setores e pode ser empilhado. A ordem
muda as propriedades: criptografar antes de snapshot não equivale a snapshot de
dados criptografados; cache, thin e verity também impõem restrições. Desenhe a
pilha do filesystem ao backing device e indique onde existem metadados, chaves,
checksums e pontos de falha.

O status de uma camada não resume as demais. Um thin volume pode parecer
saudável enquanto metadata se aproxima do limite; um snapshot pode ficar
inválido ao encher a área COW; um device verity pode verificar bytes mas não a
origem do root hash. Monitoramento precisa consultar target específico e
propagar falha para o consumidor.

## Thin provisioning operacional

Capacidade virtual maior que física é contrato baseado em padrão de uso e
expansão antecipada. Defina alertas separados para data e metadata, taxa de
crescimento, ação antes do limite e margem para recuperação. Autoextend sem
storage real disponível apenas posterga o incidente. Teste o modo de falha em
pool descartável: I/O deve falhar de forma observável, nunca silenciosamente.

## Cleanup verificável

Desmonte filesystem, remova consumidores, desative volumes, remova mappings e só
então destaque loops. Um target ocupado informa referência viva; não force
remoção sem descobrir o proprietário. Compare árvore `lsblk`/`dmsetup` e lista de
loops antes e depois.

## Falhas comuns

- monitorar apenas tamanho lógico do thin volume;
- apagar backing file com mapping ativo;
- expor chave por `dmsetup --showkeys` em relatório;
- confiar em root hash armazenado junto da imagem mutável;
- fazer teardown fora da ordem de dependências.

## Laboratório C

Com dois arquivos de imagem e loop devices explicitamente registrados:

1. crie PV, VG e thin pool;
2. crie dois thin volumes pequenos;
3. acompanhe `data_percent` e `metadata_percent`;
4. tire snapshot e altere somente a origem;
5. restaure e desmonte;
6. remova volumes, VG, PV e loops nessa ordem.

Não use discos físicos. Salve `losetup --list` antes/depois como evidência de
cleanup.

## Exercícios

1. Desenhe duas ordens de targets e compare confidencialidade, snapshot e
   recuperação.
2. Crie orçamento de pool thin com alertas para data, metadata e crescimento.
3. Force apenas numa imagem o preenchimento controlado e documente o erro visto
   pelo filesystem e pela aplicação.
4. Execute cleanup e prove que não sobraram mappings nem loops.

## Checklist de domínio

- [ ] Leio uma tabela Device Mapper como transformação de setores.
- [ ] Distingo LVM, snapshot clássico, thin pool, crypt e verity.
- [ ] Monitoro data e metadata separadamente.
- [ ] Protejo chaves e autentico o root hash fora da imagem.
- [ ] Removo camadas na ordem inversa sem usar disco físico.

Fonte: [Device Mapper](https://docs.kernel.org/admin-guide/device-mapper/index.html).
