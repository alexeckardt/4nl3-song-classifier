"use client";

import { useState } from "react";

import { api } from "~/trpc/react";
import { ScrollArea } from "~/components/ui/scroll-area";

export function LatestPost() {
  const [latestPost] = api.post.getLatest.useSuspenseQuery();

  const utils = api.useUtils();
  const [name, setName] = useState("");
  const createPost = api.post.create.useMutation({
    onSuccess: async () => {
      await utils.post.invalidate();
      setName("");
    },
  });
  return (
  <div>
    <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: "50%" }}>
      <ScrollArea className="h-[calc(100vh-2rem)] w-[40vw] rounded-md border p-4 overflow-auto text-center" style={{ whiteSpace: "pre-wrap" }} type="always">
        {latestPost?.lyrics}
      </ScrollArea>
    </div>
  </div>
  );
}
