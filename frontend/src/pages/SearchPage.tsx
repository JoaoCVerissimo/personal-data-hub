import SearchBar from "../components/Search/SearchBar";
import ResultList from "../components/Search/ResultList";
import { useSearch } from "../hooks/useSearch";

export default function SearchPage() {
  const { mutate, data, isPending } = useSearch();

  const handleSearch = (query: string) => {
    mutate({ query });
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">Search Your Data</h2>
      <SearchBar onSearch={handleSearch} isLoading={isPending} />
      <div className="mt-6">
        {data && (
          <ResultList
            results={data.results}
            total={data.total}
            queryTimeMs={data.query_time_ms}
          />
        )}
      </div>
    </div>
  );
}
