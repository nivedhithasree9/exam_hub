import React from 'react'
import { BrowserRouter, Link, Routes, Route } from 'react-router-dom'
import ExamList from './pages/ExamList'
import ExamDetail from './pages/ExamDetail'

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-50">
        <header className="border-b border-slate-200 bg-white">
          <div className="bg-slate-900 text-white">
            <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-2 text-xs sm:px-6">
              <span>Competitive Exam Information Portal</span>
              <span className="hidden text-slate-300 sm:inline">Updated sample guide for students</span>
            </div>
          </div>
          <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-5 sm:px-6">
            <Link to="/" className="flex items-center gap-3">
              <span className="flex h-11 w-11 items-center justify-center rounded bg-amber-500 text-lg font-bold text-slate-950">
                EH
              </span>
              <span>
                <span className="block text-2xl font-bold tracking-normal text-slate-950">Exam Hub</span>
                <span className="block text-sm text-slate-600">Search, compare, and prepare with clarity</span>
              </span>
            </Link>
            <nav className="hidden items-center gap-1 text-sm font-medium text-slate-700 md:flex">
              <Link to="/" className="rounded px-3 py-2 hover:bg-slate-100">All Exams</Link>
              <a href="#categories" className="rounded px-3 py-2 hover:bg-slate-100">Categories</a>
            </nav>
          </div>
        </header>
        <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6">
          <Routes>
            <Route path="/" element={<ExamList />} />
            <Route path="/exam/:id" element={<ExamDetail />} />
          </Routes>
        </main>
        <footer className="mt-8 border-t border-slate-200 bg-white">
          <div className="mx-auto max-w-7xl px-4 py-5 text-sm text-slate-600 sm:px-6">
            Exam Hub provides structured exam guidance. Always verify final dates and rules from the official website.
          </div>
        </footer>
      </div>
    </BrowserRouter>
  )
}
