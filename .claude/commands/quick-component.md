# Quick Component Command

## Description
Generate a component with mobile-first design and TypeScript

## Usage
```
/quick-component [component-name] [component-type]
```

## Component Types
- `atom` - Basic UI element (Button, Input, Label)
- `molecule` - Composed element (FormField, Card, Modal)
- `organism` - Complex component (Header, Sidebar, Dashboard)
- `template` - Page layout (AuthLayout, DashboardLayout)

## Process
1. **Design Phase** (webapp-ui-designer)
   - Mobile-first layout
   - Responsive breakpoints
   - Accessibility attributes
   - Tailwind classes

2. **Architecture Phase** (webapp-component-architect)
   - TypeScript interfaces
   - Props validation
   - State management
   - Performance optimization

## Example
```
/quick-component UserCard molecule
```

## Output Structure
```
components/
  molecules/
    UserCard/
      UserCard.tsx
      UserCard.types.ts
      UserCard.stories.tsx
      UserCard.test.tsx
      index.ts
```

## Features
- Mobile-first responsive design
- TypeScript with strict typing
- Tailwind CSS styling
- Shadcn/UI integration
- Accessibility compliant
- Unit tests included
- Storybook stories