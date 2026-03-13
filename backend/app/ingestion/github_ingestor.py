import base64
import logging

from github import Auth, Github

from app.config import settings
from app.ingestion.base import BaseIngestor, IngestedDocument

logger = logging.getLogger(__name__)


class GitHubIngestor(BaseIngestor):
    async def validate_config(self, config: dict) -> bool:
        return bool(config.get("repo"))

    async def ingest(self, config: dict) -> list[IngestedDocument]:
        repo_name = config["repo"]
        token = config.get("token") or settings.github_token
        include_issues = config.get("include_issues", True)
        include_prs = config.get("include_prs", True)
        include_code = config.get("include_code", True)

        g = Github(auth=Auth.Token(token)) if token else Github()
        repo = g.get_repo(repo_name)
        documents: list[IngestedDocument] = []

        # README
        try:
            readme = repo.get_readme()
            content = base64.b64decode(readme.content).decode("utf-8", errors="replace")
            documents.append(
                IngestedDocument(
                    external_id=f"readme:{readme.path}",
                    title=f"README - {repo_name}",
                    doc_type="readme",
                    content=content,
                    metadata={"repo": repo_name, "path": readme.path},
                )
            )
        except Exception:
            logger.warning("No README found for %s", repo_name)

        # Issues
        if include_issues:
            for issue in repo.get_issues(state="all"):
                if issue.pull_request:
                    continue
                body = issue.body or ""
                documents.append(
                    IngestedDocument(
                        external_id=f"issue:{issue.number}",
                        title=f"Issue #{issue.number}: {issue.title}",
                        doc_type="issue",
                        content=f"{issue.title}\n\n{body}",
                        metadata={
                            "repo": repo_name,
                            "number": issue.number,
                            "state": issue.state,
                            "labels": [lbl.name for lbl in issue.labels],
                            "author": (
                                issue.user.login
                                if issue.user else None
                            ),
                            "created_at": (
                                issue.created_at.isoformat()
                                if issue.created_at else None
                            ),
                        },
                    )
                )

        # Pull Requests
        if include_prs:
            for pr in repo.get_pulls(state="all"):
                body = pr.body or ""
                documents.append(
                    IngestedDocument(
                        external_id=f"pr:{pr.number}",
                        title=f"PR #{pr.number}: {pr.title}",
                        doc_type="pr",
                        content=f"{pr.title}\n\n{body}",
                        metadata={
                            "repo": repo_name,
                            "number": pr.number,
                            "state": pr.state,
                            "author": (
                                pr.user.login
                                if pr.user else None
                            ),
                            "merged": pr.merged,
                            "created_at": (
                                pr.created_at.isoformat()
                                if pr.created_at else None
                            ),
                        },
                    )
                )

        # Code files
        if include_code:
            code_extensions = {
                ".py", ".js", ".ts", ".tsx", ".md",
                ".yml", ".yaml", ".json", ".toml",
            }
            try:
                contents = repo.get_contents("")
                while contents:
                    file_content = contents.pop(0)
                    if file_content.type == "dir":
                        contents.extend(repo.get_contents(file_content.path))
                    elif any(file_content.path.endswith(ext) for ext in code_extensions):
                        try:
                            decoded = base64.b64decode(file_content.content).decode(
                                "utf-8", errors="replace"
                            )
                            if len(decoded) > 50000:
                                continue
                            documents.append(
                                IngestedDocument(
                                    external_id=f"file:{file_content.path}",
                                    title=file_content.path,
                                    doc_type="code",
                                    content=decoded,
                                    metadata={
                                        "repo": repo_name,
                                        "path": file_content.path,
                                        "size_bytes": file_content.size,
                                    },
                                )
                            )
                        except Exception:
                            logger.warning("Failed to decode %s", file_content.path)
            except Exception:
                logger.warning("Failed to list repo contents for %s", repo_name)

        g.close()
        return documents
