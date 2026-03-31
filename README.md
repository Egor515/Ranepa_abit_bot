# Ranepa Abit Bot

Telegram-бот для помощи абитуриентам с использованием RAG (Retrieval-Augmented Generation).

---

## 📌 Описание

Бот обрабатывает запрос пользователя через несколько этапов:

1. Проверка на ненормативную лексику
2. Проверка корректности запроса
3. Поиск релевантных FAQ через векторную БД (Milvus)
4. Выдача топ-5 наиболее близких вопросов
5. Переход в fallback-логику при отсутствии ответа

---

## 🧠 Архитектура

```text
User message
   ↓
StopWordsAgent
   ↓
SafetyContextAgent
   ↓
Embedding (sentence-transformers)
   ↓
Milvus vector search
   ↓
Top-5 FAQ
   ↓
Ответ / fallback
