import { z } from "zod";

import { createTRPCRouter, publicProcedure } from "~/server/api/trpc";

export const postRouter = createTRPCRouter({
  hello: publicProcedure
    .input(z.object({ text: z.string() }))
    .query(({ input }) => {
      return {
        greeting: `Hello ${input.text}`,
      };
    }),

    updateAnnotation: publicProcedure
      .input(z.object({
        id: z.number(),
        recognized: z.string(),
        topics: z.array(z.string()),
        decade: z.string(),
      }))
      .mutation(async ({ input, ctx }) => {
        const updatedAnnotation = await ctx.db.song.update({
          where: { id: input.id },
          data: {
            recognized: input.recognized == "yes" ? 1 : 0,
            topic1: input.topics[0],
            topic2: input.topics[1],
            decade: parseInt(input.decade, 10),
          },
        });
        return updatedAnnotation;
      }),

    getLatest: publicProcedure.query(async ({ ctx }) => {
    const post = await ctx.db.song.findFirst({
      orderBy: { id: "desc" },
    });

    return post ?? null;
  }),
});
