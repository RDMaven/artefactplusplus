import styles from "./Export.module.css";
import croix from "./assets/x.svg";
import { useState } from "react";
import type { mmap } from "./utils";
import { newToast } from "./utils";

type Props = {
  setIsOpenExport: React.Dispatch<React.SetStateAction<boolean>>;
  fileList: File[];
  mapList: mmap[];
  isOpenButton: boolean;
  setIsOpenButton: React.Dispatch<React.SetStateAction<boolean>>;
};

export default function Export({ setIsOpenExport, fileList, mapList }: Props) {
  const [isOpenButton, setIsOpenButton] = useState<boolean>(true);
  const [data, setData] = useState("");
  const [selectedFiles, setSelectedFiles] = useState<number[]>([]);
  async function getCommit() {
    const res = await fetch("http://localhost:3001/commitAndPush", {
      method: "POST",
    });
    const data = await res.text();
    return data;
  }
  async function getPull() {
    const res = await fetch("http://localhost:3001/pull", { method: "POST" });
    const data = await res.text();
    return data;
  }
  async function getFile(index: number[]) {
    const res = await fetch("http://localhost:3001/createFiles", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(
        mapList
          .map((elt, ind) => ({
            grid: elt.getGrid(),
            name: fileList[ind].name,
          }))
          .filter((_, ind) => index.includes(ind)),
      ),
    });
    const data = await res.text();
    return data;
  }
  async function handleExport() {
    if (selectedFiles.length === 0) {
      newToast(false, `Aucun fichier déposé !`);
    } else {
      setIsOpenButton(false);
      const data = await getPull();
      setData(data);
      const data2 = await getFile(selectedFiles);
      setData((prev) => prev + " " + data2);
      const data3 = await getCommit();
      setData((prev) => prev + " " + data3);
      setTimeout(() => {
        setIsOpenExport(false);
        setIsOpenButton(true);
      }, 1000);
    }
  }
  return (
    <div className={styles.mainExport}>
      <div className={styles.container}>
        <img
          src={croix}
          className={styles.exportExit}
          onClick={() => setIsOpenExport(false)}
        ></img>
        <p className={styles.title}>Prêts à exporter ?</p>
        <p className={styles.explain}>
          Sélectionnez les fichiers que vous souhaitez exporter et modifiez au
          besoin leur nom, puis cliquez sur exporter.
        </p>
        {fileList.map((file, index) => (
          <div className={styles.fileRow} key={index}>
            <input
              type="checkbox"
              checked={selectedFiles.includes(index)}
              onChange={() => {
                setSelectedFiles((prev) => {
                  if (prev.includes(index)) {
                    return prev.filter((i) => i !== index);
                  } else {
                    return [...prev, index];
                  }
                });
              }}
            />
            <p>Fichier {index}</p>
            <input type="text" value={file.name.slice(0, -4)} />
            <p>.txt</p>
          </div>
        ))}
        {isOpenButton && (
          <button className={styles.finalExport} onClick={handleExport}>
            Export backend
          </button>
        )}
        <p>{data}</p>
      </div>
    </div>
  );
}
