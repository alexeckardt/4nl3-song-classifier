"use client";

import { api } from "~/trpc/react";
import { ScrollArea } from "~/components/ui/scroll-area";
import { useState } from 'react'
import { Button } from "~/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "~/components/ui/table";
import { Checkbox } from "~/components/ui/checkbox";
import * as Select from '@radix-ui/react-select';


export function LatestPost() {
  const [latestPost] = api.post.getLatest.useSuspenseQuery();
  const [selectedValue, setSelectedValue] = useState("yes");

  const [selectedTopics, setSelectedTopics] = useState<number[]>([]);

  const handleTopicChange = (id: number) => {
    setSelectedTopics((prev) =>
      prev.includes(id) ? prev.filter((topicId) => topicId !== id) : [...prev, id]
    );
  };

  const songsToRead = 10

  const decades = [
    "1950s",
    "1960s",
    "1970s",
    "1980s",
    "1990s",
    "2000s",
    "2010s",
    "2020s",
  ];

  const topics = [
    { id: 1, name: "Love" },
    { id: 2, name: "Heartbreak" },
    { id: 3, name: "Party" },
    { id: 4, name: "Life" },
  ];

  return (

    <div>

      <div className='pb-2 text-xl'>Song Classifier - Group 17</div>
      <div className='pb-2 text-xl'>{latestPost && latestPost.id} / {songsToRead} Song</div>

    {/* //  Center Content */}
    <div style={{display: 'flex', gap: '50px'}}>
      <div className='float'>
        <ScrollArea className="h-[calc(100vh-2rem)] w-[40vw] rounded-md border p-4 overflow-auto text-center" style={{ whiteSpace: "pre-wrap" }} type="always">
          {latestPost?.lyrics}
        </ScrollArea>
      </div>

      <div className="text-primary-foreground float" >
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
        <ScrollArea className="h-[200px] w-full overflow-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Topic</TableHead>
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
        </ScrollArea>

        {/* Divide Section */}
        <div className='height-10 pb-10' />

        <h1>What decade do you think this song was written in?</h1>
        <div style={{ marginTop: "16px" }}>
          <Select.Root onValueChange={(value) => console.log(value)}>
            <Select.Trigger className="inline-flex items-center justify-between rounded-md border px-4 py-2 text-sm">
              <Select.Value placeholder="Select a decade" />
              <Select.Icon />
            </Select.Trigger>
            <Select.Content position="popper">
              <Select.ScrollUpButton />
              <Select.Viewport>
                {decades.map((decade) => (
                  <Select.Item className='cursor-pointer hover:color-red' key={decade} value={decade}>
                    <Select.ItemText>
                      <div className='color-sky-500 hover:color-sky-200'>
                        {decade}
                      </div>
                    </Select.ItemText>

                  </Select.Item>
                ))}
              </Select.Viewport>
              <Select.ScrollDownButton />
            </Select.Content>
          </Select.Root>
        </div>
      </div>

    </div>
    </div>
  );
}