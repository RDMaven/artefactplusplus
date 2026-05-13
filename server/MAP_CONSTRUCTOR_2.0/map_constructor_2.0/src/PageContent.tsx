import { useState } from "react";
import DragZone from "./DragAndDrop";
import styles from "./PageContent.module.css";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import BuildMap from "./BuildMap";
import { mmap } from "./utils";

type Props = {
  fileList: File[],
  setFileList: React.Dispatch<React.SetStateAction<File[]>>
  mapList: mmap[];
  setMapList: React.Dispatch<React.SetStateAction<mmap[]>>;
}

export default function PageContent({fileList, setFileList, mapList, setMapList}: Props) {
  const [isOpenCreateMap, setIsOpenCreateMap] = useState<boolean>(false);
  return (
    <div className={styles.mainContent}>
      <ToastContainer />
      <p className={styles.title}>Création de cartes en pixel !</p>
      {isOpenCreateMap ? (
        <BuildMap fileList={fileList} mapList={mapList} setMapList={setMapList}/>
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
