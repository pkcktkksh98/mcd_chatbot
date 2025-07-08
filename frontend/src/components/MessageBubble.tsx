import React from "react";

type MessageBubbleProps = {
  sender: "user" | "bot";
  message: string;
};

const MessageBubble: React.FC<MessageBubbleProps> = ({ sender, message }) => {
  const isUser = sender === "user";
  const isTyping = message === "Typing...";

  return (
    <div className={`flex mb-2 ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[70%] px-4 py-2 rounded-2xl font-sans ${
          isUser
            ? "bg-green-500 text-white self-end"
            : "bg-gray-200 text-black self-start"
        }`}
      >
        {isTyping ? (
          <span className="inline-flex items-center space-x-1">
            <span>Typing</span>
            <span className="animate-bounce delay-[0ms]">.</span>
            <span className="animate-bounce delay-[200ms]">.</span>
            <span className="animate-bounce delay-[400ms]">.</span>
          </span>
        ) : (
          message
        )}
      </div>
    </div>
  );
};

export default MessageBubble;
