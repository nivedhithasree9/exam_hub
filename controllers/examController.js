const useMemoryDb = process.env.USE_MEMORY_DB === 'true';
const sampleExams = require('../server/sampleExams');

let Exam;
let Op;

if (!useMemoryDb) {
  Exam = require('../models/Exam');
  Op = require('sequelize').Op;
}

let memoryExams = sampleExams.map((exam, index) => ({
  id: index + 1,
  ...exam
}));

function getMemoryExam(id) {
  return memoryExams.find((exam) => exam.id === Number(id));
}

async function getExams(req, res, next) {
  try {
    const { q, category, page = 1, limit = 20 } = req.query;

    if (useMemoryDb) {
      const normalizedQuery = q ? q.toLowerCase() : '';
      const filtered = memoryExams.filter((exam) => {
        const matchesQuery = !normalizedQuery || exam.name.toLowerCase().includes(normalizedQuery);
        const matchesCategory = !category || exam.category === category;
        return matchesQuery && matchesCategory;
      });
      const start = (Number(page) - 1) * Number(limit);
      return res.json(filtered.slice(start, start + Number(limit)));
    }

    const where = {};
    if (q) where.name = { [Op.like]: `%${q}%` };
    if (category) where.category = category;

    const exams = await Exam.findAll({
      where,
      offset: (page - 1) * limit,
      limit: parseInt(limit)
    });
    res.json(exams);
  } catch (err) {
    next(err);
  }
}

async function getExam(req, res, next) {
  try {
    if (useMemoryDb) {
      const exam = getMemoryExam(req.params.id);
      if (!exam) return res.status(404).json({ message: 'Exam not found' });
      return res.json(exam);
    }

    const exam = await Exam.findByPk(req.params.id);
    if (!exam) return res.status(404).json({ message: 'Exam not found' });
    res.json(exam);
  } catch (err) {
    next(err);
  }
}

async function createExam(req, res, next) {
  try {
    if (useMemoryDb) {
      const nextId = memoryExams.length ? Math.max(...memoryExams.map((exam) => exam.id)) + 1 : 1;
      const exam = { id: nextId, ...req.body };
      memoryExams.push(exam);
      return res.status(201).json(exam);
    }

    const exam = await Exam.create(req.body);
    res.status(201).json(exam);
  } catch (err) {
    next(err);
  }
}

async function updateExam(req, res, next) {
  try {
    if (useMemoryDb) {
      const exam = getMemoryExam(req.params.id);
      if (!exam) return res.status(404).json({ message: 'Exam not found' });
      Object.assign(exam, req.body);
      return res.json(exam);
    }

    const exam = await Exam.findByPk(req.params.id);
    if (!exam) return res.status(404).json({ message: 'Exam not found' });
    await exam.update(req.body);
    res.json(exam);
  } catch (err) {
    next(err);
  }
}

async function deleteExam(req, res, next) {
  try {
    if (useMemoryDb) {
      const exam = getMemoryExam(req.params.id);
      if (!exam) return res.status(404).json({ message: 'Exam not found' });
      memoryExams = memoryExams.filter((item) => item.id !== exam.id);
      return res.json({ message: 'Deleted' });
    }

    const exam = await Exam.findByPk(req.params.id);
    if (!exam) return res.status(404).json({ message: 'Exam not found' });
    await exam.destroy();
    res.json({ message: 'Deleted' });
  } catch (err) {
    next(err);
  }
}

module.exports = { getExams, getExam, createExam, updateExam, deleteExam };
