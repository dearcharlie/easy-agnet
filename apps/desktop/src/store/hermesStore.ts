import { create } from "zustand";

interface HermesState {
  connected: boolean;
  messages: Array<{ role: "user" | "assistant"; content: string }>;
  streaming: boolean;
  addMessage: (msg: { role: "user" | "assistant"; content: string }) => void;
  setStreaming: (v: boolean) => void;
  setConnected: (v: boolean) => void;
}

export const useHermesStore = create<HermesState>((set) => ({
  connected: false,
  messages: [],
  streaming: false,
  addMessage: (msg) =>
    set((state) => ({ messages: [...state.messages, msg] })),
  setStreaming: (v) => set({ streaming: v }),
  setConnected: (v) => set({ connected: v }),
}));
