# Exam Hub — Competitive Exam Preparation Portal

This repository contains a full-stack project scaffold for an Indian competitive exam preparation portal.

Structure:

- client — React + Vite + Tailwind frontend
- server — Express backend
- models — Sequelize models (MySQL)
- routes — API routes
- controllers — business logic

Quick start:

1. Backend (MySQL)

```
cd server
npm install
copy .env.example .env
# edit .env to set MYSQL_URI or MySQL connection details
npm run seed
npm run dev
```

2. Frontend

```
cd client
npm install
npm run dev
```

The frontend proxies API requests to `http://localhost:5000/api`.

Features implemented:
- Exam listing with search and category filter
- Exam detail page showing syllabus, pattern, dates, books, PYQs
- REST API with CRUD endpoints
 - MySQL seed script (2020–2025 PYQs provided in sample data)
- Tailwind styling and responsive layout

Next steps: run backend + frontend and open http://localhost:3000
