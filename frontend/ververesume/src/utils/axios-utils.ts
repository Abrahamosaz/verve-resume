import axios from "axios";
import Cookies from "js-cookie";

const baseUrl = "http://localhost:8000/api";

const client = axios.create({
  baseURL: baseUrl,
  // baseURL: "http://localhost:5000/api",
});

export const request = ({ ...options }) => {
  const token = Cookies.get("jwt"); // Get the JWT token from the cookie

  if (token) {
    // Set the Authorization header with the JWT token
    client.defaults.headers.common.Authorization = `Bearer ${token}`;
  }

  client.defaults.withCredentials = true;

  return client(options);
};
