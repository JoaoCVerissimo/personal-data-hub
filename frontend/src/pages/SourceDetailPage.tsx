import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useSource, useSourceDocuments, useDeleteSource, useSyncSource } from "../hooks/useSources";

const TYPE_LABELS: Record<string, string> = {
  github: "GitHub",
  email: "Email",
  document: "Documents",
  markdown: "Markdown Notes",
};

function ConfigDisplay({ config }: { config: Record<string, unknown> }) {
  return (
    <dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1 text-sm">
      {Object.entries(config).map(([key, value]) => (
        <div key={key} className="contents">
          <dt className="text-gray-500 font-medium">{key}</dt>
          <dd className="text-gray-900">
            {Array.isArray(value) ? value.join(", ") : String(value)}
          </dd>
        </div>
      ))}
    </dl>
  );
}

export default function SourceDetailPage() {
  const { sourceId } = useParams<{ sourceId: string }>();
  const navigate = useNavigate();
  const [page, setPage] = useState(1);

  const { data: source, isLoading: sourceLoading } = useSource(sourceId!);
  const { data: docs, isLoading: docsLoading } = useSourceDocuments(sourceId!, page);
  const deleteSource = useDeleteSource();
  const syncSource = useSyncSource();

  if (sourceLoading) {
    return <div className="text-gray-500">Loading...</div>;
  }

  if (!source) {
    return <div className="text-gray-500">Source not found.</div>;
  }

  const totalPages = docs ? Math.ceil(docs.total / docs.size) : 1;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-3">
        <button
          onClick={() => navigate("/sources")}
          className="text-gray-400 hover:text-gray-600"
        >
          &larr; Back
        </button>
        <h2 className="text-2xl font-bold text-gray-900 flex-1">{source.name}</h2>
        <button
          onClick={() => syncSource.mutate(source.id)}
          className="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Sync
        </button>
        <button
          onClick={() => {
            if (confirm("Delete this source and all its documents?")) {
              deleteSource.mutate(source.id, { onSuccess: () => navigate("/sources") });
            }
          }}
          className="px-4 py-2 text-sm border border-red-300 text-red-600 rounded hover:bg-red-50"
        >
          Delete
        </button>
      </div>

      {/* Source info */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="border border-gray-200 rounded-lg p-4 space-y-3">
          <h3 className="font-medium text-gray-900">Details</h3>
          <div className="text-sm space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-500">Type</span>
              <span className="px-2 py-0.5 bg-gray-100 rounded text-xs font-medium">
                {TYPE_LABELS[source.source_type] ?? source.source_type}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500">Status</span>
              <span className={`text-xs font-medium ${source.status === "active" ? "text-green-600" : "text-gray-500"}`}>
                {source.status}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500">Documents</span>
              <span>{source.document_count}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500">Last synced</span>
              <span>{source.last_synced_at ? new Date(source.last_synced_at).toLocaleString() : "Never"}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500">Created</span>
              <span>{new Date(source.created_at).toLocaleString()}</span>
            </div>
          </div>
        </div>

        <div className="border border-gray-200 rounded-lg p-4 space-y-3">
          <h3 className="font-medium text-gray-900">Configuration</h3>
          {Object.keys(source.config).length > 0 ? (
            <ConfigDisplay config={source.config} />
          ) : (
            <p className="text-sm text-gray-400">No configuration.</p>
          )}
        </div>
      </div>

      {/* Documents list */}
      <div className="border border-gray-200 rounded-lg p-4">
        <h3 className="font-medium text-gray-900 mb-4">
          Documents {docs && <span className="text-gray-400 font-normal">({docs.total})</span>}
        </h3>

        {docsLoading ? (
          <p className="text-gray-500 text-sm">Loading documents...</p>
        ) : docs && docs.items.length > 0 ? (
          <>
            <div className="divide-y divide-gray-100">
              {docs.items.map((doc) => (
                <div key={doc.id} className="py-3 flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-900">{doc.title || "Untitled"}</p>
                    <p className="text-xs text-gray-400 mt-0.5">
                      {doc.doc_type} &middot; {new Date(doc.created_at).toLocaleDateString()}
                    </p>
                  </div>
                  <span className="text-xs px-2 py-0.5 bg-gray-100 rounded">{doc.doc_type}</span>
                </div>
              ))}
            </div>

            {totalPages > 1 && (
              <div className="flex items-center justify-center gap-2 mt-4">
                <button
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={page === 1}
                  className="px-3 py-1 text-sm border rounded disabled:opacity-40"
                >
                  Previous
                </button>
                <span className="text-sm text-gray-500">
                  Page {page} of {totalPages}
                </span>
                <button
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  disabled={page === totalPages}
                  className="px-3 py-1 text-sm border rounded disabled:opacity-40"
                >
                  Next
                </button>
              </div>
            )}
          </>
        ) : (
          <p className="text-sm text-gray-400">No documents ingested yet. Try syncing this source.</p>
        )}
      </div>
    </div>
  );
}
