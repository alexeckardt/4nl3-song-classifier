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
  const [selectedValue, setSelectedValue] = useState("n/a");
  const [errorMsg, setErrorMsg] = useState('');

  const updateAnnotation = api.post.updateAnnotation.useMutation();
  const [selectedTopics, setSelectedTopics] = useState<number[]>([]);
  const [selectedDecade, setSelectedDecade] = useState<string | null>(null);

  // ?? 
  const handleTopicChange = (id: number) => {
    setSelectedTopics((prev) => {

      //Exit, don't full stack over 2
      if (prev.length == 2 && !prev.includes(id)) return prev;

      // Normal
      return prev.includes(id) ? prev.filter((topicId) => topicId !== id) : [...prev, id]
    }

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
    { id: 1, name: "Desire (love/flirting)" },
    { id: 2, name: "Love (devotion)" },
    { id: 3, name: "Break-up (heartbreak)" },
    { id: 4, name: "Jealousy (cheating, promiscuity)" },
    { id: 5, name: "Dancing (clubbing/happy)" },
    { id: 6, name: "Friendship" },
    { id: 7, name: "Death (loss/grief)" },
    { id: 8, name: "Money (power/flexing)" },
    { id: 9, name: "Motivation (independance/confidence)" },
    { id: 10, name: "Struggle (mental health/societal issue)" },
    { id: 11, name: "Other" },
  ];

  const reset = () => {
    setSelectedDecade(null);
    setSelectedValue('n/a');
    setSelectedTopics((prev) => { return [] });

    setErrorMsg('')
  }

  const assertState = () => {

    // Asserts
    if (selectedValue === 'n/a') return 1;
    if (selectedTopics.length != 2) return 2;
    if (selectedDecade === null) return 3;

    return 0;
  }

  const pushNotif = (msg: string) => {
    console.log(msg)
    setErrorMsg(msg);
  }

  const pushAnnotation = (annotation: any) => {
    if (annotation.id === -1) return;

    updateAnnotation.mutate(annotation);
    console.log(annotation);
  }

  // Submit Handler
  const submitHandle = () => {

    try {

    const passes = assertState();
    console.log(passes);
    if (passes != 0) return pushNotif('Please complete the field')

    const annotation = {
      recognized: selectedValue,
      topics: selectedTopics,
      decade: selectedDecade,
    };

    // Push
    pushAnnotation(annotation);
    
    // Fetch New
    reset();
    handleTopicChange();

      return 0;
    } catch (e) {
      pushNotif('An Error Occured.')
    }
  }

  return (

    <div>

      <div className='pb-2 text-xl'>Song Classifier - Group 17</div>
      <div className='pb-2 text-xl'>{latestPost && latestPost.id} / {songsToRead} Song</div>

      {/* //  Center Content */}
      <div style={{ display: 'flex', gap: '50px' }}>
        <div className='float'>
          <ScrollArea className="h-[calc(70vh-2rem)] w-[40vw] rounded-md p-4 overflow-auto text-center bg-zinc-200 text-zinc-900" style={{ whiteSpace: "pre-wrap" }} type="always">
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

          <h1 className='pb-4'>Select the Top 2 Topics you assosiate with this song: ({selectedTopics.length}/2)</h1>

          <ScrollArea className="h-[200px] w-full overflow-auto">
            <Table className='w-[500px]'>
              <TableBody>
                {topics.map((topic) => {

                  const selected = selectedTopics.includes(topic.id);
                  const rowClass = 'h-[60px] ' + (selected ? 'font-semibold text-green-500' : 'bg-transparent');
                  const color = selected ? 'rgb(169, 235, 181)' : 'white';

                  return (
                    <TableRow key={topic.id}>
                      <TableCell
                        className={rowClass}
                        onClick={() => { handleTopicChange(topic.id) }}
                        // style={{ color }}
                        >
                        {topic.name}
                      </TableCell>
                    </TableRow>
                  )
                })}
              </TableBody>
            </Table>
          </ScrollArea>

          <h3>
          Selected Topics: <span className='text-purple-400'>
            {(selectedTopics.length == 0 ?
              '<None>'
              :
              topics.filter(topic => selectedTopics.includes(topic.id)).map(topic => topic.name).join(' / ')
            )}
          </span>
          </h3>

          {/* Divide Section */}
          <div className='height-10 pb-10' />

          <h1>What decade do you think this song was written in?</h1>
          <Select.Root onValueChange={(value) => setSelectedDecade(value)}>
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

          <div>
          </div>

          <div className="pt-5 flex-col justify-items-end">
            {errorMsg && <div className="text-red-300">{errorMsg}</div>}
            <div className="">
              <Button onClick={submitHandle} variant={errorMsg ? 'destructive' : 'default'}>Submit</Button>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}