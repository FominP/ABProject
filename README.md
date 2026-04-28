# 📊 AB Test Analyzer & Calculator

> Пет-проект: Python-библиотека для анализа A/B-тестов

## 🧠 Зачем?

Разобраться в статистике A/B-тестирования на практике:
- написать собственную реализацию основных критериев (Z-тест, T-тест, χ², SRM, MDE);
- оформить как библиотеку

## ✨ Возможности библиотеки

| Функция | Что делает |
|---------|-------------|
| `ztest_proportions` | Z-тест для двух пропорций (конверсии) |
| `ttest_means` | T-тест Уэлча для средних (по статистикам) |
| `chi_square_test` | χ²-тест для таблицы 2×2 |
| `check_srm` | Проверка Sample Ratio Mismatch |
| `calculate_mde` | Минимально детектируемый эффект (пропорции) |

Все функции возвращают словарь (`p_value`, `statistic` и пр.).

## 🗂️ Структура репозитория

ABProject/

├── ab_test_analyzer/ # Библиотека (со своим setup.py)

│ ├── init.py

│ ├── core.py # Все статистические функции

│ └── setup.py

├── calculator/ # Flask-калькулятор (код)

│ ├── app.py

│ ├── templates/

│ └── static/

├── tests/ # Модульные тесты (pytest)

│ └── test_core.py

├── requirements.txt # Общие зависимости

├── pytest.ini # Настройки pytest

└── README.md

## 🛠️ Установка и использование

### Локальная установка библиотеки
```bash
pip install ab_test_analyzer
```

### Использование библиотеки напрямую
```python
from ab_test_analyzer.core import ztest_proportions

# Z-тест
res = ztest_proportions(conv_control=200, n_control=1000, conv_test=250, n_test=1000)
print(f"p-value = {res['p_value']:.4f}")

# SRM (ожидаемое соотношение 50/50)
srm = check_srm(users_control=1050, users_test=950)
print(f"SRM p-value = {srm['p_value']:.4f}")
```

## 🤝 Вклад (Contributing)
Проект создан для самообучения, но я буду рад ISSUE или советам по улучшению статистической части.
Если захотите добавить новый тест – форкайте и делайте PR.

## 📄 Лицензия
MIT — делайте что хотите, но ссылку на автора оставьте 😊

Автор: Павел Фомин
GitHub: FominP
Проект создан с ❤️ для изучения статистики и веб-разработки.
