const dotenv = require('dotenv');
const { sequelize } = require('./db');
const Exam = require('../models/Exam');
const sampleExams = require('./sampleExams');

dotenv.config();

async function seed() {
  try {
    if (process.env.USE_MEMORY_DB === 'true') {
      console.log('USE_MEMORY_DB=true: seed is not needed for in-memory mode');
      process.exit(0);
    }

    await sequelize.authenticate();
    await sequelize.sync({ force: true });
    await Exam.bulkCreate(sampleExams);
    console.log('Seeded sample exams');
    process.exit(0);
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
}

seed();
