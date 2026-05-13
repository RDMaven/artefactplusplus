import Header from "./Header";
import styles from "./App.module.css";
import PageContent from "./PageContent";
import { useState } from "react";
import { mmap } from "./utils";

export default function App() {
  const [fileList, setFileList] = useState<File[]>([]);
  const [mapList, setMapList] = useState<mmap[]>([])
  return (
    <div className={styles.main}>
      <Header />
      <PageContent fileList={fileList} setFileList={setFileList} mapList={mapList} setMapList={setMapList}/>
    </div>
  );
}
