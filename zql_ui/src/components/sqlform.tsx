import { zodResolver } from "@hookform/resolvers/zod";
import { useForm, Controller } from "react-hook-form";
import { z } from "zod";
import axios from "axios";
import { useState, useEffect } from "react";
import * as monaco from "monaco-editor";

import { Button } from "@/components/ui/button";
// import { Form, FormControl, FormField, FormItem } from "@/components/ui/form";
import { DataTable } from "./data-table";

const FormSchema = z.object({
  query: z.string(),
});

const BASE_API_URL = import.meta.env.VITE_BASE_API_URL;

// Register the custom language
monaco.languages.register({ id: "zql" });

// Set the custom language configuration
monaco.languages.setMonarchTokensProvider("zql", {
  ignoreCase: true,
  keywords: [
    "yass",
    "tfw",
    "say",
    "be",
    "sike",
    "fax",
    "uh",
    "let",
    "cook",
    "hands",
    "ngl",
    "perchance",
    "rizz",
    "af",
    "bops",
    "flops",
    "inner",
    "cross",
    "left",
    "right",
  ],
  tokenizer: {
    root: [
      // Select Star
      [/(shee)(e)*(sh)/, "type"],
      // Keywords
      // Multi-Token Keywords
      [/its giving/, "keyword"],
      [/real ones/, "keyword"],
      [/say less/, "keyword"],
      [/no cap/, "keyword"],
      [/come through/, "keyword"],
      [/left outer/, "keyword"],
      [/right outer/, "keyword"],
      [/full outer/, "keyword"],
      [/catch these/, "keyword"],
      [/kinda bops/, "keyword"],
      [/kinda flops/, "keyword"],
      [/high key/, "keyword"],
      [/low key/, "keyword"],
      [/high key yikes/, "keyword"],
      [/low key yikes/, "keyword"],
      [/with the bois/, "keyword"],
      [/with all the bois/, "keyword"],
      [/whats good with/, "keyword"],
      [/yeet queen/, "keyword"],
      [/yeet girlie/, "keyword"],
      [/or nah/, "keyword"],
      [/built different queen/, "keyword"],
      [/built different girlie/, "keyword"],
      [/pushin p into/, "keyword"],
      [
        /@?[a-zA-Z][\w$]*/,
        {
          cases: {
            "@keywords": "keyword",
            "@default": "source",
          },
        },
      ],
      // Literal Values
      [/".*?"/, "string"],
      [/'.*?'/, "string"],
      [/\d*\.\d+([eE][\-+]?\d+)?/, "number.float"],
      [/\d+/, "number"],
    ],
  },
});

export function SqlForm() {
  const [transpiledQuery, setTranspiledQuery] = useState("");
  const [dataRows, setDataRows] = useState([]);
  const [dataColumns, setDataColumns] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");

  const { control, handleSubmit, setValue } = useForm<
    z.infer<typeof FormSchema>
  >({
    resolver: zodResolver(FormSchema),
  });

  useEffect(() => {
    // Setup Monaco editor

    const defaultQuery =
      "its giving\n\tname,\n\tfave_color,\n\tfollowers\nyass peeps\nsay less 3\nno cap";

    const editor = monaco.editor.create(
      document.getElementById("monaco-editor")!,
      {
        value: defaultQuery,
        theme: "vs-dark",
        language: "zql",
        fontSize: 16,
        minimap: { enabled: false },
      }
    );

    setValue("query", editor.getValue());

    editor.onDidChangeModelContent(() => {
      const value = editor.getValue();
      setValue("query", value); // Synchronize editor content with form
    });

    // Add keydown event listener for Cmd+Enter or Ctrl+Enter
    editor.addCommand(
      monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter,
      function () {
        handleSubmit(onSubmit)(); // Manually trigger the form submission
      }
    );

    return () => editor.dispose();
  }, [setValue]);

  async function onSubmit(data: z.infer<typeof FormSchema>) {
    try {
      const formData = new FormData();
      formData.append("query", data.query);

      const response = await axios.post(`${BASE_API_URL}/run`, formData);

      setTranspiledQuery(response.data["transpiled_query"]);
      setDataRows(response.data["rows"]);
      setDataColumns(response.data["columns"]);
      setErrorMessage(response.data["error_message"]);
    } catch (error) {
      console.error("Transpilation failed:", error);
    }
  }

  return (
    <div>
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="flex flex-col justify-center items-center space-y-2 p-5"
      >
        <Controller
          name="query"
          control={control}
          render={({}) => (
            <div
              id="monaco-editor"
              style={{ height: "200px", width: "500px" }}
            ></div>
          )}
        />
        <Button className="bg-slate-900 h-12 text-lg" type="submit">
          {`Send it (${
            navigator.userAgent.includes("Mac") ? "⌘" : "Ctrl"
          }+Enter)`}
        </Button>
      </form>
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

      {transpiledQuery && (
        <div className="flex flex-col mt-3">
          <h1 className="text-2xl font-bold py-2"> sql for boomers </h1>
          <div>{transpiledQuery}</div>
        </div>
      )}
    </div>
  );
}
