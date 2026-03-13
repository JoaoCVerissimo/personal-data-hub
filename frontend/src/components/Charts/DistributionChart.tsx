import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from "recharts";
import type { ChartDataPoint } from "../../api/types";

interface DistributionChartProps {
  data: ChartDataPoint[];
  title: string;
}

const COLORS = ["#8b5cf6", "#3b82f6", "#22c55e", "#eab308", "#ef4444", "#ec4899"];

export default function DistributionChart({ data, title }: DistributionChartProps) {
  if (data.length === 0) {
    return <div className="text-center py-8 text-gray-400">No data</div>;
  }

  return (
    <div>
      <h3 className="text-sm font-medium text-gray-700 mb-3">{title}</h3>
      <ResponsiveContainer width="100%" height={250}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="label"
            cx="50%"
            cy="50%"
            outerRadius={80}
            label={({ label, value }) => `${label}: ${value}`}
          >
            {data.map((_, index) => (
              <Cell key={index} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
