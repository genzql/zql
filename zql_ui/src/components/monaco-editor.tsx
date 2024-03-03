// MonacoEditorForm.tsx
import React, { useEffect, useRef } from "react";
import * as monaco from "monaco-editor";

interface MonacoEditorFormProps {
  value: string;
  onChange: (value: string) => void;
}

const MonacoEditorForm: React.FC<MonacoEditorFormProps> = ({
  value,
  onChange,
}) => {
  const editorRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (editorRef.current) {
      const editor = monaco.editor.create(editorRef.current, {
        value,
        language: "sql",
        theme: "vs-dark",
      });

      editor.onDidChangeModelContent(() => {
        onChange(editor.getValue());
      });

      return () => editor.dispose();
    }
  }, [onChange]);

  return <div ref={editorRef}></div>;
};

export default MonacoEditorForm;
