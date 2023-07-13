import { Message } from "./Message";
import { WikiEntry } from "./WikiEntry";

export interface Analysis extends Message {
  wikiEntry: WikiEntry;
}

export const isAnalysis = (object: any): object is Analysis => {
  return "wikiEntry" in object;
};
