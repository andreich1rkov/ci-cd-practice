from flask import Flask, jsonify

app = Flask(__name__)


def add(a: int, b: int) -> int:
    """Складывает два числа. Простая функция - её удобно покрывать тестами."""
    return a + b


@app.get("/")
def index():
    return jsonify(message="Hello, CI/CD!")


@app.get("/health")
def health():
    # Эндпоинт "жив ли сервис" - пригодится позже для Docker и Kubernetes
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
