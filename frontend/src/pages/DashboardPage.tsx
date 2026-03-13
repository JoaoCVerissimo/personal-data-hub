import { useQuery } from "@tanstack/react-query";
import client from "../api/client";
import DistributionChart from "../components/Charts/DistributionChart";
import TimelineChart from "../components/Charts/TimelineChart";
import type { ChartDataPoint, TimeSeriesPoint } from "../api/types";

export default function DashboardPage() {
  const { data: distribution } = useQuery({
    queryKey: ["charts", "distribution"],
    queryFn: async () => {
      const { data } = await client.get<ChartDataPoint[]>("/charts/source-distribution");
      return data;
    },
  });

  const { data: timeline } = useQuery({
    queryKey: ["charts", "timeline"],
    queryFn: async () => {
      const { data } = await client.get<TimeSeriesPoint[]>("/charts/ingestion-timeline");
      return data;
    },
  });

  const { data: queryActivity } = useQuery({
    queryKey: ["charts", "query-activity"],
    queryFn: async () => {
      const { data } = await client.get<TimeSeriesPoint[]>("/charts/query-activity");
      return data;
    },
  });

  return (
    <div className="max-w-6xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">Dashboard</h2>
      <div className="grid gap-6 md:grid-cols-2">
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <DistributionChart
            data={distribution ?? []}
            title="Documents by Source Type"
          />
        </div>
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <TimelineChart
            data={timeline ?? []}
            title="Ingestion Timeline"
            color="#22c55e"
          />
        </div>
        <div className="bg-white border border-gray-200 rounded-lg p-4 md:col-span-2">
          <TimelineChart
            data={queryActivity ?? []}
            title="Query Activity"
            color="#8b5cf6"
          />
        </div>
      </div>
    </div>
  );
}
