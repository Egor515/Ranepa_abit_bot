from functools import lru_cache

from app.agents.faq_response_agent import FAQResponseAgent
from app.agents.faq_retrieval_agent import FAQRetrievalAgent
from app.agents.safety_context_agent import SafetyContextAgent
from app.agents.stopwords_agent import StopWordsAgent
from app.core.config import settings
from app.graph.faq_pipeline import AdmissionFAQPipeline


@lru_cache(maxsize=1)
def get_pipeline() -> AdmissionFAQPipeline:
    faq_agent = FAQRetrievalAgent()
    return AdmissionFAQPipeline(
        stopwords_agent=StopWordsAgent(settings.STOPWORDS_FILES),
        safety_agent=SafetyContextAgent(),
        faq_retrieval_agent=faq_agent,
        faq_response_agent=FAQResponseAgent(faq_agent),
    )
