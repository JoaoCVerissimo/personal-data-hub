import client from "./client";
import type { Source, SourceCreate, Job } from "./types";

export async function fetchSources(): Promise<Source[]> {
  const { data } = await client.get<Source[]>("/sources");
  return data;
}

export async function createSource(payload: SourceCreate): Promise<Source> {
  const { data } = await client.post<Source>("/sources", payload);
  return data;
}

export async function deleteSource(id: string): Promise<void> {
  await client.delete(`/sources/${id}`);
}

export async function syncSource(
  id: string,
  jobType: string = "full",
): Promise<Job> {
  const { data } = await client.post<Job>(`/sources/${id}/sync`, {
    job_type: jobType,
  });
  return data;
}
