import argparse
import threading
import requests
import time


def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Page download failed: {url}")


def save_image(data, filename):
    with open(filename, "wb") as f:
        f.write(data)
    print(f"Image saved as {filename}")


def process_url(url, index):
    start_time = time.time()

    extension = url.split('.')[-1]
    filename = f'images\\image{index}.{extension}'
    data = download_image(url)
    if data:
        save_image(data, filename)
        print(f"{index}: {time.time() - start_time:.2f} seconds")


def main(urls):
    start_time = time.time()
    threads = []
    for i, url in enumerate(urls, start=1):
        t = threading.Thread(target=process_url, args=(url, i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Total time: {time.time() - start_time:.2f} ")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download images from URLs")
    parser.add_argument("urls", metavar="url", type=str, nargs="*", help="URLs of images to download")
    args = parser.parse_args()

    main(args.urls)
