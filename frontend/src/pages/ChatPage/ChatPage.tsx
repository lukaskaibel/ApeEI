import React, { useState } from "react";
import axios from "axios";
import { MessageView } from "../../components/MessageView/MessageView";
import { Message, MessageRole, isMessage } from "../../interfaces/Message";
import "./ChatPage.css";
import { Analysis, isAnalysis } from "../../interfaces/Analysis";
import TextField from "@mui/material/TextField";
import CircularProgress from "@mui/material/CircularProgress";
import { LinearProgress } from "@mui/material";

export const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");

  const [isLoading, setIsLoading] = useState<boolean>(false);

  const sendMessage = async (event: React.FormEvent) => {
    event.preventDefault();

    const userMessage: Message = {
      content: input,
      role: MessageRole.User,
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);

    setInput("");
    setIsLoading(true);

    try {
      const response = await axios.post<Message | Analysis>(
        "http://127.0.0.1:5000/api/chat",
        {
          message: input,
        }
      );

      setIsLoading(false);

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
    <div className="container">
      <h1>ApeEI</h1>
      <div>
        {messages.map((message) => (
          <MessageView message={message} />
        ))}
      </div>
      {isLoading && <LinearProgress />}
      <form onSubmit={sendMessage}>
        <div className="textfield-container">
          <TextField
            fullWidth
            label="Send a message or reflection"
            value={input}
            id="fullWidth"
            onChange={(e) => setInput(e.target.value)}
          />
        </div>
      </form>
    </div>
  );
};
