export interface Account {
  username: string;
  full_name: string | null;
  posts: number;
  last_fetched_at: string | null;
  last_error: string | null;
  paused: boolean;
  feed_url: string;
}

const token = () => localStorage.getItem("gramfeed.token") ?? "";

async function call<T>(path: string, init: RequestInit = {}): Promise<T> {
  const res = await fetch(path, { ...init, headers: { authorization: `Bearer ${token()}`, "content-type": "application/json" } });
  if (res.status === 401) throw new Error("Wrong admin token");
  if (!res.ok) throw new Error((await res.json().catch(() => null))?.detail ?? res.statusText);
  return (res.status === 204 || res.status === 202 ? undefined : res.json()) as T;
}

export const api = {
  accounts: () => call<Account[]>("/api/accounts"),
  add: (username: string) => call<{ feed_url: string }>("/api/accounts", { method: "POST", body: JSON.stringify({ username }) }),