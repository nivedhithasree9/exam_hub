const { Sequelize, DataTypes } = require('sequelize');
const dotenv = require('dotenv');

dotenv.config();

const mysqlUri = process.env.MYSQL_URI || process.env.DATABASE_URL || (() => {
  const user = process.env.MYSQL_USER || 'root';
  const password = encodeURIComponent(process.env.MYSQL_PASSWORD || '');
  const host = process.env.MYSQL_HOST || '127.0.0.1';
  const port = process.env.MYSQL_PORT || '3306';
  const database = process.env.MYSQL_DATABASE || 'examhub';
  return `mysql://${user}:${password}@${host}:${port}/${database}`;
})();

const sequelize = new Sequelize(mysqlUri, {
  logging: false,
});

module.exports = { sequelize, DataTypes, Sequelize };
