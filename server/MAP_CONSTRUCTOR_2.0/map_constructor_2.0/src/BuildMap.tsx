import styles from "./BuildMap.module.css";
import picture from "./assets/picture.svg";
import fleche from "./assets/fleche.svg";
import { useRef, useState, useEffect} from "react";
import { mmap } from "./utils";

type Props = {
  fileList: File[];
  mapList: mmap[];
  setMapList: React.Dispatch<React.SetStateAction<mmap[]>>;
};

export default function BuildMap({ fileList, mapList, setMapList }: Props) {
  const sortie = useRef<HTMLImageElement>(null);
  const [isOpenSortie, setIsOpenSortie] = useState<boolean>(false);

  function n_letters(word: string, n: number): string {
    if (word.length <= n + 4) {
      return word;
    } else {
      return word.slice(0, -4).slice(0, n) + "...";
    }
  }

  function getImageSize(
    file: File,
  ): Promise<{ width: number; height: number }> {
    return new Promise((res, rej) => {
      const img = new Image();
      const url = URL.createObjectURL(file);

      img.onload = () => {
        res({
          width: img.width,
          height: img.height,
        });
        URL.revokeObjectURL(url);
      };

      img.onerror = (err) => {
        URL.revokeObjectURL(url);
        rej(err);
      };
      img.src = url;
    });
  }
  useEffect(()=>{
  setMapList(()=>{
    const newMapList: mmap[] = [];
    fileList.map((elt)=>{
      getImageSize(elt).then((res)=>{
        const mapi: mmap = new mmap(res.width, res.height, 0, 0, [[]]);
        newMapList.push(mapi);
      })
    })
    console.log(newMapList)
    return newMapList
  })
},[])

  return (
    <div
      className={styles.mainBuildMap}
      style={
        {
          "--rotationFleche": isOpenSortie ? "0deg" : "180deg",
          "--translateAllFile": isOpenSortie ? "80%" : "0%",
        } as React.CSSProperties
      }
    >
      <div className={styles.allFiles}>
        <div className={styles.croixContainer}>
          <img
            src={fleche}
            className={styles.exitAllFiles}
            ref={sortie}
            onClick={() => setIsOpenSortie((prev) => !prev)}
          ></img>
          <div className={styles.filesDiv}>
            {fileList.map((file, index) => (
              <div key={`fichier_${index}`} className={styles.fileChoice}>
                <img src={picture} id={`${index}-image`}></img>
                <p>
                  {fileList.length > 7 ? n_letters(file.name, 10) : file.name}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
