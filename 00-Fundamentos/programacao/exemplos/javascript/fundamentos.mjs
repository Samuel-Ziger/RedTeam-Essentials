#!/usr/bin/env node
/**
 * Analisador de notas autocontido.
 *
 * As funções de domínio não dependem de console/process, portanto o mesmo
 * módulo pode ser usado no Node.js, em testes ou no navegador.
 */
import { pathToFileURL } from "node:url";

export const CONCEPTS = Object.freeze(["A", "B", "C", "D"]);

export class ScoreValidationError extends RangeError {
  constructor(message, options) {
    super(message, options);
    this.name = "ScoreValidationError";
  }
}

export function validateScore(score) {
  if (typeof score !== "number" || !Number.isFinite(score)) {
    throw new ScoreValidationError("score must be a finite number");
  }
  if (score < 0 || score > 10) {
    throw new ScoreValidationError("score must be between 0 and 10");
  }
  return score;
}

export function concept(score) {
  const value = validateScore(score);
  if (value >= 9) return "A";
  if (value >= 7) return "B";
  if (value >= 5) return "C";
  return "D";
}

export function summarize(scores) {
  if (scores == null || typeof scores[Symbol.iterator] !== "function") {
    throw new TypeError("scores must be iterable");
  }

  // Materializamos uma vez para aceitar qualquer iterável e preservar a fonte.
  const values = Array.from(scores, validateScore);
  if (values.length === 0) {
    throw new ScoreValidationError("provide at least one score");
  }

  const concepts = Object.fromEntries(CONCEPTS.map((label) => [label, 0]));
  let total = 0;
  for (const score of values) {
    total += score;
    concepts[concept(score)] += 1;
  }

  return {
    count: values.length,
    average: Number((total / values.length).toFixed(2)),
    concepts,
  };
}

export function parseScores(arguments_) {
  return arguments_.map((text, index) => {
    // Number("") seria zero; a fronteira rejeita texto vazio explicitamente.
    if (typeof text !== "string" || text.trim() === "") {
      throw new ScoreValidationError(`argument ${index + 1} is empty`);
    }
    const value = Number(text);
    try {
      return validateScore(value);
    } catch (error) {
      throw new ScoreValidationError(
        `invalid argument ${index + 1} (${JSON.stringify(text)}): ${error.message}`,
        { cause: error },
      );
    }
  });
}

export function main(arguments_, { stdout = console.log, stderr = console.error } = {}) {
  if (arguments_.length === 0) {
    stderr("usage: node fundamentos.mjs SCORE [SCORE ...]");
    return 2;
  }

  try {
    stdout(JSON.stringify(summarize(parseScores(arguments_))));
    return 0;
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    stderr(`error: ${message}`);
    return 2;
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  process.exitCode = main(process.argv.slice(2));
}
