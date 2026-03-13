import type { SearchResult } from "../../api/types";
import ResultCard from "./ResultCard";

interface ResultListProps {
  results: SearchResult[];
  total: number;
  queryTimeMs: number;
}

export default function ResultList({ results, total, queryTimeMs }: ResultListProps) {
  if (results.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        No results found. Try a different query or add more data sources.
      </div>
    );
  }

  return (
    <div>
      <p className="text-sm text-gray-500 mb-4">
        {total} results in {queryTimeMs}ms
      </p>
      <div className="space-y-3">
        {results.map((result) => (
          <ResultCard key={result.chunk_id} result={result} />
        ))}
      </div>
    </div>
  );
}
