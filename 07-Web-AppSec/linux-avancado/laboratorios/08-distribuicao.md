# Lab 08 — Pacote e imagem reproduzível

**Classe:** B. **Duração:** 14–20 h.

## Pré-requisitos e gate

Conclua o Lab 07 e os capítulos 30–33. Arquive fontes e dependências, valide
hashes e desligue acesso de rede do ambiente de build. Registre toolchain,
locale, timezone, umask, path e `SOURCE_DATE_EPOCH`.

## Objetivo

Empacotar `proc_snapshot`, construir offline duas vezes e incorporar o pacote a
uma pequena imagem local.

## Procedimento

1. Fixe fonte, toolchain e dependências por hash.
2. Crie receita nativa DEB ou RPM sem scripts de rede.
3. Defina `SOURCE_DATE_EPOCH` a partir do commit.
4. Compile em dois diretórios limpos com ordem diferente.
5. Compare hashes do pacote.
6. Se divergirem, gere `diffoscope` e corrija a causa.
7. Instale em root temporário e execute teste.
8. Gere SBOM, manifesto e assinatura de laboratório.

## Receita e lifecycle

A receita declara fonte, checksum, patches, build/runtime dependencies, licença,
flags, arquivos e permissões. Separe upstream de patches downstream e informe
origem, razão e condição de remoção. Scripts de pacote não podem consultar rede
nem iniciar serviço durante construção da imagem.

Teste em raiz temporária:

1. instalação limpa e inventário;
2. execução da fixture e schema de saída;
3. upgrade para segunda versão compatível;
4. remoção e distinção entre pacote, configuração e estado;
5. reinstalação sem depender do build anterior.

## Reprodutibilidade e confiança

Faça o segundo build em path diferente, com ordem de filesystem, locale e
timezone alterados. Se o hash divergir, use `diffoscope` e preserve o primeiro
nível diferente. Não copie o artefato do primeiro diretório nem compartilhe
cache não declarado.

SBOM, assinatura, provenance e rebuild respondem perguntas diferentes. A
assinatura só ocorre após manifesto e testes. Use chave exclusiva do laboratório
e documente revogação; nunca reutilize chave pessoal.

## Variações obrigatórias

Repita uma vez mudando locale, timezone e caminho. O artefato final deve continuar
idêntico. Se a toolchain inserir informação inevitável, documente a limitação em
vez de esconder a divergência.

## Critério

Outra pessoa consegue verificar origem, hash, lista de arquivos, dependências e
resultado sem acessar rede. A desinstalação não deixa arquivos fora dos caminhos
de estado declarados.

Também deve demonstrar que nenhum download ocorreu, que o patch didático compila
em cada commit e que a mensagem inclui problema, causa, mudança e teste. Não
envie patch a lista ou mantenedor real.

## Perguntas para defesa

- Qual entrada não estava no lockfile na primeira tentativa?
- O que um hash idêntico prova e o que não prova?
- Por que SBOM não é análise de vulnerabilidade nem garantia de segurança?
- Como ABI ou schema podem impedir downgrade do pacote?
