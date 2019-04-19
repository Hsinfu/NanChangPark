import argparse
import json
import time
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

    def upload_photo(self, photo_path, caption, max_retry=10):
        if max_retry == 0:
            return
        self.api.uploadPhoto(photo_path, caption=caption)
        if self.api.LastJson.get('status', None) != 'ok':
            time.sleep(20)
            self.upload_photo(photo_path, caption, max_retry - 1)


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
