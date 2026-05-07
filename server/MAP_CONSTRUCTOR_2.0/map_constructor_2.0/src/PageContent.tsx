import { useState } from "react";
import DragZone from "./DragAndDrop";
import styles from "./PageContent.module.css";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import BuildMap from "./BuildMap";

export default function PageContent() {
  const [fileList, setFileList] = useState<File[]>([]);
  const [isOpenCreateMap, setIsOpenCreateMap] = useState<boolean>(false);
  return (
    <div className={styles.mainContent}>
      <ToastContainer />
      <p className={styles.title}>Création de cartes en pixel !</p>
      {isOpenCreateMap ? (
        <BuildMap />
      ) : (
        <DragZone
          fileList={fileList}
          setFileList={setFileList}
          setIsOpenCreateMap={setIsOpenCreateMap}
        />
      )}
    </div>
  );
}
