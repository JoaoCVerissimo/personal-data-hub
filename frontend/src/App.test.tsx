import { describe, it, expect, afterEach } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter } from "react-router-dom";
import App from "./App";

afterEach(cleanup);

function renderApp(route = "/") {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={[route]}>
        <App />
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

describe("App", () => {
  it("renders the sidebar with navigation links", () => {
    renderApp();
    expect(screen.getByText("Personal Data Hub")).toBeDefined();
    expect(screen.getByRole("link", { name: "Search" })).toBeDefined();
    expect(screen.getByRole("link", { name: "Sources" })).toBeDefined();
    expect(screen.getByRole("link", { name: "Jobs" })).toBeDefined();
    expect(screen.getByRole("link", { name: "Dashboard" })).toBeDefined();
    expect(screen.getByRole("link", { name: "Settings" })).toBeDefined();
  });

  it("renders the search page by default", () => {
    renderApp("/");
    expect(screen.getByRole("heading", { name: "Search Your Data" })).toBeDefined();
    expect(screen.getByPlaceholderText(/search your data/i)).toBeDefined();
  });

  it("renders the settings page", () => {
    renderApp("/settings");
    expect(screen.getByRole("heading", { name: "Settings" })).toBeDefined();
  });
});
