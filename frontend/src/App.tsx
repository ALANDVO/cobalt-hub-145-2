import { useState } from "react";
import { loadContext, ContextLoadRequest, ContextLoadResponse } from "./api";

function App() {
  const [projectRoot, setProjectRoot] = useState(".");
  const [productPath, setProductPath] = useState("");
  const [designPath, setDesignPath] = useState("");
  const [response, setResponse] = useState<ContextLoadResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLoad = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const request: ContextLoadRequest = {
        project_root: projectRoot,
        product_path: productPath || undefined,
        design_path: designPath || undefined,
      };
      const result = await loadContext(request);
      setResponse(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  const renderFile = (file: ContextLoadResponse["product"]) => {
    if (!file) return <div className="missing">Not found</div>;
    return (
      <div>
        <div className="file-meta">
          Path: {file.path} | SHA-256: {file.sha256.slice(0, 16)}... | {file.size_bytes} bytes
        </div>
        <pre className="file-content">{file.content}</pre>
      </div>
    );
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "900px", margin: "0 auto", fontFamily: "system-ui, sans-serif" }}>
      <h1>cobalt-hub-145-alan-vo</h1>
      <p style={{ color: "#666" }}>The design language that makes your AI harness better at design.</p>

      <form onSubmit={handleLoad} style={{ marginBottom: "2rem", display: "flex", flexDirection: "column", gap: "1rem", maxWidth: "500px" }}>
        <div>
          <label htmlFor="project-root" style={{ display: "block", marginBottom: "0.25rem", fontWeight: 500 }}>Project Root</label>
          <input
            id="project-root"
            type="text"
            value={projectRoot}
            onChange={(e) => setProjectRoot(e.target.value)}
            style={{ width: "100%", padding: "0.5rem", fontSize: "1rem" }}
            placeholder="."
          />
        </div>
        <div>
          <label htmlFor="product-path" style={{ display: "block", marginBottom: "0.25rem", fontWeight: 500 }}>Product Path (optional)</label>
          <input
            id="product-path"
            type="text"
            value={productPath}
            onChange={(e) => setProductPath(e.target.value)}
            style={{ width: "100%", padding: "0.5rem", fontSize: "1rem" }}
            placeholder="e.g., governance/context/product.md"
          />
        </div>
        <div>
          <label htmlFor="design-path" style={{ display: "block", marginBottom: "0.25rem", fontWeight: 500 }}>Design Path (optional)</label>
          <input
            id="design-path"
            type="text"
            value={designPath}
            onChange={(e) => setDesignPath(e.target.value)}
            style={{ width: "100%", padding: "0.5rem", fontSize: "1rem" }}
            placeholder="e.g., docs/brand/design.md"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          style={{ padding: "0.75rem 1.5rem", fontSize: "1rem", alignSelf: "flex-start" }}
        >
          {loading ? "Loading..." : "Load Context"}
        </button>
      </form>

      {error && <div style={{ color: "#dc2626", marginBottom: "1rem", padding: "1rem", background: "#fef2f2", borderRadius: "4px" }}>{error}</div>}

      {response && (
        <div>
          {response.warnings.length > 0 && (
            <div style={{ marginBottom: "1rem", padding: "1rem", background: "#fffbeb", borderRadius: "4px", color: "#92400e" }}>
              <strong>Warnings:</strong>
              <ul style={{ margin: "0.5rem 0 0 1.5rem" }}>
                {response.warnings.map((w, i) => <li key={i}>{w}</li>)}
              </ul>
            </div>
          )}

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1.5rem" }}>
            <div>
              <h2>PRODUCT.md</h2>
              {renderFile(response.product)}
            </div>
            <div>
              <h2>DESIGN.md</h2>
              {renderFile(response.design)}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
