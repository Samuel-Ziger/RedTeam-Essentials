import { pathToFileURL } from "node:url";

function validateNode(node) {
  if (typeof node !== "string" || !/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(node)) {
    throw new TypeError("o identificador deve usar apenas ASCII seguro");
  }
}

/** Grafo dirigido: uma dependencia aponta para a tarefa que ela libera. */
export class DependencyGraph {
  #prerequisites = new Map();
  #dependents = new Map();

  addNode(node) {
    validateNode(node);
    if (!this.#prerequisites.has(node)) this.#prerequisites.set(node, new Set());
    if (!this.#dependents.has(node)) this.#dependents.set(node, new Set());
  }

  addDependency(task, prerequisite) {
    validateNode(task);
    validateNode(prerequisite);
    this.addNode(task);
    this.addNode(prerequisite);
    this.#prerequisites.get(task).add(prerequisite);
    this.#dependents.get(prerequisite).add(task);
  }

  topologicalOrder() {
    const indegree = new Map(
      [...this.#prerequisites].map(([task, values]) => [task, values.size]),
    );
    const ready = [...indegree]
      .filter(([, degree]) => degree === 0)
      .map(([task]) => task)
      .sort();
    const result = [];

    while (ready.length > 0) {
      const task = ready.shift();
      result.push(task);
      for (const dependent of [...this.#dependents.get(task)].sort()) {
        const degree = indegree.get(dependent) - 1;
        indegree.set(dependent, degree);
        if (degree === 0) {
          ready.push(dependent);
          ready.sort();
        }
      }
    }

    if (result.length !== indegree.size) {
      const blocked = [...indegree]
        .filter(([, degree]) => degree > 0)
        .map(([task]) => task)
        .sort();
      throw new Error(`ciclo detectado entre: ${blocked.join(", ")}`);
    }
    return result;
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const graph = new DependencyGraph();
  graph.addDependency("api", "modelo");
  graph.addDependency("testes", "api");
  console.log(graph.topologicalOrder().join(" -> "));
}
