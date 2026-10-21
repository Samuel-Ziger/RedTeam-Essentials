# 16 — Preservação e cadeia de custódia

Preserve primeiro, analise cópia depois. Para cada item registre:

- identificador único e descrição;
- origem e método de aquisição;
- data/hora/fuso e responsável;
- hash com algoritmo e ferramenta;
- tamanho e permissões;
- armazenamento e controle de acesso;
- cada transferência, acesso e transformação;
- vínculo com ticket/caso.

## Original e derivado

Mantenha original somente leitura quando possível. Normalização, descompressão,
conversão de timezone e filtros criam derivados. Registre comando/versão e hash
de entrada/saída.

## Hash

SHA-256 detecta alteração acidental ou posterior. Ele não atesta coleta correta,
relógio, completude nem autenticidade da fonte. Assinatura e cadeia do coletor
podem fortalecer proveniência.

## Dados sensíveis

Evite duplicar conteúdo pessoal sem necessidade. Cifre armazenamento, restrinja
acesso, use redaction em relatórios e defina destruição ao encerrar retenção.

## Prática

Execute `evidence_manifest.py` sobre os arquivos fictícios. Depois altere uma
cópia e compare hashes. Não use evidência real no repositório.

