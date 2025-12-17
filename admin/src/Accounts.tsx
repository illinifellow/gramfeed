import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { App as AntApp, Badge, Button, Input, Popconfirm, Space, Table, Tag, Tooltip, Typography } from "antd";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import { useState } from "react";
import { type Account, api } from "./api/client";

dayjs.extend(relativeTime);

export function Accounts() {
  const qc = useQueryClient();
  const { message } = AntApp.useApp();
  const [username, setUsername] = useState("");
  // while a refresh is queued the list polls, so the new posts count appears without a reload
  const [polling, setPolling] = useState(false);
  const accounts = useQuery({ queryKey: ["accounts"], queryFn: api.accounts, refetchInterval: polling ? 3000 : false });
  const done = () => qc.invalidateQueries({ queryKey: ["accounts"] });

  const add = useMutation({
    mutationFn: api.add,
    onSuccess: ({ feed_url }) => {
      message.success(`Feed ready at ${feed_url}`);
      setUsername("");
      setPolling(true);
      setTimeout(() => setPolling(false), 60_000);
      void done();
    },
    onError: (e: Error) => message.error(e.message),
  });
  const refresh = useMutation({ mutationFn: api.refresh, onSuccess: () => { setPolling(true); void done(); } });
  const remove = useMutation({ mutationFn: api.remove, onSuccess: done });

  return (
    <Space direction="vertical" size="large" style={{ width: "100%" }}>