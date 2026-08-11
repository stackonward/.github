from __future__ import annotations

import datetime as dt
import tempfile
import unittest
from pathlib import Path
from zoneinfo import ZoneInfo

from scripts.refresh_published_articles import (
    BlogPost,
    StackOnwardRssSource,
    render_blog_posts,
    replace_generated_region,
    write_text_atomically,
)


class StaticHttpClient:
    def __init__(self, response: str) -> None:
        self._response = response

    def get_text(self, url: str) -> str:
        return self._response


class PublishedArticleRefreshTest(unittest.TestCase):
    def test_rss_keeps_only_canonical_posts_and_sorts_newest_first(self) -> None:
        rss = """<?xml version="1.0"?>
<rss version="2.0"><channel>
  <item><title>Older</title><link>https://stackonward.com/posts/older/</link><pubDate>Mon, 01 Jan 2024 08:00:00 +0800</pubDate></item>
  <item><title>About</title><link>https://stackonward.com/about/</link><pubDate>Tue, 02 Jan 2024 08:00:00 +0800</pubDate></item>
  <item><title>Other host</title><link>https://example.com/posts/copied/</link><pubDate>Tue, 02 Jan 2024 08:00:00 +0800</pubDate></item>
  <item><title>Newer</title><link>https://stackonward.com/posts/newer/</link><pubDate>Wed, 03 Jan 2024 08:00:00 +0800</pubDate></item>
</channel></rss>"""

        posts = StackOnwardRssSource(StaticHttpClient(rss), "https://feed.test").latest_posts(5)

        self.assertEqual([post.title for post in posts], ["Newer", "Older"])

    def test_generated_region_requires_one_marker_pair(self) -> None:
        document = "before\n<!-- BLOG-POST-LIST:START -->\nold\n<!-- BLOG-POST-LIST:END -->\nafter\n"

        updated = replace_generated_region(document, "new")

        self.assertEqual(
            updated,
            "before\n<!-- BLOG-POST-LIST:START -->\nnew\n<!-- BLOG-POST-LIST:END -->\nafter\n",
        )
        with self.assertRaises(ValueError):
            replace_generated_region("missing", "new")

    def test_rendering_escapes_markdown_and_uses_china_date(self) -> None:
        posts = [
            BlogPost(
                title="A [verified] post",
                url="https://stackonward.com/posts/verified/",
                published_at=dt.datetime(
                    2026, 8, 11, 16, 30, tzinfo=dt.timezone.utc
                ),
            )
        ]

        rendered = render_blog_posts(posts)

        self.assertIn("A \\[verified\\] post", rendered)
        self.assertTrue(rendered.endswith("2026-08-12"))

    def test_atomic_write_reports_real_changes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "README.md"

            self.assertTrue(write_text_atomically(path, "first\n"))
            self.assertFalse(write_text_atomically(path, "first\n"))
            self.assertTrue(write_text_atomically(path, "second\n"))
            self.assertEqual(path.read_text(encoding="utf-8"), "second\n")


if __name__ == "__main__":
    unittest.main()
