import styles from "./BuildMap.module.css";
import picture from "./assets/picture.svg";
import fleche from "./assets/fleche.svg";
import { useRef, useState, useEffect, useMemo } from "react";
import { mmap } from "./utils";
import MapGrid from "./MapGrid";

type Props = {
  fileList: File[];
  mapList: mmap[];
  setMapList: React.Dispatch<React.SetStateAction<mmap[]>>;
  mapIndex: number;
  setMapIndex: React.Dispatch<React.SetStateAction<number>>;
};

export default function BuildMap({
  fileList,
  mapList,
  setMapList,
  mapIndex,
  setMapIndex,
}: Props) {
  const sortie = useRef<HTMLImageElement>(null);
  const [isOpenSortie, setIsOpenSortie] = useState<boolean>(false);

  const [urlList, setUrlList] = useState<string[]>([]);

  useEffect(() => {
    const urls = fileList.map((file) => URL.createObjectURL(file));

    setUrlList(urls);

    return () => {
      urls.forEach((url) => URL.revokeObjectURL(url));
    };
  }, [fileList]);

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
  useEffect(() => {
    async function buildMaps() {
      const newMapList = await Promise.all(
        fileList.map(async (elt) => {
          const res = await getImageSize(elt);

          return new mmap(res.width, res.height, 1, 1, [[]]);
        }),
      );
      setMapList(newMapList);

      console.log("HEY J AI DES CARTES");
      console.log(newMapList);
      return newMapList;
    }
    buildMaps();
  }, [fileList]);

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
              <div
                key={`fichier_${index}`}
                className={`${styles.fileChoice} ${mapIndex === index ? styles.isSelected : ""}`}
              >
                <img src={picture} onClick={() => setMapIndex(index)}></img>
                <p>
                  {fileList.length > 7 ? n_letters(file.name, 10) : file.name}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
      {urlList.length > 0 &&
      urlList[mapIndex] &&
      mapList.length > 0 &&
      mapList[mapIndex] ? (
        <MapGrid
          mapList={mapList}
          setMapList={setMapList}
          index={mapIndex}
          urlList={urlList}
        />
      ) : (
        <p>Chargement...</p>
      )}
    </div>
  );
}
