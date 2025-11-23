import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { App as AntApp, Badge, Button, Input, Popconfirm, Space, Table, Tag, Tooltip, Typography } from "antd";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import { useState } from "react";
import { type Account, api } from "./api/client";
