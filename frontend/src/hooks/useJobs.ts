import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { fetchJobs, cancelJob } from "../api/jobs";

export function useJobs(sourceId?: string) {
  return useQuery({
    queryKey: ["jobs", sourceId],
    queryFn: () => fetchJobs(sourceId),
    refetchInterval: 3000,
  });
}

export function useCancelJob() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => cancelJob(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["jobs"] }),
  });
}
