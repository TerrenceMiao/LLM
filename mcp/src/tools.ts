// Allowed values
const messageTypes = ["greeting", "farewell", "thank-you"] as const;
const tones = ["formal", "casual", "playful"] as const;

// tool definitions
export const tools = {
  "create-message": {
    name: "create-message",
    description: "Generate a custom message with various options",
    inputSchema: {
      type: "object",
      properties: {
        messageType: {
          type: "string",
          enum: messageTypes,
          description: "Type of message to generate",
        },
        recipient: {
          type: "string",
          description: "Name of the person to address",
        },
        tone: {
          type: "string",
          enum: tones,
          description: "Tone of the message",
        },
      },
      required: ["messageType", "recipient"],
    },
  },
};

type CreateMessageArgs = {
  messageType: (typeof messageTypes)[number];
  recipient: string;
  tone?: (typeof tones)[number];
};

// Simple templates for the various message combinations
const messageFns = {
  greeting: {
    formal: (recipient: string) =>
      `Dear ${recipient}, I hope this message finds you well`,
    playful: (recipient: string) => `Hey hey ${recipient}! 🎉 What's shakin'?`,
    casual: (recipient: string) => `Hi ${recipient}! How are you?`,
  },
  farewell: {
    formal: (recipient: string) =>
      `Best regards, ${recipient}. Until we meet again.`,
    playful: (recipient: string) =>
      `Catch you later, ${recipient}! 👋 Stay awesome!`,
    casual: (recipient: string) => `Goodbye ${recipient}, take care!`,
  },
  "thank-you": {
    formal: (recipient: string) =>
      `Dear ${recipient}, I sincerely appreciate your assistance.`,
    playful: (recipient: string) =>
      `You're the absolute best, ${recipient}! 🌟 Thanks a million!`,
    casual: (recipient: string) =>
      `Thanks so much, ${recipient}! Really appreciate it!`,
  },
};

const createMessage = (args: CreateMessageArgs) => {
  if (!args.messageType) throw new Error("Must provide a message type.");
  if (!args.recipient) throw new Error("Must provide a recipient.");

  const { messageType, recipient } = args;
  const tone = args.tone || "casual";
  if (!messageTypes.includes(messageType)) {
    throw new Error(
      `Message type must be one of the following: ${messageTypes.join(", ")}`
    );
  }
  if (!tones.includes(tone)) {
    throw new Error(
      `If tone is provided, it must be one of the following: ${tones.join(
        ", "
      )}`
    );
  }

  const message = messageFns[messageType][tone](recipient);

  return {
    content: [
      {
        type: "text",
        text: message,
      },
    ],
  };
};

export const toolHandlers = {
  "create-message": createMessage,
};
