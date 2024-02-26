import { SqlForm } from "./components/sqlform";

function App() {
  return (
    <div className="flex flex-col items-center justify-center">
      <h1 className="text-7xl font-bold mt-8">zql</h1>
      <h1 className="text-3xl py-5">its giving sql for gen z</h1>
      <SqlForm />
    </div>
  );
}

export default App;
