import type { mmap } from "./utils";
import styles from "./MapGrid.module.css";
import React, { useRef, useEffect, useState } from "react";
import Export from "./Export";

type Props = {
  mapList: mmap[];
  setMapList: React.Dispatch<React.SetStateAction<mmap[]>>;
  index: number;
  urlList: string[];
  isOpenExport: boolean;
  setIsOpenExport: React.Dispatch<React.SetStateAction<boolean>>;
  fileList: File[];
};

export default function MapGrid({
  mapList,
  setMapList,
  index,
  urlList,
  isOpenExport,
  setIsOpenExport,
  fileList,
}: Props) {
  const [isDrawing, setIsDrawing] = useState(false);
  const [paintingValue, setPaintingValue] = useState(1);

  function changeGrid(value: number) {
    //Fonction qui a value le nombre de cases en ligne associe le nombre de colonnes, et change ces valeurs dans l'objet map associé
    const [picture_width, picture_height] = mapList[index].getPictureSize();
    const width: number = value; //nombre de cases en largeur
    const height: number = Math.round((value / picture_width) * picture_height); //nombre de cases en hauteur
    setMapList((prev) => {
      const newList = [...prev];
      newList[index].setGridSize(width, height);
      return newList;
    });
    mapList[index].gridInit(width, height);
    console.log(width, height);
    console.log(mapList);
  }

  const [gridWidth, gridHeight] = mapList[index].getGridSize();

  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const [w, h] = mapList[index].getPictureSize();
    const [gridWidth, gridHeight] = mapList[index].getGridSize();

    canvas.width = w;
    canvas.height = h;

    const cellSizeX = w / gridWidth;
    const cellSizeY = h / gridHeight;

    ctx.clearRect(0, 0, w, h);

    ctx.beginPath();

    // vertical lines
    for (let x = 0; x <= gridWidth; x++) {
      ctx.moveTo(x * cellSizeX, 0);
      ctx.lineTo(x * cellSizeX, h);
    }

    // horizontal lines
    for (let y = 0; y <= gridHeight; y++) {
      ctx.moveTo(0, y * cellSizeY);
      ctx.lineTo(w, y * cellSizeY);
    }

    //fillCases
    for (let i = 0; i < gridHeight; i++) {
      for (let j = 0; j < gridWidth; j++) {
        if (mapList[index].getGridCase(i, j)) {
          ctx.fillStyle = "black";
          ctx.fillRect(j * cellSizeX, i * cellSizeY, cellSizeX, cellSizeY);
        }
      }
    }

    ctx.stroke();
  }, [mapList, index]);
  const [zoom, setZoom] = useState<number>(1);

  function getCell(e: React.MouseEvent<HTMLCanvasElement>): number[] | void {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const [w, h] = mapList[index].getPictureSize();
    const [gridWidth, gridHeight] = mapList[index].getGridSize();

    const [cellSizeX, cellSizeY] = [w / gridWidth, h / gridHeight];

    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX - rect.left) / zoom;
    const y = (e.clientY - rect.top) / zoom;

    const [j, i] = [Math.floor(x / cellSizeX), Math.floor(y / cellSizeY)];

    return [i, j];
  }

  function paintCell(e: React.MouseEvent<HTMLCanvasElement>, value: number) {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const [w, h] = mapList[index].getPictureSize();
    const [gridWidth, gridHeight] = mapList[index].getGridSize();

    const [cellSizeX, cellSizeY] = [w / gridWidth, h / gridHeight];

    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX - rect.left) / zoom;
    const y = (e.clientY - rect.top) / zoom;

    const [j, i] = [Math.floor(x / cellSizeX), Math.floor(y / cellSizeY)];

    setMapList((prev) => {
      const newList = [...prev];
      if (newList[index].getGridCase(i, j) !== value) {
        newList[index].setGridCase(i, j, value);
      }
      return newList;
    });
    console.log(mapList[index]);
  }

  function onMouseDown(e: React.MouseEvent<HTMLCanvasElement>) {
    setIsDrawing(true);

    const cell = getCell(e);
    if (!cell) return;
    const [i, j] = cell;

    setPaintingValue(1 - mapList[index].getGridCase(i, j));

    paintCell(e, paintingValue);
  }

  function onMouseMove(e: React.MouseEvent<HTMLCanvasElement>) {
    if (isDrawing) {
      paintCell(e, paintingValue);
    }
  }

  function onMouseUp() {
    setIsDrawing(false);
  }

  return (
    <div className={styles.mainMapGrid}>
      <div className={styles.prepaIMG}>
        <p>Veuillez sélectionner la précision souhaitée pour la grille :</p>
        <div className={styles.inputRow}>
          <input
            type="range"
            value={gridWidth}
            min="1"
            max="201"
            step="10"
            onChange={(e) => changeGrid(Number(e.target.value))}
          />
          <p>
            Nombre de cases : {gridWidth} x {gridHeight}
          </p>
          <input
            type="range"
            value={zoom}
            min="0.2"
            max="3"
            step="0.1"
            onChange={(e) => setZoom(Number(e.target.value))}
          />
          <p>Zoom : {zoom}</p>
          <button
            className={styles.exportButton}
            onClick={() => setIsOpenExport(true)}
          >
            Exporter
          </button>
        </div>
      </div>
      <div className={styles.ImageZone}>
        <div className={styles.scrollZone}>
          <img
            src={urlList[index]}
            style={{
              transform: `scale(${zoom})`,
              transformOrigin: "top left",
              touchAction: "none",
            }}
          ></img>
          <canvas
            ref={canvasRef}
            style={{
              transform: `scale(${zoom})`,
              transformOrigin: "top left",
              touchAction: "none",
            }}
            onMouseDown={(e) => onMouseDown(e)}
            onMouseMove={(e) => onMouseMove(e)}
            onMouseLeave={() => onMouseUp()}
            onMouseUp={() => onMouseUp()}
          />
        </div>
      </div>
      {isOpenExport && (
        <Export
          setIsOpenExport={setIsOpenExport}
          fileList={fileList}
          mapList={mapList}
        />
      )}
    </div>
  );
}
