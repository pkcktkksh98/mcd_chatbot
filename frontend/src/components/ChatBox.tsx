/* eslint-disable @typescript-eslint/no-unused-vars */
import { useState,useRef, useEffect } from "react";
import axios from "axios";
import MessageBubble from "./MessageBubble";
export default function ChatBox() {
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement | null>(null);
  const [isLoading, setIsLoading] = useState(false);


  const sendMessage = async () => {
    if (!input.trim()) return;

    // Show user message immediately
    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput("");
    setIsLoading(true);    

    try {
      const res = await axios.post("http://localhost:8000/rag", { q: input });
      setIsLoading(false);
      setMessages([...newMessages, { role: "assistant", content: res.data.answer }]);
    } catch (err) {
      setIsLoading(false);
      setMessages([...newMessages, { role: "assistant", content: "Error getting response." }]);
    }
    
    
  };

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);



  return (
    <div style={{ padding: "1rem", height: "80vh", overflowY: "auto", display: "flex", flexDirection: "column" }}>
      <div style={{ flexGrow: 1, overflowY: "auto", marginBottom: "1rem" }}>
        {messages.map((msg, idx) => (
          <MessageBubble key={idx} sender={msg.role} message={msg.content} />
        ))}
        {isLoading && (
          <div style={{ fontStyle: "italic", color: "gray", marginTop: "5px" }}>
            Bot is thinking...
          </div>
        )}
        
        <div ref={bottomRef} />
      </div>
      <div style={{ display: "flex", gap: "0.5rem" }}>
        <input
          style={{ flexGrow: 1, padding: "0.5rem" }}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") sendMessage();
          }}
          placeholder="Ask something like: 'Which outlet opens 24 hours?'"
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>

  );
}
