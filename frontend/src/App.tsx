import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout/Layout";
import SearchPage from "./pages/SearchPage";
import SourcesPage from "./pages/SourcesPage";
import JobsPage from "./pages/JobsPage";
import DashboardPage from "./pages/DashboardPage";
import SourceDetailPage from "./pages/SourceDetailPage";
import SettingsPage from "./pages/SettingsPage";

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<SearchPage />} />
        <Route path="/sources" element={<SourcesPage />} />
        <Route path="/sources/:sourceId" element={<SourceDetailPage />} />
        <Route path="/jobs" element={<JobsPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Routes>
    </Layout>
  );
}
