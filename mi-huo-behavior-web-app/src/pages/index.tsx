import { useState } from "react";
import { fetchConfusion } from "../services/api";

const App = () => {
  const [theme, setTheme] = useState("职场");
  const [level, setLevel] = useState(3);
  const [result, setResult] = useState("");

  const handleGenerate = async () => {
    try {
      const confusion = await fetchConfusion(theme);
      setResult(confusion);
    } catch (error) {
      console.error("Error generating confusion:", error);
      setResult("生成失败，请稍后再试！");
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold">迷惑行为生成器</h1>
      <select value={theme} onChange={(e) => setTheme(e.target.value)}>
        <option value="职场">职场</option>
        <option value="校园">校园</option>
        <option value="家庭">家庭</option>
      </select>
      <input
        type="range"
        min={1}
        max={5}
        value={level}
        onChange={(e) => setLevel(Number(e.target.value))}
      />
      <button onClick={handleGenerate}>生成迷惑行为</button>
      {result && <p>{result}</p>}
    </div>
  );
};

export default App;
