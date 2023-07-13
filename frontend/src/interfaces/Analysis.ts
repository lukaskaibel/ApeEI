import { Message } from "./Message";
import { WikiEntry } from "./WikiEntry";
import { Event } from "./Event";

export interface Analysis extends Message {
  event: Event;
  wikiEntry: WikiEntry;
}

export const isAnalysis = (object: any): object is Analysis => {
  return "wikiEntry" in object && "event" in object;
};
