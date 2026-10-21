import assert from "node:assert/strict";
import test from "node:test";

import {
  ScoreValidationError,
  concept,
  main,
  parseScores,
  summarize,
  validateScore,
} from "./fundamentos.mjs";

test("classifies every boundary", () => {
  const cases = new Map([
    [10, "A"],
    [9, "A"],
    [8.999, "B"],
    [7, "B"],
    [5, "C"],
    [0, "D"],
  ]);
  for (const [score, expected] of cases) assert.equal(concept(score), expected);
});

test("summarizes without mutating its source", () => {
  const scores = [10, 8, 4];
  assert.deepEqual(summarize(scores), {
    count: 3,
    average: 7.33,
    concepts: { A: 1, B: 1, C: 0, D: 1 },
  });
  assert.deepEqual(scores, [10, 8, 4]);
});

test("summarize accepts a generator", () => {
  function* scores() {
    yield 9;
    yield 5;
  }
  assert.equal(summarize(scores()).average, 7);
});

test("rejects types, non-finite values and out-of-range scores", () => {
  for (const score of ["8", null, undefined, -1, 11, Number.NaN, Number.POSITIVE_INFINITY]) {
    assert.throws(() => validateScore(score), ScoreValidationError);
  }
  assert.throws(() => summarize([]), ScoreValidationError);
  assert.throws(() => summarize(null), TypeError);
});

test("parses only explicit valid numeric arguments", () => {
  assert.deepEqual(parseScores(["10", "7.5", "0"]), [10, 7.5, 0]);
  assert.throws(() => parseScores([""]), /argument 1 is empty/);
  assert.throws(
    () => parseScores(["8", "oito"]),
    (error) => error instanceof ScoreValidationError && error.cause instanceof Error,
  );
});

test("main separates output from error and returns process-style codes", () => {
  const output = [];
  const errors = [];
  assert.equal(main(["10", "8", "4"], { stdout: (line) => output.push(line), stderr: (line) => errors.push(line) }), 0);
  assert.equal(JSON.parse(output[0]).average, 7.33);
  assert.deepEqual(errors, []);

  assert.equal(main(["11"], { stdout: () => {}, stderr: (line) => errors.push(line) }), 2);
  assert.match(errors.at(-1), /between 0 and 10/);
});
