#!/usr/bin/env sh
# Gera PDF e arquivo 7z a partir de Markdown ou Org.
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPORT_ID=${REPORT_ID:-LAB}
OSID=${OSID:-}
INPUT_PATH=${ROOT}/relatorio.md

die() {
	printf '[ERRO] %s\n' "$1" >&2
	exit 1
}

validate_identifier() {
	name=$1
	value=$2
	case "$value" in
		''|*[!A-Za-z0-9._-]*) die "$name deve conter somente letras, numeros, ponto, sublinhado ou hifen" ;;
	esac
}

validate_identifier REPORT_ID "$REPORT_ID"
if [ -n "$OSID" ]; then
	validate_identifier OSID "$OSID"
	BASENAME=OSCP-OS-${OSID}-Exam-Report
else
	BASENAME=RTE-Report-${REPORT_ID}
fi
REPORT_PDF_PATH=${ROOT}/${BASENAME}.pdf
ARCHIVE_NAME=${ROOT}/${BASENAME}.7z

check_requirements() {
	if [ "$#" -eq 1 ]; then
		[ -f "$1" ] || die "arquivo de entrada inexistente: $1"
		INPUT_PATH=$1
	elif [ "$#" -gt 1 ]; then
		die 'use no maximo um argumento (caminho do .md/.org)'
	fi
	[ -f "$INPUT_PATH" ] || die "relatorio ausente: $INPUT_PATH (copie ../REPORT-TEMPLATE.md)"
	case "${INPUT_PATH##*.}" in
		md|org) ;;
		*) die "o arquivo de entrada deve terminar em .md ou .org" ;;
	esac
	command -v pandoc >/dev/null 2>&1 || die 'pandoc nao encontrado'
	command -v 7z >/dev/null 2>&1 || die '7z nao encontrado'
}

convert_report() {
	input=$1
	output=$2
	format=$3
	resource_dir=$(CDPATH= cd -- "$(dirname -- "$input")" && pwd)
	pandoc "$input" -o "$output" \
		--from "$format" \
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
		--resource-path="${resource_dir}:${resource_dir}/src:${ROOT}/src"
}

main() {
	check_requirements "$@"
	printf '[INFO] entrada: %s\n' "$INPUT_PATH"
	printf '[INFO] saida:   %s\n' "$REPORT_PDF_PATH"
	case "${INPUT_PATH##*.}" in
		md) convert_report "$INPUT_PATH" "$REPORT_PDF_PATH" markdown+yaml_metadata_block+raw_html ;;
		org) convert_report "$INPUT_PATH" "$REPORT_PDF_PATH" org ;;
	esac
	7z a -y "$ARCHIVE_NAME" "$REPORT_PDF_PATH" >/dev/null
	if command -v sha256sum >/dev/null 2>&1; then
		sha256sum "$ARCHIVE_NAME"
	elif command -v shasum >/dev/null 2>&1; then
		shasum -a 256 "$ARCHIVE_NAME"
	else
		printf '[AVISO] utilitario SHA-256 nao encontrado.\n' >&2
	fi
	printf '[OK] PDF: %s\n[OK] 7z:  %s\n' "$REPORT_PDF_PATH" "$ARCHIVE_NAME"
}

main "$@"
