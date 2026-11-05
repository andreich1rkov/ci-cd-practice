# ci-cd-practice

Маленькое учебное приложение (Flask) для практики по CI/CD.

![CI](https://github.com/<ВАШ_ЛОГИН>/ci-cd-practice/actions/workflows/ci.yml/badge.svg)

## Запуск локально

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
pytest -v                        # тесты
python app.py                    # приложение: http://localhost:5000
```
