## Table of Contents

1. [Overview](#overview)
2. [Tech Stack](#tech-stack)
   - [Backend](#backend)
   - [Frontend](#frontend)
3. [Repository Structure](#repository-structure)
4. [Code Structure (Core Components)](#code-structure-core-components)
   - [Backend](#backend-1)
   - [Frontend](#frontend-1)
5. [Running The App](#running-the-app)
   - [Prerequisite](#prerequisite)
   - [Seeding The Application With CVs](#seeding-the-application-with-cvs)
   - [Running the Backend](#running-the-backend)
   - [Run Frontend](#run-frontend)
6. [Running The Tests](#running-the-tests)
   - [Backend](#backend-2)
   - [Frontend](#frontend-2)
7. [CV Screening Algorithm](#cv-screening-algorithm)
8. [Improvements To Be Done If I Had More Time](#improvements-to-be-done-if-i-had-more-time)

## Overview

This application helps users screen applicants from a collection of CVs by allowing them to ask questions about candidates in the pool.
Users are provided with an interactive conversational interface for exploring and evaluating candidates from the CV pool.

## Tech Stack

### Backend

- Programming Language: Python
- API Framework: FastAPI
- LLM: Gemini (Used for embeddings and LLM processing)
- Data Store: ChromaDB (Used to Store Embeddings)

### Frontend

- Programming Language: TypeScript
- Framework: React
- UI Library: Chakra UI

## Repository Structure

```text
.
├── README.md
├── backend/
│   ├── .dockerignore
│   ├── .env
│   ├── .env.example
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── app/
│   │   ├── api/
│   │   │   ├── router.py
│   │   │   └── routes/
│   │   │       └── search.py
│   │   ├── config.py
│   │   ├── cv_ingestion/
│   │   │   ├── chunker.py
│   │   │   ├── cv_text_extractor.py
│   │   │   └── ingest.py
│   │   ├── schemas/
│   │   │   └── search.py
│   │   ├── services/
│   │   │   └── search_service.py
│   │   ├── storage/
│   │   │   └── vector_store.py
│   │   └── utils/
│   │       ├── embeddings.py
│   │       ├── llm.py
│   │       ├── prompts.py
│   │       └── rate_limit.py
│   └── requirements.txt
└── frontend/
    ├── .env.example
    ├── package.json
    ├── src/
    │   ├── App.tsx
    │   ├── context/
    │   ├── env/
    │   ├── hooks/
    │   ├── lib/
    │   ├── pages/
    │   │   └── Home/
    │   │       ├── ConversationPanel.tsx
    │   │       ├── MessageBubble.tsx
    │   │       ├── MessagesPanel.tsx
    │   │       ├── QuestionInput.tsx
    │   │       ├── TypingIndicator.tsx
    │   │       ├── index.tsx
    │   │       └── messages.ts
    │   ├── services/
    │   ├── types/
    │   └── main.tsx
    └── vite.config.ts
```

## Code Structure (Core Components)

### Backend

These are the core components of the backend:

- `cv_ingestion`: A folder in the application that contains a script (`ingest.py`) used to seed the application with the fake CV PDFs. The script extracts text from each PDF, chunks the content, generates embeddings, and stores the chunks in ChromaDB with useful metadata.
- `ChromaDB` is a vector database used to store and search embeddings. The system uses it to store generated embeddings alongside metadata that identifies a text chunk of a particular CV.
- API Endpoints
  - `POST /search` accepts a request body containing a query property and an optional chat_history property. It searches the CV collection for information that best answers the query and returns the most relevant answer.

  Example request:

  ```json
  {
    "query": "Who has Python experience?",
    "chat_history": []
  }
  ```

  Example response:

  ```json
  {
    "response": "The following candidates have Python experience: ..."
  }
  ```

### Frontend

The frontend is a single-page React application built with Chakra UI. It uses a small Context API state container for conversation state, and the Home page is the only page in the app.

- `Home` renders the full chat experience.
- The page shows the title, description, conversation history, loading state, error state, and the question input area.
- The UI supports follow-up questions by keeping prior messages in frontend state and sending them with each request.

## Running The App

### Prerequisite

The app runs with Docker and Docker Compose.

If you do not have Docker installed, you can install it via [Docker Desktop](https://docs.docker.com/get-started/introduction/get-docker-desktop/) or [OrbStack](https://orbstack.dev/). OrbStack only works on MacBook.

### Seeding The Application With CVs

Before running the app, a collection of CVs must first be seeded into the system.
Execute the steps below to seed the system with a collection of cvs.

1. Create a folder that contains the CV PDFs you want to seed the system with.
2. Make sure each CV PDF is named after the applicant, for example `jane_doe.pdf`.
3. Move into the `backend/` directory.
4. Run the ingestion command:

```bash
docker compose run --rm -v "$(pwd)/${resume_folder_path}:/app/data/cvs" api python -m app.cv_ingestion.ingest
```

Replace `${resume_folder_path}` with the folder that contains your CV PDFs.

### Running the Backend

From the `backend/` directory:

1. Ensure `backend/.env` exists and contains your `GOOGLE_API_KEY`.
2. Start the backend container:

```bash
docker compose up --build
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

The API endpoint is:

```text
POST /search
```

### Run Frontend

From the `frontend/` directory:

1. Install dependencies:

```bash
npm install
```

2. Start the development server:

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

## Running The Tests

### Backend

From the `backend/` directory:

```bash
docker compose run --rm tests
```

### Frontend

From the `frontend/` directory:

```bash
npm test
```

## CV Screening Algorithm

The backend uses a retrieval-augmented generation (RAG) flow to answer questions about the CV collection.

1. When seeding the application with generated CVs, the backend extracts text from all CV PDFs and breaks the text into small chunks.
2. Each chunk is converted into an embedding using the Gemini LLM.
3. The embeddings are stored in ChromaDB together with metadata that identifies each chunk, such as the file name, page number, and chunk index.
4. When the backend receives a question, it first converts the question text into an embedding.
5. That question embedding is used to find the closest matching CV chunks from ChromaDB.
6. The matching chunks are sent to the Gemini LLM to generate a response for the user.
7. If the user asks a follow-up question, the backend first asks Gemini to rewrite the follow-up into a new standalone question that captures the full context of the conversation.
8. The rewritten question is then converted into an embedding and used to search ChromaDB for the most relevant CV chunks before generating the final response.

## Improvements To Be Done If I Had More Time

1. Add end-to-end test cases with Cypress for the full application flow.
2. Replace ChromaDB with a proper database like MySQL to store the embeddings of the resumes.
3. Improve the embeddings retrieval process to generate fewer chunks with more context so qualified applicants do not slip through search queries.
4. Store the conversation history in the database instead of sending it from the frontend.
5. Use techniques to compact conversation history when it becomes too long and exceeds the token limit.
6. Add project-specific Skills to document the backend workflow and make onboarding easier for new developers.
