import JobList from "../components/Jobs/JobList";
import { useJobs, useCancelJob } from "../hooks/useJobs";

export default function JobsPage() {
  const { data: jobs, isLoading } = useJobs();
  const cancelJob = useCancelJob();

  if (isLoading) {
    return <div className="text-center py-8 text-gray-500">Loading...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">Ingestion Jobs</h2>
      <JobList jobs={jobs ?? []} onCancel={(id) => cancelJob.mutate(id)} />
    </div>
  );
}
