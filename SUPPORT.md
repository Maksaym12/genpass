# Поддержка проекта GenPass

Этот документ содержит информацию о том, как получить помощь при использовании GenPass.

## Часто задаваемые вопросы (FAQ)

### Общие вопросы

#### Что такое GenPass?
GenPass - это современное приложение для создания криптостойких паролей с интуитивно понятным интерфейсом. Приложение разработано с использованием PyQt5 и предлагает широкий набор функций для генерации и управления паролями.

#### Является ли GenPass бесплатным?
Да, GenPass полностью бесплатен и распространяется под лицензией MIT.

#### На каких операционных системах работает GenPass?
GenPass оптимизирован для работы на Windows 10/11, но также может работать на других операционных системах, где установлен Python и необходимые зависимости.

### Технические вопросы

#### Как работает генерация по мастер-паролю?
Генерация по мастер-паролю использует алгоритм PBKDF2 с 100,000 итераций для создания уникальных 16-символьных паролей на основе мастер-пароля и домена. Это обеспечивает детерминированную генерацию (одинаковые входные данные всегда дают одинаковый пароль) и высокую криптостойкость.

#### Насколько безопасны генерируемые пароли?
Пароли, генерируемые GenPass, используют криптографически стойкий модуль `secrets` вместо стандартного `random`. Это обеспечивает высокую степень случайности и защиту от предсказуемости. Кроме того, приложение гарантирует включение всех выбранных типов символов в пароль.

#### Сохраняет ли GenPass мои пароли?
Нет, GenPass не сохраняет сгенерированные пароли. Все вычисления происходят локально на вашем устройстве, и никакие данные не отправляются в интернет.

## Получение помощи

### Сообщение о проблемах

Если вы столкнулись с проблемой при использовании GenPass:

1. Проверьте раздел [FAQ](#часто-задаваемые-вопросы-faq) выше
2. Просмотрите существующие [Issues](https://github.com/MaksymLeiber/genpass/issues) на GitHub
3. Если ваша проблема не решена, создайте новый Issue с подробным описанием проблемы

### Запрос новых функций

Если вы хотите предложить новую функцию для GenPass:

1. Проверьте, не предлагал ли кто-то уже подобную функцию в [Issues](https://github.com/MaksymLeiber/genpass/issues)
2. Создайте новый Issue с тегом "enhancement" и подробным описанием предлагаемой функции

## Контактная информация

- GitHub: [MaksymLeiber](https://github.com/MaksymLeiber)
- Репозиторий проекта: [GenPass](https://github.com/MaksymLeiber/genpass)

## Дополнительные ресурсы

- [README.md](README.md) - основная информация о проекте
- [CHANGELOG.md](CHANGELOG.md) - история изменений
- [CONTRIBUTING.md](CONTRIBUTING.md) - руководство по внесению вклада в проект
- [LICENSE](LICENSE) - лицензия MIT 