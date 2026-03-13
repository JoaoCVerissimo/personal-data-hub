import { useState, FormEvent } from "react";
import type { SourceCreate } from "../../api/types";

interface AddSourceModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (source: SourceCreate) => void;
}

const SOURCE_TYPES = [
  { value: "github", label: "GitHub Repository" },
  { value: "email", label: "Email (mbox/eml)" },
  { value: "document", label: "Documents (txt/pdf)" },
  { value: "markdown", label: "Markdown Notes" },
];

export default function AddSourceModal({
  isOpen,
  onClose,
  onSubmit,
}: AddSourceModalProps) {
  const [name, setName] = useState("");
  const [sourceType, setSourceType] = useState("github");
  const [configValue, setConfigValue] = useState("");

  if (!isOpen) return null;

  const getConfigPlaceholder = () => {
    switch (sourceType) {
      case "github":
        return "owner/repo";
      case "email":
        return "/path/to/emails.mbox";
      case "document":
        return "/path/to/documents/";
      case "markdown":
        return "/path/to/notes/";
      default:
        return "";
    }
  };

  const getConfigKey = () => {
    return sourceType === "github" ? "repo" : "path";
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    onSubmit({
      name,
      source_type: sourceType,
      config: { [getConfigKey()]: configValue },
    });
    setName("");
    setConfigValue("");
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 className="text-lg font-bold mb-4">Add Data Source</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Name
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="My data source"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Type
            </label>
            <select
              value={sourceType}
              onChange={(e) => setSourceType(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {SOURCE_TYPES.map((t) => (
                <option key={t.value} value={t.value}>
                  {t.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {sourceType === "github" ? "Repository" : "Path"}
            </label>
            <input
              type="text"
              value={configValue}
              onChange={(e) => setConfigValue(e.target.value)}
              required
              placeholder={getConfigPlaceholder()}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="flex justify-end gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Add Source
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
