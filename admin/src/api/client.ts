export interface Account {
  username: string;
  full_name: string | null;
  posts: number;
  last_fetched_at: string | null;
  last_error: string | null;
  paused: boolean;
  feed_url: string;
}