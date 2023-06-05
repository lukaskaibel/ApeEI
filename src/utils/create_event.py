from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import logging
from typing import Optional
from datetime import timedelta

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s: %(message)s")


def create_event(
    name: str,
    start_date: str,
    end_date: Optional[str] = None,
    location: Optional[str] = None,
    all_day: bool = False,
):
    creds = None

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
    logging.info(f'Event created: {event.get("htmlLink")}')
