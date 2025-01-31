"use client";

import { api } from "~/trpc/react";
import { ScrollArea } from "~/components/ui/scroll-area";
import { useState } from 'react'
import { Button } from "~/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "~/components/ui/table";
import { Checkbox } from "~/components/ui/checkbox";

export function LatestPost() {
  const [latestPost] = api.post.getLatest.useSuspenseQuery();
  const [selectedValue, setSelectedValue] = useState("yes");

  const [selectedTopics, setSelectedTopics] = useState<number[]>([]);

  const handleTopicChange = (id: number) => {
    setSelectedTopics((prev) =>
      prev.includes(id) ? prev.filter((topicId) => topicId !== id) : [...prev, id]
    );
  };

  const topics = [
    { id: 1, name: "Love" },
    { id: 2, name: "Heartbreak" },
    { id: 3, name: "Party" },
    { id: 4, name: "Life" },
  ];

  return (
  <div>
    <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: "50%" }}>
      <ScrollArea className="h-[calc(100vh-2rem)] w-[40vw] rounded-md border p-4 overflow-auto text-center" style={{ whiteSpace: "pre-wrap" }} type="always">
        {latestPost?.lyrics}
      </ScrollArea>
    </div>

    <div className="text-primary-foreground" style={{ position: "absolute", right: 0, top: "10%", bottom: 0, width: "50%" }}>
      <h1>Do you recognize this song?</h1>
        <div>
            <Button
            onClick={() => setSelectedValue("yes")}
            variant={selectedValue === "yes" ? "secondary" : "default"}
            >
            Yes
            </Button>
            <span style={{ margin: "0 8px" }}></span>
            <Button
            onClick={() => setSelectedValue("no")}
            variant={selectedValue === "no" ? "secondary" : "default"}
            >
            No
            </Button>
        </div>

        {/* Divide Section */}
        <div className='height-10 pb-10' />

       <h1>Select the top 2 topics for this song</h1>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="text-white">Topics</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
        {topics.map((topic) => (
          <TableRow key={topic.id}>
            <TableCell>
              <Checkbox
              checked={selectedTopics.includes(topic.id)}
              onCheckedChange={() => {
                if (selectedTopics.includes(topic.id)) {
                handleTopicChange(topic.id);
                } else if (selectedTopics.length < 2) {
                handleTopicChange(topic.id);
                }
              }}
              />
              {topic.name}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
      </Table>

      {/* Divide Section */}
      <div className='height-10 pb-10' />
        
      <h1>What decade do you think this song was written in?</h1>
      <select>
        <option value="1960s">60s</option>
        <option value="1970s">70s</option>
        <option value="1980s">80s</option>
        <option value="1990s">90s</option>
        <option value="2000s">00s</option>
        <option value="2010s">10s</option>
        <option value="2020s">20s</option>
      </select>
    </div>

  </div>
  );
}