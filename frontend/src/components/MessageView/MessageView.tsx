import React from "react";
import { Message } from "../../interfaces/Message";
import "./MessageView.css";
import { isAnalysis } from "../../interfaces/Analysis";

interface MessageViewProps {
  message: Message;
}

export const MessageView: React.FC<MessageViewProps> = ({ message }) => {
  const { content, role } = message;

  return (
    <div>
      <div
        className={`message ${
          role === "User" ? "message-user" : "message-bot"
        }`}
      >
        {content}
      </div>
      {isAnalysis(message) && (
        <a href={message.wikiEntry.url}>{message.wikiEntry.title}</a>
      )}
      <div></div>
    </div>
  );
};
