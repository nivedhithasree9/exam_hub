const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const { sequelize } = require('./db');

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const examRoutes = require('../routes/exams');
const { errorHandler } = require('./middleware/errorHandler');

const PORT = process.env.PORT || 5000;
const useMemoryDb = process.env.USE_MEMORY_DB === 'true';

app.use('/api/exams', examRoutes);
app.use(errorHandler);

async function start() {
  try {
    if (useMemoryDb) {
      console.log('Using in-memory sample data; MySQL is not required');
      app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
      return;
    }

    await sequelize.authenticate();
    await sequelize.sync();
    console.log('MySQL connected');
    app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
  } catch (err) {
    console.error('DB connection error', err);
    process.exit(1);
  }
}

start();
