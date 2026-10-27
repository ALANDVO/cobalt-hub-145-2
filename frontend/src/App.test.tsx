import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import App from "./App";
import * as api from "./api";

// Mock the API module
vi.mock("./api", () => ({
  loadContext: vi.fn(),
}));

describe("App", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders the title and description", () => {
    render(<App />);
    expect(screen.getByText("cobalt-hub-145-alan-vo")).toBeInTheDocument();
    expect(screen.getByText("The design language that makes your AI harness better at design.")).toBeInTheDocument();
  });

  it("renders form with project root, product path, and design path inputs", () => {
    render(<App />);
    expect(screen.getByLabelText("Project Root")).toBeInTheDocument();
    expect(screen.getByLabelText("Product Path (optional)")).toBeInTheDocument();
    expect(screen.getByLabelText("Design Path (optional)")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Load Context" })).toBeInTheDocument();
  });

  it("calls loadContext with form values on submit", async () => {
    const mockResponse = {
      project_root: "/test",
      product: { path: "/test/PRODUCT.md", content: "# Product", sha256: "abc123", size_bytes: 10 },
      design: { path: "/test/DESIGN.md", content: "# Design", sha256: "def456", size_bytes: 10 },
      warnings: [],
    };
    (api.loadContext as vi.Mock).mockResolvedValue(mockResponse);

    render(<App />);
    fireEvent.change(screen.getByLabelText("Project Root"), { target: { value: "/my/project" } });
    fireEvent.change(screen.getByLabelText("Product Path (optional)"), { target: { value: "custom/product.md" } });
    fireEvent.click(screen.getByRole("button", { name: "Load Context" }));

    await waitFor(() => {
      expect(api.loadContext).toHaveBeenCalledWith({
        project_root: "/my/project",
        product_path: "custom/product.md",
        design_path: undefined,
      });
    });
  });

  it("displays loaded product and design content", async () => {
    const mockResponse = {
      project_root: "/test",
      product: { path: "/test/PRODUCT.md", content: "# My Product", sha256: "abc123", size_bytes: 12 },
      design: { path: "/test/DESIGN.md", content: "# My Design", sha256: "def456", size_bytes: 11 },
      warnings: [],
    };
    (api.loadContext as vi.Mock).mockResolvedValue(mockResponse);

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Load Context" }));

    await waitFor(() => {
      expect(screen.getByText("# My Product")).toBeInTheDocument();
      expect(screen.getByText("# My Design")).toBeInTheDocument();
    });
  });

  it("displays warnings when files are missing", async () => {
    const mockResponse = {
      project_root: "/test",
      product: { path: "/test/PRODUCT.md", content: "# Product", sha256: "abc123", size_bytes: 10 },
      design: null,
      warnings: ["DESIGN.md not found in project root or common locations"],
    };
    (api.loadContext as vi.Mock).mockResolvedValue(mockResponse);

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Load Context" }));

    await waitFor(() => {
      expect(screen.getByText("DESIGN.md not found in project root or common locations")).toBeInTheDocument();
      expect(screen.getByText("Not found")).toBeInTheDocument();
    });
  });

  it("displays error message on API failure", async () => {
    (api.loadContext as vi.Mock).mockRejectedValue(new Error("Project root not found"));

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Load Context" }));

    await waitFor(() => {
      expect(screen.getByText("Project root not found")).toBeInTheDocument();
    });
  });

  it("shows loading state during request", async () => {
    let resolve: (value: any) => void;
    const promise = new Promise((r) => { resolve = r; });
    (api.loadContext as vi.Mock).mockReturnValue(promise);

    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Load Context" }));

    expect(screen.getByRole("button", { name: "Loading..." })).toBeDisabled();

    resolve!({ project_root: "/test", product: null, design: null, warnings: [] });
    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Load Context" })).not.toBeDisabled();
    });
  });
});
