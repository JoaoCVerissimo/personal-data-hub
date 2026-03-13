import { useState } from "react";
import SourceCard from "../components/Sources/SourceCard";
import AddSourceModal from "../components/Sources/AddSourceModal";
import { useSources, useCreateSource, useDeleteSource, useSyncSource } from "../hooks/useSources";
import type { SourceCreate } from "../api/types";

export default function SourcesPage() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { data: sources, isLoading } = useSources();
  const createSource = useCreateSource();
  const deleteSource = useDeleteSource();
  const syncSource = useSyncSource();

  const handleAdd = (payload: SourceCreate) => {
    createSource.mutate(payload);
  };

  if (isLoading) {
    return <div className="text-center py-8 text-gray-500">Loading...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">Data Sources</h2>
        <button
          onClick={() => setIsModalOpen(true)}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Add Source
        </button>
      </div>
      {sources && sources.length > 0 ? (
        <div className="grid gap-4 sm:grid-cols-2">
          {sources.map((source) => (
            <SourceCard
              key={source.id}
              source={source}
              onSync={(id) => syncSource.mutate(id)}
              onDelete={(id) => deleteSource.mutate(id)}
            />
          ))}
        </div>
      ) : (
        <div className="text-center py-12 text-gray-500">
          No data sources yet. Click "Add Source" to get started.
        </div>
      )}
      <AddSourceModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleAdd}
      />
    </div>
  );
}
