import React from "react";

type MessageBubbleProps = {
  sender: "user" | "bot";
  message: string;
};

const MessageBubble: React.FC<MessageBubbleProps> = ({ sender, message }) => {
  const isUser = sender === "user";

  return (
    <div
      style={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        marginBottom: "8px",
      }}
    >
      <div
        style={{
          maxWidth: "70%",
          padding: "10px 15px",
          borderRadius: "20px",
          backgroundColor: isUser ? "#4caf50" : "#e0e0e0",
          color: isUser ? "white" : "black",
          alignSelf: isUser ? "flex-end" : "flex-start",
        }}
      >
        {message}
      </div>
    </div>
  );
};

export default MessageBubble;
