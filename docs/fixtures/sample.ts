// Fixture file used for theme screenshots.
// Exercises: interfaces, generics, async, template strings,
// numbers, keywords, comments, errors.

declare function fetchStatement(path: string): Promise<string>;

export interface Statement<T extends string = string> {
  readonly id: T;
  amount: number;
  currency: "EUR" | "USD" | "GBP";
  tags?: readonly string[];
}

export type Aggregate = Readonly<{
  total: number;
  count: number;
  skipped: number;
}>;

const DEFAULT_THRESHOLD = 0.01 as const;

export async function load(path: string): Promise<Statement[]> {
  const raw = await fetchStatement(path);
  if (!raw.trim()) {
    throw new Error(`empty statement: ${path}`);
  }
  return JSON.parse(raw) as Statement[];
}

export function aggregate(
  rows: readonly Statement[],
  { threshold = DEFAULT_THRESHOLD }: { threshold?: number } = {},
): Aggregate {
  let total = 0;
  let skipped = 0;
  for (const row of rows) {
    if (row.amount < threshold) {
      skipped += 1;
      continue; // dust — ignored for rollups
    }
    total += row.amount;
  }
  return { total, count: rows.length - skipped, skipped };
}
