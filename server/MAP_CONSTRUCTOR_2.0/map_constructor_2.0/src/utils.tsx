import { toast } from "react-toastify";

export function newToast(success: boolean, message: string) {
  if (success) {
    toast.success(message , {
      position: "top-right",
      autoClose: 3000,
      hideProgressBar: false,
    });
  } else {
    toast.error(message, {
        position: "top-right",
        autoClose: 3000,
        hideProgressBar: false,
      });
  }
}

export class mmap {
  private picture_width: number;
  private picture_height: number;

  private grid_width: number;
  private grid_height: number;

  private grid: number[][];

  constructor(picture_width: number, picture_height: number, grid_width: number, grid_height: number, grid: number[][]){
    this.picture_width = picture_width;
    this.picture_height = picture_height;
    this.grid_width = grid_width;
    this.grid_height = grid_height;
    this.grid = grid;
  }

  getPictureSize(): number[] {
    return [this.picture_width, this.picture_height]
  }

  getGridSize(): number[] {
    return [this.grid_width, this.grid_height]
  }

  setPictureSize(width: number, height: number){
    this.picture_height = height;
    this.picture_width = width;
  }

  setGridSize(width: number, height: number){
    this.grid_height = height;
    this.grid_width = width;
  }

  getGrid(){
    return this.grid;
  }

  gridInit(width: number, height: number){
    const newGrid: number[][] = [];
    for (let l = 0; l<height; l++){
      const newLine: number[] = new Array(width).fill(0);
      newGrid.push(newLine)
    }

    this.grid = newGrid
  }

  setGridCase(i: number, j: number, value: number){
    this.grid[i][j] = value;
  }

}