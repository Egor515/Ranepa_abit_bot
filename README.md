# Ranepa Abit Bot

Telegram-бот для абитуриентов с tree-based pipeline архитектурой.

## Что уже заложено

- отдельные агенты для `stopwords`, `safety`, `FAQ retrieval`, `FAQ response`
- единый `PipelineState` для всего запроса
- orchestration-слой, который не смешан с Telegram-хендлерами
- подготовленный FastAPI entrypoint для health/readiness
- конфиг под Gemini, Milvus и FAQ-источник

## Целевой pipeline

```text
User message
  -> StopWordsAgent
  -> SafetyContextAgent
  -> FAQRetrievalAgent
  -> Telegram buttons with top-5 FAQ
  -> FAQResponseAgent
  -> SQLGeneratorAgent
  -> SQLValidator
  -> SQL execution
  -> AnswerSynthesisAgent
```

## Текущий статус

Реализованы стадии:

1. `StopWordsAgent`
2. `SafetyContextAgent`
3. `FAQRetrievalAgent`
4. выбор FAQ через inline-кнопки
5. `FAQResponseAgent`
6. состояние сессии пользователя через `PipelineState`

SQL fallback и LangGraph orchestration будут добавляться следующими этапами поверх уже подготовленного state-driven каркаса.

## Структура

```text
app/
  agents/      # отдельные этапы pipeline
  api/         # FastAPI entrypoint и будущие внешние endpoints
  bot/         # aiogram transport layer
  core/        # config, logging, dependency container
  db/          # будущая SQL-инфраструктура
  graph/       # pipeline state и orchestration
  prompts/     # LLM prompts
  services/    # интеграции и инфраструктурные сервисы
data/          # stopwords, excel, источники FAQ
```

## Переменные окружения

Пример `.env`:

```env
BOT_TOKEN=telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
FAQ_SOURCE_PATH=data/Database.xlsx
FAQ_QUESTION_COLUMN=Question
FAQ_ANSWER_COLUMN=Answer
MILVUS_URI=./milvus_faq.db
MILVUS_COLLECTION_NAME=faq_collection
FAQ_TOP_K=5
FAQ_SCORE_THRESHOLD=0.75
STOPWORDS_FILES=data/ru_abusive_words.txt,data/ru_curse_words.txt
```

## Локальный запуск

Установка зависимостей:

```bash
pip install -r requirements.txt
```

Индексация FAQ:

```bash
python -m app.services.index_faq_to_milvus
```

Запуск Telegram-бота:

```bash
python run_bot.py
```

Запуск API:

```bash
uvicorn app.api.main:app --reload
```

## Что делаем дальше

Следующий правильный шаг: построить SQL fallback-ветку как отдельный набор компонентов:

1. `SQLGeneratorAgent`
2. `SQLValidator`
3. SQL repository / executor
4. `AnswerSynthesisAgent`
5. после этого подключить `LangGraph` как оркестратор всего дерева
