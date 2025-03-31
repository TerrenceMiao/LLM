export const resources = [
  {
    uri: "hello://world",
    name: "Hello World Message",
    description: "A simple greeting message",
    mimeType: "text/plain",
  },
];

export const resourceHandlers = {
  "hello://world": () => ({
    contents: [
      {
        uri: "hello://world",
        text: "Hello, World! This is my first MCP resource.",
      },
    ],
  }),
};
