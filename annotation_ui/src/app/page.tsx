import Link from "next/link";

import { LatestPost } from "~/app/_components/post";
import { api, HydrateClient } from "~/trpc/server";

export default async function Home() {
  void await api.post.getLatest.prefetch();

  return (
    <HydrateClient>
      <main className="flex min-h-screen flex-col items-center justify-center bg-zinc-600 text-white">
        <div className="container flex flex-col items-center justify-center gap-12 px-4 py-16">
          
          <LatestPost />

        </div>
      </main>
    </HydrateClient>
  );
}
