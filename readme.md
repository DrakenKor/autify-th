# Web Page Fetcher

This project is a command-line tool that fetches web pages, saves them to disk for later retrieval and browsing, and can display metadata about the fetched pages.

## Features

- Fetch and save complete web pages, including assets (images, CSS, JavaScript)
- Display metadata about fetched pages (number of links, images, last fetch time)
- Save metadata to disk for quick retrieval
- Support for fetching multiple URLs in a single command

## Prerequisites

- Docker

## Setup

1. Clone this repository
2. Build the Docker image:

```
docker build -t fetch .

```

3. Run the app:

```
docker run --rm -v $(pwd):/app fetch https://www.example.com https://another-example.com
```

4. Fetch metadata

```
docker run --rm -v $(pwd):/app fetch --metadata https://www.example.com https://another-example.com
```

## Improvements

Some improvements could be made

1. Using sqlite for database instead of JSON file would make the metadata storage more robust
2. Parallelising the download of assets would speed up the fetching process
3. Adding a cache layer to reduce the number of requests to the same URL
4. Adding a progress bar to show the progress of the download
5. Adding a way to specify the output directory for the fetched pages
6. Add a more friendly command for running the project
