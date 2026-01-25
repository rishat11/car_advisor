# **ПРОЕКТ СИСТЕМЫ ПОДБОРА АВТОМОБИЛЕЙ**
backend-developer
## **I. БИЗНЕС-КОНТЕКСТ И ОПИСАНИЕ СЕРВИСА**

### **1.1. Проблема пользователя**
Пользователи, которые хотят купить автомобиль, часто сталкиваются со сложностями:
- Не могут сформулировать технический запрос ("не знаю, что нужно")
- Запутались в разнообразии марок, моделей и характеристик
- Не понимают, какие параметры действительно важны для их нужд
- Тратится много времени на самостоятельный поиск и сравнение

### **1.2. Решение**
Интеллектуальный помощник, который:
- Общается с пользователем на естественном языке
- Задает уточняющие вопросы для понимания реальных потребностей
- Переводит расплывчатые формулировки в конкретные технические параметры
- Ищет подходящие автомобили в структурированной базе данных
- Предоставляет персонализированные рекомендации

### **1.3. Цели бизнеса (сети автосалонов)**
1. **Генерация лидов** - привлечение новых клиентов через полезный сервис
2. **Повышение конверсии** - квалификация клиентов до обращения в салон
3. **Снижение нагрузки** на менеджеров автосалонов
4. **Создание дополнительного канала** продаж
5. **Сбор аналитики** о предпочтениях покупателей

### **1.4. Ценностное предложение**
- **Для пользователя**: бесплатная экспертная помощь в выборе, экономия времени, объективные рекомендации
- **Для бизнеса**: дополнительные продажи, лояльность клиентов, конкурентное преимущество

## **II. СЦЕНАРИИ ИСПОЛЬЗОВАНИЯ (USER STORIES)**

### **2.1. Основные роли пользователей**
- **Покупатель автомобиля** - основной пользователь системы
- **Менеджер автосалона** - просматривает лиды и результаты подбора
- **Администратор системы** - управляет каталогом и настройками

### **2.2. User Stories для покупателя**
```
US-1: Как покупатель, я хочу описать свои потребности простыми словами,
      чтобы система поняла, что мне нужно.
      Критерии успеха: система корректно интерпретирует разговорный запрос.

US-2: Как покупатель, я хочу получить уточняющие вопросы,
      когда мой запрос недостаточно конкретен.
      Критерии успеха: система задает релевантные вопросы, не требующие технических знаний.

US-3: Как покупатель, я хочу увидеть список подходящих автомобилей
      с понятным объяснением, почему они мне подходят.
      Критерии успеха: для каждого автомобиля указано соответствие моим критериям.

US-4: Как покупатель, я хочу сохранить результаты поиска,
      чтобы вернуться к ним позже или поделиться с семьей.
      Критерии успеха: система сохраняет историю и позволяет экспортировать результаты.

US-5: Как покупатель, я хочу оставить заявку на понравившийся автомобиль,
      чтобы менеджер связался со мной.
      Критерии успеха: заявка отправляется в CRM системы автосалона.

US-6: Как покупатель, я хочу сравнить несколько автомобилей по ключевым параметрам,
      чтобы принять обоснованное решение.
      Критерии успеха: система предоставляет сравнительную таблицу.
```

### **2.3. User Stories для менеджера автосалона**
```
US-7: Как менеджер, я хочу видеть список "горячих" лидов,
      чтобы своевременно связаться с потенциальными покупателями.
      Критерии успеха: система ранжирует лиды по вероятности покупки.

US-8: Как менеджер, я хочу видеть полную историю диалога с клиентом,
      чтобы понимать его потребности перед звонком.
      Критерии успеха: доступны все сообщения и извлеченные параметры.

US-9: Как менеджер, я хочу получать уведомления о новых заявках,
      чтобы оперативно реагировать.
      Критерии успеха: уведомления приходят в Telegram/email в течение 5 минут.
```

### **2.4. User Stories для администратора**
```
US-10: Как администратор, я хочу управлять каталогом автомобилей,
       чтобы актуализировать данные.
       Критерии успеха: CRUD операции для автомобилей через админ-панель.

US-11: Как администратор, я хочу настраивать промпты LLM,
       чтобы улучшать качество диалогов.
       Критерии успеха: возможность редактировать промпты без передеплоя.

US-12: Как администратор, я хочу видеть аналитику использования системы,
       чтобы принимать решения о развитии.
       Критерии успеха: дашборды с ключевыми метриками.
```

### **2.5. Диаграммы путей пользователя**
```
1. Путь "Быстрый подбор":
   Старт → Описание потребностей → Уточняющие вопросы (опционально) →
   Результаты поиска → Сравнение → Заявка на тест-драйв → Конец

2. Путь "Углубленный поиск":
   Старт → Регистрация → Сохранение предпочтений → Диалог с ассистентом →
   Расширенные фильтры → Сохранение результатов → Получение уведомлений →
   Заявка на просмотр → Конец

3. Путь "Повторный пользователь":
   Вход → История поисков → Изменение критериев → Новый поиск →
   Сравнение с предыдущими результатами → Заявка → Конец
```

## **III. СТРУКТУРА БАЗЫ ДАННЫХ**

### **3.1. Таблица автомобилей (cars)**
```
cars:
- id (INT, PK) - уникальный идентификатор автомобиля
- mark (VARCHAR) - марка автомобиля в нижнем регистре (toyota, marussia)
- folder_name (VARCHAR) - модель/поколение (B2, Camry, CC850)
- model_code (VARCHAR) - код модели (MARUSSIA, COROLLA)
- body_type (VARCHAR) - тип кузова (седан, внедорожник, купе)
- engine_capacity (DECIMAL) - объем двигателя в литрах (2.8, 1.5)
- engine_power (INT) - мощность в л.с. (177, 300)
- transmission_type (VARCHAR) - тип КПП (MT, AT, CVT, AMT)
- drive_type (VARCHAR) - тип привода (FWD, RWD, 4WD)
- fuel_type (VARCHAR) - тип топлива (petrol, diesel, hybrid, electric)
- year_from (INT) - год начала выпуска
- year_to (INT) - год окончания выпуска (NULL для текущих)
- country (VARCHAR) - страна производства (Япония, Россия, Швеция)
- color (VARCHAR) - базовый цвет (Красный, Серый, Черный)
- base_price (DECIMAL) - ориентировочная базовая цена
- is_available (BOOLEAN) - доступен ли в наличии
- features (JSON) - {
    "seats": 5,
    "doors": 5,
    "fuel_consumption_city": 10.5,
    "fuel_consumption_highway": 7.2,
    "trunk_volume": 480,
    "safety_rating": 5
  }
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

ИНДЕКСЫ:
- idx_cars_mark (mark)
- idx_cars_body_type (body_type)
- idx_cars_engine_power (engine_power)
- idx_cars_price (base_price)
- idx_cars_year_from (year_from)
```

### **3.2. Таблица пользователей (users)**
```
users:
- id (INT, PK)
- email (VARCHAR, UNIQUE)
- password_hash (VARCHAR)
- full_name (VARCHAR)
- phone (VARCHAR)
- preferences (JSON) - {
    "preferred_body_types": ["внедорожник", "кроссовер"],
    "max_budget": 2500000,
    "fuel_type_preference": "petrol",
    "transmission_preference": "AT"
  }
- search_history (JSON) - последние 10 поисков
- created_at (TIMESTAMP)
- last_login (TIMESTAMP)
- is_active (BOOLEAN)
```

### **3.3. Таблица диалогов (dialogs)**
```
dialogs:
- id (INT, PK)
- user_id (INT, FK → users.id)
- status (VARCHAR) - active, completed, archived
- extracted_params_count (INT) - количество успешно извлеченных параметров
- context (JSON) - {
    "current_parameters": {
      "mark": "toyota",
      "body_type": "внедорожник",
      "min_power": 150,
      "max_price": 3000000
    },
    "can_search": true,  // true если параметров достаточно для поиска
    "clarification_needed": false
  }
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- completed_at (TIMESTAMP)
```

### **3.4. Таблица сообщений (messages)**
```
messages:
- id (INT, PK)
- dialog_id (INT, FK → dialogs.id)
- sender_type (VARCHAR) - user или assistant
- content (TEXT) - текст сообщения
- extraction_result (JSON) - {
    "extracted_params": {
      "mark": {"value": "toyota", "confidence": 0.9},
      "body_type": {"value": "внедорожник", "confidence": 0.85},
      "min_power": {"value": 150, "confidence": 0.7}
    },
    "total_params_extracted": 3,
    "can_proceed_to_search": true,
    "missing_parameters": ["max_price", "transmission_type"]
  }
- is_parsed_successfully (BOOLEAN)
- created_at (TIMESTAMP)
```

### **3.5. Таблица рекомендаций (recommendations)**
```
recommendations:
- id (INT, PK)
- dialog_id (INT, FK → dialogs.id)
- car_id (INT, FK → cars.id)
- relevance_score (DECIMAL) - 0.85
- matched_parameters_count (INT) - сколько параметров совпало
- match_explanation (JSON) - {
    "matched_parameters": ["mark", "body_type", "engine_power"],
    "close_matches": ["price"],
    "missing_parameters": ["color"]
  }
- user_feedback (VARCHAR) - liked, disliked, neutral
- presented_at (TIMESTAMP)
- feedback_at (TIMESTAMP)
```

## **IV. АРХИТЕКТУРНЫЕ ДИАГРАММЫ**

### **4.1. Диаграмма компонентов системы**
```mermaid
graph TB
    subgraph "Frontend Layer"
        WEB[Web Application<br/>React/TypeScript]
        MOBILE[Mobile Web]
        ADMIN[Admin Panel]
    end

    subgraph "API Gateway Layer"
        APIGW[API Gateway<br/>Nginx + FastAPI]
        AUTH[Auth Service]
        RATE[Rate Limiter]
    end

    subgraph "Business Layer"
        CHAT[Chat Service]
        LLM[LLM Orchestrator]
        SEARCH[Car Search Service]
        REC[Recommendation Engine]
        NOTIF[Notification Service]
    end

    subgraph "Data Layer"
        DB[(PostgreSQL)]
        CACHE[(Redis Cache)]
        BLOB[(Object Storage<br/>Images)]
    end

    subgraph "External Services"
        OPENAI[OpenAI API]
        TELEGRAM[Telegram API]
        EMAIL[Email Service]
        CRM[External CRM]
    end

    WEB --> APIGW
    MOBILE --> APIGW
    ADMIN --> APIGW

    APIGW --> AUTH
    AUTH --> CHAT
    AUTH --> SEARCH
    AUTH --> ADMIN

    CHAT --> LLM
    LLM --> OPENAI
    LLM --> SEARCH
    SEARCH --> DB
    SEARCH --> CACHE

    CHAT --> REC
    REC --> DB

    CHAT --> NOTIF
    NOTIF --> TELEGRAM
    NOTIF --> EMAIL
    NOTIF --> CRM
```

### **4.2. Диаграмма последовательности (основной сценарий)**
```mermaid
sequenceDiagram
    participant U as Пользователь
    participant F as Frontend
    participant A as API Gateway
    participant C as Chat Service
    participant L as LLM Orchestrator
    participant O as OpenAI
    participant S as Search Service
    participant D as Database

    U->>F: Отправляет сообщение
    F->>A: POST /api/chat/message
    A->>C: Передает сообщение
    C->>D: Сохраняет сообщение

    alt Новый диалог
        C->>L: Извлечение параметров (Промпт 1)
        L->>O: Запрос к GPT-4
        O-->>L: JSON с параметрами
        L->>C: Возвращает результат

        C->>S: Проверка достаточности параметров
        S-->>C: can_search = false

        C->>L: Генерация уточняющего вопроса (Промпт 2)
        L->>O: Запрос к GPT-4
        O-->>L: Текст вопроса
        L->>C: Возвращает вопрос

    else Продолжение диалога
        C->>D: Получает контекст диалога
        C->>L: Извлечение параметров + контекст
        L->>O: Запрос к GPT-4
        O-->>L: JSON с параметрами

        C->>S: Проверка достаточности параметров
        S-->>C: can_search = true

        C->>S: Поиск автомобилей
        S->>D: SQL запрос
        D-->>S: Результаты
        S-->>C: Список автомобилей

        C->>L: Форматирование результатов (Промпт 3)
        L->>O: Запрос к GPT-4
        O-->>L: Форматированный ответ
    end

    C->>D: Сохраняет результат
    C-->>A: Ответ
    A-->>F: Ответ
    F-->>U: Показывает ответ
```

## **V. ПРОМПТЫ ДЛЯ LLM**

### **Промпт 1: Извлечение параметров из запроса**
```
ЗАДАЧА: Ты — ИИ-ассистент для подбора автомобилей. Извлекай структурированные параметры из запросов пользователей.

ДОСТУПНЫЕ ПАРАМЕТРЫ (должны соответствовать полям в базе данных):
1. mark (марка): toyota, bmw, mercedes, audi, honda, kia, hyundai, marussia, koenigsegg
2. body_type (тип кузова): седан, внедорожник, кроссовер, хэтчбек, универсал, купе, кабриолет, минивен
3. min_power (минимальная мощность): число в л.с. (150, 200, 300)
4. max_power (максимальная мощность): число в л.с.
5. max_price (максимальная цена): число в рублях (2000000, 3500000)
6. transmission_type (тип КПП): AT (автомат), MT (механика), CVT (вариатор), AMT (робот)
7. drive_type (привод): FWD (передний), RWD (задний), 4WD (полный)
8. fuel_type (тип топлива): petrol (бензин), diesel (дизель), hybrid (гибрид), electric (электро)
9. color (цвет): красный, синий, черный, белый, серый, зеленый, серебристый
10. country (страна): Япония, Германия, Корея, США, Россия, Швеция, Китай
11. min_year (минимальный год выпуска): 2015, 2020
12. max_year (максимальный год выпуска): 2023, 2024

ПРАВИЛА ПРЕОБРАЗОВАНИЯ:
- "автомат/автоматическая" → "AT"
- "механика/механическая" → "MT"
- "вариатор" → "CVT"
- "полный привод/4x4" → "4WD"
- "передний привод" → "FWD"
- "задний привод" → "RWD"
- "дизель/дизельный" → "diesel"
- "бензин/бензиновый" → "petrol"
- "гибрид/гибридный" → "hybrid"
- "электро/электрический" → "electric"

FEW-SHOT ПРИМЕРЫ:

Пример 1:
Запрос: "Хочу красный внедорожник до 3 миллионов"
Выход: {
  "parameters": {
    "body_type": {"value": "внедорожник", "confidence": 0.95},
    "color": {"value": "красный", "confidence": 0.90},
    "max_price": {"value": 3000000, "confidence": 0.85}
  },
  "total_params_extracted": 3,
  "can_proceed_to_search": true,
  "missing_parameters": ["mark", "transmission_type", "min_power"],
  "next_action": "search"
}

Пример 2:
Запрос: "Нужен автомобиль для семьи"
Выход: {
  "parameters": {
    "body_type": {"value": "минивен", "confidence": 0.70},
    "seats": {"value": 5, "confidence": 0.65}
  },
  "total_params_extracted": 2,
  "can_proceed_to_search": false,
  "missing_parameters": ["mark", "max_price", "transmission_type", "min_year"],
  "next_action": "clarify"
}

Пример 3:
Запрос: "Ищу японский седан с автоматом, мощностью от 150 л.с."
Выход: {
  "parameters": {
    "country": {"value": "Япония", "confidence": 0.92},
    "body_type": {"value": "седан", "confidence": 0.88},
    "transmission_type": {"value": "AT", "confidence": 0.90},
    "min_power": {"value": 150, "confidence": 0.87}
  },
  "total_params_extracted": 4,
  "can_proceed_to_search": true,
  "missing_parameters": ["mark", "max_price", "color"],
  "next_action": "search"
}

ВХОД: Текст запроса пользователя
ВЫХОД: JSON строго в указанном формате
```

### **Промпт 2: Генерация уточняющих вопросов**
```
ЗАДАЧА: Сгенерировать уточняющий вопрос для сбора недостающих параметров.

ПРАВИЛА:
1. Спрашивай о наиболее важных параметрах для поиска
2. Предлагай конкретные варианты, чтобы упростить выбор
3. Учитывай уже известные параметры
4. Будь дружелюбным и экспертым

ПРИМЕРЫ:

Пример 1:
Известно: {"body_type": "внедорожник"}
Требуется: еще параметры для поиска
Выход: "Отлично, внедорожник — хороший выбор! Подскажите:
1. Какой бюджет вы рассматриваете (например, до 2, 3 или 4 миллионов)?
2. Есть ли предпочтения по марке (Toyota, Kia, Hyundai) или стране производства?"

Пример 2:
Известно: {"max_price": 2500000, "color": "черный"}
Требуется: еще параметры для поиска
Выход: "Понял, черный автомобиль до 2.5 млн рублей. Какой тип автомобиля вам нужен: седан для города, внедорожник для поездок или хэтчбек для экономии?"

Пример 3:
Известно: {"mark": "toyota", "transmission_type": "AT", "min_year": 2020}
Не хватает: ["body_type", "max_price"]
Выход: "Отлично! У нас уже есть основные параметры. Для более точных результатов уточните:
- Какой тип кузова предпочитаете (внедорожник, седан, хэтчбек)?
- Какой максимальный бюджет?"

ВХОД: {
  "current_parameters": {...},
  "missing_parameters": [...]
}
ВЫХОД: Естественный вопрос на русском языке
```

### **Промпт 3: Форматирование результатов поиска**
```
ЗАДАЧА: Представить результаты поиска понятным и полезным образом.

ПРАВИЛА:
1. Начинай с краткого итога
2. Для каждого автомобиля выдели ключевые преимущества
3. Упоминай соответствие параметрам поиска
4. Предложи следующий шаг

ПРИМЕР:

ВХОД: {
  "search_parameters": {
    "mark": "toyota",
    "body_type": "внедорожник",
    "max_price": 3000000,
    "transmission_type": "AT"
  },
  "cars": [
    {
      "mark": "toyota",
      "folder_name": "RAV4",
      "year_from": 2019,
      "engine_power": 150,
      "transmission_type": "AT",
      "base_price": 2800000,
      "body_type": "внедорожник",
      "match_score": 0.95
    }
  ]
}

ВЫХОД: "Я нашел варианты по вашим критериям: Toyota, внедорожник, до 3 млн рублей, автоматическая КПП.

1. **Toyota RAV4** (от 2019 года) - совпадение 95%
   - ✅ Toyota (соответствует марке)
   - ✅ Внедорожник (правильный тип кузова)
   - ✅ 2.8 млн рублей (укладывается в бюджет)
   - ✅ Автоматическая КПП
   - Дополнительно: мощность 150 л.с., расход 8.5л/100км

По этим параметрам найдено X вариантов. Для более точного подбора можете уточнить дополнительные параметры."
```

### **Промпт 4: Обработка некорректных запросов**
```
ЗАДАЧА: Вежливо обработать нерелевантные запросы и вернуть разговор к теме.

ПРИМЕРЫ:

Пример 1:
Запрос: "Привет"
Выход: "Привет! Я помогу вам подобрать автомобиль. Расскажите, какую машину вы ищете?"

Пример 2:
Запрос: "Посоветуй что-нибудь"
Выход: "С удовольствием помогу с выбором! Назовите несколько параметров, например, для каких целей нужна машина и какой бюджет?"

Пример 3:
Запрос: "Хочу машину"
Выход: "Отлично, давайте подберем! Ответьте на несколько вопросов:
1. Какой тип автомобиля нужен?
2. Какой максимальный бюджет?
3. Автоматическая или механическая коробка передач?"

ВХОД: Любой текст пользователя
ВЫХОД: Вежливый ответ с возвратом к теме
```

## **VI. ЛОГИКА СИСТЕМЫ (С МИНИМАЛЬНЫМ КОЛИЧЕСТВОМ ПАРАМЕТРОВ)**

### **Алгоритм работы:**
```
1. ПОЛЬЗОВАТЕЛЬ: Отправляет запрос
2. LLM: Извлекает параметры (Промпт 1)
3. ПРОВЕРКА: Если total_params_extracted >= 3 → can_proceed_to_search = true
              Иначе → can_proceed_to_search = false
4. ДЕЙСТВИЕ: Если can_proceed_to_search = true → поиск и показ результатов
              Если can_proceed_to_search = false → уточняющий вопрос
5. ПОВТОР: Пока can_proceed_to_search = false, продолжаем уточнять
```

### **Бизнес-логика:**
```python
MIN_PARAMS_FOR_SEARCH = 3

def should_proceed_to_search(llm_output):
    """Определяет, достаточно ли параметров для поиска"""
    return llm_output.get("total_params_extracted", 0) >= MIN_PARAMS_FOR_SEARCH

def generate_response(user_message, dialog_context):
    # Извлечение параметров
    extraction_result = call_llm_prompt1(user_message)

    # Проверка минимального количества
    if should_proceed_to_search(extraction_result):
        # Поиск автомобилей
        cars_found = search_cars(extraction_result["parameters"])
        response = call_llm_prompt3(extraction_result["parameters"], cars_found)
    else:
        # Уточняющий вопрос
        response = call_llm_prompt2(
            current_parameters=extraction_result["parameters"],
            missing_parameters=extraction_result["missing_parameters"]
        )

    return response
```

## **VII. ТЕСТИРОВАНИЕ**

### **Тест 1: Запрос с достаточным количеством параметров**
```
ВХОД: "Ищу немецкий седан с автоматом до 4 миллионов"
ПРОМПТ 1 ВЫХОД: {
  "parameters": {
    "country": {"value": "Германия", "confidence": 0.94},
    "body_type": {"value": "седан", "confidence": 0.92},
    "transmission_type": {"value": "AT", "confidence": 0.90},
    "max_price": {"value": 4000000, "confidence": 0.88}
  },
  "total_params_extracted": 4,
  "can_proceed_to_search": true,
  "missing_parameters": ["mark", "min_power", "color"],
  "next_action": "search"
}
ДЕЙСТВИЕ: Поиск автомобилей → показ результатов
```

### **Тест 2: Запрос с недостаточным количеством параметров**
```
ВХОД: "Хочу красную машину"
ПРОМПТ 1 ВЫХОД: {
  "parameters": {
    "color": {"value": "красный", "confidence": 0.95},
    "body_type": {"value": "седан", "confidence": 0.65}
  },
  "total_params_extracted": 2,
  "can_proceed_to_search": false,
  "missing_parameters": ["mark", "max_price", "transmission_type", "min_year"],
  "next_action": "clarify"
}
ПРОМПТ 2 ВЫХОД: "Понял, красный автомобиль. Уточните:
1. Какой тип кузова предпочитаете (седан, хэтчбек, внедорожник)?
2. Какой максимальный бюджет?"
ДЕЙСТВИЕ: Ожидание ответа пользователя
```

### **Тест 3: Расплывчатый запрос**
```
ВХОД: "Нужна экономичная машина для города"
ПРОМПТ 1 ВЫХОД: {
  "parameters": {
    "fuel_type": {"value": "hybrid", "confidence": 0.75},
    "body_type": {"value": "хэтчбек", "confidence": 0.70},
    "engine_capacity": {"value": 1.5, "confidence": 0.65}
  },
  "total_params_extracted": 3,
  "can_proceed_to_search": true,
  "missing_parameters": ["mark", "max_price", "transmission_type", "color"],
  "next_action": "search"
}
ДЕЙСТВИЕ: Поиск автомобилей → показ результатов
```

## **VIII. БЕЗОПАСНОСТЬ**

### **8.1. Аутентификация и авторизация**
```yaml
security_schemes:
  JWT_Token:
    type: apiKey
    in: header
    name: Authorization
    description: JWT токен формата "Bearer {token}"

roles:
  - USER: может создавать диалоги, искать автомобили, оставлять заявки
  - MANAGER: может просматривать лиды, историю диалогов, статистику
  - ADMIN: полный доступ ко всем функциям системы
```

### **8.2. Хранение паролей**
```python
# Использование bcrypt для хеширования паролей
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed.encode('utf-8')
    )
```

### **8.3. Защита данных**
```python
# Конфигурация безопасности
SECURITY_CONFIG = {
    "jwt_secret_key": os.getenv("JWT_SECRET_KEY"),  # 256-битный ключ
    "jwt_algorithm": "HS256",
    "jwt_expiration_minutes": 60,
    "password_min_length": 8,
    "password_complexity": True,  # требовать цифры и спецсимволы
    "rate_limit_requests": 100,  # запросов в минуту
    "rate_limit_period": 60,
    "cors_origins": ["https://example.com"],  # разрешенные домены
    "https_only": True,
    "session_timeout_minutes": 30,
    "data_encryption": {
        "enabled": True,
        "algorithm": "AES-256-GCM",
        "key_rotation_days": 90
    }
}
```

## **IX. СПЕЦИФИКАЦИЯ API**

### **9.1. Base URL и версионирование**
```
https://api.car-finder.example.com/v1
```

### **9.2. Endpoints**

#### **Аутентификация**
```yaml
POST /auth/register:
  summary: Регистрация нового пользователя
  requestBody:
    required: true
    content:
      application/json:
        schema:
          type: object
          properties:
            email:
              type: string
              format: email
            password:
              type: string
              minLength: 8
            full_name:
              type: string
            phone:
              type: string
  responses:
    201:
      description: Пользователь создан
      content:
        application/json:
          schema:
            type: object
            properties:
              user_id: {type: integer}
              access_token: {type: string}
              refresh_token: {type: string}
    400:
      description: Неверные данные

POST /auth/login:
  summary: Вход в систему
  requestBody:
    required: true
    content:
      application/json:
        schema:
          type: object
          properties:
            email: {type: string}
            password: {type: string}
  responses:
    200:
      description: Успешный вход
    401:
      description: Неверные учетные данные

POST /auth/refresh:
  summary: Обновление токена
  requestBody:
    required: true
    content:
      application/json:
        schema:
          type: object
          properties:
            refresh_token: {type: string}
  responses:
    200:
      description: Токен обновлен
```

#### **Диалоги и поиск**
```yaml
POST /chat/dialogs:
  summary: Создание нового диалога
  security:
    - JWT_Token: []
  responses:
    201:
      description: Диалог создан
      content:
        application/json:
          schema:
            type: object
            properties:
              dialog_id: {type: integer}
              created_at: {type: string}

POST /chat/dialogs/{dialog_id}/messages:
  summary: Отправка сообщения в диалог
  security:
    - JWT_Token: []
  parameters:
    - name: dialog_id
      in: path
      required: true
      schema: {type: integer}
  requestBody:
    required: true
    content:
      application/json:
        schema:
          type: object
          properties:
            content: {type: string}
  responses:
    200:
      description: Ответ от ассистента
      content:
        application/json:
          schema:
            type: object
            properties:
              message_id: {type: integer}
              content: {type: string}
              parameters_extracted: {type: object}
              cars_found: {type: array, items: {type: object}}
              requires_clarification: {type: boolean}

GET /chat/dialogs/{dialog_id}/messages:
  summary: Получение истории сообщений
  security:
    - JWT_Token: []
  parameters:
    - name: dialog_id
      in: path
      required: true
      schema: {type: integer}
    - name: limit
      in: query
      schema: {type: integer, default: 50}
  responses:
    200:
      description: История сообщений
```

#### **Поиск автомобилей**
```yaml
GET /cars/search:
  summary: Поиск автомобилей по параметрам
  security:
    - JWT_Token: []
  parameters:
    - name: mark
      in: query
      schema: {type: string}
    - name: body_type
      in: query
      schema: {type: string}
    - name: min_price
      in: query
      schema: {type: integer}
    - name: max_price
      in: query
      schema: {type: integer}
    - name: min_year
      in: query
      schema: {type: integer}
    - name: max_year
      in: query
      schema: {type: integer}
    - name: limit
      in: query
      schema: {type: integer, default: 20}
    - name: offset
      in: query
      schema: {type: integer, default: 0}
  responses:
    200:
      description: Список автомобилей
      content:
        application/json:
          schema:
            type: object
            properties:
              total_count: {type: integer}
              cars: {type: array, items: {$ref: '#/components/schemas/Car'}}


```

### **9.3. WebSocket для реального времени**
```javascript
// Подключение к WebSocket
const ws = new WebSocket('wss://api.car-finder.example.com/v1/ws');

ws.onopen = () => {
  // Аутентификация
  ws.send(JSON.stringify({
    type: 'auth',
    token: 'jwt_token_here'
  }));

  // Отправка сообщения
  ws.send(JSON.stringify({
    type: 'message',
    dialog_id: 123,
    content: 'Ищу красный внедорожник'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);

  switch(data.type) {
    case 'message':
      // Новое сообщение от ассистента
      break;
    case 'typing':
      // Индикатор набора текста
      break;
    case 'search_results':
      // Результаты поиска
      break;
  }
};
```

## **X. СТРАТЕГИЯ ТЕСТИРОВАНИЯ**

### **10.1. Unit-тесты**
```python
# tests/unit/test_parameter_extraction.py
import pytest
from services.llm_orchestrator import ParameterExtractor

class TestParameterExtraction:
    def test_extract_parameters_simple(self):
        extractor = ParameterExtractor()
        result = extractor.extract("Красный внедорожник до 3 миллионов")

        assert result["parameters"]["color"]["value"] == "красный"
        assert result["parameters"]["body_type"]["value"] == "внедорожник"
        assert result["parameters"]["max_price"]["value"] == 3000000
        assert result["total_params_extracted"] == 3

    def test_extract_parameters_complex(self):
        extractor = ParameterExtractor()
        result = extractor.extract(
            "Японский седан с автоматом мощностью от 150 л.с."
        )

        assert result["parameters"]["country"]["value"] == "Япония"
        assert result["parameters"]["transmission_type"]["value"] == "AT"
        assert result["parameters"]["min_power"]["value"] == 150

    @pytest.mark.parametrize("input_text,expected_count", [
        ("Хочу машину", 1),
        ("Автомобиль для семьи", 2),
        ("Немецкий седан с автоматом до 4 млн", 4),
    ])
    def test_parameter_count(self, input_text, expected_count):
        extractor = ParameterExtractor()
        result = extractor.extract(input_text)
        assert result["total_params_extracted"] >= expected_count

# tests/unit/test_search_service.py
class TestSearchService:
    def test_search_with_minimal_parameters(self):
        service = CarSearchService()
        results = service.search({
            "body_type": "внедорожник",
            "max_price": 3000000
        })

        assert len(results) > 0
        for car in results:
            assert car["body_type"] == "внедорожник"
            assert car["base_price"] <= 3000000

    def test_search_ranking(self):
        service = CarSearchService()
        params = {
            "mark": "toyota",
            "body_type": "внедорожник",
            "transmission_type": "AT"
        }

        results = service.search(params)

        # Проверяем что полные совпадения выше
        full_matches = [r for r in results if r["match_score"] > 0.9]
        partial_matches = [r for r in results if r["match_score"] <= 0.9]

        assert len(full_matches) > 0
        if len(partial_matches) > 0:
            assert full_matches[0]["match_score"] > partial_matches[0]["match_score"]
```

### **10.2. Интеграционные тесты**
```python
# tests/integration/test_chat_flow.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestChatFlow:
    @pytest.fixture
    def auth_headers(self):
        # Регистрация и получение токена
        response = client.post("/auth/register", json={
            "email": "test@example.com",
            "password": "Test123!",
            "full_name": "Test User"
        })
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_complete_chat_flow(self, auth_headers):
        # 1. Создание диалога
        response = client.post(
            "/chat/dialogs",
            headers=auth_headers
        )
        dialog_id = response.json()["dialog_id"]

        # 2. Отправка сообщения
        response = client.post(
            f"/chat/dialogs/{dialog_id}/messages",
            headers=auth_headers,
            json={"content": "Красный внедорожник до 3 миллионов"}
        )

        assert response.status_code == 200
        data = response.json()

        # 3. Проверка ответа
        assert "content" in data
        assert "parameters_extracted" in data

        # 4. Получение истории
        response = client.get(
            f"/chat/dialogs/{dialog_id}/messages",
            headers=auth_headers
        )

        assert response.status_code == 200
        messages = response.json()
        assert len(messages) == 2  # Запрос пользователя + ответ ассистента

    def test_lead_creation(self, auth_headers):
        # Поиск автомобиля
        response = client.get(
            "/cars/search?body_type=внедорожник&max_price=3000000",
            headers=auth_headers
        )
        cars = response.json()["cars"]
        car_id = cars[0]["id"]

        # Создание заявки
        response = client.post(
            "/leads",
            headers=auth_headers,
            json={
                "car_id": car_id,
                "contact_preference": "phone",
                "notes": "Интересует тест-драйв"
            }
        )

        assert response.status_code == 201
```

## **XI. ПЛАН ДЕПЛОЯ И CI/CD**

### **11.1. Инфраструктура**
```yaml
# docker-compose.production.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: car_finder
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend
    deploy:
      resources:
        limits:
          memory: 2G

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - backend

  api:
    build:
      context: ./backend
      dockerfile: Dockerfile.production
    environment:
      DATABASE_URL: postgresql://${DB_USER}:${DB_PASSWORD}@postgres/car_finder
      REDIS_URL: redis://:${REDIS_PASSWORD}@redis:6379
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    depends_on:
      - postgres
      - redis
    networks:
      - backend
      - frontend
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 1G

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.production
    environment:
      API_URL: https://api.car-finder.example.com
    networks:
      - frontend
    deploy:
      replicas: 2

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - api
      - frontend
    networks:
      - frontend
      - backend

networks:
  frontend:
  backend:

volumes:
  postgres_data:
  redis_data:
```

### **11.2. Конвейер CI/CD (GitHub Actions)**
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Run unit tests
      run: |
        cd backend
        pytest tests/unit/ -v --cov=app --cov-report=xml

    - name: Run integration tests
      run: |
        cd backend
        pytest tests/integration/ -v

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./backend/coverage.xml

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v3

    - name: Log in to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Build and push backend
      uses: docker/build-push-action@v4
      with:
        context: ./backend
        file: ./backend/Dockerfile.production
        push: true
        tags: |
          ${{ secrets.DOCKER_USERNAME }}/car-finder-backend:latest
          ${{ secrets.DOCKER_USERNAME }}/car-finder-backend:${{ github.sha }}

    - name: Build and push frontend
      uses: docker/build-push-action@v4
      with:
        context: ./frontend
        file: ./frontend/Dockerfile.production
        push: true
        tags: |
          ${{ secrets.DOCKER_USERNAME }}/car-finder-frontend:latest
          ${{ secrets.DOCKER_USERNAME }}/car-finder-frontend:${{ github.sha }}

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest

    steps:
    - name: Deploy to production
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.SSH_HOST }}
        username: ${{ secrets.SSH_USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /opt/car-finder
          docker-compose pull
          docker-compose up -d
          docker system prune -f
```

## **XII. МИГРАЦИИ БАЗЫ ДАННЫХ**

### **12.1. Система миграций с Alembic**
```python
# migrations/versions/001_initial_schema.py
"""initial_schema

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # Таблица users
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('preferences', postgresql.JSONB(), nullable=True),
        sa.Column('search_history', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Таблица cars
    op.create_table('cars',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('mark', sa.String(length=100), nullable=False),
        sa.Column('folder_name', sa.String(length=100), nullable=True),
        sa.Column('model_code', sa.String(length=50), nullable=True),
        sa.Column('body_type', sa.String(length=50), nullable=True),
        sa.Column('engine_capacity', sa.Numeric(precision=3, scale=1), nullable=True),
        sa.Column('engine_power', sa.Integer(), nullable=True),
        sa.Column('transmission_type', sa.String(length=10), nullable=True),
        sa.Column('drive_type', sa.String(length=10), nullable=True),
        sa.Column('fuel_type', sa.String(length=20), nullable=True),
        sa.Column('year_from', sa.Integer(), nullable=True),
        sa.Column('year_to', sa.Integer(), nullable=True),
        sa.Column('country', sa.String(length=50), nullable=True),
        sa.Column('color', sa.String(length=50), nullable=True),
        sa.Column('base_price', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('is_available', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('features', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Индексы для cars
    op.create_index('idx_cars_mark', 'cars', ['mark'])
    op.create_index('idx_cars_body_type', 'cars', ['body_type'])
    op.create_index('idx_cars_engine_power', 'cars', ['engine_power'])
    op.create_index('idx_cars_price', 'cars', ['base_price'])
    op.create_index('idx_cars_year_from', 'cars', ['year_from'])

    # Таблица dialogs
    op.create_table('dialogs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=20), server_default=sa.text("'active'"), nullable=False),
        sa.Column('extracted_params_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column('context', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Таблица messages
    op.create_table('messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dialog_id', sa.Integer(), nullable=False),
        sa.Column('sender_type', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('extraction_result', postgresql.JSONB(), nullable=True),
        sa.Column('is_parsed_successfully', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['dialog_id'], ['dialogs.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Таблица recommendations
    op.create_table('recommendations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dialog_id', sa.Integer(), nullable=False),
        sa.Column('car_id', sa.Integer(), nullable=False),
        sa.Column('relevance_score', sa.Numeric(precision=3, scale=2), nullable=False),
        sa.Column('matched_parameters_count', sa.Integer(), nullable=False),
        sa.Column('match_explanation', postgresql.JSONB(), nullable=True),
        sa.Column('user_feedback', sa.String(length=20), nullable=True),
        sa.Column('presented_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('feedback_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['car_id'], ['cars.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['dialog_id'], ['dialogs.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Индексы для производительности
    op.create_index('idx_dialogs_user_id', 'dialogs', ['user_id'])
    op.create_index('idx_dialogs_status', 'dialogs', ['status'])
    op.create_index('idx_messages_dialog_id', 'messages', ['dialog_id'])
    op.create_index('idx_messages_created_at', 'messages', ['created_at'])
    op.create_index('idx_recommendations_dialog_id', 'recommendations', ['dialog_id'])
    op.create_index('idx_recommendations_score', 'recommendations', ['relevance_score'])


def downgrade():
    op.drop_index('idx_recommendations_score', table_name='recommendations')
    op.drop_index('idx_recommendations_dialog_id', table_name='recommendations')
    op.drop_index('idx_messages_created_at', table_name='messages')
    op.drop_index('idx_messages_dialog_id', table_name='messages')
    op.drop_index('idx_dialogs_status', table_name='dialogs')
    op.drop_index('idx_dialogs_user_id', table_name='dialogs')

    op.drop_table('recommendations')
    op.drop_table('messages')
    op.drop_table('dialogs')

    op.drop_index('idx_cars_year_from', table_name='cars')
    op.drop_index('idx_cars_price', table_name='cars')
    op.drop_index('idx_cars_engine_power', table_name='cars')
    op.drop_index('idx_cars_body_type', table_name='cars')
    op.drop_index('idx_cars_mark', table_name='cars')
    op.drop_table('cars')
    op.drop_table('users')
```

## **XIII. ОБРАБОТКА ОШИБОК И ЛОГИРОВАНИЕ**

### **13.1. Централизованная обработка ошибок**
```python
# middleware/error_handler.py
import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import ValidationError

logger = logging.getLogger(__name__)

def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"Validation error: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "Validation Error",
                "details": exc.errors(),
                "message": "Некорректные данные в запросе"
            }
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.warning(f"HTTP error {exc.status_code}: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "HTTP Error",
                "message": exc.detail
            }
        )

    @app.exception_handler(ValidationError)
    async def pydantic_validation_handler(request: Request, exc: ValidationError):
        logger.error(f"Pydantic validation error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Validation Error",
                "message": "Внутренняя ошибка валидации данных"
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Server Error",
                "message": "Произошла внутренняя ошибка сервера",
                "request_id": request.state.request_id if hasattr(request.state, 'request_id') else None
            }
        )

    @app.exception_handler(TimeoutError)
    async def timeout_exception_handler(request: Request, exc: TimeoutError):
        logger.error(f"Timeout error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            content={
                "error": "Timeout Error",
                "message": "Превышено время ожидания ответа"
            }
        )
```

### **13.2. Настройка логирования**
```python
# config/logging_config.py
import logging
import sys
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import json_log_formatter

class JSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):
        extra['message'] = message
        extra['level'] = record.levelname
        extra['module'] = record.module
        extra['funcName'] = record.funcName
        extra['lineno'] = record.lineno

        if hasattr(record, 'request_id'):
            extra['request_id'] = record.request_id

        if record.exc_info:
            extra['exc_info'] = self.formatException(record.exc_info)

        return extra

def setup_logging():
    # Форматтер для консоли
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Форматтер для файлов (JSON)
    json_formatter = JSONFormatter()

    # Консольный обработчик
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)

    # Файловый обработчик для всех логов
    file_handler = RotatingFileHandler(
        '/var/log/car-finder/app.log',
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=10
    )
    file_handler.setFormatter(json_formatter)
    file_handler.setLevel(logging.INFO)

    # Файловый обработчик для ошибок
    error_handler = TimedRotatingFileHandler(
        '/var/log/car-finder/error.log',
        when='midnight',
        backupCount=30
    )
    error_handler.setFormatter(json_formatter)
    error_handler.setLevel(logging.ERROR)

    # Обработчик для логов запросов
    access_handler = RotatingFileHandler(
        '/var/log/car-finder/access.log',
        maxBytes=10*1024*1024,
        backupCount=10
    )
    access_handler.setFormatter(json_formatter)

    # Настройка логгеров
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)

    # Логгер для доступа
    access_logger = logging.getLogger('uvicorn.access')
    access_logger.addHandler(access_handler)

    # Логгер для LLM запросов
    llm_logger = logging.getLogger('llm')
    llm_file_handler = RotatingFileHandler(
        '/var/log/car-finder/llm.log',
        maxBytes=10*1024*1024,
        backupCount=10
    )
    llm_file_handler.setFormatter(json_formatter)
    llm_logger.addHandler(llm_file_handler)
```

## **XIV. ЛОКАЛИЗАЦИЯ**

### **14.1. Поддержка мультиязычности**
```python
# i18n/locales.py
from typing import Dict
import json
from pathlib import Path

class LocaleManager:
    def __init__(self, locale_dir: str = "locales"):
        self.locale_dir = Path(locale_dir)
        self.locales: Dict[str, Dict] = {}
        self.default_locale = "ru"

        # Загрузка всех локалей
        for locale_file in self.locale_dir.glob("*.json"):
            locale_name = locale_file.stem
            with open(locale_file, 'r', encoding='utf-8') as f:
                self.locales[locale_name] = json.load(f)

    def get_text(self, key: str, locale: str = None, **kwargs) -> str:
        """Получение локализованного текста"""
        locale = locale or self.default_locale

        if locale not in self.locales:
            locale = self.default_locale

        # Поиск по ключу (поддерживает вложенность через точку)
        keys = key.split('.')
        value = self.locales[locale]

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                # Fallback на дефолтную локаль
                if locale != self.default_locale:
                    return self.get_text(key, self.default_locale, **kwargs)
                return key  # Возвращаем ключ, если перевод не найден

        # Подстановка параметров
        if isinstance(value, str) and kwargs:
            return value.format(**kwargs)

        return value

    def get_available_locales(self) -> list:
        """Получение списка доступных локалей"""
        return list(self.locales.keys())

# Файлы локалей
# locales/ru.json
ru_translations = {
    "car_selection": {
        "welcome": "Привет! Я помогу вам подобрать автомобиль.",
        "ask_budget": "Какой бюджет вы рассматриваете?",
        "ask_body_type": "Какой тип кузова предпочитаете?",
        "search_results": "Найдено {count} автомобилей по вашим критериям:",
        "no_results": "По вашим критериям автомобили не найдены."
    },
    "car_parameters": {
        "body_types": {
            "sedan": "седан",
            "suv": "внедорожник",
            "crossover": "кроссовер",
            "hatchback": "хэтчбек",
            "coupe": "купе"
        },
        "transmissions": {
            "AT": "автоматическая",
            "MT": "механическая",
            "CVT": "вариатор"
        },
        "fuel_types": {
            "petrol": "бензин",
            "diesel": "дизель",
            "hybrid": "гибрид"
        }
    },
    "errors": {
        "generic": "Произошла ошибка. Пожалуйста, попробуйте позже.",
        "no_params": "Пожалуйста, укажите больше параметров для поиска."
    }
}

# locales/en.json
en_translations = {
    "car_selection": {
        "welcome": "Hello! I'll help you choose a car.",
        "ask_budget": "What's your budget?",
        "ask_body_type": "What body type do you prefer?",
        "search_results": "Found {count} cars matching your criteria:",
        "no_results": "No cars found matching your criteria."
    },
    "car_parameters": {
        "body_types": {
            "sedan": "sedan",
            "suv": "SUV",
            "crossover": "crossover",
            "hatchback": "hatchback",
            "coupe": "coupe"
        },
        "transmissions": {
            "AT": "automatic",
            "MT": "manual",
            "CVT": "CVT"
        },
        "fuel_types": {
            "petrol": "petrol",
            "diesel": "diesel",
            "hybrid": "hybrid"
        }
    },
    "errors": {
        "generic": "An error occurred. Please try again later.",
        "no_params": "Please provide more parameters for search."
    }
}
```

## **XV. ПЛАН МАСШТАБИРОВАНИЯ**

### **15.1. Горизонтальное масштабирование**
```yaml
# docker-compose.scale.yml
version: '3.8'

services:
  api:
    image: car-finder-api:latest
    deploy:
      mode: replicated
      replicas: 6
      update_config:
        parallelism: 2
        delay: 10s
        order: start-first
      resources:
        limits:
          cpus: '1'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 1G
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      placement:
        constraints:
          - node.role == worker

  postgres:
    image: postgres:15-alpine
    deploy:
      mode: replicated
      replicas: 2
      placement:
        constraints:
          - node.role == manager
    configs:
      - source: postgres_config
        target: /etc/postgresql/postgresql.conf

  redis:
    image: redis:7-alpine
    deploy:
      mode: replicated
      replicas: 3
      placement:
        spread: node.labels.zone

  load_balancer:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    deploy:
      mode: replicated
      replicas: 2
      placement:
        constraints:
          - node.role == manager

configs:
  postgres_config:
    file: ./config/postgres.conf
```

### **15.2. План масштабирования по этапам**

#### **Этап 1: Начальный (до 1000 пользователей в день)**
- 1 сервер приложений
- 1 сервер базы данных
- 1 Redis инстанс
- Мониторинг базовых метрик

#### **Этап 2: Рост (до 10,000 пользователей в день)**
- 3 сервера приложений (балансировка нагрузки)
- Репликация базы данных (master + 2 replicas)
- Redis кластер (3 ноды)
- CDN для статических файлов

#### **Этап 3: Масштаб (до 100,000 пользователей в день)**
- Микросервисная архитектура
- Шардинг базы данных
- Redis кластер (6 нод)
- Геораспределение (2 региона)
- Автоматическое масштабирование

#### **Этап 4: Глобальный (1,000,000+ пользователей в день)**
- Multiple availability zones
- Активная-активная репликация между регионами
- Глобальная балансировка нагрузки
- Специализированные сервисы для LLM, поиска, рекомендаций