from app.agents.faq_retrieval_agent import FAQCandidate, FAQRetrievalAgent


class FAQResponseAgent:
    def __init__(self, faq_agent: FAQRetrievalAgent):
        self.faq_agent = faq_agent

    def get_response(self, faq_id: int) -> FAQCandidate | None:
        return self.faq_agent.get_by_id(faq_id)
