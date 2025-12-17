import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { App as AntApp, ConfigProvider, Input, Layout, Typography, theme } from "antd";
import { StrictMode, useState } from "react";
import { createRoot } from "react-dom/client";
import { Accounts } from "./Accounts";

const queryClient = new QueryClient();

function Shell() {
  const [token, setToken] = useState(localStorage.getItem("gramfeed.token") ?? "");
  const dark = matchMedia("(prefers-color-scheme: dark)").matches;
  return (
    <ConfigProvider
      theme={{
        algorithm: dark ? theme.darkAlgorithm : theme.defaultAlgorithm,
        token: {
          colorPrimary: "#006a7a",
          colorLink: "#006a7a",