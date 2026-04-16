# Script to create and store embeddings for KB articles in Pinecone

import logging
import re
from typing import Dict, List

logger = logging.getLogger(__name__)


class KBEmbedder:
    """Parse KB articles, generate embeddings, and upsert to Pinecone."""

    def __init__(self, openai_client, pinecone_client):
        """
        Args:
            openai_client: OpenAIClient instance (or any object with an
                           ``embed(text)`` method returning a list[float]).
            pinecone_client: PineconeClient instance.
        """
        self.openai = openai_client
        self.pinecone = pinecone_client

    # ------------------------------------------------------------------
    # Parsing
    # ------------------------------------------------------------------

    def extract_articles(self, md_file: str) -> List[Dict]:
        """Parse a markdown file and return a list of article dicts.

        Each article dict has:
          - ``id``:      URL-safe identifier derived from the title
          - ``title``:   Article title (from the ## heading)
          - ``content``: Full article text
        """
        with open(md_file, "r") as f:
            raw = f.read()

        # Split on level-2 headings; first element is the file header → skip
        sections = re.split(r"\n## ", raw)
        articles = []
        for section in sections[1:]:  # skip preamble before first ##
            lines = section.strip().splitlines()
            title = lines[0].strip()
            content = "\n".join(lines).strip()
            article_id = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")
            articles.append({"id": article_id, "title": title, "content": content})

        return articles

    # ------------------------------------------------------------------
    # Embedding & upsert
    # ------------------------------------------------------------------

    def embed_text(self, text: str) -> List[float]:
        """Create an embedding for ``text`` via OpenAI."""
        response = self.openai.embeddings.create(
            input=text,
            model="text-embedding-ada-002",
        )
        return response.data[0].embedding

    def create_and_store_embeddings(self, md_file: str) -> int:
        """Parse articles, embed each one, upsert to Pinecone.

        Returns the number of articles processed.
        """
        articles = self.extract_articles(md_file)
        vectors = []
        for article in articles:
            embedding = self.embed_text(article["content"])
            vectors.append(
                {
                    "id": article["id"],
                    "values": embedding,
                    "metadata": {
                        "title": article["title"],
                        "content": article["content"],
                    },
                }
            )
            logger.info(f"Embedded article: {article['title']}")

        self.pinecone.upsert(vectors)
        logger.info(f"Upserted {len(vectors)} articles to Pinecone")
        return len(vectors)
