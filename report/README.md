# Relatorio PDF (RedTeam-Essentials)

> Gera PDF e arquivo `.7z` a partir de Markdown ou Org, para labs e engagements.
> Conteudo sugerido: adapte [`../REPORT-TEMPLATE.md`](../REPORT-TEMPLATE.md) — nao ha sample de exame com OSID falso neste diretorio.

**Credito:** script baseado no `generate.sh` HexSec (Leonardo Tamiano), inspirado em Alexandre ZANNI / noraj ([OSERT](https://github.com/noraj/OSCP-Exam-Report-Template-Markdown)). Adaptado para naming RTE / `REPORT_ID`.

---

## Requisitos

| Ferramenta | Uso |
|------------|-----|
| [pandoc](https://pandoc.org/) | Conversao md/org → PDF |
| [eisvogel](https://github.com/Wandmalfarbe/pandoc-latex-template) | Template LaTeX (`--template eisvogel`) |
| [7z](https://www.7-zip.org/) | Arquivo compactado do PDF |
| TeX engine | Tipicamente TeX Live / MiKTeX (dependencia do pandoc+eisvogel) |

Instale o template eisvogel no path que o pandoc resolve (ex.: `~/.pandoc/templates/eisvogel.latex`).

---

## Uso rapido

```bash
cd report
chmod +x generate-pdf.sh

# 1) Prepare o markdown (a partir do template da raiz)
cp ../REPORT-TEMPLATE.md ./relatorio.md
# edite relatorio.md (YAML title/author ajuda o eisvogel)

# 2) Gere PDF + 7z (nome padrao: RTE-Report-LAB.pdf)
./generate-pdf.sh

# Ou passe o path do arquivo
./generate-pdf.sh ../REPORT-TEMPLATE.md
./generate-pdf.sh ./meu-lab.md
```

---

## Variaveis de ambiente

| Variavel | Default | Efeito |
|----------|---------|--------|
| `REPORT_ID` | `LAB` | Nome `RTE-Report-$REPORT_ID.pdf` e `.7z` |
| `OSID` | *(vazio)* | Se definido, usa `OSCP-OS-$OSID-Exam-Report.pdf` (quem for prestar exame OffSec) |

Exemplos:

```bash
REPORT_ID=ACME-2026 ./generate-pdf.sh ./relatorio.md
# -> RTE-Report-ACME-2026.pdf

OSID=12345678 ./generate-pdf.sh ./exam.md
# -> OSCP-OS-12345678-Exam-Report.pdf
# Use SEU OSID real na hora do exame; nao invente IDs de amostra neste repo.
```

Se `OSID` e `REPORT_ID` estiverem ambos setados, **OSID tem prioridade** no nome do arquivo.

---

## Fluxo recomendado

1. Copie [`REPORT-TEMPLATE.md`](../REPORT-TEMPLATE.md) e preencha achados do engagement/lab.
2. Inclua evidencias minimas (screenshots em `src/` ou pasta relativa; o script passa `--resource-path=.:src`).
3. Rode `./generate-pdf.sh [arquivo.md|arquivo.org]`.
4. Confira o PDF; o `.7z` e o MD5 sao impressos no final (util para entrega).

---

## O que este diretorio nao inclui

- Sample de exam report com OSID falso de prova real.
- Copia do PDF / `report.md` / `report.org` enormes de clones OSCP.
- Politica oficial OffSec — consulte o exam guide vigente se for usar o naming `OSCP-OS-*`.

Para o conteudo textual do relatorio Red Team, o canone do repo e o template na raiz.

---

## Troubleshooting

| Sintoma | Acao |
|---------|------|
| `missing pandoc` / `missing 7z` | Instale as ferramentas e garanta que estao no `PATH` |
| Erro de template eisvogel | Instale eisvogel e teste `pandoc --template eisvogel -o /tmp/t.pdf minimal.md` |
| `missing input report` | Passe o path ou crie `report/relatorio.md` |
| Imagens quebradas no PDF | Coloque assets sob `report/src/` ou ajuste paths relativos |
