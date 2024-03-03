import { useState } from "react";
import MonacoInput from "./components/monaco-input";
import { Button } from "./components/ui/button";
import { callTranspile } from "./callApi";
import { DataTable } from "./components/data-table";

function App() {
  const defaultZqlQuery =
    "its giving\n\tname,\n\tfave_color,\n\tfollowers\nyass peeps\nsay less 3\nno cap";

  const [zqlQuery, setZqlQuery] = useState(defaultZqlQuery);
  const [transpiledQuery, setTranspiledQuery] = useState("");
  const [dataRows, setDataRows] = useState([]);
  const [dataColumns, setDataColumns] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");

  const handleTranspile = async () => {
    const transpiledResult = await callTranspile(zqlQuery);
    console.log(transpiledResult); // Log the output of the transpile function
    setTranspiledQuery(transpiledResult.transpiledQuery);
    setDataRows(transpiledResult.dataRows);
    setDataColumns(transpiledResult.dataColumns);
    setErrorMessage(transpiledResult.errorMessage);
  };

  return (
    <div className="flex flex-col items-center justify-center mx-auto max-w-screen-lg px-4">
      <h1 className="text-7xl font-bold mt-8">zql</h1>
      <h1 className="text-2xl py-4">its giving sql for gen z</h1>
      <div className="flex flex-col sm:flex-row justify-center w-full">
        <div className="sm:w-1/2 sm:pr-2 mb-4 sm:mb-0 flex flex-col items-center">
          <h2 className="text-xl font-bold">zql</h2>
          <MonacoInput
            language={"zql"}
            value={zqlQuery}
            setValue={setZqlQuery}
          />
        </div>
        <div className="sm:w-1/2 sm:pl-2 flex flex-col items-center">
          <h2 className="text-xl font-bold">sql for boomers</h2>
          <MonacoInput
            language={"sql"}
            value={transpiledQuery}
            setValue={(_) => {}}
            readOnly={true}
          />
        </div>
      </div>
      <div className="mt-4">
        <Button onClick={handleTranspile}>Send it</Button>
      </div>

      {dataColumns.length ? (
        <div className="flex flex-col">
          <h1 className="text-2xl font-bold py-2"> sheeeesh that zql bussin</h1>
          <DataTable columns={dataColumns} data={dataRows} />
        </div>
      ) : (
        <div />
      )}

      {errorMessage && (
        <div className="flex flex-col">
          <h1 className="text-2xl font-bold py-2">
            {" "}
            that zql is a bit sus iykyk{" "}
          </h1>
          <div>{errorMessage}</div>
        </div>
      )}
    </div>
  );
}

export default App;
