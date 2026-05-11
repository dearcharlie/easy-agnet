import { useState } from "react";
import ProjectList from "./components/ProjectList";
import Editor from "./components/Editor";
import AiChat from "./components/AiChat";
import Sidebar from "./components/Sidebar";
import ActionBar from "./components/ActionBar";
import type { Project } from "./store/projectStore";

type Tab = "characters" | "outline" | "chat" | "stats";

function App() {
  const [currentProject, setCurrentProject] = useState<Project | null>(null);
  const [activeTab, setActiveTab] = useState<Tab>("chat");
  const [currentChapter, setCurrentChapter] = useState<string>("");

  if (!currentProject) {
    return (
      <div className="app">
        <ProjectList onSelect={setCurrentProject} />
      </div>
    );
  }

  return (
    <div className="app">
      <div className="main-layout">
        <div className="sidebar-left">
          <Sidebar
            project={currentProject}
            activeTab={activeTab}
            onTabChange={setActiveTab}
            onSelectChapter={setCurrentChapter}
          />
        </div>
        <div className="content-area">
          <Editor
            project={currentProject}
            chapterPath={currentChapter}
          />
          <ActionBar
            project={currentProject}
            onAction={(action) => {
              // Handled through AI Chat
            }}
          />
        </div>
      </div>
      <AiChat project={currentProject} />
    </div>
  );
}

export default App;
