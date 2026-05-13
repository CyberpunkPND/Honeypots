# 🛡️ Honeypots Infrastructure & Monitoring

Единая инфраструктура для развёртывания honeypot-ов с централизованным сбором логов, агрегацией и визуализацией атак в реальном времени.

## 🏗️ Архитектура

```
Атакующий → [Honeypots] → Docker Logs → [Vector] → [Loki] → [Grafana]
```

### 📦 Стек
| Компонент | Назначение | Образ |
|-----------|------------|-------|
| **Cowrie** | SSH/Telnet honeypot | `cowrie/cowrie:latest` |
| **Dionaea** | Multi-protocol (SMB, HTTP, FTP, MySQL, TFTP) | `dinotools/dionaea-docker:latest` |
| **PyRDP** | RDP MITM & session recording | `gosecure/pyrdp:latest` |
| **PostgreSQL** | Lightweight DB honeypot (0xnslabs) | Custom build |
| **Vector** | Log collection & routing | `timberio/vector:0.48.0-debian` |
| **Loki** | Log aggregation & storage | `grafana/loki:latest` |
| **Grafana** | Dashboards & visualization | `grafana/grafana:latest` |

## 🚀 Быстрый запуск

### 1. Требования
- Docker & Docker Compose v2+
- Свободные порты: `21, 69, 80, 445, 3000, 3100, 3306, 3389, 8081, 2222-2223`

### 2. Запуск
```bash
git clone https://github.com/CyberpunkPND/Honeypots
cd Honeypots
docker compose up -d
```

### 3. Остановка и очистка
```bash
docker compose down
# Опционально: удалить volumes с данными
docker compose down -v
```

## 🌐 Доступные сервисы

| Сервис | URL / Порт | Логин / Пароль |
|--------|------------|----------------|
| **Grafana** | `http://localhost:3000` | `admin` / `27462005Anton+` |
| **Loki API** | `http://localhost:3100` | — |
| **Cowrie SSH** | `ssh -p 2222 root@localhost` | Любой |
| **Cowrie Telnet** | `telnet localhost 2223` | Любой |
| **Dionaea** | `ftp/http/smb/mysql` на `localhost:21/8081/445/3306` | — |
| **PyRDP** | RDP клиент на `localhost:3389` | — |

## ⚙️ Конфигурация

Ханипоты запускаются **out-of-the-box**, но для полноценного мониторинга используются кастомные конфиги:

| Сервис | Конфиг | Назначение |
|--------|--------|------------|
| **Cowrie** | `cowrie/cowrie.cfg` | Баннеры, порты, уровень логирования |
| **Dionaea** | `dionaea/config/log_json.yaml` | Вывод событий подключений в JSON для Vector |
| **PyRDP** | Встроен в `docker-compose.yml` (`command:`) | Параметры MITM-перехвата и вывода |
| **Vector** | `vector.yaml` | Сбор логов из Docker socket → отправка в Loki |
| **Loki** | `loki-config.yaml` | Политики хранения, схемы индексации |

> ⚠️ Runtime-данные (`grafana-data/`, `loki-data/`, `logs/`, `pyrdp_output/`) исключены из Git через `.gitignore`.

## 📊 Мониторинг и логи

Поток данных: `Docker Logs → Vector → Loki → Grafana`.
- **LogQL примеры**:
  ```logql
  {container_name="hp_cowrie"} | json
  {container_name="hp_dionaea"} | json | event_type="connection"
  ```
- Дашборды создаются в Grafana UI или через provisioning.

## ️ Текущий статус и задачи

-  **Dionaea JSON-логи**: Настройка `log_json` ihandler для корректного вывода событий `connection` в `stdout`. Контейнер стабилен, конфиг смонтирован. Требуется финальная валидация синтаксиса и перезапуск.
- 📈 **Grafana Dashboards**: В процессе создания панелей для гео-распределения атак, топ-IP, скачанных артефактов и временных рядов.
- 🛡️ **Безопасность**: Все учётные данные Grafana заменены на дефолтные для учебных целей. В продакшене рекомендуется использовать secrets/vault.

## 📁 Структура проекта

```
honeypots/
├── docker-compose.yml        # Оркестрация всех сервисов
├── vector.yaml               # Конфиг сбора и маршрутизации логов
├── loki-config.yaml          # Конфиг агрегатора логов
├── cowrie/cowrie.cfg         # Конфиг SSH/Telnet honeypot
├── dionaea/config/           # Конфиги Dionaea (вкл. log_json.yaml)
├── postgresql-honeypot/      # Исходный код PG honeypot
└── README.md                 # Документация
```

## 👤 Автор
**CyberpunkPND**  
🔗 [GitHub Profile](https://github.com/CyberpunkPND)

## 📜 Лицензия
MIT License
