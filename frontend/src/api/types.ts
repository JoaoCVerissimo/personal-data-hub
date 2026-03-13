export interface Source {
  id: string;
  name: string;
  source_type: string;
  config: Record<string, unknown>;
  status: string;
  document_count: number;
  last_synced_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface SourceCreate {
  name: string;
  source_type: string;
  config: Record<string, unknown>;
}

export interface Job {
  id: string;
  source_id: string;
  status: string;
  job_type: string;
  documents_total: number;
  documents_processed: number;
  chunks_created: number;
  error_message: string | null;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
}

export interface SearchResult {
  chunk_id: string;
  document_id: string;
  document_title: string | null;
  source_name: string;
  source_type: string;
  content: string;
  score: number;
  metadata: Record<string, unknown>;
}

export interface SearchResponse {
  results: SearchResult[];
  total: number;
  query_time_ms: number;
}

export interface QueryFilters {
  source_types?: string[];
  source_ids?: string[];
  doc_types?: string[];
}

export interface ChartDataPoint {
  label: string;
  value: number;
}

export interface TimeSeriesPoint {
  date: string;
  value: number;
}

export interface DocumentItem {
  id: string;
  source_id: string;
  title: string | null;
  doc_type: string;
  content_hash: string | null;
  created_at: string;
}

export interface PaginatedDocuments {
  items: DocumentItem[];
  total: number;
  page: number;
  size: number;
}
