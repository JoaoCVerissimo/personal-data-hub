import type { SearchResult } from "../../api/types";

interface ResultCardProps {
  result: SearchResult;
}

const SOURCE_COLORS: Record<string, string> = {
  github: "bg-purple-100 text-purple-800",
  email: "bg-blue-100 text-blue-800",
  document: "bg-green-100 text-green-800",
  markdown: "bg-yellow-100 text-yellow-800",
};

export default function ResultCard({ result }: ResultCardProps) {
  const badgeClass = SOURCE_COLORS[result.source_type] ?? "bg-gray-100 text-gray-800";
  const scorePercent = Math.round(result.score * 100);

  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-2">
        <h3 className="font-medium text-gray-900 truncate flex-1">
          {result.document_title || "Untitled"}
        </h3>
        <div className="flex items-center gap-2 ml-3">
          <span className={`px-2 py-0.5 rounded text-xs font-medium ${badgeClass}`}>
            {result.source_type}
          </span>
          <span className="text-xs text-gray-500">{scorePercent}%</span>
        </div>
      </div>
      <p className="text-sm text-gray-600 line-clamp-3">{result.content}</p>
      <div className="mt-2 text-xs text-gray-400">
        Source: {result.source_name}
        {result.source_type === "github" && result.source_config?.repos && (
          <span className="ml-1">
            ({(result.source_config.repos as string[]).join(", ")})
          </span>
        )}
      </div>
    </div>
  );
}
