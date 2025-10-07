# WebApp Knowledge Base

## Tech Stack Overview

### Frontend
- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS + Shadcn/UI
- **State**: Zustand/Jotai
- **Forms**: React Hook Form + Zod
- **Animation**: Framer Motion

### Backend
- **Database**: Convex (real-time)
- **Auth**: Clerk
- **API**: Next.js API Routes + tRPC
- **Edge**: Vercel Edge Functions
- **Caching**: Redis

### Infrastructure
- **Hosting**: Vercel
- **CDN**: Vercel Edge Network
- **Monitoring**: Vercel Analytics + Sentry
- **CI/CD**: GitHub Actions + Vercel

## Development Principles

### Mobile-First Design
1. Start with 320px viewport
2. Progressive enhancement
3. Touch-friendly interactions
4. Optimized images and assets
5. Offline-first capabilities

### Performance Targets
- LCP < 2.5s
- FID < 100ms
- CLS < 0.1
- Bundle size < 200KB initial JS
- 90+ Lighthouse score

### Security Standards
- HTTPS everywhere
- CSP headers configured
- XSS protection
- SQL injection prevention
- Rate limiting
- Input validation

## Common Patterns

### Component Architecture
```typescript
// Atomic design structure
components/
  atoms/       // Button, Input, Label
  molecules/   // FormField, Card, Modal
  organisms/   // Header, Sidebar, Dashboard
  templates/   // PageLayout, AuthLayout
```

### State Management
```typescript
// Zustand store pattern
const useStore = create((set) => ({
  user: null,
  setUser: (user) => set({ user }),
}))
```

### API Route Pattern
```typescript
// Type-safe API with tRPC
const appRouter = router({
  user: {
    get: publicProcedure
      .input(z.object({ id: z.string() }))
      .query(({ input }) => {
        return getUserById(input.id)
      }),
  },
})
```

## Best Practices

### Code Quality
- ESLint + Prettier configured
- Husky pre-commit hooks
- Unit tests (Jest)
- E2E tests (Playwright)
- 80% coverage target

### Git Workflow
- Feature branches
- Conventional commits
- PR reviews required
- Automated testing
- Preview deployments

### Documentation
- README with setup instructions
- API documentation (OpenAPI)
- Component documentation (Storybook)
- Architecture decisions (ADRs)
- Deployment guides