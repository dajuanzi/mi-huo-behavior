import axios from "axios";

export const fetchConfusion = async (theme: string) => {
  try {
    const response = await axios.post(
      `http://127.0.0.1:8000/generate_confusion/?theme=${encodeURIComponent(
        theme
      )}`
    );
    console.log("Response:", response.data);
    return response.data.confusion;
  } catch (error) {
    console.error("Error fetching confusion:", error);
    throw error; // Rethrow the error for the caller to handle
  }
};
