import {
  ListResourcesRequestSchema,
  ListResourceTemplatesRequestSchema,
  ReadResourceRequestSchema,
  GetPromptRequestSchema,
  ListPromptsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { type Server } from "@modelcontextprotocol/sdk/server/index.js";
import { resourceHandlers, resources } from "./resources.js";
import {
  getResourceTemplate,
  resourceTemplates,
} from "./resource-templates.js";
import { promptHandlers, prompts } from "./prompts.js";

export const setupHandlers = (server: Server): void => {
  // List available resources when clients request them
  server.setRequestHandler(ListResourcesRequestSchema, () => ({ resources }));

  // Resource Templates
  server.setRequestHandler(ListResourceTemplatesRequestSchema, () => ({
    resourceTemplates,
  }));

  // Prompts
  server.setRequestHandler(ListPromptsRequestSchema, () => ({
    prompts: Object.values(prompts),
  }));

  // Return resource content when clients request it
  server.setRequestHandler(ReadResourceRequestSchema, (request) => {
    const { uri } = request.params ?? {};
    const resourceHandler =
      resourceHandlers[uri as keyof typeof resourceHandlers];

    if (resourceHandler) return resourceHandler();

    const resourceTemplateHandler = getResourceTemplate(uri);

    if (resourceTemplateHandler) return resourceTemplateHandler();

    throw new Error("Resource not found");
  });

  server.setRequestHandler(GetPromptRequestSchema, (request) => {
    const { name, arguments: args } = request.params;
    const promptHandler = promptHandlers[name as keyof typeof promptHandlers];

    if (promptHandler)
      return promptHandler(args as { name: string; style?: string });

    throw new Error("Prompt not found");
  });
};
