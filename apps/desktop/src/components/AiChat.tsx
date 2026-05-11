import { useState, useRef, useEffect } from "react";
import type { Project } from "../store/projectStore";
import { useHermesStore } from "../store/hermesStore";

interface Props {
  project: Project;
}

const HERMES_API = "http://127.0.0.1:8520/v1/chat/completions";

async function sendMessage(messages: Array<{ role: string; content: string }>) {
  const res = await fetch(HERMES_API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "hermes-agent",
      messages,
      stream: true,
    }),
  });

  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res;
}

export default function AiChat({ project }: Props) {
  const { messages, addMessage, streaming, setStreaming, connected, setConnected } =
    useHermesStore();
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    // Check Hermes API health
    fetch(`${HERMES_API.slice(0, -22)}/health`)
      .then(() => setConnected(true))
      .catch(() => setConnected(false));
  }, []);

  const handleSend = async () => {
    if (!input.trim() || streaming) return;
    const userMsg = { role: "user" as const, content: input.trim() };
    addMessage(userMsg);
    setInput("");
    setStreaming(true);

    try {
      const response = await sendMessage([...messages, userMsg]);
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let assistantContent = "";

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          const lines = chunk.split("\n").filter((l) => l.startsWith("data: "));
          for (const line of lines) {
            const data = line.slice(6);
            if (data === "[DONE]") break;
            try {
              const parsed = JSON.parse(data);
              const delta = parsed.choices?.[0]?.delta?.content || "";
              assistantContent += delta;
            } catch {
              // skip malformed JSON
            }
          }
        }
      }

      if (assistantContent) {
        addMessage({ role: "assistant", content: assistantContent });
      }
    } catch (err) {
      addMessage({
        role: "assistant",
        content: `[!] Connection error: ${err}. Make sure Hermes API Server is running.`,
      });
    } finally {
      setStreaming(false);
    }
  };

  return (
    <div className="ai-chat">
      <div className="chat-header">
        <span>AI 助手</span>
        <span className={`status ${connected ? "connected" : "disconnected"}`}>
          {connected ? "已连接" : "未连接"}
        </span>
      </div>

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="chat-welcome">
            <p>欢迎使用 Easy-Agent Novel Studio!</p>
            <p>试试以下命令:</p>
            <ul>
              <li><code>/novel quick {"<点子>"}</code> — 速写模式</li>
              <li><code>/novel craft</code> — 精细模式</li>
              <li><code>/novel continue</code> — 续写模式</li>
              <li><code>/novel polish</code> — 润色模式</li>
              <li><code>/novel inspire</code> — 灵感模式</li>
            </ul>
          </div>
        )}
        {messages.map((msg, i) => (
          <div key={i} className={`chat-message ${msg.role}`}>
            <div className="message-content">{msg.content}</div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="输入消息或 /novel 命令..."
          disabled={streaming}
        />
        <button onClick={handleSend} disabled={streaming || !input.trim()}>
          发送
        </button>
      </div>
    </div>
  );
}
