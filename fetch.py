#!/usr/bin/env python3

import sys
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from datetime import datetime
import os
import mimetypes
import json

def fetch_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text, response.headers.get('Content-Type', '')
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None, None

def save_content(content, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        f.write(content)

def get_metadata(content, url):
    soup = BeautifulSoup(content, 'html.parser')
    return {
        'site': urlparse(url).netloc,
        'num_links': len(soup.find_all('a')),
        'images': len(soup.find_all('img')),
        'last_fetch': datetime.utcnow().strftime('%a %b %d %Y %H:%M UTC')
    }

def save_metadata(metadata, filename):
    with open(filename, 'w') as f:
        json.dump(metadata, f)

def load_metadata(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None

def download_asset(url, base_url, save_dir):
    try:
        full_url = urljoin(base_url, url)
        response = requests.get(full_url)
        response.raise_for_status()
        
        parsed_url = urlparse(full_url)
        path = parsed_url.path.lstrip('/')
        if not path:
            path = 'index'
        
        content_type = response.headers.get('Content-Type', '').split(';')[0]
        ext = mimetypes.guess_extension(content_type) or ''
        
        local_path = os.path.join(save_dir, path + ext)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        with open(local_path, 'wb') as f:
            f.write(response.content)
        
        return os.path.relpath(local_path, save_dir)
    except requests.RequestException as e:
        print(f"Error downloading asset {url}: {e}", file=sys.stderr)
        return url

def create_local_mirror(content, url, save_dir):
    soup = BeautifulSoup(content, 'html.parser')
    base_url = url

    for tag in soup.find_all(['img', 'link', 'script']):
        if tag.name == 'img' and tag.has_attr('src'):
            tag['src'] = download_asset(tag['src'], base_url, save_dir)
        elif tag.name == 'link' and tag.has_attr('href'):
            tag['href'] = download_asset(tag['href'], base_url, save_dir)
        elif tag.name == 'script' and tag.has_attr('src'):
            tag['src'] = download_asset(tag['src'], base_url, save_dir)

    return str(soup)

def process_url(url, metadata_mode):
    parsed_url = urlparse(url)
    base_filename = parsed_url.netloc
    save_dir = os.path.join(os.getcwd(), 'downloads/' + base_filename)
    metadata_file = os.path.join(save_dir, 'metadata.json')

    if metadata_mode:
        metadata = load_metadata(metadata_file)
        if metadata:
            print(f"site: {metadata['site']}")
            print(f"num_links: {metadata['num_links']}")
            print(f"images: {metadata['images']}")
            print(f"last_fetch: {metadata['last_fetch']}")
            print()
        else:
            print(f"No metadata found for {url}")
        return
    else:
        content, content_type = fetch_url(url)
        if not content:
            return
        mirrored_content = create_local_mirror(content, url, save_dir)
        filename = os.path.join(save_dir, "index.html")
        save_content(mirrored_content.encode('utf-8'), filename)
        print(f"Saved {url} to {filename}")

        metadata = get_metadata(content, url)
        save_metadata(metadata, metadata_file)
        print(f"Saved metadata to {metadata_file}")        

def main():
    if len(sys.argv) < 2:
        print("Usage: ./fetch [--metadata] <url1> [<url2> ...]", file=sys.stderr)
        sys.exit(1)

    metadata_mode = False
    urls = sys.argv[1:]

    if '--metadata' in urls:
        metadata_mode = True
        urls.remove('--metadata')

    for url in urls:
        process_url(url, metadata_mode)

if __name__ == "__main__":
    main()
