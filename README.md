# Golden Raspberry API

Esta API RESTful foi desenvolvida em Python usando FastAPI, com base no Nível 2 do Modelo de Maturidade de Richardson.
Ela processa uma lista de filmes da categoria *Pior Filme* do Golden Raspberry Awards e retorna produtores com maiores e menores intervalos entre prêmios consecutivos.

---

## 📊 Requisitos

- Python 3.9+
- pip (gerenciador de pacotes do Python)

---

## 🚀 Como executar o projeto

1. Clone ou baixe o repositório.

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute o servidor com:

```bash
uvicorn movies:app --reload
```

5. Acesse no navegador:

```
http://127.0.0.1:8000/producers/intervals
```

6. A documentação interativa da API estará disponível em:

```
http://127.0.0.1:8000/docs
```

---

## 🔧 Executando os testes de integração

Execute:

```bash
python -m pytest -v
```

---

## 📂 Tecnologias Utilizadas

- FastAPI
- SQLite
- SQLAlchemy
- Pytest
