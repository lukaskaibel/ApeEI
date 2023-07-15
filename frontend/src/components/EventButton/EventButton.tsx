import React from "react";
import { Event } from "../../interfaces/Event";
import axios from "axios";
import Button from "@mui/material/Button";

interface EventButtonProps {
  event: Event;
}

export const EventButton: React.FC<EventButtonProps> = ({ event }) => {
  const startDate = new Date(event.startDate);
  const endDate = new Date(event.endDate);

  const formatDate = (date: Date) => {
    return date.toLocaleDateString();
  };

  const formatTime = (date: Date) => {
    let hours = date.getHours();
    let minutes = date.getMinutes();

    // Convert to 12 hour format if it's more than 12
    let twelveHour = hours > 12 ? hours - 12 : hours;

    // Add a leading 0 if it's less than 10
    let twelveHourFormatted =
      twelveHour < 10 ? `0${twelveHour}` : `${twelveHour}`;
    let minutesFormatted = minutes < 10 ? `0${minutes}` : `${minutes}`;

    let amPm = hours >= 12 ? "PM" : "AM";

    return `${twelveHourFormatted}:${minutesFormatted} ${amPm}`;
  };

  const renderEventTime = () => {
    if (event.allDay) {
      return "All day";
    } else {
      return `${formatTime(startDate)} - ${formatTime(endDate)}`;
    }
  };

  const createEvent = async (reactEvent: React.MouseEvent) => {
    console.log("Pressed");
    try {
      await axios.post("http://127.0.0.1:5000/api/create_event", {
        message: JSON.stringify(event),
      });
    } catch {}
  };

  return (
    <Button variant="contained" onClick={createEvent}>
      Add to calendar
    </Button>
  );
};
