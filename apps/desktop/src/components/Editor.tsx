import { useEffect, useState } from "react";
import type { Project } from "../store/projectStore";

interface Props {
  project: Project;
  chapterPath: string;
}

async function loadChapter(path: string): Promise<string> {
  try {
    const res = await fetch(
      `http://127.0.0.1:8520/v1/file?path=${encodeURIComponent(path)}`,
    );
    if (res.ok) return await res.text();
  } catch {
    // fallback
  }
  return "# 新章节\n\n开始写作...";
}

export default function Editor({ project, chapterPath }: Props) {
  const [content, setContent] = useState("");
  const [preview, setPreview] = useState(false);

  useEffect(() => {
    if (chapterPath) {
      loadChapter(chapterPath).then(setContent);
    } else {
      setContent("# 选择或创建新章节\n\n从左侧大纲面板选择一个章节开始编辑。");
    }
  }, [chapterPath, project]);

  // Simple markdown rendering for preview
  const renderMarkdown = (md: string) => {
    return md
      .replace(/^### (.+)$/gm, "<h3>$1</h3>")
      .replace(/^## (.+)$/gm, "<h2>$1</h2>")
      .replace(/^# (.+)$/gm, "<h1>$1</h1>")
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/\n\n/g, "</p><p>")
      .replace(/^- (.+)$/gm, "<li>$1</li>");
  };

  return (
    <div className="editor">
      <div className="editor-toolbar">
        <button onClick={() => setPreview(!preview)}>
          {preview ? "编辑" : "预览"}
        </button>
      </div>

      {preview ? (
        <div
          className="editor-preview"
          dangerouslySetInnerHTML={{ __html: renderMarkdown(content) }}
        />
      ) : (
        <textarea
          className="editor-textarea"
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />
      )}
    </div>
  );
}
