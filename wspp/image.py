import io
from pathlib import Path

from PIL import Image

_resources_dir = Path(__file__).parent.parent / "resources"


def create_profile_photo(background: Path, foreground: Path) -> io.BytesIO:
    """
    :return: the binary data of an image containing the given background image, with
    the provided foreground image on top.
    """
    background_image = Image.open(background)
    foreground_image = Image.open(foreground).convert("RGBA")
    new_image = Image.new(
        mode="RGB",
        size=background_image.size,
    )
    new_image.paste(background_image)
    new_image.paste(foreground_image, (0, 0), foreground_image)
    bio = io.BytesIO()
    new_image.save(bio, format="JPEG")
    bio.seek(0)
    return bio


def get_image_file(prefix: str) -> Path:
    """
    :return: the background image file starting with the given prefix
    """
    return next(_resources_dir.glob(f"{prefix}*"))
