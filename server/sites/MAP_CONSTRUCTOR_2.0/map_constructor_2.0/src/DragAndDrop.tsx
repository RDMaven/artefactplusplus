import React, { useRef } from "react";
import styles from "./DragAndDrop.module.css";
import picture from "./assets/picture.svg";
import x from "./assets/x.svg";
import { newToast } from "./utils";

type Props = {
  fileList: File[];
  setFileList: React.Dispatch<React.SetStateAction<File[]>>;
  setIsOpenCreateMap: React.Dispatch<React.SetStateAction<boolean>>
};

export default function DragZone({ fileList, setFileList, setIsOpenCreateMap }: Props) {
  const inputFile = useRef<HTMLInputElement>(null);

  function newFile() {
    const files = inputFile.current?.files;
    if (!files) return;
    const newFiles = Array.from(files).filter(
        (elt) => elt.type.startsWith("image/"),
    );
    const nonImage = Array.from(files).filter(
      (elt) => !elt.type.startsWith("image/"),
    );

    if (nonImage.length != 0) {
      newToast(false, "Des fichiers n'étant pas des images ont été ignorés")
    }

    setFileList((prev) => [...prev, ...newFiles]);
    newToast(true, `${newFiles.length} fichiers déposés !`)
  }

  function dragButton() {
    inputFile.current?.click();
  }

  function onDrop(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();

    const files = e.dataTransfer.files;
    if (!files || files.length === 0) {
      newToast(false, "Aucun fichier déposé")
      return;
    }
    const newFiles = Array.from(files).filter(
        (elt) => elt.type.startsWith("image/"),
    );
    const nonImage = Array.from(files).filter(
      (elt) => !elt.type.startsWith("image/"),
    );

    if (nonImage.length != 0) {
      newToast(false,"Des fichiers n'étant pas des images ont été ignorés")
    }

    setFileList((prev) => [...prev, ...newFiles]);
    newToast(true, `${newFiles.length} fichiers déposés !`)
  }

  function supprimerFile(index: number) {
    newToast(true, "Un fichier vient d'être supprimé")
    setFileList(fileList.filter((_,i)=> i != index));
  }

  function buildMap(){
    if (fileList.length === 0){
      newToast(false, "Aucun fichier sélectionné...")
    } else {
      setIsOpenCreateMap(true)
      newToast(true, "Passage à l'étape suivante!")
    }
  }

  return (
    <div className={styles.mainDragZone}>
      <input
        type="file"
        hidden
        accept="image/*"
        ref={inputFile}
        onChange={newFile}
        multiple
      ></input>
      <div
        className={styles.dragZone}
        onDrop={onDrop}
        onDragOver={(e) => {
          e.preventDefault();
        }}
      >
        <p>Déposez ici vos fichiers</p>
      </div>
      <button className={styles.dragButton} onClick={dragButton}>
        Sélectionner un fichier
      </button>
      {fileList.length != 0 ? (
        <div className={styles.filesList}>
          <p>Vous avez déposé les fichiers suivants :</p>
          {fileList.map((elt, index) => (
            <div key={index} className={styles.Div}>
              <img src={picture} alt="img"/>
              <p>{elt.name}</p>
              <img src={x} alt="X" className={styles.croix} onClick={()=>supprimerFile(index)}/>
            </div>
          ))}
        </div>
      ) : (
        <p>Pas encore de fichiers.</p>
      )}
      <button className={styles.dragButton} onClick={buildMap}>Passer à l'étape suivante !</button>
    </div>
  );
}
