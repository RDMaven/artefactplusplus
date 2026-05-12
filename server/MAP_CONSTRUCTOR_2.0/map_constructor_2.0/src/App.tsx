import Header from "./Header";
import styles from "./App.module.css";
import PageContent from "./PageContent";
import { useState } from "react";

export default function App() {
  const [fileList, setFileList] = useState<File[]>([]);
  return (
    <div className={styles.main}>
      <Header />
      <PageContent fileList={fileList} setFileList={setFileList}/>
    </div>
  );
}
