import styles from "./BuildMap.module.css";
import React from "react";
import picture from "./assets/picture.svg";

type Props = {
    fileList: File[]
}

export default function BuildMap({fileList}: Props){
    function n_letters(word:string, n: number): string{
        if (word.length<=n+4){
            return word
        } else {
            return word.slice(0,-4).slice(0,n) + "..."
        }
    }
    return (
        <div className={styles.mainBuildMap}>
            <div className={styles.allFiles}>
                <img></img>
                <div className={styles.filesDiv}>
                    {fileList.map((file, index)=>(
                        <div key={`fichier_${index}`} className={styles.fileChoice}>
                            <img src={picture}></img>
                            <p>{fileList.length > 7 ? n_letters(file.name,10) : file.name}</p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}