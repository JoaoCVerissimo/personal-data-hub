import { useNavigate } from "react-router-dom";
import type { Source } from "../../api/types";

interface SourceCardProps {
  source: Source;
  onSync: (id: string) => void;
  onDelete: (id: string) => void;
}

const TYPE_LABELS: Record<string, string> = {
  github: "GitHub",
  email: "Email",
  document: "Documents",
  markdown: "Markdown Notes",
};

export default function SourceCard({ source, onSync, onDelete }: SourceCardProps) {
  const navigate = useNavigate();

  return (
    <div
      className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
      onClick={() => navigate(`/sources/${source.id}`)}
    >
      <div className="flex items-center justify-between mb-2">
        <h3 className="font-medium text-gray-900">{source.name}</h3>
        <span className="text-xs px-2 py-1 bg-gray-100 rounded">
          {TYPE_LABELS[source.source_type] ?? source.source_type}
        </span>
      </div>
      <div className="text-sm text-gray-500 space-y-1">
        <p>{source.document_count} documents</p>
        <p>
          Last synced:{" "}
          {source.last_synced_at
            ? new Date(source.last_synced_at).toLocaleString()
            : "Never"}
        </p>
      </div>
      <div className="mt-3 flex gap-2">
        <button
          onClick={(e) => { e.stopPropagation(); onSync(source.id); }}
          className="px-3 py-1.5 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Sync
        </button>
        <button
          onClick={(e) => { e.stopPropagation(); onDelete(source.id); }}
          className="px-3 py-1.5 text-sm border border-red-300 text-red-600 rounded hover:bg-red-50"
        >
          Delete
        </button>
      </div>
    </div>
  );
}
