import express from 'express';
import fs from 'fs/promises';
import path from 'path';
import cors from 'cors';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DB_PATH = path.join(__dirname, '..', 'content_memory.json');
const RENDERS_PATH = path.join(__dirname, '..', 'renders');

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());
app.use('/renders', express.static(RENDERS_PATH));

async function initDB() {
  try {
    await fs.access(DB_PATH);
  } catch {
    await fs.writeFile(DB_PATH, JSON.stringify([]));
  }
}

app.get('/api/posts', async (req, res) => {
  try {
    await initDB();
    const data = await fs.readFile(DB_PATH, 'utf-8');
    res.json(JSON.parse(data));
  } catch (error) {
    res.status(500).json({ error: 'Failed to read database' });
  }
});

app.post('/api/posts', async (req, res) => {
  try {
    const posts = req.body;
    await fs.writeFile(DB_PATH, JSON.stringify(posts, null, 2));
    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ error: 'Failed to save database' });
  }
});

app.listen(PORT, () => {
  console.log(`Backend server running on http://localhost:${PORT}`);
});
