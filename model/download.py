import argparse
import http
import logging
import urllib.request

_serialized = {
    "mobilenet_v3_large": "https://download.pytorch.org/models/fasterrcnn_mobilenet_v3_large_fpn-fb6a3cc7.pth",
    "resnet50": "https://download.pytorch.org/models/fasterrcnn_resnet50_fpn_coco-258fb6c6.pth"
}


def download(model_name: str) -> http.HTTPStatus:
    url = _serialized.get(model_name)
    # Better to return an Error
    assert url, f"No valid model file url corresponding to model_name = `{model_name}`!"

    url_stripped = url.split("/")[-1]

    try:
        res = urllib.request.urlopen(url)
        if http.HTTPStatus(res.status) == http.HTTPStatus.OK:
            urllib.request.urlretrieve(url, filename=f"./{url_stripped}")

        return http.HTTPStatus(res.status)

    except urllib.error.HTTPError as err:
        logging.error(
            f"url pointing to model file: {url} not found! Returned status: {http.HTTPStatus(err.status_code)}"
        )
        return http.HTTPStatus(err.status)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--model_name",
        required=True,
        help="",
        choices=list(_serialized.keys()),
        type=str,
    )

    args = parser.parse_args()

    download(args.model_name)
