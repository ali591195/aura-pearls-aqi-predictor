import { BrowserRouter, Route, Routes } from "react-router-dom";

import Aurora from "./components/Aurora";
import Footer from "./components/Footer";
import Sidebar from "./components/Sidebar";

import PredictionPage from "./pages/PredictionPage";
import StatsPage from "./pages/StatsPage";

import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <main className="app">
        <Aurora />

        <div className="app-layout">
          <Sidebar />

          <main className="main-content">
            <Routes>
              <Route path="/" element={<PredictionPage />} />
              <Route path="/stats" element={<StatsPage />} />
            </Routes>
          </main>
        </div>

        <Footer />
      </main>
    </BrowserRouter>
  );
}

export default App;