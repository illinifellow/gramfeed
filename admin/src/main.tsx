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
          colorWarning: "#ff905c",
          colorError: "#ff573a",
          colorSuccess: "#57bd8a",
          colorBgLayout: dark ? "#151515" : "#faf6ee",
          colorBgContainer: dark ? "#1d1d1d" : "#ffffff",
          colorText: dark ? "#faf6ee" : "#181310",
          fontFamily: '"DecimaMonoX", "JetBrains Mono", ui-monospace, monospace',
          borderRadius: 5,
        },
        components: { Tag: { borderRadiusSM: 0 }, Table: { headerBg: dark ? "#151515" : "#f0eadd" } },