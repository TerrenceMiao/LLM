import {
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
  ListResourceTemplatesRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { type Server } from "@modelcontextprotocol/sdk/server/index.js";

export const setupHandlers = (server: Server): void => {
  // List available resources when clients request them
  server.setRequestHandler(ListResourcesRequestSchema, async () => {
    return {
      resources: [
        {
          uri: "hello://world",
          name: "Hello World Message",
          description: "A simple greeting message",
          mimeType: "text/plain",
        },
      ],
    };
  });

  // Resource Templates
  server.setRequestHandler(ListResourceTemplatesRequestSchema, async () => ({
    resourceTemplates: [
      {
        greetings: {
          uriTemplate: "greetings://{name}",
          name: "Personal Greeting",
          description: "A personalized greeting message",
          mimeType: "text/plain",
        },
      },
    ],
  }));

  // Return resource content when clients request it
  server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
    if (request.params.uri === "hello://world") {
      return {
        contents: [
          {
            uri: "hello://world",
            text: "Hello, World! This is my first MCP resource.",
          },
        ],
      };
    }

    // Template-based resource code
    const greetingExp = /^greetings:\/\/(.+)$/;
    const greetingMatch = request.params.uri.match(greetingExp);
    if (greetingMatch) {
      const name = decodeURIComponent(greetingMatch[1]);
      return {
        contents: [
          {
            uri: request.params.uri,
            text: `Hello, ${name}! Welcome to MCP.`,
          },
        ],
      };
    }

    throw new Error("Resource not found");
  });
};
