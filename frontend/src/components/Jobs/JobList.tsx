import type { Job } from "../../api/types";

interface JobListProps {
  jobs: Job[];
  onCancel: (id: string) => void;
}

const STATUS_STYLES: Record<string, string> = {
  pending: "bg-yellow-100 text-yellow-800",
  running: "bg-blue-100 text-blue-800",
  completed: "bg-green-100 text-green-800",
  failed: "bg-red-100 text-red-800",
  cancelled: "bg-gray-100 text-gray-800",
};

export default function JobList({ jobs, onCancel }: JobListProps) {
  if (jobs.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No ingestion jobs yet. Add a source and trigger a sync.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {jobs.map((job) => {
        const statusClass = STATUS_STYLES[job.status] ?? "bg-gray-100 text-gray-800";
        const progress =
          job.documents_total > 0
            ? Math.round((job.documents_processed / job.documents_total) * 100)
            : 0;

        return (
          <div key={job.id} className="border border-gray-200 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${statusClass}`}>
                {job.status}
              </span>
              <span className="text-xs text-gray-500">
                {new Date(job.created_at).toLocaleString()}
              </span>
            </div>
            {job.status === "running" && (
              <div className="mb-2">
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all"
                    style={{ width: `${progress}%` }}
                  />
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  {job.documents_processed}/{job.documents_total} documents ({job.chunks_created} chunks)
                </p>
              </div>
            )}
            {job.status === "completed" && (
              <p className="text-sm text-gray-600">
                {job.documents_processed} documents, {job.chunks_created} chunks
              </p>
            )}
            {job.error_message && (
              <p className="text-sm text-red-600 mt-1">{job.error_message}</p>
            )}
            {(job.status === "pending" || job.status === "running") && (
              <button
                onClick={() => onCancel(job.id)}
                className="mt-2 px-3 py-1 text-xs border border-gray-300 rounded hover:bg-gray-50"
              >
                Cancel
              </button>
            )}
          </div>
        );
      })}
    </div>
  );
}
