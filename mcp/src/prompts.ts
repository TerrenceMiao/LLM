export const prompts = {
  "create-greeting": {
    name: "create-greeting",
    description: "Generate a customized greeting message",
    arguments: [
      {
        name: "name",
        description: "Name of the person to greet",
        required: true,
      },
      {
        name: "style",
        description:
          "The style of greeting, such a formal, excited, or casual. If not specified casual will be used",
      },
    ],
  },
};

export const promptHandlers = {
  "create-greeting": ({
    name,
    style = "casual",
  }: {
    name: string;
    style?: string;
  }) => {
    return {
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: `Please generate a greeting in ${style} style to ${name}.`,
          },
        },
      ],
    };
  },
};
