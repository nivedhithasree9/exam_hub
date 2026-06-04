import React, { useEffect, useState } from 'react'
import api from '../api'
import ExamCard from '../components/ExamCard'

export default function ExamList() {
  const [exams, setExams] = useState([])
  const [q, setQ] = useState('')
  const [category, setCategory] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    fetchExams()
  }, [])

  async function fetchExams() {
    try {
      const res = await api.get('/exams')
      setExams(res.data)
    } catch (err) {
      setError('Unable to load exams. Please check that the backend server is running.')
    }
  }

  const filtered = exams.filter(e => e.name.toLowerCase().includes(q.toLowerCase()) && (category ? e.category === category : true))

  const categories = Array.from(new Set(exams.map(e => e.category).filter(Boolean)))

  return (
    <div className="space-y-6">
      <section className="border border-slate-200 bg-white p-6 shadow-sm">
        <div className="grid gap-6 lg:grid-cols-[1fr_320px] lg:items-end">
          <div>
            <p className="text-sm font-semibold uppercase tracking-normal text-amber-700">Student exam directory</p>
            <h1 className="mt-2 text-3xl font-bold leading-tight text-slate-950">Find complete exam information in one place</h1>
            <p className="mt-3 max-w-3xl leading-7 text-slate-600">
              Explore eligibility, syllabus, pattern, dates, preparation resources, and official links for major Indian competitive exams.
            </p>
          </div>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div className="border border-slate-200 bg-slate-50 p-4">
              <p className="text-2xl font-bold text-slate-950">{exams.length}</p>
              <p className="mt-1 text-slate-600">Exams listed</p>
            </div>
            <div className="border border-slate-200 bg-slate-50 p-4">
              <p className="text-2xl font-bold text-slate-950">{categories.length}</p>
              <p className="mt-1 text-slate-600">Categories</p>
            </div>
          </div>
        </div>
      </section>

      <section id="categories" className="border border-slate-200 bg-white p-5 shadow-sm">
        <div className="grid gap-3 md:grid-cols-[1fr_220px]">
          <label className="block">
            <span className="mb-1 block text-sm font-semibold text-slate-800">Search exams</span>
            <input
              value={q}
              onChange={e => setQ(e.target.value)}
              placeholder="Search by exam name, for example NEET or UPSC"
              className="w-full rounded border border-slate-300 px-3 py-2.5 text-slate-900 outline-none focus:border-slate-700 focus:ring-2 focus:ring-slate-200"
            />
          </label>
          <label className="block">
            <span className="mb-1 block text-sm font-semibold text-slate-800">Category</span>
            <select
              value={category}
              onChange={e => setCategory(e.target.value)}
              className="w-full rounded border border-slate-300 px-3 py-2.5 text-slate-900 outline-none focus:border-slate-700 focus:ring-2 focus:ring-slate-200"
            >
              <option value="">All categories</option>
              {categories.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </label>
        </div>
      </section>

      {error && (
        <div className="border border-red-200 bg-red-50 p-4 text-sm font-medium text-red-800">
          {error}
        </div>
      )}

      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-slate-950">Available Exams</h2>
        <p className="text-sm text-slate-600">{filtered.length} result{filtered.length === 1 ? '' : 's'}</p>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
        {filtered.map(exam => (
          <ExamCard key={exam.id ?? exam._id} exam={exam} />
        ))}
      </div>

      {!error && filtered.length === 0 && (
        <div className="border border-slate-200 bg-white p-8 text-center text-slate-600">
          No exams found. Try a different search term or category.
        </div>
      )}
    </div>
  )
}
