import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { fetchSources, fetchSource, fetchSourceDocuments, createSource, deleteSource, syncSource } from "../api/sources";
import type { SourceCreate } from "../api/types";

export function useSources() {
  return useQuery({
    queryKey: ["sources"],
    queryFn: fetchSources,
  });
}

export function useSource(id: string) {
  return useQuery({
    queryKey: ["sources", id],
    queryFn: () => fetchSource(id),
  });
}

export function useSourceDocuments(sourceId: string, page: number = 1) {
  return useQuery({
    queryKey: ["sources", sourceId, "documents", page],
    queryFn: () => fetchSourceDocuments(sourceId, page),
  });
}

export function useCreateSource() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: SourceCreate) => createSource(payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["sources"] }),
  });
}

export function useDeleteSource() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => deleteSource(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["sources"] }),
  });
}

export function useSyncSource() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => syncSource(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["sources"] });
      queryClient.invalidateQueries({ queryKey: ["jobs"] });
    },
  });
}
