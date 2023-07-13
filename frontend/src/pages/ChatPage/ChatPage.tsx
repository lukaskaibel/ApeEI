import React, { useState } from "react";
import axios from "axios";
import { MessageView } from "../../components/MessageView/MessageView";
import { Message, MessageRole, isMessage } from "../../interfaces/Message";
import "./ChatPage.css";
import { Analysis, isAnalysis } from "../../interfaces/Analysis";

export const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");

  const sendMessage = async (event: React.FormEvent) => {
    event.preventDefault();

    const userMessage: Message = {
      content: input,
      role: MessageRole.User,
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);

    setInput("");

    try {
      const response = await axios.post<Message | Analysis>(
        "http://127.0.0.1:5000/api/chat",
        {
          message: input,
        }
      );

      if (response.status !== 200) {
        alert("There was an error with the request. Please try again.");
        return;
      }

      const responseData = response.data;

      if (isMessage(responseData)) {
        console.log(`ChatPage: Received message: ${responseData}`);
        setMessages((prevMessages) => [...prevMessages, responseData]);
        return;
      }

      if (isAnalysis(responseData)) {
        console.log(`ChatPage: Received analysis: ${responseData}`);
        setMessages((prevMessages) => [...prevMessages, responseData]);
        return;
      }

      console.log(`ChatPage: Unsupported response type: ${responseData}`);
    } catch (error) {
      console.error("Error:", error);
      alert("There was an error with the request. Please try again.");
    }
  };

  return (
    <div>
      <h1>Chat</h1>
      <div>
        {messages.map((message) => (
          <MessageView message={message} />
        ))}
      </div>
      <form onSubmit={sendMessage}>
        <div className="container">
          <input
            className="text-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button className="send-button" type="submit">
            Send
          </button>
        </div>
      </form>
    </div>
  );
};
