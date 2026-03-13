import client from "./client";
import type { Job } from "./types";

export async function fetchJobs(sourceId?: string): Promise<Job[]> {
  const params = sourceId ? { source_id: sourceId } : {};
  const { data } = await client.get<Job[]>("/jobs", { params });
  return data;
}

export async function cancelJob(id: string): Promise<void> {
  await client.delete(`/jobs/${id}`);
}
