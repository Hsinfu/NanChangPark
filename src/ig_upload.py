import argparse
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


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--img-fpath',
        required=True,
        help='img file path for upload Ex. /Users/hsinfu/Downloads/man01.png',
    )
    parser.add_argument(
        '--caption',
        required=True,
        default='NanChangPark Never Lock',
        help='instagram post caption',
    )
    return parser.parse_args()


def _main():
    args = _parse_arguments()
    ig_uploader = InstagramUploader()
    ig_uploader.upload_photo(args.img_fpath, caption=args.caption)


if __name__ == "__main__":
    _main()
