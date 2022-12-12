import time

from plyer import notification
from PIL import Image
import requests
import os

CATPIC_API = "https://cataas.com/cat"
CATFACT_API = "https://meowfacts.herokuapp.com/"
with open('cat_pic.png', 'wb') as f:
    f.write(requests.get(CATPIC_API).content)
img = Image.open("cat_pic.png", "r")
img.save("cat_pic.ico")

response = requests.get(CATFACT_API)
response.raise_for_status()
fact = "".join(response.json()["data"])

notification.notify(
    title="Here is a new cat fact!",
    message=f"Did you know...\n{fact}",
    app_icon="cat_pic.ico",
    timeout=10
)
time.sleep(1)
os.remove("cat_pic.ico")
os.remove("cat_pic.png")
