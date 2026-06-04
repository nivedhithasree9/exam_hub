import React from 'react'
import { Link } from 'react-router-dom'

export default function ExamCard({ exam }) {
  const examId = exam.id ?? exam._id;

  return (
    <article className="flex h-full flex-col rounded border border-slate-200 bg-white p-5 shadow-sm hover:border-slate-300 hover:shadow">
      <div className="flex items-start justify-between gap-3">
        <span className="rounded bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-700">
          {exam.category}
        </span>
        <span className="whitespace-nowrap text-xs font-medium text-emerald-700">
          {exam.dates?.examDate || 'TBA'}
        </span>
      </div>
      <h2 className="mt-4 text-lg font-bold leading-snug text-slate-950">{exam.name}</h2>
      <p className="mt-2 line-clamp-3 text-sm leading-6 text-slate-600">{exam.description}</p>
      <div className="mt-4 grid grid-cols-2 gap-2 text-xs text-slate-600">
        <div className="rounded border border-slate-200 bg-slate-50 p-2">
          <p className="font-semibold text-slate-900">Mode</p>
          <p className="mt-1">{exam.examMode || 'Check details'}</p>
        </div>
        <div className="rounded border border-slate-200 bg-slate-50 p-2">
          <p className="font-semibold text-slate-900">Frequency</p>
          <p className="mt-1">{exam.frequency || 'Check details'}</p>
        </div>
      </div>
      <Link
        to={`/exam/${examId}`}
        className="mt-5 inline-flex w-full items-center justify-center rounded bg-slate-900 px-4 py-2.5 text-sm font-semibold text-white hover:bg-slate-800"
      >
        View complete details
      </Link>
    </article>
  )
}
