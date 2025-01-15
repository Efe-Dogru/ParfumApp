# Parfum App Frontend

A modern web application for discovering and exploring perfumes, built with Nuxt.js 3, Vue 3, and TailwindCSS.

## Features

- Browse perfume collection
- Search perfumes by name, brand, or notes
- View detailed perfume information
- Responsive design
- Modern UI with Shadcn Vue components

## Tech Stack

- Nuxt.js 3
- Vue 3 (Composition API)
- TypeScript
- TailwindCSS
- Shadcn Vue
- Radix Vue
- VueUse
- Pinia (State Management)

## Prerequisites

- Node.js 18.x or later
- pnpm (recommended) or npm

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd parfum-app
```

2. Install dependencies:
```bash
pnpm install
```

3. Create a `.env` file in the root directory and add your environment variables:
```bash
NUXT_PUBLIC_API_BASE=http://localhost:8000
```

4. Start the development server:
```bash
pnpm dev
```

The application will be available at `http://localhost:3000`.

## Build

To build the application for production:

```bash
pnpm build
```

## Project Structure

```
├── components/       # Vue components
├── composables/     # Composable functions
├── layouts/         # Page layouts
├── pages/          # Application pages
├── public/         # Static files
├── server/         # Server API routes
├── types/          # TypeScript types
└── utils/          # Utility functions
```

## Development Guidelines

- Follow the Vue 3 Composition API patterns
- Use TypeScript for type safety
- Implement responsive design with Tailwind CSS
- Follow the established naming conventions
- Write clean, maintainable code
- Use Nuxt's built-in features when possible

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

[MIT License](LICENSE) 