# Triad Index

Unified index of all methodology knowledge — reasoning patterns and operational lessons.
One line per unique triad. Source of truth for similarity matching and Seen counters.

| # | Trigger | Action | Goal | Scope | Seen | Section |
|---|---------|--------|------|-------|------|---------|
| 1 | создание нового артефакта | проверить доступность в runtime среде | не объявлять "готово" пока не виден потребителю | universal | 1 | Universal |
| 2 | изменение сигнатуры функции-callback | запустить build до коммита | не ломать deploy из-за type error | universal | 2 | Universal |
| 3 | generic retry decorator оборачивает API-вызов | явно исключить non-retryable exceptions | не ретраить ошибки, которые повторятся всегда | universal | 1 | Universal |
| 4 | tech-spec использует библиотечные методы из code-research | проверить методы по реальной документации до включения в спек | предотвратить propagation миражей code-research → tech-spec → implementation | universal | 1 | Universal |
| 5 | tech-spec для проекта с внешними API | задокументировать error state machine в Decisions | предотвратить неоднозначную реализацию error handling | universal | 1 | Universal |
| 6 | post-deploy verification с пользователем | планировать 2-4 итерации UX-правок как норму | не считать UX-корректировки проблемой процесса | universal | 1 | Universal |
| 7 | генерация задач из tech-spec | проверять каждый путь через test -e, валидировать depends_on | предотвратить задачи с несуществующими файлами | universal | 1 | Universal |
| 8 | AC для markdown-only фич | формулировать через наличие конкретных артефактов | сделать AC автоматически проверяемыми | universal | 1 | Universal |
| 9 | audit-агенты сообщают о невозможности записи | lead сразу записывает результаты сам | не терять время на повторные попытки агента | situational | 1 | Situational |
| 10 | ревью нашло паттерн ошибки (не разовый баг) | добавить предупреждение в промт следующего teammate | предотвратить повторение ошибки в следующих задачах | situational | 1 | Situational |
| 11 | написание тестов в multi-agent workflow | требовать assertion на результат функции, не только на mock | тесты ловят баги, а не проверяют форму вызова | situational | 1 | Situational |
| 12 | security/code audit в multi-task feature | вести known-issues.md, аудитор читает перед ревью | не тратить время на повторный репорт известных проблем | situational | 1 | Situational |
