#!/usr/bin/env sh
#
# Gera PDF (+ arquivo 7z) a partir de Markdown ou Org.
#
# Adaptado para RedTeam-Essentials a partir do generate.sh HexSec
# (Leonardo Tamiano), inspirado no trabalho de Alexandre ZANNI / noraj
# (OSERT — OSCP Exam Report Template Markdown).
#
# Uso:
#   ./generate-pdf.sh
#   ./generate-pdf.sh ../caminho/meu-relatorio.md
#   REPORT_ID=ACME-2026 ./generate-pdf.sh relatorio.md
#   OSID=12345678 ./generate-pdf.sh exam.md   # nome estilo OffSec
#
# Conteudo sugerido: copie/adapte ../REPORT-TEMPLATE.md
#

ROOT=$(dirname $(realpath "$0"))

# Identificador padrao do relatorio (labs / clientes)
REPORT_ID="${REPORT_ID:-LAB}"

# Input default: relatorio.md na pasta report/ (crie a partir do template)
INPUT_PATH="${ROOT}/relatorio.md"

# Nomes de saida:
# - Se OSID estiver definido: OSCP-OS-$OSID-Exam-Report.pdf (conveniencia exame)
# - Caso contrario: RTE-Report-$REPORT_ID.pdf
if [ -n "${OSID}" ]; then
	REPORT_PDF_PATH="${ROOT}/OSCP-OS-${OSID}-Exam-Report.pdf"
	ARCHIVE_NAME="${ROOT}/OSCP-OS-${OSID}-Exam-Report.7z"
else
	REPORT_PDF_PATH="${ROOT}/RTE-Report-${REPORT_ID}.pdf"
	ARCHIVE_NAME="${ROOT}/RTE-Report-${REPORT_ID}.7z"
fi

RED='\033[0;31m'
NC='\033[0m'

# ----------------------------

check_requirements() {
	if [ $# -eq 1 ] && [ -f "$1" ]; then
		filename=$(basename -- "$1")
		extension="${filename##*.}"
		[ ! "$extension" = "org" ] && [ ! "$extension" = "md" ] \
			&& echo "[ERROR]: Input file can only be '.org' or '.md'" && exit 1

		INPUT_PATH=$1
	elif [ $# -gt 1 ]; then
		echo "[ERROR]: use no maximo um argumento (caminho do .md/.org)" && exit 1
	fi

	[ ! -f "$INPUT_PATH" ] && echo "[ERROR]: missing input report: $INPUT_PATH" && \
		echo "[HINT]: passe o path ou copie ../REPORT-TEMPLATE.md para $ROOT/relatorio.md" && exit 1

	which pandoc >/dev/null 2>&1
	[ $? -eq 1 ] && echo "[ERROR]: missing pandoc!" && exit 1

	which 7z >/dev/null 2>&1
	[ $? -eq 1 ] && echo "[ERROR]: missing 7z!" && exit 1

	# eisvogel: template LaTeX do pandoc (instalacao tipica em ~/.pandoc/templates)
	if [ ! -f "${HOME}/.pandoc/templates/eisvogel.latex" ] && \
	   [ ! -f "/usr/share/pandoc/data/templates/eisvogel.latex" ]; then
		echo "[WARN]: template eisvogel nao encontrado nos paths comuns."
		echo "        Instale eisvogel e garanta que pandoc o resolva com --template eisvogel"
	fi
}

# -----

md2pdf() {
	REPORT_MD_PATH=$1
	REPORT_PDF_OUT=$2

	pandoc "$REPORT_MD_PATH" -o "$REPORT_PDF_OUT" \
		--from markdown+yaml_metadata_block+raw_html \
		--template eisvogel \
		--listing \
		-V colorlinks=true \
		-V linkcolor=orange \
		-V urlcolor=orange \
		-V toccolor=black \
		--table-of-contents \
		--toc-depth 6 \
		--number-sections \
		--top-level-division=chapter \
		--highlight-style zenburn \
		--resource-path=.:src \
		--resource-path=.:/usr/share/osert/src

	[ $? -eq 1 ] && echo "[ERROR]: Problems during generation of PDF!" && exit 1
}

# -----

org2pdf() {
	REPORT_ORG_PATH=$1
	REPORT_PDF_OUT=$2

	pandoc "$REPORT_ORG_PATH" -o "$REPORT_PDF_OUT" \
		--from org \
		--template eisvogel \
		--listing \
		-V colorlinks=true \
		-V linkcolor=orange \
		-V urlcolor=orange \
		-V toccolor=black \
		-V titlepage=true \
		-V titlepage-color="F2F3F5" \
		-V titlepage-text-color="000000" \
		-V titlepage-rule-color="000000" \
		-V titlepage-rule-height=2 \
		-V book=true \
		-V classoption=oneside \
		-V code-block-font-size=\\scriptsize \
		--table-of-contents \
		--toc-depth 6 \
		--number-sections \
		--top-level-division=chapter \
		--highlight-style zenburn \
		--resource-path=.:src \
		--resource-path=.:/usr/share/osert/src

	[ $? -eq 1 ] && echo "[ERROR]: Problems during generation of PDF!" && exit 1
}

# -----

main() {
	echo "[INFO]: Checking requirements"

	check_requirements "$@"

	echo "[INFO]: input=$INPUT_PATH"
	echo "[INFO]: output=$REPORT_PDF_PATH"
	echo "[INFO]: All good, we're ready to generate!"

	[ "${INPUT_PATH##*.}" = "org" ] && \
		echo "[INFO]: org->pdf" && \
		org2pdf "$INPUT_PATH" "$REPORT_PDF_PATH"

	[ "${INPUT_PATH##*.}" = "md" ] && \
		echo "[INFO]: md->pdf" && \
		md2pdf "$INPUT_PATH" "$REPORT_PDF_PATH"

	echo "[INFO]: Generated succesfully, creating 7z archive!"
	7z a "$ARCHIVE_NAME" "$REPORT_PDF_PATH" >/dev/null 2>/dev/null
	[ $? -eq 1 ] && echo "[ERROR]: Problems during 7z archive creation!" && exit 1

	if which md5sum >/dev/null 2>&1; then
		MD5=$(md5sum "$ARCHIVE_NAME" | awk -F '  ' '{print $1}')
		[ $? -eq 1 ] && echo "[ERROR]: Problems during computation of MD5" && exit 1
		printf "[INFO]: MD5 of archive (${RED}${MD5}${NC})\n"
	elif which md5 >/dev/null 2>&1; then
		MD5=$(md5 -q "$ARCHIVE_NAME")
		printf "[INFO]: MD5 of archive (${RED}${MD5}${NC})\n"
	fi

	echo "[INFO]: PDF: $REPORT_PDF_PATH"
	echo "[INFO]: 7z:  $ARCHIVE_NAME"
}

# ----------------------------

main "$@"
