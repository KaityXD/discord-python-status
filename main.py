import requests
import time
from datetime import datetime
from pytz import timezone

TOKEN = "YOUR_DISCORD_TOKEN"
TZ = timezone("Asia/Bangkok")

morning_activities = [
    "Good morning! 🌅 Time for a fresh start at {time}",
    "Enjoying a morning coffee ☕ {time}",
    "Starting the day with some energy 💪 {time}",
]
afternoon_activities = [
    "Working through the day 🌞 {time}",
    "Productivity mode: ON 🛠️ {time}",
    "Afternoon hustle 💼 {time}",
]
evening_activities = [
    "Winding down the day 🌇 {time}",
    "Relaxing evening vibes 🌆 {time}",
    "Enjoying a peaceful evening 🌙 {time}",
]
night_activities = [
    "Burning the midnight oil 🔥 {time}",
    "Late-night coding session 💻 {time}",
    "It's quiet out here... 🌌 {time}",
]

def get_local_time():
    return datetime.now(TZ)

def get_status_for_time():
    current_time = get_local_time()
    formatted_time = current_time.strftime("%I:%M %p")
    
    if 5 <= current_time.hour < 12:
        activities = morning_activities
    elif 12 <= current_time.hour < 17:
        activities = afternoon_activities
    elif 17 <= current_time.hour < 21:
        activities = evening_activities
    else:
        activities = night_activities

    activity = activities[current_time.minute % len(activities)]
    return activity.format(time=formatted_time)

def set_discord_status(token, status_text):
    url = "https://discordapp.com/api/v9/users/@me/settings"
    payload = {"custom_status": {"text": status_text}}
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) discord/0.0.9 Chrome/69.0.3497.128 "
                      "Electron/4.0.8 Safari/537.36",
    }
    try:
        response = requests.patch(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"Status updated to: {status_text}")
        else:
            print(f"Failed to update status. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error updating status: {e}")

while True:
    current_status = get_status_for_time()
    set_discord_status(TOKEN, current_status)
    time.sleep(60)
