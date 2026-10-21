/* Ordenacao topologica deterministica em C17, sem alocacao dinamica. */
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define MAX_NODES 32
#define MAX_ID 32

typedef struct {
    char ids[MAX_NODES][MAX_ID];
    bool edges[MAX_NODES][MAX_NODES]; /* prerequisite -> dependent */
    size_t count;
} Graph;

static void graph_init(Graph *graph) {
    memset(graph, 0, sizeof(*graph));
}

static int graph_find(const Graph *graph, const char *id) {
    for (size_t index = 0; index < graph->count; ++index) {
        if (strcmp(graph->ids[index], id) == 0) {
            return (int)index;
        }
    }
    return -1;
}

static bool graph_valid_id(const char *id) {
    if (id == NULL || id[0] == '\0' || strlen(id) >= MAX_ID) {
        return false;
    }
    for (size_t index = 0; id[index] != '\0'; ++index) {
        unsigned char value = (unsigned char)id[index];
        bool alpha_numeric = (value >= 'A' && value <= 'Z') ||
                             (value >= 'a' && value <= 'z') ||
                             (value >= '0' && value <= '9');
        if (!alpha_numeric &&
            (index == 0 || (value != '.' && value != '_' && value != '-'))) {
            return false;
        }
    }
    return true;
}

static int graph_add_node(Graph *graph, const char *id) {
    int existing;
    if (!graph_valid_id(id)) {
        return -1;
    }
    existing = graph_find(graph, id);
    if (existing >= 0) {
        return existing;
    }
    if (graph->count == MAX_NODES) {
        return -1;
    }
    (void)snprintf(graph->ids[graph->count], MAX_ID, "%s", id);
    return (int)graph->count++;
}

static bool graph_add_dependency(Graph *graph, const char *task, const char *prerequisite) {
    int task_index;
    int prerequisite_index;
    size_t missing = 0;

    /* Validar formato e capacidade antes da primeira mutacao torna a operacao atomica. */
    if (!graph_valid_id(task) || !graph_valid_id(prerequisite)) {
        return false;
    }
    task_index = graph_find(graph, task);
    prerequisite_index = graph_find(graph, prerequisite);
    if (task_index < 0) {
        ++missing;
    }
    if (prerequisite_index < 0 && strcmp(task, prerequisite) != 0) {
        ++missing;
    }
    if (missing > MAX_NODES - graph->count) {
        return false;
    }

    task_index = graph_add_node(graph, task);
    prerequisite_index = graph_add_node(graph, prerequisite);
    if (task_index < 0 || prerequisite_index < 0) {
        return false;
    }
    graph->edges[prerequisite_index][task_index] = true;
    return true;
}

static int lexicographically_first_ready(
    const Graph *graph, const size_t indegree[MAX_NODES], const bool emitted[MAX_NODES]
) {
    int best = -1;
    for (size_t index = 0; index < graph->count; ++index) {
        if (!emitted[index] && indegree[index] == 0 &&
            (best < 0 || strcmp(graph->ids[index], graph->ids[best]) < 0)) {
            best = (int)index;
        }
    }
    return best;
}

/* Retorna quantidade de itens; SIZE_MAX indica ciclo. */
static size_t graph_topological_order(const Graph *graph, size_t output[MAX_NODES]) {
    size_t indegree[MAX_NODES] = {0};
    bool emitted[MAX_NODES] = {false};
    size_t produced = 0;

    for (size_t from = 0; from < graph->count; ++from) {
        for (size_t to = 0; to < graph->count; ++to) {
            if (graph->edges[from][to]) {
                ++indegree[to];
            }
        }
    }

    while (produced < graph->count) {
        int current = lexicographically_first_ready(graph, indegree, emitted);
        if (current < 0) {
            return SIZE_MAX;
        }
        emitted[current] = true;
        output[produced++] = (size_t)current;
        for (size_t dependent = 0; dependent < graph->count; ++dependent) {
            if (graph->edges[current][dependent]) {
                if (indegree[dependent] == 0) {
                    return SIZE_MAX; /* invariante interna violada */
                }
                --indegree[dependent];
            }
        }
    }
    return produced;
}

static size_t position_of(
    const Graph *graph, const size_t order[MAX_NODES], size_t count, const char *id
) {
    for (size_t index = 0; index < count; ++index) {
        if (strcmp(graph->ids[order[index]], id) == 0) {
            return index;
        }
    }
    return SIZE_MAX;
}

static bool check(bool condition, const char *message) {
    if (!condition) {
        fprintf(stderr, "falha: %s\n", message);
        return false;
    }
    return true;
}

int main(void) {
    Graph graph;
    size_t order[MAX_NODES];
    graph_init(&graph);
    if (!check(graph_add_dependency(&graph, "api", "modelo"), "modelo -> api") ||
        !check(graph_add_dependency(&graph, "testes", "api"), "api -> testes") ||
        !check(graph_add_dependency(&graph, "release", "testes"), "testes -> release") ||
        !check(graph_add_dependency(&graph, "release", "docs"), "docs -> release")) {
        return 1;
    }

    Graph invalid;
    graph_init(&invalid);
    if (!check(!graph_add_dependency(&invalid, "api", " modelo"), "ID invalido deve falhar") ||
        !check(invalid.count == 0, "falha nao pode deixar mutacao parcial")) {
        return 1;
    }

    size_t count = graph_topological_order(&graph, order);
    if (!check(count == graph.count, "grafo aciclico deve produzir todos os nos") ||
        !check(
            position_of(&graph, order, count, "modelo") <
                position_of(&graph, order, count, "api"),
            "modelo deve preceder api"
        ) ||
        !check(
            position_of(&graph, order, count, "api") <
                position_of(&graph, order, count, "testes"),
            "api deve preceder testes"
        )) {
        return 1;
    }
    for (size_t index = 0; index < count; ++index) {
        printf("%s%s", graph.ids[order[index]], index + 1 == count ? "\n" : " -> ");
    }

    Graph cyclic;
    graph_init(&cyclic);
    if (!check(graph_add_dependency(&cyclic, "A", "B"), "B -> A") ||
        !check(graph_add_dependency(&cyclic, "B", "A"), "A -> B") ||
        !check(graph_topological_order(&cyclic, order) == SIZE_MAX, "ciclo deve ser rejeitado")) {
        return 1;
    }
    puts("ciclo detectado corretamente");
    return 0;
}
