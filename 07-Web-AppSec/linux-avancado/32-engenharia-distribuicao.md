# 32 — Pacotes, distribuições e builds reproduzíveis

## Objetivos

- transformar fonte em pacote auditável;
- distinguir upstream, downstream, patch e integração;
- controlar dependências, toolchain e ambiente;
- produzir dois artefatos bit a bit iguais.

## Papel da distribuição

Uma distribuição integra kernel, libc, init, pacotes, repositórios, políticas,
assinaturas, atualizações e suporte. O mantenedor downstream não apenas compila:
acompanha CVEs, backports, compatibilidade, testes e ciclo de vida.

## Anatomia de pacote

Receita deve declarar:

- fonte e checksum;
- patches com origem e justificativa;
- build e runtime dependencies;
- flags, arquitetura e features;
- arquivos, permissões e scripts de lifecycle;
- licença e metadados;
- testes e forma de desinstalação.

Scripts de instalação rodam com alto privilégio. Devem ser idempotentes,
não depender de rede e não iniciar serviço inesperadamente em chroot/image build.

## Reprodutibilidade

Fontes comuns de variação:

- timestamps, locale, timezone e hostname;
- ordem de filesystem e paralelismo;
- caminhos absolutos de build;
- seeds aleatórios e IDs gerados;
- versão da toolchain e dependências;
- compressão com metadados variáveis.

`SOURCE_DATE_EPOCH` fornece um timestamp derivado da fonte. Prefix maps removem
caminhos; ordenação explícita e flags determinísticas tratam outros fatores.

O script [`reproducible_archive.sh`](exemplos/reproducible_archive.sh) normaliza
ordem, ownership e mtime de um tar didático.

## Verificação independente

Duas execuções na mesma pasta podem compartilhar estado. Use diretórios limpos,
ordens diferentes e, depois, ambientes independentes. Compare SHA-256. Quando
divergir, `diffoscope` mostra camadas, mas ainda é preciso encontrar a causa.

SBOM descreve componentes; assinatura/provenance liga declaração a identidade e
processo. Nenhum deles prova que o código é seguro. Rebuild independente aumenta
confiança de que binário corresponde à fonte declarada.

## Fronteiras do build

Um build offline só é verificável se todas as entradas forem enumeradas:
tarballs, patches, submódulos, toolchain, gerador, locale, variáveis e relógio.
Lockfile sem artefatos disponíveis não basta; espelhe dependências permitidas e
valide hashes antes de iniciar. Falha de checksum encerra o build, nunca dispara
download alternativo silencioso.

Separe fonte original, patches downstream e arquivos gerados. Cada patch deve ter
origem, motivo, status upstream e condição de remoção. Regerar código com versão
diferente do gerador pode alterar o resultado mesmo quando o fonte principal não
mudou.

## Pacote e lifecycle

Declare ownership de cada path. Configuração administrada não deve ser
sobrescrita sem política; dados mutáveis não pertencem à imagem imutável.
Pre/post-install precisam ser mínimos, idempotentes e seguros em chroot. Instalar
pacote não deve iniciar serviço durante construção de imagem nem consultar rede.

Teste install, upgrade, downgrade suportado, purge e reinstalação. Depois de
remover, diferencie arquivos de pacote, configuração preservada e estado da
aplicação. ABI e schema podem impedir rollback ainda que o gerenciador aceite uma
versão antiga.

## Provenance em camadas

SBOM enumera componentes declarados; assinatura autentica quem aprovou; attestation
descreve etapa; build reproduzível permite comparação independente. Nenhum item
sozinho prova ausência de vulnerabilidade. A confiança aumenta quando revisores
separados reconstroem em ambiente independente e publicam hashes coincidentes.

## Falhas comuns

- depender de cache não inventariado;
- usar `latest` ou URL mutável;
- normalizar timestamps e ignorar paths e toolchain;
- assinar artefato antes de verificar testes e manifesto;
- inserir segredo em camada ou log do build;
- tratar SBOM como laudo de segurança.

## Prática B

1. Empacote `proc_snapshot` em formato nativo de uma distribuição.
2. Construa offline duas vezes em diretórios diferentes.
3. Compare hashes e use `diffoscope` se necessário.
4. Instale numa raiz temporária, liste arquivos e remova.
5. Gere SBOM e manifesto de hashes.

## Exercícios

1. Produza grafo de todas as entradas de um pacote e associe hash e licença.
2. Faça dois builds em paths, locale e timezone diferentes; use `diffoscope`
   para classificar a primeira divergência.
3. Teste install, upgrade, remoção e reinstalação numa raiz temporária.
4. Diferencie SBOM, assinatura, provenance e rebuild independente no seu relatório.

## Checklist de domínio

- [ ] Inventario todas as entradas e rejeito checksum divergente.
- [ ] Separo upstream, patches downstream e gerados.
- [ ] Projeto scripts de lifecycle offline, mínimos e idempotentes.
- [ ] Produzo SBOM, manifesto, assinatura e evidência de rebuild.
- [ ] Explico o que reprodutibilidade prova e o que não prova.

Fonte: [Reproducible Builds](https://reproducible-builds.org/docs/).
