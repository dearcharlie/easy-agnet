import { useEffect, useState } from "react";
import type { Project } from "../store/projectStore";

interface Props {
  onSelect: (project: Project) => void;
}

async function fetchProjects(): Promise<Project[]> {
  try {
    const res = await fetch("http://127.0.0.1:8520/v1/projects");
    if (res.ok) return await res.json();
  } catch {
    // Hermes API may not be running — use Tauri shell command
  }

  // Fallback: parse from Tauri invoke or hardcoded mock
  return [];
}

async function createProject(name: string): Promise<void> {
  await fetch("http://127.0.0.1:8520/v1/projects", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
}

export default function ProjectList({ onSelect }: Props) {
  const [projects, setProjects] = useState<Project[]>([]);
  const [creating, setCreating] = useState(false);
  const [newName, setNewName] = useState("");

  useEffect(() => {
    fetchProjects().then(setProjects);
  }, []);

  const handleCreate = async () => {
    if (!newName.trim()) return;
    setCreating(true);
    await createProject(newName.trim());
    const updated = await fetchProjects();
    setProjects(updated);
    setNewName("");
    setCreating(false);
  };

  return (
    <div className="project-list">
      <h1>Easy-Agent Novel Studio</h1>
      <div className="project-grid">
        {projects.map((p) => (
          <div
            key={p.name}
            className="project-card"
            onClick={() => onSelect(p)}
          >
            <h3>{p.name}</h3>
            <p>
              章节: {p.chapters} | 草稿: {p.drafts}
            </p>
          </div>
        ))}
      </div>

      <div className="create-project">
        <input
          type="text"
          placeholder="新项目名称"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
        />
        <button onClick={handleCreate} disabled={creating || !newName.trim()}>
          新建项目
        </button>
      </div>
    </div>
  );
}
