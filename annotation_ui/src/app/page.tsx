import Link from "next/link";

import { LatestPost } from "~/app/_components/post";
import { api, HydrateClient } from "~/trpc/server";

export default async function Home() {

  return (
    <HydrateClient>
      <main className="flex min-h-screen flex-col items-center justify-center bg-zinc-600 text-white">
        <div className="container flex flex-col items-center justify-center gap-12 p-4 py-10">
          
          <LatestPost />

        </div>
      </main>
    </HydrateClient>
  );
}
