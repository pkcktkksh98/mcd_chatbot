import { useState, useRef, useEffect } from "react";
import axios from "axios";
import MessageBubble from "./MessageBubble";

export default function ChatBox() {
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement | null>(null);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput("");
    setIsLoading(true);

    try {
      const res = await axios.post("http://localhost:8000/rag", { q: input });
      setMessages([...newMessages, { role: "assistant", content: res.data.answer }]);
    } catch (err) {
      setMessages([...newMessages, { role: "assistant", content: "Error getting response." }]);
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessageWithPrompt = async (prompt: string) => {
    if (!prompt.trim()) return;

    const newMessages = [...messages, { role: "user", content: prompt }];
    setMessages(newMessages);
    setInput("");
    setIsLoading(true);

    try {
      const res = await axios.post("http://localhost:8000/rag", { q: prompt });
      setMessages([...newMessages, { role: "assistant", content: res.data.answer }]);
    } catch (err) {
      setMessages([...newMessages, { role: "assistant", content: "Error getting response." }]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="h-full p-4 flex flex-col bg-white dark:bg-gray-800 transition-colors">
      {/* Chat messages */}
      <div className="flex-grow overflow-y-auto mb-4">
        {messages.map((msg, idx) => (
          <MessageBubble key={idx} sender={msg.role} message={msg.content} />
        ))}
        {isLoading && <MessageBubble sender="assistant" message="Typing..." />}
        <div ref={bottomRef} />
      </div>

      {/* Suggested prompts */}
      <div className="mb-3">
        <strong className="block mb-2">Suggestions:</strong>
        <div className="flex flex-wrap gap-2">
          {[
            "Which outlets are open 24 hours?",
            "Where can I host a birthday party?",
            "Show all Drive-Thru outlets in Selangor",
            "List outlets with McCafe in Pulau Pinang",
          ].map((suggestion, index) => (
            <button
              key={index}
              className="px-3 py-1 bg-gray-100 border border-gray-300 rounded-lg hover:bg-gray-200 transition dark:bg-gray-900 border dark:text-gray-400 dark:border-gray-800"
              onClick={() => {
                setInput(suggestion);
                sendMessageWithPrompt(suggestion);
              }}
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>

      {/* Input field */}
      <div className="flex gap-2">
        <input
          className="flex-grow p-2 border border-gray-300 rounded-md dark:bg-gray-900 dark:text-white dark:border-gray-600"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") sendMessage();
          }}
          placeholder="Example: 'Which outlet opens 24 hours?'"
        />
        <button
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700"
          onClick={sendMessage}
        >
          Send
        </button>
      </div>
    </div>
  );
}
