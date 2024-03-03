import axios from "axios";
import FormData from "form-data";

const BASE_API_URL = import.meta.env.VITE_BASE_API_URL;

export async function callTranspile(input: string) {
  try {
    const formData = new FormData();
    formData.append("query", input);

    const response = await axios.post(`${BASE_API_URL}/run`, formData);

    return {
      transpiledQuery: response.data["transpiled_query"],
      dataRows: response.data["rows"],
      dataColumns: response.data["columns"],
      errorMessage: response.data["error_message"],
    };
  } catch (error) {
    console.error("Transpilation failed:", error);
    return {
      transpiledQuery: "",
      dataRows: [],
      dataColumns: [],
      errorMessage:
        "Transpilation failed. Please check your input and try again.",
    };
  }
}
