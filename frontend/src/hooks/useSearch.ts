import { useMutation } from "@tanstack/react-query";
import { search } from "../api/query";
import type { QueryFilters } from "../api/types";

export function useSearch() {
  return useMutation({
    mutationFn: ({
      query,
      filters,
      limit,
    }: {
      query: string;
      filters?: QueryFilters;
      limit?: number;
    }) => search(query, filters, limit),
  });
}
