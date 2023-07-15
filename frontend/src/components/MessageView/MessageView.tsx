import React from "react";
import { Message } from "../../interfaces/Message";
import "./MessageView.css";
import { isAnalysis } from "../../interfaces/Analysis";
import { EventButton } from "../EventButton/EventButton";
import { Link } from "@mui/material";

interface MessageViewProps {
  message: Message;
}

export const MessageView: React.FC<MessageViewProps> = ({ message }) => {
  const { content, role } = message;

  return (
    <div
      className={
        message.role === "User"
          ? "message-background-user"
          : "message-background-bot"
      }
    >
      <div
        className={`message ${
          role === "User" ? "message-user" : "message-bot"
        }`}
      >
        <div className="message-text">{content}</div>
        {isAnalysis(message) && (
          <div>
            {message.wikiEntry != null && (
              <Link href={message.wikiEntry.url}>
                Helpful link: {message.wikiEntry.title}
              </Link>
            )}
            {message.event != null && (
              <EventButton event={message.event}></EventButton>
            )}
          </div>
        )}
        <div></div>
      </div>
    </div>
  );
};
