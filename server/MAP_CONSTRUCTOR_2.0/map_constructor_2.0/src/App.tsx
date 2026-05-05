import Header from "./Header";
import styles from "./App.module.css";
import PageContent from "./PageContent";

export default function App() {
  return (
    <div className={styles.main}>
      <Header />
      <PageContent />
    </div>
  );
}
