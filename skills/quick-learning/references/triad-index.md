# Triad Index

| # | Trigger | Action | Goal | Scope | Seen | Section |
|---|---------|--------|------|-------|------|---------|
| 1 | tech-spec использует библиотечные методы из code-research | проверить методы по реальной документации до включения в спек | предотвратить propagation миражей code-research → tech-spec → implementation | universal | 1 | Universal |
| 2 | tech-spec для проекта с внешними API | задокументировать error state machine (HTTP код → состояние приложения) в Decisions | предотвратить неоднозначную реализацию error handling разными исполнителями | universal | 1 | Universal |
| 3 | создание нового артефакта | проверить доступность в runtime среде | не объявлять "готово" пока не виден потребителю | universal | 1 | Universal |
| 4 | изменение сигнатуры функции-callback | запустить build до коммита | не ломать deploy из-за type error | universal | 1 | Universal |
| 5 | generic retry decorator оборачивает API-вызов | явно исключить non-retryable exceptions | не ретраить ошибки, которые повторятся всегда | universal | 1 | Universal |
