# Modern Tech Stack Preferences

## The "Lazy Capitalist" Stack

### Core Philosophy
- **Minimize operational overhead** - Use managed services
- **Maximize developer velocity** - Choose productive tools
- **Scale without thinking** - Auto-scaling by default
- **Pay for what you use** - Usage-based pricing
- **Focus on product** - Not infrastructure

## Preferred Technologies

### Frontend Framework
**Next.js 14+ (App Router)**
- Server Components by default
- Built-in optimization
- Edge runtime support
- ISR/SSG/SSR flexibility
- TypeScript first

### Styling Solution
**Tailwind CSS + Shadcn/UI**
- Utility-first approach
- Component library included
- Dark mode support
- Accessible by default
- Customizable themes

### Database
**Convex**
- Real-time by default
- Type-safe queries
- Built-in auth
- Automatic caching
- Zero configuration

### Authentication
**Clerk**
- Complete auth solution
- Social logins included
- Organizations support
- Billing integration ready
- Compliance built-in

### Deployment
**Vercel**
- Git-based deployments
- Preview environments
- Edge functions
- Analytics included
- Global CDN

## Alternative Stacks

### For Enterprises
- **Frontend**: Next.js + Material-UI
- **Backend**: NestJS + GraphQL
- **Database**: PostgreSQL + Prisma
- **Auth**: Auth0
- **Deploy**: AWS/Azure

### For Startups
- **Frontend**: Remix + Tailwind
- **Backend**: Supabase
- **Database**: Supabase (PostgreSQL)
- **Auth**: Supabase Auth
- **Deploy**: Fly.io

### For MVPs
- **Frontend**: Next.js + Mantine
- **Backend**: PocketBase
- **Database**: SQLite (PocketBase)
- **Auth**: PocketBase Auth
- **Deploy**: Railway

## Decision Matrix

| Factor | Convex | Supabase | Firebase | PostgreSQL |
|--------|--------|----------|----------|------------|
| Real-time | ✅ Native | ✅ Native | ✅ Native | ❌ Needs setup |
| Type Safety | ✅ Built-in | ⚠️ With Prisma | ❌ Limited | ⚠️ With ORM |
| Scaling | ✅ Auto | ✅ Auto | ✅ Auto | ⚠️ Manual |
| Cost | 💰 Usage | 💰 Usage | 💰 Usage | 💰 Fixed |
| Learning | 🟢 Easy | 🟡 Medium | 🟡 Medium | 🔴 Hard |

## Integration Priorities

### Must Have
1. GitHub integration
2. Stripe payments
3. Email service (Resend/SendGrid)
4. Error tracking (Sentry)
5. Analytics (Vercel/Posthog)

### Nice to Have
1. CMS (Sanity/Contentful)
2. Search (Algolia/Typesense)
3. File storage (Uploadthing/S3)
4. Feature flags (LaunchDarkly)
5. Customer support (Intercom)