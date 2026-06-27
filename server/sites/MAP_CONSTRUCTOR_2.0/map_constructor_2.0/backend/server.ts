import express from "express";
import { exec } from "child_process";
import cors from "cors";
import path from "path";
import fs from "fs/promises";
import util from "util";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PATH = path.resolve(__dirname, "../../CARTES");

const execAsync = util.promisify(exec);

async function fileExist(filepath: string) {
  try {
    await fs.access(filepath);
    return true;
  } catch {
    return false;
  }
}

const app = express();
app.use(express.json());
app.use(cors());
app.post("/pull", (req, res) => {
  exec(`git -C ${PATH} pull`, (err, stdout, stderr) => {
    if (err) return res.status(500).send(stderr);
    res.send(stdout);
  });
});

app.post("/createFiles", async (req, res) => {
  try {
    const maps = req.body;

    for (const elt of maps) {
      let i = 0;

      let newFilePath = `${elt.name}.txt`;
      let fullNewFilePath = path.join(PATH, newFilePath);

      let resultExist = await fileExist(fullNewFilePath);

      while (resultExist) {
        i++;

        newFilePath = `${elt.name}(${i}).txt`;
        fullNewFilePath = path.join(PATH, newFilePath);
        resultExist = await fileExist(fullNewFilePath);
      }
      const fullPath = path.join(PATH, newFilePath);
      await fs.writeFile(fullPath, JSON.stringify(elt.grid));
    }

    res.send("Fichiers créés");
  } catch (err) {
    res.status(500).send(String(err));
  }
});
app.post("/commitAndPush", async (req, res) => {
  try {
    await execAsync(`git -C "${PATH}" add .`);

    const status = await execAsync(`git -C "${PATH}" status --porcelain`);

    if (!status.stdout.trim()) {
      return res.send("Aucun changement");
    }

    await execAsync(
      `git -C "${PATH}" commit -m "Mise à jour automatique des cartes"`,
    );

    //const pushResult = await execAsync(`git -C "${PATH}" push`);

    res.send("Données Push");
  } catch (err) {
    res.status(500).json({
      message: err.message,
      stderr: err.stderr,
      stdout: err.stdout,
    });
  }
});

app.listen(3001);
