This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

## Application skeleton

Set up a NEXT.js applicaiton:

```bash
$ npx create-next-app@latest --ts --tailwind --eslint
✔ What is your project named? … gemini
✔ Would you like to use `src/` directory? … No / Yes
✔ Would you like to use App Router? (recommended) … No / Yes
✔ Would you like to customize the default import alias (@/*)? … No / Yes
Creating a new Next.js app in /Users/terrence/Projects/LLM/gemini.

Using npm.

Initializing project with template: app-tw

Installing dependencies:
- react
- react-dom
- next

Installing devDependencies:
- typescript
- @types/node
- @types/react
- @types/react-dom
- autoprefixer
- postcss
- tailwindcss
- eslint
- eslint-config-next

added 333 packages, and audited 334 packages in 3s

117 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
Success! Created gemini at /Users/terrence/Projects/LLM/gemini
```

Add dependencies:

```bash
$ npm install ai openai silence-aware-recorder @wmik/use-media-recorder merge-images

added 69 packages, and audited 403 packages in 17s

119 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
```

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/basic-features/font-optimization) to automatically optimize and load Inter, a custom Google Font.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js/) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/deployment) for more details.

## References

- Recreating the experience of the staged Gemini demo, but for real — using GPT4 Vision and Whisper, _https://jidefr.medium.com/recreating-the-experience-of-the-staged-gemini-demo-but-for-real-using-gpt4-vision-and-whisper-fc559c38bd24_
- GPT Video - Reproducing the Gemini demo using GPT 4 Vision, _https://github.com/jide/gpt-video_
