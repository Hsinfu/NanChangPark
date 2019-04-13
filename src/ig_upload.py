import json
from InstagramAPI import InstagramAPI
from constant import INSTAGRAM_ACCOUNT_PATH


class InstagramUploader:
    def __init__(self):
        self._api = None

    @property
    def api(self):
        if not self._api:
            with open(INSTAGRAM_ACCOUNT_PATH) as fptr:
                info = json.load(fptr)
            self._api = InstagramAPI(info['username'], info['password'])
            self._api.login()
        return self._api

    def upload_photo(self, photo_path, caption):
        self.api.uploadPhoto(photo_path, caption=caption)


def _main():
    caption = "NanChangPark Never Lock"
    photo_path = '/Users/hsinfu/Downloads/man01.png'
    # photo_path = '/Users/hsinfu/Downloads/final.jpg'
    ig_uploader = InstagramUploader()
    ig_uploader.upload_photo(photo_path, caption=caption)


if __name__ == "__main__":
    _main()
