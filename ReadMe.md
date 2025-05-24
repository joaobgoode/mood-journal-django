
# 📘 Documentação da API - Mood Journal

Esta documentação descreve como o frontend (Vue) deve interagir com o backend (Django).

**URL Base da API:** `http://127.0.0.1:8000/api/` (ambiente de desenvolvimento)

---

## 🔐 Conceitos Gerais

### Autenticação JWT (JSON Web Token)

A maioria das rotas é protegida e exige autenticação via token JWT.

#### Fluxo de Autenticação

1. O usuário se registra (`/register/`) ou faz login (`/token/`).
2. Em caso de sucesso no login, o backend retorna dois tokens: `access` e `refresh`.
3. O frontend deve armazenar esses tokens de forma segura (ex: `localStorage` ou `sessionStorage`).
4. Para rotas protegidas, envie o token de acesso no cabeçalho da requisição:

```
Authorization: Bearer <seu_access_token>
```

5. O token `access` expira após 60 minutos.
6. Quando expirar, use o token `refresh` para obter um novo `access` token via `/token/refresh/`.

---

### Tipos de Conteúdo

Requisições que enviam dados (POST, PUT, PATCH) devem incluir o cabeçalho:

```
Content-Type: application/json
```

---

## 👤 Autenticação e Usuários

### 1. Registrar um Novo Usuário

- **Método:** `POST`
- **URL:** `/api/register/`
- **Autenticação:** ❌ Não requer

**Body:**
```json
{
  "username": "novo_usuario",
  "email": "usuario@exemplo.com",
  "password": "uma_senha_forte_123",
  "password2": "uma_senha_forte_123",
  "first_name": "Nome",
  "last_name": "Sobrenome"
}
```

**Resposta 201 (Criado):**
```json
{
  "id": 1,
  "username": "novo_usuario",
  "email": "usuario@exemplo.com",
  "first_name": "Nome",
  "last_name": "Sobrenome"
}
```

**Resposta 400 (Erro):**
```json
{
  "username": ["A user with that username already exists."]
}
```

---

### 2. Login (Obter Tokens)

- **Método:** `POST`
- **URL:** `/api/token/`
- **Autenticação:** ❌ Não requer

**Body:**
```json
{
  "username": "novo_usuario",
  "password": "uma_senha_forte_123"
}
```

**Resposta 200 (OK):**
```json
{
  "refresh": "eyJhbGciOiJIUz...<token_de_refresh>",
  "access": "eyJhbGciOiJIUz...<token_de_acesso>"
}
```

**Resposta 401 (Erro):**
```json
{
  "detail": "No active account found with the given credentials"
}
```

---

### 3. Atualizar Token de Acesso

- **Método:** `POST`
- **URL:** `/api/token/refresh/`
- **Autenticação:** ❌ Não requer

**Body:**
```json
{
  "refresh": "<seu_token_de_refresh>"
}
```

**Resposta 200 (OK):**
```json
{
  "access": "eyJhbGciOiJIUz...<novo_token_de_acesso>"
}
```

---

## 😊 Humores Padrão (Default Moods)

### Listar Todos os Humores

- **Método:** `GET`
- **URL:** `/api/default-moods/`
- **Autenticação:** ❌ Não requer

**Resposta 200 (OK):**
```json
[
  {
    "id": 1,
    "name": "Feliz",
    "description": "Sentindo-se bem e positivo.",
    "image": "https://public.seu-bucket.dev/media/mood_images/happy.png"
  },
  {
    "id": 2,
    "name": "Triste",
    "description": "Sentindo-se para baixo.",
    "image": "https://public.seu-bucket.dev/media/mood_images/sad.png"
  }
]
```

---

## 📅 Entradas de Humor (Moods)

> Todas as rotas abaixo **requerem autenticação**.

### 1. Criar uma Nova Entrada

- **Método:** `POST`
- **URL:** `/api/moods/`

**Headers:**
```
Authorization: Bearer <seu_access_token>
Content-Type: application/json
```

**Body:**
```json
{
  "mood_id": 1,
  "entry_date": "2025-05-23",
  "description": "Tive um ótimo dia no trabalho hoje!"
}
```

**Resposta 201 (Criado):**
```json
{
  "id": 10,
  "user": { "...": "..." },
  "mood": { "...": "..." },
  "description": "Tive um ótimo dia no trabalho hoje!",
  "entry_date": "2025-05-23",
  "created_at": "2025-05-23T13:30:00Z",
  "updated_at": "2025-05-23T13:30:00Z"
}
```

---

### 2. Listar Entradas do Mês

- **Método:** `GET`
- **URL:** `/api/moods/?month=5&year=2025`

**Headers:**
```
Authorization: Bearer <seu_access_token>
```

**Resposta 200 (OK):**
```json
[
  {
    "id": 10,
    "user": { "...": "..." },
    "mood": { "...": "..." },
    "description": "Tive um ótimo dia no trabalho hoje!",
    "entry_date": "2025-05-23"
  },
  {
    "id": 9,
    "user": { "...": "..." },
    "mood": { "...": "..." },
    "description": "Dia um pouco estressante.",
    "entry_date": "2025-05-21"
  }
]
```

---

### 3. Obter / Atualizar / Deletar Entrada

**Base URL:** `/api/moods/{id}/`

#### Obter (GET)
- Retorna uma entrada específica

#### Atualizar (PUT)
```json
{
  "mood_id": 2,
  "entry_date": "2025-05-23",
  "description": "Na verdade, o dia foi mais ou menos."
}
```

#### Atualizar parcialmente (PATCH)
```json
{
  "description": "A descrição foi atualizada."
}
```

#### Deletar (DELETE)
- Resposta: `204 No Content`

---

## ⚠️ Formatos de Erro Comuns

| Código | Significado | Exemplo |
|--------|-------------|---------|
| 400    | Requisição malformada | `{"entry_date": ["Já existe uma entrada de humor para esta data."]}` |
| 401    | Token ausente ou inválido | `{"detail": "Authentication credentials were not provided."}` |
| 403    | Sem permissão | `{"detail": "You do not have permission to perform this action."}` |
| 404    | Recurso não encontrado | `{"detail": "Not found."}` |
