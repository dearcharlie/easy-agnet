import { useEffect, useState } from "react";
import type { Project, Chapter } from "../store/projectStore";

interface Props {
  project: Project;
  activeTab: string;
  onTabChange: (tab: "characters" | "outline" | "chat" | "stats") => void;
  onSelectChapter: (path: string) => void;
}

async function fetchChapters(project: Project): Promise<Chapter[]> {
  try {
    const res = await fetch(`http://127.0.0.1:8520/v1/projects/${project.name}/chapters`);
    if (res.ok) return await res.json();
  } catch {
    // fallback
  }
  return [];
}

const tabs = [
  { id: "characters" as const, label: "角色" },
  { id: "outline" as const, label: "大纲" },
  { id: "chat" as const, label: "AI 对话" },
  { id: "stats" as const, label: "统计" },
];

export default function Sidebar({ project, activeTab, onTabChange, onSelectChapter }: Props) {
  const [chapters, setChapters] = useState<Chapter[]>([]);

  useEffect(() => {
    fetchChapters(project).then(setChapters);
  }, [project]);

  return (
    <div className="sidebar">
      <h2 className="sidebar-title">{project.name}</h2>

      <div className="sidebar-tabs">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`tab-btn ${activeTab === tab.id ? "active" : ""}`}
            onClick={() => onTabChange(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {activeTab === "outline" && (
        <div className="chapter-list">
          <h3>章节列表</h3>
          {chapters.map((ch) => (
            <div
              key={ch.number}
              className="chapter-item"
              onClick={() => onSelectChapter(ch.path)}
            >
              <span>{ch.isDraft ? "📝" : "📄"} 第{ch.number}章</span>
            </div>
          ))}
        </div>
      )}

      {activeTab === "characters" && (
        <div className="panel-placeholder">
          <p>角色面板</p>
          <small>角色卡管理即将上线</small>
        </div>
      )}

      {activeTab === "stats" && (
        <div className="panel-placeholder">
          <p>统计面板</p>
          <small>字数 / 章节数统计即将上线</small>
        </div>
      )}
    </div>
  );
}
