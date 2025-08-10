# FastAPI do Zero 🚀 #

Bem-vindo ao repositório de estudos e execução do curso **FastAPI do Zero**, ministrado por [Dunossauro](https://github.com/dunossauro)!

O curso está disponível em: [https://fastapidozero.dunossauro.com/estavel/](https://fastapidozero.dunossauro.com/estavel/)

---

## Estrutura do Repositório

Este repositório contém o código desenvolvido durante as aulas do curso, organizado por branches conforme o progresso das aulas.

### 📚 Conteúdo das Aulas

#### 🔧 Aula 1 - Configurando o Ambiente de Desenvolvimento
- **Material:** [Aula 1 - Configuração do Ambiente](https://fastapidozero.dunossauro.com/estavel/01/)
- **Status:** ✅ **COMPLETA**

**Implementações realizadas:**
- ✅ **Ambiente de desenvolvimento:** Python 3.13, Git configurados
- ✅ **Gerenciador de pacotes:** UV (moderno substituto do Poetry)
- ✅ **Estrutura do projeto:** Layout flat com fast_zero/ criado
- ✅ **FastAPI:** Instalado com `[standard]` extras
- ✅ **Ferramentas de desenvolvimento:**
  - pytest (testes) e pytest-cov (cobertura)
  - ruff (linting e formatação)
  - taskipy (automação de tarefas)
- ✅ **Configurações:**
  - Ruff: line-length 79, aspas simples, regras I/F/E/W/PL/PT
  - Pytest: pythonpath configurado, warnings suprimidos
  - Taskipy: comandos lint, format, run, test com pré/pós hooks
- ✅ **Hello World:** Endpoint `/` implementado e funcionando
- ✅ **Primeiro teste:** Estrutura AAA (Arrange-Act-Assert)
- ✅ **Cobertura de testes:** 100% alcançada
- ✅ **Git:** Repositório inicializado com .gitignore
- ✅ **Exercícios da aula:** Todos implementados

#### 🌐 Aula 2 - Introdução ao Desenvolvimento WEB
- **Material:** [Aula 2 - Introdução ao Desenvolvimento WEB](https://fastapidozero.dunossauro.com/estavel/02/)
- **Status:** ✅ **COMPLETA**

**Implementações realizadas:**
- ✅ **Conceitos Web:** Cliente-servidor, URLs, HTTP compreendidos
- ✅ **Protocolo HTTP:**
  - Verbos GET/POST/PUT/DELETE implementados
  - Status codes com HTTPStatus (boas práticas)
  - Cabeçalhos e corpo de mensagens
- ✅ **APIs e JSON:**
  - Endpoint `/` retornando JSON
  - Contratos de dados com schemas
- ✅ **Pydantic integrado:**
  - Schema `Message` criado e utilizado
  - `response_model` configurado nos endpoints
- ✅ **Documentação OpenAPI:**
  - Swagger UI disponível em `/docs`
  - ReDoc disponível em `/redoc`
  - Schemas documentados automaticamente
- ✅ **Endpoint HTML:** `/html` com HTMLResponse
- ✅ **Testes completos:**
  - Teste do endpoint JSON (`test_root_deve_retornar_ok_e_ola_mundo`)
  - Teste do endpoint HTML (`test_root_html_deve_retornar_ok_e_ola_mundo`)
- ✅ **Exercício da aula:** Endpoint HTML implementado e testado

#### 📝 Aula 3 - Estruturando o Projeto e Criando Rotas CRUD
- **Material:** [Aula 3 - Estruturando o Projeto e Criando Rotas CRUD](https://fastapidozero.dunossauro.com/estavel/03/)
- **Status:** ✅ **COMPLETA**

**Implementações realizadas:**
- ✅ **Sistema CRUD completo:**
  - POST `/users/` para criar usuários
  - GET `/users/` para listar usuários
  - PUT `/users/{user_id}` para atualizar usuários
  - DELETE `/users/{user_id}` para remover usuários
  - GET `/users/{user_id}` para buscar usuário específico
- ✅ **Modelos de dados:**
  - UserSchema: modelo de entrada
  - UserPublic: modelo de saída
  - UserDB: modelo do banco
  - UserList: modelo para listagem
- ✅ **Validações:**
  - Email com EmailStr
  - Campos obrigatórios
  - Respostas HTTP adequadas
- ✅ **Testes:**
  - Cobertura 100%
  - Fixture de cliente de teste
  - Testes de sucesso e erro
- ✅ **Exercícios da aula:** Todos implementados

#### 🗄️ Aula 4 - Banco de Dados e Migrações
- **Material:** [Aula 4 - Banco de Dados e Migrações](https://fastapidozero.dunossauro.com/estavel/04/)
- **Status:** ✅ **COMPLETA**

**Implementações realizadas:**
- ✅ **SQLAlchemy configurado:**
  - Modelos com Mapped columns
  - Registro de tabelas com registry
  - Tipos de dados apropriados
- ✅ **Modelo User aprimorado:**
  - Campos únicos (email, username)
  - Campos automáticos (id, created_at, updated_at)
  - Configurações de colunas otimizadas
- ✅ **Ambiente de banco:**
  - Settings com pydantic-settings
  - Configuração via .env
  - URL do banco configurável
- ✅ **Alembic configurado:**
  - Inicialização correta
  - Migração inicial criada
  - Migração para novos campos
- ✅ **Testes do banco:**
  - Fixture de sessão SQLite em memória
  - Mock de tempo para testes determinísticos
  - Validação completa de objetos
- ✅ **Exercícios da aula:** Todos implementados
  - Campo updated_at adicionado
  - Eventos ORM configurados
  - Testes adaptados

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.13+
- UV (gerenciador de pacotes moderno para Python)

### Setup do Projeto

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd fast_zero
   ```

2. **Instale as dependências:**
   ```bash
   uv sync
   ```

3. **Execute os testes:**
   ```bash
   uv run pytest -s -x --cov=fast_zero -vv
   ```

4. **Execute o linting:**
   ```bash
   uv run ruff check
   ```

5. **Formate o código:**
   ```bash
   uv run ruff format
   ```

6. **Execute a aplicação:**
   ```bash
   uv run fastapi dev fast_zero/app.py
   ```

### 📊 Status dos Testes
- **Cobertura:** 100%
- **Total de testes:** 10
- **Status:** ✅ Todos passando

### 📖 Documentação da API
Com a aplicação rodando, acesse:
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

---

## Como utilizar este repositório

## 📋 Como utilizar este repositório

### Navegação por Aulas
- **Aula 1-3:** Código atual (main branch)
- Para aulas futuras, branches específicas serão criadas

### Comandos Úteis

**Usando UV (recomendado):**
```bash
# Instalar dependências
uv sync

# Executar testes
uv run pytest -s -x --cov=fast_zero -vv

# Executar aplicação
uv run fastapi dev fast_zero/app.py

# Linting
uv run ruff check

# Formatação
uv run ruff format
```

**Usando taskipy (alternativo):**
```bash
# Executar testes
uv run task test

# Executar aplicação  
uv run task run

# Linting
uv run task lint

# Formatação
uv run task format
```

---

## Sobre o Curso

O curso **FastAPI do Zero** aborda desde a configuração do ambiente até a construção de APIs completas utilizando FastAPI, com explicações detalhadas e exemplos práticos.

Acesse o conteúdo completo em: [https://fastapidozero.dunossauro.com/estavel/](https://fastapidozero.dunossauro.com/estavel/)

---

> **Autor do curso:** [Dunossauro](https://github.com/dunossauro)

> **Repositório mantido por:** [Fábio Belotto](https://github.com/frbelotto)

---

Sinta-se à vontade para contribuir ou utilizar este material para seus estudos!