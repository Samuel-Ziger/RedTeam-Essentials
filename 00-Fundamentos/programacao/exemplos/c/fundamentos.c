#include <errno.h>
#include <math.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

/* Enum restringe o domínio a quatro valores conhecidos. */
typedef enum {
    CONCEITO_A,
    CONCEITO_B,
    CONCEITO_C,
    CONCEITO_D,
    TOTAL_CONCEITOS
} conceito_t;

typedef struct {
    size_t quantidade;
    double media;
    double menor;
    double maior;
    size_t frequencias[TOTAL_CONCEITOS];
} resumo_notas_t;

static int nota_valida(double nota) {
    return isfinite(nota) && nota >= 0.0 && nota <= 10.0;
}

static conceito_t classificar(double nota) {
    if (nota >= 9.0) return CONCEITO_A;
    if (nota >= 7.0) return CONCEITO_B;
    if (nota >= 5.0) return CONCEITO_C;
    return CONCEITO_D;
}

/*
 * Retorna 1 no sucesso e 0 na falha. O resultado só é escrito no sucesso,
 * evitando que o chamador use parcialmente um valor inválido.
 */
static int ler_nota(const char *texto, double *saida) {
    char *fim = NULL;
    double valor;

    if (texto == NULL || saida == NULL || *texto == '\0') return 0;

    errno = 0;
    valor = strtod(texto, &fim);
    if (errno == ERANGE || fim == texto || *fim != '\0' || !nota_valida(valor)) {
        return 0;
    }

    *saida = valor;
    return 1;
}

static int analisar_notas(
    const double *notas,
    size_t quantidade,
    resumo_notas_t *saida
) {
    resumo_notas_t resumo = {0};
    double total = 0.0;

    if (notas == NULL || saida == NULL || quantidade == 0) return 0;

    resumo.quantidade = quantidade;
    resumo.menor = notas[0];
    resumo.maior = notas[0];

    for (size_t i = 0; i < quantidade; i++) {
        double nota = notas[i];
        if (!nota_valida(nota)) return 0;

        total += nota;
        if (nota < resumo.menor) resumo.menor = nota;
        if (nota > resumo.maior) resumo.maior = nota;
        resumo.frequencias[classificar(nota)]++;
    }

    resumo.media = total / (double)quantidade;
    *saida = resumo;
    return 1;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        fputs("uso: fundamentos NOTA [NOTA ...]\n", stderr);
        return 2;
    }

    size_t quantidade = (size_t)(argc - 1);
    if (quantidade > SIZE_MAX / sizeof(double)) {
        fputs("quantidade de notas excede o limite suportado\n", stderr);
        return EXIT_FAILURE;
    }

    /* calloc devolve memória dinâmica pertencente a main; free encerra a posse. */
    double *notas = calloc(quantidade, sizeof *notas);
    if (notas == NULL) {
        fputs("não foi possível reservar memória\n", stderr);
        return EXIT_FAILURE;
    }

    int status = EXIT_FAILURE;
    for (size_t i = 0; i < quantidade; i++) {
        if (!ler_nota(argv[i + 1], &notas[i])) {
            fprintf(stderr, "nota inválida no argumento %zu: %s\n", i + 1, argv[i + 1]);
            status = 2;
            goto cleanup;
        }
    }

    resumo_notas_t resumo;
    if (!analisar_notas(notas, quantidade, &resumo)) {
        fputs("não foi possível analisar as notas\n", stderr);
        goto cleanup;
    }

    printf(
        "media=%.2f conceitos={A:%zu,B:%zu,C:%zu,D:%zu}\n",
        resumo.media,
        resumo.frequencias[CONCEITO_A],
        resumo.frequencias[CONCEITO_B],
        resumo.frequencias[CONCEITO_C],
        resumo.frequencias[CONCEITO_D]
    );
    status = EXIT_SUCCESS;

cleanup:
    free(notas);
    return status;
}
