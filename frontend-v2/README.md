# Parfum App - Frontend

A modern web application for perfume enthusiasts to explore, discover, and learn about different fragrances. This application provides a comprehensive platform for users to browse perfumes, understand their notes, and explore various aspects of fragrances.

## 🌟 Features

- **Perfume Catalog**: Browse through an extensive collection of perfumes with detailed information
- **Detailed Perfume Views**: Access comprehensive information about each perfume including:
  - Notes (top, middle, base)
  - Brand information
  - Concentration
  - Release year
  - Seasonality
  - Longevity and sillage
  - Country of origin
  - Perfumer details
  - Occasions
  - Main accords

- **Note Explorer**: Discover and learn about different fragrance notes
- **Responsive Design**: Beautiful and functional across all device sizes
- **Modern UI**: Built with Shadcn UI components for a sleek, modern look
- **Dark/Light Mode**: Support for different color schemes

## 🛠️ Technology Stack

- **Framework**: Nuxt.js 3
- **Language**: TypeScript
- **UI Framework**: Vue.js
- **Styling**: 
  - TailwindCSS
  - Shadcn UI Components
  - Radix Vue
- **State Management**: Vue Composition API with Nuxt Composables
- **Database Integration**: Supabase
- **Additional Libraries**:
  - @vueuse/core - Vue Composition Utilities
  - lucide-vue-next - Icon System
  - class-variance-authority - Component Styling
  - tailwindcss-animate - Animations

## 🚀 Getting Started

### Prerequisites

- Node.js (Latest LTS version recommended)
- npm or yarn package manager

### Installation

1. Clone the repository
2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

4. Start the development server:
```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`

## 📁 Project Structure

- `/components` - Reusable Vue components
  - `/custom` - Custom application components
  - `/ui` - Shadcn UI components
- `/composables` - Vue composables for state and logic management
- `/pages` - Application routes and page components
- `/types` - TypeScript type definitions
- `/utils` - Utility functions
- `/assets` - Static assets and global styles
- `/layouts` - Page layouts
- `/server` - Server-side code and API routes

## 🔧 Configuration

- `nuxt.config.ts` - Nuxt.js configuration
- `tailwind.config.js` - TailwindCSS configuration
- `components.json` - Shadcn UI configuration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
