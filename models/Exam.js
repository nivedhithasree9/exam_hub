const { sequelize, DataTypes } = require('../server/db');

const Exam = sequelize.define('Exam', {
  name: { type: DataTypes.STRING, allowNull: false },
  category: DataTypes.STRING,
  description: DataTypes.TEXT,
  eligibility: DataTypes.TEXT,
  syllabus: DataTypes.JSON,
  pattern: DataTypes.TEXT,
  books: DataTypes.JSON,
  pyq: DataTypes.JSON,
  dates: DataTypes.JSON
}, {
  tableName: 'exams'
});

module.exports = Exam;
