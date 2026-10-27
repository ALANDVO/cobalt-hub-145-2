export interface ContextFile {
  path: string;
  content: string;
  sha256: string;
  size_bytes: number;
}

export interface ContextLoadRequest {
  project_root: string;
  product_path?: string;
  design_path?: string;
}

export interface ContextLoadResponse {
  project_root: string;
  product: ContextFile | null;
  design: ContextFile | null;
  warnings: string[];
}

export interface HealthResponse {
  status: string;
  version: string;
}

const API_BASE = "";

export async function checkHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE}/health`);
  if (!response.ok) {
    throw new Error(`Health check failed: ${response.status}`);
  }
  return response.json();
}

export async function loadContext(request: ContextLoadRequest): Promise<ContextLoadResponse> {
  const response = await fetch(`${API_BASE}/context/load`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(error.detail || `Request failed: ${response.status}`);
  }
  return response.json();
}
