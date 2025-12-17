import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { App as AntApp, ConfigProvider, Input, Layout, Typography, theme } from "antd";
import { StrictMode, useState } from "react";
import { createRoot } from "react-dom/client";
import { Accounts } from "./Accounts";