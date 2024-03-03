import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import axios from "axios";

import { Button } from "@/components/ui/button";
import { Form, FormControl, FormField, FormItem } from "@/components/ui/form";
import { Textarea } from "@/components/ui/textarea";
import { useState } from "react";
import { DataTable } from "./data-table";

const FormSchema = z.object({
  query: z.string(),
});

const BASE_API_URL = import.meta.env.VITE_BASE_API_URL;

export function SqlForm() {
  const [transpiledQuery, setTranspiledQuery] = useState("");
  const [dataRows, setDataRows] = useState([]);
  const [dataColumns, setDataColumns] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");

  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
  });

  async function onSubmit(data: z.infer<typeof FormSchema>) {
    try {
      const formData = new FormData();
      formData.append("query", data.query);

      // Make a POST request to the transpile endpoint with form data
      const response = await axios.post(BASE_API_URL + "/run", formData);

      // Handle the response
      setTranspiledQuery(response.data["transpiled_query"]);
      setDataRows(response.data["rows"]);
      setDataColumns(response.data["columns"]);
      setErrorMessage(response.data["error_message"]);
    } catch (error) {
      // Handle errors
      console.error("Transpilation failed:", error);
    }
  }

  return (
    <div>
      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="flex flex-col justify-center items-center space-y-2 p-5"
        >
          <FormField
            control={form.control}
            name="query"
            render={({ field }) => (
              <FormItem className="">
                <FormControl>
                  <Textarea
                    placeholder="its giving 1 no cap"
                    className="resize-none text-lg w-96 h-56" // Adjust width and height here
                    {...field}
                  />
                </FormControl>
              </FormItem>
            )}
          />
          <Button className="bg-slate-900 h-12 text-lg" type="submit">
            send it
          </Button>
        </form>
      </Form>
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
      <div className="mt-10"></div>
    </div>
  );
}
