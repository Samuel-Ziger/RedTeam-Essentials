import assert from "node:assert/strict";
import test from "node:test";

import { DependencyGraph } from "./dependencyGraph.mjs";

test("pre-requisitos aparecem antes dos dependentes", () => {
  const graph = new DependencyGraph();
  graph.addDependency("api", "modelo");
  graph.addDependency("testes", "api");
  graph.addDependency("release", "testes");
  graph.addDependency("release", "docs");
  const order = graph.topologicalOrder();

  assert.ok(order.indexOf("modelo") < order.indexOf("api"));
  assert.ok(order.indexOf("api") < order.indexOf("testes"));
  assert.ok(order.indexOf("docs") < order.indexOf("release"));
});

test("ciclo e rejeitado", () => {
  const graph = new DependencyGraph();
  graph.addDependency("A", "B");
  graph.addDependency("B", "A");

  assert.throws(() => graph.topologicalOrder(), /ciclo detectado entre: A, B/);
});

test("identificador vazio e rejeitado", () => {
  assert.throws(() => new DependencyGraph().addNode(" "), TypeError);
});

test("entrada invalida nao deixa mutacao parcial", () => {
  const graph = new DependencyGraph();

  assert.throws(() => graph.addDependency("api", " modelo"), /ASCII seguro/);
  assert.deepEqual(graph.topologicalOrder(), []);
});

test("Unicode e rejeitado para preservar ordem comum entre runtimes", () => {
  assert.throws(() => new DependencyGraph().addNode("tarefa-á"), /ASCII seguro/);
});
