from __future__ import annotations

from app.agents.faq_response_agent import FAQResponseAgent
from app.agents.faq_retrieval_agent import FAQRetrievalAgent
from app.agents.safety_context_agent import SafetyContextAgent
from app.agents.stopwords_agent import StopWordsAgent
from app.core.config import settings
from app.graph.state import FAQCandidateView, PipelineStage, PipelineState, SafetyDecision


class AdmissionFAQPipeline:
    def __init__(
        self,
        stopwords_agent: StopWordsAgent,
        safety_agent: SafetyContextAgent,
        faq_retrieval_agent: FAQRetrievalAgent,
        faq_response_agent: FAQResponseAgent,
    ):
        self.stopwords_agent = stopwords_agent
        self.safety_agent = safety_agent
        self.faq_retrieval_agent = faq_retrieval_agent
        self.faq_response_agent = faq_response_agent

    def handle_question(self, user_id: int, text: str) -> PipelineState:
        state = PipelineState(user_id=user_id, original_question=(text or "").strip())

        stopwords_result = self.stopwords_agent.check(state.original_question)
        state.current_stage = PipelineStage.STOPWORDS_CHECKED
        if not stopwords_result.passed:
            state.safety_decision = SafetyDecision.REJECT
            state.rejection_reason = stopwords_result.reason
            state.final_answer = "Я не буду отвечать на сообщения с ненормативной лексикой."
            state.current_stage = PipelineStage.COMPLETED
            return state

        safety_result = self.safety_agent.check(state.original_question)
        state.current_stage = PipelineStage.SAFETY_CHECKED
        state.safety_decision = SafetyDecision(safety_result.decision)
        if state.safety_decision is SafetyDecision.REJECT:
            state.rejection_reason = safety_result.reason
            state.final_answer = safety_result.reply
            state.current_stage = PipelineStage.COMPLETED
            return state

        if state.safety_decision is SafetyDecision.CLARIFY:
            state.clarification_message = safety_result.reply
            state.final_answer = safety_result.reply
            state.current_stage = PipelineStage.COMPLETED
            return state

        candidates = self.faq_retrieval_agent.search(
            query=state.original_question,
            top_k=settings.FAQ_TOP_K,
            threshold=settings.FAQ_SCORE_THRESHOLD,
        )
        state.faq_candidates = [FAQCandidateView.model_validate(candidate.__dict__) for candidate in candidates]
        state.current_stage = PipelineStage.FAQ_RETRIEVED

        if state.has_faq_candidates:
            return state

        state.requires_sql_fallback = True
        state.current_stage = PipelineStage.SQL_FALLBACK_PENDING
        state.final_answer = (
            "Я не нашел подходящий FAQ. Следующим этапом подключим SQL fallback-ветку."
        )
        return state

    def handle_faq_selection(self, state: PipelineState, faq_id: int | None) -> PipelineState:
        if faq_id is None:
            state.requires_sql_fallback = True
            state.current_stage = PipelineStage.SQL_FALLBACK_PENDING
            state.final_answer = (
                "Понял, среди FAQ подходящего ответа нет. "
                "Следующим этапом этот запрос будет отправляться в SQL fallback-ветку."
            )
            return state

        faq_item = self.faq_response_agent.get_response(faq_id)
        if faq_item is None:
            state.final_answer = "Не удалось найти выбранный FAQ."
            state.current_stage = PipelineStage.COMPLETED
            return state

        state.selected_faq_id = faq_item.id
        state.selected_faq_question = faq_item.question
        state.final_answer = faq_item.answer
        state.current_stage = PipelineStage.FAQ_ANSWERED
        return state
