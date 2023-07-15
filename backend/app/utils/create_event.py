"""
This module provides functionality for creating events in Google Calendar.
"""

import json
import logging
from typing import Optional
from datetime import datetime, timedelta

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s: %(message)s")


def create_event(
    name: str,
    start_date: datetime,
    end_date: Optional[datetime] = None,
    location: Optional[str] = None,
    all_day: bool = False,
) -> str:
    """
    Creates an event in Google Calendar.

    Args:
        name (str): The name of the event.
        start_date (datetime): The start date and time of the event.
        end_date (Optional[datetime]): The end date and time of the event. If the event lasts all day and
            `end_date` is not provided, it defaults to the end of the start date. If the event does not last
            all day and `end_date` is not provided, it defaults to one hour after the start time.
        location (Optional[str]): The location of the event.
        all_day (bool): Indicates whether the event lasts all day. Defaults to False.

    Returns:
        The URL of the created event.

    Raises:
        google.auth.exceptions.RefreshError: If the authentication fails.
        googleapiclient.errors.HttpError: If the request to the Google Calendar API fails.
    """
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)

    service = build("calendar", "v3", credentials=creds)

    # Fetch calendar timezone
    calendar = service.calendars().get(calendarId="primary").execute()
    timezone = calendar["timeZone"]

    event = {"summary": name}

    # Correctly set the start and end date
    if all_day:
        # If all day, set start to beginning of the day and end to the end of the day
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        if end_date is None:
            end_date = start_date.replace(hour=23, minute=59, second=59, microsecond=0)
    elif end_date is None:
        end_date = start_date + timedelta(hours=1)

    event["start"] = {
        "dateTime": start_date.strftime("%Y-%m-%dT%H:%M:%S"),
        "timeZone": timezone,
    }
    event["end"] = {
        "dateTime": end_date.strftime("%Y-%m-%dT%H:%M:%S"),
        "timeZone": timezone,
    }

    if location:
        event["location"] = location

    event = service.events().insert(calendarId="primary", body=event).execute()
    logging.info("Successfully added event to Google calendar!")
    return event.get("htmlLink")
