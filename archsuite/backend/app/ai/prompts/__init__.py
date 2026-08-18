"""AI prompt 模板集合。"""

from app.ai.prompts.contract_review import build_review_prompt
from app.ai.prompts.project_info import build_extract_prompt

__all__ = ["build_extract_prompt", "build_review_prompt"]
