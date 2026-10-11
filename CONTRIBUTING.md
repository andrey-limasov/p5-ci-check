# Правила работы в команде

## Git-стратегия

Мы используем **GitHub Flow** (решение — [ADR 001](docs/adr/001-branching-strategy.md)): одна долгоживущая ветка `main`, каждое изменение — короткая ветка от `main` и Pull Request обратно в `main`.

```
main:   ●────────────●────────────●──────
         \          /  \         /
          ●───●────●    ●───●───●
        feature/version-   docs/contributing-
        endpoint           rules
```

Фича ответвляется от свежего `main` и вливается в `main` только через PR с approval.

### Ветвление
- `main` — стабильная версия, прямой push запрещён (см. «Защита ветки»)
- Шаблон имени: `<тип>/<кратко-через-дефис>`, тип — `feature`, `bugfix`, `docs`, `chore`
- `feature/<кратко>` — новые функции: `feature/version-endpoint`, `feature/tickets-crud`
- `bugfix/<кратко>` — исправление ошибок: `bugfix/health-status-code`
- `docs/<кратко>` — только документация: `docs/pr-template`, `docs/contributing-rules`
- `chore/<кратко>` — зависимости и конфигурация: `chore/dependency-files`

### Коммиты
Используем [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` новая функция
- `fix:` исправление бага
- `docs:` изменения в документации
- `style:` форматирование кода
- `refactor:` рефакторинг
- `test:` добавление тестов
- `chore:` рутинные задачи

Примеры из нашего репозитория:
- `feat: add initial FastAPI application with health check`
- `docs: describe API endpoints in README`

## Code Review

### Регламент code review

- Ревьюер назначается автором PR при создании, из числа участников команды
- Автор PR не может одобрить собственный PR — approval всегда ставит другой участник
- Срок первого ответа ревьюера: 24 часа с момента создания PR
- Автор отвечает на каждый комментарий: правкой либо аргументом, почему правка не нужна
- Комментарий сокомандника закрывает (Resolve) тот, кто его оставил
- Комментарий ревьюера другой команды закрывает автор PR — после ответа ревьюера в том же обсуждении («исправлено, принимаю») или его Approve: у ревьюера без права записи кнопки Resolve нет
- Два круга «Request changes» без сближения позиций — вопрос выносится на встречу команды

### Критерии approval

Ревьюер ставит Approve, только если выполнено всё:

1. Чек-лист автора в PR заполнен полностью
2. Ветка названа по шаблону из раздела «Ветвление»
3. Все коммиты в PR начинаются с типа Conventional Commits
4. В diff нет `.env`, ключей, паролей, токенов
5. Локальный запуск по инструкции из раздела «Как проверить» даёт описанный результат
6. Все комментарии предыдущих кругов ревью отвечены и закрыты

Если хотя бы один пункт не выполнен — Request changes с указанием номера пункта.

### Разрешение конфликтов в коде

GitHub пишет `This branch has conflicts that must be resolved` — в базовую ветку попал чужой PR.

```bash
git checkout <ваша-ветка>
git fetch origin
git merge origin/main
```

В файлах из сообщения git найти блоки `<<<<<<<`, `=======`, `>>>>>>>`, оставить нужный вариант
(часто — оба фрагмента подряд), удалить маркеры. Затем:

```bash
git add <файл>
git commit -m "chore: resolve merge conflict with main"
git push
```

Approval после этого сбрасывается (`Dismiss stale approvals`): нажать **Re-request review**.
Конфликт не решается через `git push --force` — он ломает привязку комментариев ревью.

## Защита ветки

Ruleset `protect-main` (Settings → Rules → Rulesets), `Active`, Bypass list пуст, цель — default branch (`main`). Настраивает и меняет только владелец (@ivan-petrov).

Включено:
- Restrict deletions
- Block force pushes
- Require a pull request before merging: Required approvals — **1**; Dismiss stale pull request approvals when new commits are pushed; Require conversation resolution before merging

Выключено: Require status checks to pass (CI ещё нет), Require linear history.

Settings → General → Pull Requests: Automatically delete head branches — включено.

`Restrict deletions` включено; на default-ветке экспериментом не проверяется.

Проверка «на отказ» (практика №2, 2026-10-11), прямой push:

```
remote: error: GH013: Repository rule violations found for refs/heads/main.
remote: - Changes must be made through a pull request.
 ! [remote rejected] main -> main
```

Force-push:

```
remote: error: GH013: Repository rule violations found for refs/heads/main.
remote: - Cannot force-push to this branch
remote: - Changes must be made through a pull request.
```

Временное отключение защиты (`Disabled` и сразу обратно) записывается здесь: кто, когда, зачем. Записей нет.

> TODO (модуль 3, практика №5): после появления CI-пайплайна включить в ruleset `protect-main`
> правило «Require status checks to pass» и добавить в список обязательных проверок джобы
> линтера и тестов. До этого момента зелёный пайплайн не является условием merge.

## Как запустить тесты

TODO (модуль 3): тестов пока нет, раздел появится вместе с ними

## Встречи команды

- Частота: 2 раза в неделю (вторник и пятница, 18:00)
- Канал связи: Telegram, https://t.me/+repair-requests-team
- Время ответа на сообщения: в течение 24 часов

## Разрешение конфликтов

1. Обсуждение в команде
2. Голосование (большинство голосов)
3. Если не можем решить — обращаемся к преподавателю

## Контакты

Канал команды: Telegram, https://t.me/+repair-requests-team. Время ответа — в течение 24 часов, ревью PR — 24 часа.

- Иван Петров — тимлид, владелец репозитория (настройки и защита веток), Telegram @ivan_petrov, GitHub @ivan-petrov
- Мария Соколова — Tech Lead, Telegram @maria_sokolova, GitHub @maria-sokolova
- Олег Ким — разработчик, Telegram @oleg_kim, GitHub @oleg-kim
