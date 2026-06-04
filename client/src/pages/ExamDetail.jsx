import React, { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import api from '../api'

export default function ExamDetail() {
  const { id } = useParams()
  const [exam, setExam] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    setExam(null)
    setError('')
    api.get(`/exams/${id}`)
      .then(r => setExam(r.data))
      .catch(() => setError('Exam details could not be loaded.'))
  }, [id])

  if (error) {
    return (
      <div className="bg-white rounded shadow p-6">
        <Link to="/" className="text-sm font-medium text-indigo-600">Back to exams</Link>
        <p className="mt-4 text-gray-700">{error}</p>
      </div>
    )
  }

  if (!exam) {
    return (
      <div className="bg-white rounded shadow p-6">
        <p className="text-gray-700">Loading exam details...</p>
      </div>
    )
  }

  const quickFacts = [
    ['Conducted by', exam.conductedBy],
    ['Frequency', exam.frequency],
    ['Application mode', exam.applicationMode],
    ['Exam mode', exam.examMode],
    ['Duration', exam.duration],
    ['Fee', exam.fee]
  ].filter(([, value]) => value)

  function getBookTitle(book) {
    return typeof book === 'string' ? book : book.title
  }

  function getBookLink(book) {
    if (typeof book === 'object' && book.link) return book.link
    return `https://www.amazon.in/s?k=${encodeURIComponent(getBookTitle(book))}`
  }

  return (
    <div className="space-y-5 animate-fade-up">
      <Link to="/" className="inline-flex text-sm font-semibold text-slate-700 hover:text-slate-950">
        Back to exams
      </Link>

      <section className="border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-normal text-amber-700">{exam.category}</p>
            <h2 className="mt-1 text-3xl font-semibold leading-tight text-gray-950">{exam.name}</h2>
            <p className="mt-3 max-w-3xl text-gray-700">{exam.description}</p>
          </div>
          <div className="border border-slate-200 bg-slate-50 px-4 py-3 text-sm">
            <p className="font-semibold text-gray-900">Exam Date</p>
            <p className="mt-1 text-gray-700">{exam.dates?.examDate || 'To be announced'}</p>
          </div>
        </div>
      </section>

      <section className="border border-slate-200 bg-white p-6 shadow-sm">
        <h3 className="text-lg font-semibold text-gray-950">Quick Facts</h3>
        <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {quickFacts.map(([label, value]) => (
            <div key={label} className="border border-slate-200 bg-slate-50 p-3">
              <p className="text-xs uppercase text-gray-500">{label}</p>
              <p className="mt-1 font-medium text-gray-900">{value}</p>
            </div>
          ))}
        </div>
      </section>

      <div className="grid gap-5 lg:grid-cols-3">
        <div className="space-y-5 lg:col-span-2">
          <section className="border border-amber-200 bg-amber-50 p-6 shadow-sm">
            <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
              <div>
                <p className="text-sm font-semibold uppercase tracking-normal text-amber-800">Application guide</p>
                <h3 className="mt-1 text-xl font-bold text-slate-950">How to Apply for This Exam</h3>
                <p className="mt-2 leading-7 text-slate-700">
                  Follow these steps only after checking the latest official notification, because dates, fees, documents, and rules can change.
                </p>
              </div>
              {exam.officialWebsite && (
                <a
                  href={exam.officialWebsite}
                  target="_blank"
                  rel="noreferrer"
                  className="animate-soft-pulse inline-flex shrink-0 justify-center rounded bg-amber-500 px-4 py-2.5 text-sm font-bold text-slate-950 hover:bg-amber-400"
                >
                  Apply / Check Official Site
                </a>
              )}
            </div>
            <ol className="mt-5 grid gap-3 md:grid-cols-2">
              {exam.applicationSteps?.map((step, index) => (
                <li
                  key={step}
                  className="animate-fade-up border border-amber-200 bg-white p-4"
                  style={{ animationDelay: `${index * 70}ms` }}
                >
                  <div className="flex gap-3">
                    <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded bg-slate-900 text-sm font-bold text-white">
                      {index + 1}
                    </span>
                    <p className="pt-1 text-sm leading-6 text-slate-700">{step}</p>
                  </div>
                </li>
              ))}
            </ol>
          </section>

          <section className="border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-950">What This Exam Is Used For</h3>
            <p className="mt-2 leading-7 text-gray-700">{exam.useFor}</p>
          </section>

          <section className="border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-950">Eligibility</h3>
            <p className="mt-2 leading-7 text-gray-700">{exam.eligibility}</p>
          </section>

          <section className="border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-950">Exam Pattern</h3>
            <p className="mt-2 leading-7 text-gray-700">{exam.pattern}</p>
            {exam.markingScheme && (
              <div className="mt-4 border border-slate-200 bg-slate-50 p-3">
                <p className="text-sm font-semibold text-gray-900">Marking scheme</p>
                <p className="mt-1 text-sm text-gray-700">{exam.markingScheme}</p>
              </div>
            )}
          </section>

          <section className="border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-950">Selection Process</h3>
            <ol className="mt-4 space-y-3">
              {exam.selectionProcess?.map((step, index) => (
                <li key={step} className="flex gap-3">
                  <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-slate-900 text-sm font-semibold text-white">
                    {index + 1}
                  </span>
                  <span className="pt-1 text-gray-700">{step}</span>
                </li>
              ))}
            </ol>
          </section>

          <section className="border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-950">Syllabus</h3>
            <div className="mt-3 flex flex-wrap gap-2">
              {exam.syllabus?.map((item, i) => (
                <span key={i} className="rounded bg-slate-100 px-3 py-1 text-sm font-medium text-slate-800">
                  {item}
                </span>
              ))}
            </div>
          </section>

          <section className="border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-950">Best Books and Study Material</h3>
            <p className="mt-1 text-sm text-slate-600">
              Standard books, publisher guides, and practice material commonly useful for exam preparation.
            </p>
            <div className="mt-3 grid gap-3 md:grid-cols-2">
              {exam.books?.map((book, i) => (
                <a
                  key={i}
                  href={getBookLink(book)}
                  target="_blank"
                  rel="noreferrer"
                  className="group border border-slate-200 bg-slate-50 p-3 text-sm text-gray-800 hover:border-amber-300 hover:bg-amber-50"
                >
                  <span className="block font-medium text-slate-900 group-hover:text-amber-800">
                    {getBookTitle(book)}
                  </span>
                  <span className="mt-2 block text-xs font-semibold text-slate-500 group-hover:text-amber-700">
                    Search online to buy
                  </span>
                </a>
              ))}
            </div>
          </section>

          <section className="border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-950">Preparation Tips</h3>
            <ul className="mt-3 grid gap-2 md:grid-cols-2">
              {exam.preparationTips?.map((tip) => (
                <li key={tip} className="border border-slate-200 bg-slate-50 p-3 text-sm text-gray-800">
                  {tip}
                </li>
              ))}
            </ul>
          </section>
        </div>

        <aside className="space-y-5">
          <section className="border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-950">Important Dates</h3>
            <div className="mt-4 space-y-3">
              <div className="border border-slate-200 p-3">
                <p className="text-xs uppercase text-gray-500">Notification</p>
                <p className="mt-1 font-medium text-gray-900">{exam.dates?.notification || 'To be announced'}</p>
              </div>
              <div className="border border-slate-200 p-3">
                <p className="text-xs uppercase text-gray-500">Exam Date</p>
                <p className="mt-1 font-medium text-gray-900">{exam.dates?.examDate || 'To be announced'}</p>
              </div>
            </div>
          </section>

          <section className="border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-950">Official Link</h3>
            {exam.officialWebsite ? (
              <a
                href={exam.officialWebsite}
                target="_blank"
                rel="noreferrer"
                className="mt-4 block rounded bg-slate-900 px-3 py-2 text-center text-sm font-semibold text-white hover:bg-slate-800"
              >
                Visit official website
              </a>
            ) : (
              <p className="mt-2 text-sm text-gray-700">Official link not available.</p>
            )}
          </section>

          <section className="border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-950">Previous Year Questions</h3>
            <p className="mt-2 text-sm text-slate-600">
              Opens a paper search page so students can download the available official PDF.
            </p>
            <div className="mt-4 space-y-2">
              {exam.pyq?.map((paper) => (
                <a
                  key={paper.year}
                  href={paper.url}
                  target="_blank"
                  rel="noreferrer"
                  className="block w-full rounded border border-slate-200 bg-slate-50 px-3 py-2 text-left text-sm font-medium text-gray-800 hover:border-slate-400 hover:bg-white hover:text-slate-950"
                >
                  {paper.year} Question Paper
                </a>
              ))}
            </div>
          </section>
        </aside>
      </div>
    </div>
  )
}
