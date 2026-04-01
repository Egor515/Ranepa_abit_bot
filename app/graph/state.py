from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class SafetyDecision(StrEnum):
    ALLOW = "allow"
    REJECT = "reject"
    CLARIFY = "clarify"


class PipelineStage(StrEnum):
    RECEIVED = "received"
    STOPWORDS_CHECKED = "stopwords_checked"
    SAFETY_CHECKED = "safety_checked"
    FAQ_RETRIEVED = "faq_retrieved"
    FAQ_ANSWERED = "faq_answered"
    SQL_FALLBACK_PENDING = "sql_fallback_pending"
    COMPLETED = "completed"


class FAQCandidateView(BaseModel):
    id: int
    question: str
    answer: str
    score: float


class PipelineState(BaseModel):
    user_id: int
    original_question: str
    current_stage: PipelineStage = PipelineStage.RECEIVED
    safety_decision: SafetyDecision | None = None
    rejection_reason: str | None = None
    clarification_message: str | None = None
    final_answer: str | None = None
    faq_candidates: list[FAQCandidateView] = Field(default_factory=list)
    selected_faq_id: int | None = None
    selected_faq_question: str | None = None
    requires_sql_fallback: bool = False

    @property
    def has_faq_candidates(self) -> bool:
        return bool(self.faq_candidates)
