import { isAnalysis } from "./Analysis";

export enum MessageRole {
  User = "User",
  Assistant = "Assistant",
}

export interface Message {
  content: string;
  role: MessageRole;
}

export const isMessage = (object: any): object is Message => {
  return "content" in object && "role" in object && !isAnalysis(object);
};
