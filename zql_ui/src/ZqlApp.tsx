import { useState, useEffect } from "react";
import MonacoInput from "./components/monaco-input";
import { Button } from "./components/ui/button";
import { callRunQuery } from "./callApi";
import { DataTable } from "./components/data-table";
import { HelpSheet } from "./components/help-sheet";
import { exampleZqlQueries } from "./components/exampleQueries";
import { FaGithub } from "react-icons/fa";

function ZqlApp() {
  const defaultZqlQuery =
    "its giving\n\tname,\n\tfave_color,\n\tfollowers\nyass peeps\nsay less 3\nno cap";

  const [zqlQuery, setZqlQuery] = useState(defaultZqlQuery);
  const [transpiledQuery, setTranspiledQuery] = useState("");
  const [dataRows, setDataRows] = useState<any[]>([]);
  const [dataColumns, setDataColumns] = useState<string[]>([]);
  const [errorMessage, setErrorMessage] = useState("");
  const [helpSheetOpen, setHelpSheetOpen] = useState(false);

  const handleTranspile = async (overrideQuery?: string) => {
    const transpiledResult = await callRunQuery(
      overrideQuery ? overrideQuery : zqlQuery
    );
    setTranspiledQuery(transpiledResult.transpiledQuery);
    setDataRows(transpiledResult.dataRows);
    setDataColumns(transpiledResult.dataColumns);
    setErrorMessage(transpiledResult.errorMessage);
  };

  const isMac = navigator.userAgent.includes("Mac");

  const handleKeyDown = (event: KeyboardEvent) => {
    if (event.metaKey && event.key === "Enter") {
      handleTranspile();
    }
    if (event.metaKey && event.key === "k") {
      setHelpSheetOpen(!helpSheetOpen);
    }
  };

  useEffect(() => {
    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [zqlQuery]); // Listen to changes in zqlQuery

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
            onCtrlCmdEnter={handleTranspile}
          />
        </div>
        <div className="sm:w-1/2 sm:pl-2 flex flex-col items-center">
          <h2 className="text-xl font-bold">sql for boomers</h2>
          <MonacoInput
            language={"sql"}
            value={transpiledQuery}
            setValue={(_) => {}}
            onCtrlCmdEnter={() => handleTranspile()}
            readOnly={true}
          />
        </div>
      </div>
      <div className="mt-4 flex justify-center space-x-3 py-2">
        <Button onClick={() => handleTranspile()}>
          send it ({isMac ? "⌘" : "Ctrl"}+Enter)
        </Button>
        <HelpSheet
          value={zqlQuery}
          open={helpSheetOpen}
          onOpenChange={setHelpSheetOpen}
          setValue={(query) => {
            setZqlQuery(query);
            handleTranspile(query);
          }}
          title="inspo zql queries"
          description="pre-filled zql that you know is bussin'"
          exampleQueries={exampleZqlQueries}
        >
          <Button>get inspo ({isMac ? "⌘" : "Ctrl"}+K)</Button>
        </HelpSheet>
      </div>

      {dataColumns && dataColumns.length ? (
        <div className="flex flex-col">
          <h1 className="text-xl font-bold py-2 text-center">
            sheeeesh that zql bussin
          </h1>
          <DataTable columns={dataColumns} data={dataRows} />
        </div>
      ) : (
        <div />
      )}

      {errorMessage && (
        <div className="flex flex-col">
          <h1 className="text-xl font-bold py-2">
            that zql is a bit sus iykyk
          </h1>
          <div>
            <pre>{errorMessage}</pre>
          </div>
        </div>
      )}
      <a
        target="_blank"
        href="https://github.com/genzql/zql"
        rel="noopener noreferrer"
        aria-label="Github"
        className="rounded p-2 text-xl hover:bg-accent hover:text-accent-foreground mt-10"
      >
        <FaGithub />
      </a>

      <div>
        <a
          target="_blank"
          href="https://github.com/vingkan"
          rel="noopener noreferrer"
        >
          <Button variant={"link"}>vinesh</Button>
        </a>
        ·
        <a
          target="_blank"
          href="https://github.com/tamjidrahman"
          rel="noopener noreferrer"
        >
          <Button variant={"link"}>tamjid</Button>
        </a>{" "}
      </div>
    </div>
  );
}

export default ZqlApp;
