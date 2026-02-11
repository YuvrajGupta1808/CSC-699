# JobSkill

Match your skills with job opportunities through intelligent analysis of transcripts, resumes, and job postings.

## Features

- Upload and analyze academic transcripts and resumes
- Discover job opportunities with skill matching
- View detailed skill breakdowns for each position
- Track skill gaps and development areas

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

### Available Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
npm test             # Run tests
npm run test:watch   # Run tests in watch mode
```

## Tech Stack

- React 18 with TypeScript
- Vite for build tooling
- React Router for navigation
- Tailwind CSS for styling
- shadcn/ui component library
- Tanstack Query for data fetching

## Project Structure

```
client/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/          # Page components
│   ├── data/           # Mock data and types
│   ├── lib/            # Utility functions
│   └── hooks/          # Custom React hooks
├── public/             # Static assets
└── dist/               # Production build output
```

## Deployment

Build the project for production:

```bash
npm run build
```

The optimized build will be in the `dist` directory, ready to deploy to any static hosting service.

