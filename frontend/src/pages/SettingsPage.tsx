export default function SettingsPage() {
  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">Settings</h2>
      <div className="bg-white border border-gray-200 rounded-lg p-6 space-y-6">
        <div>
          <h3 className="font-medium text-gray-900 mb-2">Embedding Model</h3>
          <p className="text-sm text-gray-500 mb-2">
            Currently using: <code className="bg-gray-100 px-1 rounded">all-mpnet-base-v2</code>
          </p>
          <p className="text-xs text-gray-400">
            Change the EMBEDDING_MODEL environment variable to use a different model.
          </p>
        </div>
        <div>
          <h3 className="font-medium text-gray-900 mb-2">Chunk Size</h3>
          <p className="text-sm text-gray-500 mb-2">
            Current: <code className="bg-gray-100 px-1 rounded">512 tokens</code> with{" "}
            <code className="bg-gray-100 px-1 rounded">50 token</code> overlap
          </p>
          <p className="text-xs text-gray-400">
            Adjust via CHUNK_SIZE and CHUNK_OVERLAP environment variables.
          </p>
        </div>
        <div>
          <h3 className="font-medium text-gray-900 mb-2">Data Mount Path</h3>
          <p className="text-sm text-gray-500">
            Local files are accessible from:{" "}
            <code className="bg-gray-100 px-1 rounded">/data</code>
          </p>
          <p className="text-xs text-gray-400">
            Set DATA_MOUNT_PATH in .env to change the mounted directory.
          </p>
        </div>
      </div>
    </div>
  );
}
