import React, { useEffect, useRef } from "react";
import * as monaco from "monaco-editor";

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

interface MonacoInputProps {
  language: string;
  value: string;
  setValue: (value: string) => void;
  readOnly?: boolean;
}

const MonacoInput: React.FC<MonacoInputProps> = ({
  language,
  value,
  setValue,
  readOnly = false,
}) => {
  const editorRef = useRef<monaco.editor.IStandaloneCodeEditor | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current) {
      editorRef.current = monaco.editor.create(containerRef.current, {
        value,
        language: language,
        theme: "vs-dark",
        fontSize: 16,
        minimap: { enabled: false },
        readOnly: readOnly, // Use the readOnly prop to set readOnly option
      });

      editorRef.current.onDidChangeModelContent(() => {
        const editorValue = editorRef.current?.getValue();
        if (editorValue !== undefined) {
          setValue(editorValue);
        }
      });
    }

    return () => {
      editorRef.current?.dispose();
    };
  }, [setValue]);

  // Update editor value when prop `value` changes
  useEffect(() => {
    if (editorRef.current && value !== editorRef.current.getValue()) {
      editorRef.current.setValue(value);
    }
  }, [value]);

  // Update readOnly option when prop `readOnly` changes
  useEffect(() => {
    if (editorRef.current) {
      editorRef.current.updateOptions({ readOnly });
    }
  }, [readOnly]);

  return <div ref={containerRef} style={{ height: "200px", width: "100%" }} />;
};

export default MonacoInput;
