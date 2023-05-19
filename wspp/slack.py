import io

import requests
from pydantic import BaseModel


class SlackSettings(BaseModel):
    token: str
    cookie_d: str
    workspace: str


def set_profile_photo(settings: SlackSettings, image_data: io.BytesIO):
    """
    Update the profile photo on slack with the given image.
    """
    response = requests.post(
        url=f"https://{settings.workspace}/api/users.setPhoto",
        headers={
            "cookie": f"d={settings.cookie_d}",
        },
        data={
            "token": settings.token,
        },
        files=[("image", ("photo.jpg", image_data, "image/jpeg"))],
    )
    response_data: dict = response.json()
    if response_data.get("ok") is False:
        raise Exception(f"Error updating photo: {response_data.get('error')}")
