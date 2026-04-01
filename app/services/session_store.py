from typing import Any

from app.graph.state import PipelineState


class SessionStore:
    def __init__(self):
        self._storage: dict[int, dict[str, Any]] = {}

    def set(self, user_id: int, key: str, value: Any) -> None:
        if user_id not in self._storage:
            self._storage[user_id] = {}
        self._storage[user_id][key] = value

    def get(self, user_id: int, key: str, default: Any = None) -> Any:
        return self._storage.get(user_id, {}).get(key, default)

    def set_state(self, user_id: int, state: PipelineState) -> None:
        self.set(user_id, "pipeline_state", state.model_dump(mode="json"))

    def get_state(self, user_id: int) -> PipelineState | None:
        raw_state = self.get(user_id, "pipeline_state")
        if not raw_state:
            return None
        return PipelineState.model_validate(raw_state)

    def clear(self, user_id: int) -> None:
        if user_id in self._storage:
            del self._storage[user_id]


session_store = SessionStore()
