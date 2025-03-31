export const resourceTemplates = [
  {
    uriTemplate: "greetings://{name}",
    name: "Personal Greeting",
    description: "A personalized greeting message",
    mimeType: "text/plain",
  },
];

const greetingExp = /^greetings:\/\/(.+)$/;
const greetingMatchHandler =
  (uri: string, matchText: RegExpMatchArray) => () => {
    const name = decodeURIComponent(matchText[1]);
    return {
      contents: [
        {
          uri,
          text: `Hello, ${name}! Welcome to MCP.`,
        },
      ],
    };
  };

export const getResourceTemplate = (uri: string) => {
  const greetingMatch = uri.match(greetingExp);
  if (greetingMatch) return greetingMatchHandler(uri, greetingMatch);
};
