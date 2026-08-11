#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import email.utils
import os
import re
import tempfile
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
from zoneinfo import ZoneInfo


BLOG_REGION_START = "<!-- BLOG-POST-LIST:START -->"
BLOG_REGION_END = "<!-- BLOG-POST-LIST:END -->"
DEFAULT_FEED_URL = "https://stackonward.com/index.xml"
CHINA_TIMEZONE = ZoneInfo("Asia/Shanghai")


@dataclass(frozen=True)
class BlogPost:
    title: str
    url: str
    published_at: dt.datetime


class HttpClient(Protocol):
    def get_text(self, url: str) -> str: ...


class BlogPostSource(Protocol):
    def latest_posts(self, limit: int) -> list[BlogPost]: ...


class UrlLibHttpClient:
    def get_text(self, url: str) -> str:
        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/rss+xml, application/xml, text/xml",
                "User-Agent": "stackonward-organization-profile-refresh",
            },
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8")


class StackOnwardRssSource:
    def __init__(self, client: HttpClient, feed_url: str) -> None:
        self._client = client
        self._feed_url = feed_url

    def latest_posts(self, limit: int) -> list[BlogPost]:
        root = ET.fromstring(self._client.get_text(self._feed_url))
        posts: list[BlogPost] = []
        for item in root.findall("./channel/item"):
            title = (item.findtext("title") or "").strip()
            url = (item.findtext("link") or "").strip()
            published_text = (item.findtext("pubDate") or "").strip()
            parsed_url = urllib.parse.urlparse(url)
            if (
                not title
                or parsed_url.scheme != "https"
                or parsed_url.netloc != "stackonward.com"
                or not parsed_url.path.startswith("/posts/")
            ):
                continue
            if not published_text:
                raise ValueError(f"RSS post has no publication date: {url}")
            published_at = email.utils.parsedate_to_datetime(published_text)
            if published_at is None or published_at.tzinfo is None:
                raise ValueError(f"RSS post has no timezone: {url}")
            posts.append(BlogPost(title=title, url=url, published_at=published_at))

        posts.sort(key=lambda post: post.published_at, reverse=True)
        if not posts:
            raise ValueError("StackOnward RSS did not contain any public posts")
        return posts[:limit]


def escape_markdown_text(value: str) -> str:
    return re.sub(r"([\\\[\]])", r"\\\1", value)


def render_blog_posts(posts: list[BlogPost]) -> str:
    return "\n".join(
        f"- [{escape_markdown_text(post.title)}]({post.url}) · "
        f"{post.published_at.astimezone(CHINA_TIMEZONE).date().isoformat()}"
        for post in posts
    )


def replace_generated_region(document: str, content: str) -> str:
    if document.count(BLOG_REGION_START) != 1 or document.count(BLOG_REGION_END) != 1:
        raise ValueError("Organization profile must contain one published article region")
    start_index = document.index(BLOG_REGION_START) + len(BLOG_REGION_START)
    end_index = document.index(BLOG_REGION_END, start_index)
    return f"{document[:start_index]}\n{content}\n{document[end_index:]}"


def write_text_atomically(path: Path, content: str) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            delete=False,
        ) as temporary_file:
            temporary_file.write(content)
            temporary_path = Path(temporary_file.name)
        os.replace(temporary_path, path)
    finally:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()
    return True


def refresh(repository_root: Path, feed_url: str, limit: int) -> tuple[bool, int]:
    posts = StackOnwardRssSource(UrlLibHttpClient(), feed_url).latest_posts(limit)
    readme_path = repository_root / "profile" / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    updated_readme = replace_generated_region(readme, render_blog_posts(posts))
    return write_text_atomically(readme_path, updated_readme), len(posts)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Refresh published articles on the StackOnward organization profile"
    )
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument("--feed-url", default=DEFAULT_FEED_URL)
    parser.add_argument("--limit", type=int, default=5)
    arguments = parser.parse_args()
    if arguments.limit < 1 or arguments.limit > 10:
        raise ValueError("Article limit must be between 1 and 10")
    changed, post_count = refresh(
        arguments.repository_root.resolve(), arguments.feed_url, arguments.limit
    )
    print(
        f"published articles refreshed: posts={post_count} "
        f"readme_changed={str(changed).lower()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
