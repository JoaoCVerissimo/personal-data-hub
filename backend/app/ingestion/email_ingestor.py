import email
import email.policy
import logging
import mailbox
from pathlib import Path

from bs4 import BeautifulSoup

from app.ingestion.base import BaseIngestor, IngestedDocument

logger = logging.getLogger(__name__)


class EmailIngestor(BaseIngestor):
    async def validate_config(self, config: dict) -> bool:
        path = config.get("path", "")
        return bool(path) and Path(path).exists()

    async def ingest(self, config: dict) -> list[IngestedDocument]:
        file_path = Path(config["path"])
        documents: list[IngestedDocument] = []

        if file_path.suffix == ".mbox":
            documents = self._ingest_mbox(file_path)
        elif file_path.suffix == ".eml":
            doc = self._parse_eml(file_path)
            if doc:
                documents.append(doc)
        elif file_path.is_dir():
            for eml_file in file_path.glob("**/*.eml"):
                doc = self._parse_eml(eml_file)
                if doc:
                    documents.append(doc)

        return documents

    def _ingest_mbox(self, path: Path) -> list[IngestedDocument]:
        documents: list[IngestedDocument] = []
        mbox = mailbox.mbox(str(path))
        for i, message in enumerate(mbox):
            try:
                doc = self._message_to_document(message, f"mbox:{path.name}:{i}")
                if doc:
                    documents.append(doc)
            except Exception:
                logger.warning("Failed to parse message %d from %s", i, path)
        return documents

    def _parse_eml(self, path: Path) -> IngestedDocument | None:
        try:
            with open(path, "rb") as f:
                msg = email.message_from_binary_file(f, policy=email.policy.default)
            return self._message_to_document(msg, f"eml:{path.name}")
        except Exception:
            logger.warning("Failed to parse %s", path)
            return None

    def _message_to_document(
        self, msg: email.message.Message, external_id: str
    ) -> IngestedDocument | None:
        subject = str(msg.get("Subject", "No Subject"))
        sender = str(msg.get("From", ""))
        to = str(msg.get("To", ""))
        date = str(msg.get("Date", ""))

        body = self._extract_body(msg)
        if not body.strip():
            return None

        return IngestedDocument(
            external_id=external_id,
            title=subject,
            doc_type="email",
            content=f"Subject: {subject}\nFrom: {sender}\nTo: {to}\nDate: {date}\n\n{body}",
            metadata={
                "from": sender,
                "to": to,
                "subject": subject,
                "date": date,
            },
        )

    @staticmethod
    def _extract_body(msg: email.message.Message) -> str:
        if msg.is_multipart():
            text_parts: list[str] = []
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    payload = part.get_payload(decode=True)
                    if isinstance(payload, bytes):
                        text_parts.append(payload.decode("utf-8", errors="replace"))
                elif content_type == "text/html" and not text_parts:
                    payload = part.get_payload(decode=True)
                    if isinstance(payload, bytes):
                        html = payload.decode("utf-8", errors="replace")
                        soup = BeautifulSoup(html, "html.parser")
                        text_parts.append(soup.get_text(separator="\n", strip=True))
            return "\n".join(text_parts)
        else:
            payload = msg.get_payload(decode=True)
            if isinstance(payload, bytes):
                text = payload.decode("utf-8", errors="replace")
                if msg.get_content_type() == "text/html":
                    soup = BeautifulSoup(text, "html.parser")
                    result: str = soup.get_text(separator="\n", strip=True)
                    return result
                return text
        return ""
