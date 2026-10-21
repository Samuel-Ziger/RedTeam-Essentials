# 02 — Arquivos, caminhos e publicação segura

Arquivos parecem simples porque são familiares. Para uma automação, porém,
nomes, links, permissões, codificação, concorrência e volumes tornam o filesystem
uma fronteira não confiável.

## Objetivos

- validar raízes, caminhos relativos, tipos e limites;
- compreender traversal, symlink e condições TOCTOU;
- publicar arquivos sem sobrescrita silenciosa;
- escolher política de encoding, nomes, hashes e metadados;
- produzir plano e manifesto determinísticos.

## 1. Modelo de falha

Trate como não confiável caminho recebido por CLI ou API, nome de upload,
diretório alterado por outro processo, link criado entre validação e uso, arquivo
especial no lugar esperado, volume excessivo e texto com encoding inesperado.

O objetivo não é aceitar tudo: é recusar de maneira previsível antes do efeito.

## 2. Raiz autorizada e caminho relativo

Nunca construa destino por concatenação. Modele uma raiz controlada e um caminho
relativo validado.

~~~python
from pathlib import Path, PurePosixPath

def safe_relative(raw: str) -> PurePosixPath:
    value = PurePosixPath(raw)
    if value.is_absolute() or not value.parts:
        raise ValueError("caminho deve ser relativo")
    if any(part in {"", ".", ".."} for part in value.parts):
        raise ValueError("segmento de caminho invalido")
    return value

def destination(root: Path, raw: str) -> Path:
    relative = safe_relative(raw)
    return root.joinpath(*relative.parts)
~~~

Isso valida sintaxe, mas não elimina corrida nem symlink existente. A garantia
forte depende de APIs que operem relativas a um descritor de diretório, não sigam
links e criem o destino exclusivamente.

## 3. Normalizar não é autorizar

Resolver um caminho remove ponto-ponto e pode seguir links. Depois de resolver,
comparar se está dentro da raiz ajuda, mas não use prefixo textual:

~~~text
/dados/permitido-malicioso não está dentro de /dados/permitido
~~~

Compare componentes por API. Outro processo ainda pode trocar um diretório por
link depois da checagem. Em laboratório local, documente a janela, recuse links e
use criação exclusiva. Contra adversário local concorrente, use primitivas seguras
do sistema; checagem de alto nível não é sandbox.

## 4. Descoberta controlada

Defina antes de percorrer:

- profundidade, quantidade e bytes totais;
- extensões e tipos aceitos;
- política para ocultos, links e arquivos especiais;
- preservação de subdiretórios;
- comportamento se a origem muda durante o hash;
- ordem canônica do plano.

Não siga links por padrão. Diferencie lstat, que observa o link, de stat, que
pode observar o alvo. Link inesperado deve gerar diagnóstico, não ser ignorado.

## 5. Limites e streaming

Leia arquivos grandes em blocos. Aplique o limite durante a leitura, pois o
arquivo pode crescer depois da observação inicial.

~~~python
import hashlib

def bounded_sha256(path, max_bytes: int) -> tuple[str, int]:
    digest = hashlib.sha256()
    seen = 0
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            seen += len(chunk)
            if seen > max_bytes:
                raise ValueError("arquivo excede limite")
            digest.update(chunk)
    return digest.hexdigest(), seen
~~~

Se tamanho e hash fazem parte do plano, o executor confirma que a fonte ainda
corresponde antes de publicar. Um hash calculado ontem não valida bytes de hoje.

## 6. Nomes, Unicode e portabilidade

Sistemas diferem em separador, sensibilidade a maiúsculas, nomes reservados,
caracteres proibidos e normalização Unicode. Escolha uma política:

- preservar o nome e restringir plataformas suportadas;
- gerar identificador portável e guardar nome original como metadado;
- rejeitar colisões após normalização e case-folding;
- limitar bytes ou unidades da representação real.

Não chame genericamente de caracteres se o limite real é bytes UTF-8 ou unidades
UTF-16. Um emoji demonstra por que a diferença importa.

## 7. Texto, binário e encoding

Texto exige contrato. Prefira UTF-8 explicitamente e decida se BOM é permitido,
se fim de linha é preservado, se byte inválido rejeita e se a última linha sem
quebra é aceita.

Nunca decodifique binário para copiar. Cópia e hash operam em bytes. CSV e JSON
usam parsers que entendem aspas e escapes; split por vírgula não é parser CSV.

## 8. Publicação atômica

Para substituir arquivo pertencente à aplicação:

1. crie temporário no mesmo diretório e volume;
2. escreva e finalize os bytes;
3. sincronize quando a durabilidade exigir;
4. valide tamanho, schema ou hash;
5. substitua atomicamente com a primitiva da plataforma;
6. trate falha e remova temporário.

Substituição atômica evita meio arquivo visível, mas pode sobrescrever versão de
terceiro. Para criar somente se ausente, use criação exclusiva. Rename com replace
incondicional viola esse contrato.

### Durabilidade não é atomicidade

Uma operação pode ser atômica e ainda se perder após queda se buffers não foram
persistidos. Documente se a meta é consistência entre processos ou durabilidade
contra falha da máquina.

## 9. Colisões

| Estado | Decisão segura comum |
|---|---|
| destino ausente | copy |
| arquivo igual por hash | skip |
| arquivo diferente | conflict |
| diretório, link ou especial | conflict |
| destino apareceu depois do plano | revalidar e conflict ou skip |

Renomear com sufixo pode quebrar idempotência. Se versionar, derive a versão do
conteúdo ou identificador estável, não do primeiro nome disponível.

## 10. Integridade e autenticidade

SHA-256 ajuda a detectar alteração e identificar conteúdo. Não prova autoria.
Autenticidade exige assinatura, MAC ou canal confiável e gestão das chaves.

Um manifesto contém schema, raiz lógica, caminho relativo, tamanho, hash, ação e
razão. Evite caminhos pessoais absolutos em evidência compartilhada. Ordene por
representação canônica para permitir diff.

## 11. Permissões e metadados

Copiar conteúdo não significa preservar dono, ACL, modo, timestamp e atributos.
Preservar demais pode transportar permissão indevida; preservar de menos pode
quebrar uso. Aplique permissão segura ao criar o temporário.

Segredos não devem nascer legíveis para todos e depois ser restringidos. A janela
anterior à correção já é exposição.

## Falhas e diagnóstico

| Sintoma | Verifique | Evidência |
|---|---|---|
| arquivo fora da raiz | parsing e componentes | caminho relativo sanitizado |
| sobrescrita ocasional | TOCTOU e criação exclusiva | pré-condição |
| hashes divergentes | fonte mudou ou cópia parcial | hash antes e temporário |
| funciona em um SO | nomes, case e Unicode | matriz de plataforma |
| texto corrompido | encoding implícito | bytes da fixture e contrato |

## Exercícios

### Nível 1 — fronteiras

Teste caminho absoluto, traversal, nome Unicode, link e arquivo gigante. **Aceite:**
cada caso termina antes da mutação com erro classificado.

### Nível 2 — publicação

Implemente temp + validação + criação exclusiva. **Aceite:** falha antes do commit
preserva a versão anterior e destino concorrente não é sobrescrito.

### Nível 3 — portabilidade

Teste nomes, case e Unicode em duas plataformas ou adapters. **Aceite:** colisões
normalizadas são detectadas e o manifesto é determinístico.

## Checklist

- [ ] Entradas são relativas a raízes autorizadas.
- [ ] Links e arquivos especiais possuem política explícita.
- [ ] Quantidade, tamanho, profundidade e tempo são limitados.
- [ ] Criação e substituição não foram confundidas.
- [ ] A fonte é revalidada durante a execução.
- [ ] Encoding, nomes, metadados e portabilidade estão documentados.

