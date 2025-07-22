# Copilot Instructions for `ai-local-comp`

## Overview
This repository contains a React-based UI application built with Vite. The project is structured to facilitate modular development, with components organized under the `src/components` directory. Styling is managed using Material-UI (`@mui/material`) and Emotion (`@emotion/react`, `@emotion/styled`).

## Key Components
- **`src/components/`**: Contains reusable React components such as `LogViewer`, `MessageAlert`, `ModelSelector`, `PullModel`, and `SaveButton`.
- **`src/main.jsx`**: Entry point for the React application.
- **`vite.config.js`**: Configuration file for Vite.

## Developer Workflows
### Development
To start the development server:
```bash
npm run dev
```
This will launch the Vite development server and enable hot module replacement (HMR).

### Build
To create a production build:
```bash
npm run build
```
The output will be placed in the `dist` directory.

### Preview
To preview the production build:
```bash
npm run preview
```
This serves the `dist` directory locally.

## Project-Specific Conventions
- **Styling**: Use Material-UI and Emotion for consistent theming and styling.
- **Component Structure**: Each component should be self-contained, with its logic and styles encapsulated.
- **File Naming**: Use PascalCase for component files (e.g., `LogViewer.jsx`).

## External Dependencies
- **Material-UI**: Provides pre-styled UI components.
- **Emotion**: Enables CSS-in-JS styling.
- **Vite**: A fast build tool optimized for modern web development.

## Example Patterns
### Creating a New Component
1. Create a new file in `src/components` (e.g., `NewComponent.jsx`).
2. Use the following template:
```jsx
import React from 'react';
import { Box } from '@mui/material';

const NewComponent = () => {
  return (
    <Box>
      {/* Your component code here */}
    </Box>
  );
};

export default NewComponent;
```

### Adding Styles
Use Emotion's `styled` API:
```jsx
import styled from '@emotion/styled';

const StyledBox = styled.div`
  background-color: #f0f0f0;
  padding: 16px;
`;
```

## Notes
- Ensure all new components are added to the appropriate parent component or routing structure in `App.jsx`.
- Follow the existing patterns for state management and props usage.

For further questions or clarifications, refer to the `README.md` or contact the repository maintainers.
