import type { Project } from "../store/projectStore";

interface Props {
  project: Project;
  onAction: (action: string) => void;
}

export default function ActionBar({ project, onAction }: Props) {
  const actions = [
    { id: "quick", label: "速写", icon: "⚡" },
    { id: "continue", label: "续写", icon: "▶" },
    { id: "polish", label: "润色", icon: "✨" },
    { id: "check", label: "检查", icon: "✓" },
  ];

  return (
    <div className="action-bar">
      {actions.map((action) => (
        <button
          key={action.id}
          className="action-btn"
          onClick={() => onAction(action.id)}
          title={action.label}
        >
          <span className="action-icon">{action.icon}</span>
          <span className="action-label">{action.label}</span>
        </button>
      ))}
    </div>
  );
}
