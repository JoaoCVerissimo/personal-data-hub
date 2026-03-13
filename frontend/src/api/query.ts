import client from "./client";
import type { SearchResponse, QueryFilters } from "./types";

export async function search(
  query: string,
  filters?: QueryFilters,
  limit: number = 20,
): Promise<SearchResponse> {
  const { data } = await client.post<SearchResponse>("/query/search", {
    query,
    filters,
    limit,
  });
  return data;
}
