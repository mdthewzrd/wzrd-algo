N8N Workflow Builder: Product Requirements Document (PRD) v1.0
Goals and Background Context
Goals: 1) Achieve $20,000 MRR within six months. 2) Establish market leadership. 3) Enable a rapid, high-quality MVP development process.

Background Context: This product addresses the high barrier to entry for "Automation Entrepreneurs" by providing a "Complete Implementation Kit" via an AI chat, solving the failures of existing unguided and incomplete solutions.

Change Log:
| Date | Version | Description | Author |
| :--- | :--- | :--- | :--- |
| 2025-09-09 | 1.0 | Initial draft from Project Brief | John (PM) |

Requirements
Functional Requirements: A complete set covering user accounts (FR1), subscriptions (FR2-3), the core conversational builder (FR4-7), workflow management dashboard (FR8-9), and the video-link generation feature (FR10).

Non-Functional Requirements: The system must be performant (NFR1), usable (NFR2), reliable (NFR3), and cost-effective (NFR4).

User Interface Design Goals
The application will have a simple, intuitive, and professional UX, targeting WCAG 2.1 AA accessibility. The core interaction will be a conversational chat interface on a responsive web platform.

Technical Assumptions
Repository & Architecture: A Serverless Monorepo.

Testing: A Full Testing Pyramid (Unit, Integration, E2E).

Tech Stack: Next.js (Frontend), Node.js/Vercel Functions (Backend), Convex (Database), Vercel (Hosting), Clerk (Auth), Stripe (Billing).

AI Stack: A hybrid model using Gemini 1.5 Flash (Primary Chat), Gemini 1.5 Pro (Video Analysis), and OpenAI text-embedding-3-small (Future Embeddings).

Epic & Story Structure
Epic 1: Foundation & Commercial Core
Goal: Establish the core application infrastructure, user accounts, and billing system.

Stories: 1.1 (Project Setup), 1.2 (Signup/Login), 1.3 (Subscription), 1.4 (Dashboard), 1.5 (Subscription Management).

Epic 2: The Core AI Builder Experience
Goal: Implement the primary conversational AI builder.

Stories: 2.1 (Chat UI), 2.2 (AI Integration), 2.3 (AI Confirmation Brief), 2.4 (JSON Generation).

Epic 3: Advanced Generation & Workflow Management
Goal: Enhance the core experience with advanced features.

Stories: 3.1 (Save Workflow), 3.2 (Video Link UI), 3.3 (Backend Video Analysis).

Checklist Results Report
Executive Summary: The PRD is 100% complete and ready for the architecture phase. The MVP scope is ambitious but well-defined. All sections passed validation.

Category Statuses:
| Category | Status | Critical Issues |
| :--- | :--- | :--- |
| 1. Problem Definition & Context | PASS | None |
| 2. MVP Scope Definition | PASS | None |
| 3. User Experience Requirements | PASS | None |
| 4. Functional Requirements | PASS | None |
| 5. Non-Functional Requirements | PASS | None |
| 6. Epic & Story Structure | PASS | None |
| 7. Technical Guidance | PASS | None |
| 8. Cross-Functional Requirements | PASS | None |
| 9. Clarity & Communication | PASS | None |


Final Decision: READY FOR ARCHITECT 

Final Build Plan & Technical Stack
Updated Technical Stack
AI Stack: A hybrid/routed model:

Primary Chat: Google Gemini 1.5 Flash (for cost-effective, high-volume conversations).

Video Analysis: Google Gemini 1.5 Pro (the specialist model for the "Generate from Video" feature).

Embeddings (Future): OpenAI text-embedding-3-small (for building long-term memory).

Frontend: Next.js

Backend: Serverless on Vercel

Database: Convex

Auth & Billing: Clerk & Stripe

Build Order (Epics & Stories)
Epic 1: Foundation & Commercial Core
This epic builds the essential business infrastructure.

Story 1.1: Project Initialization and Setup

Story 1.2: User Signup and Login

Story 1.3: Subscription Selection and Payment

Story 1.4: Basic Authenticated Dashboard

Story 1.5: Subscription Management

Epic 2: The Core AI Builder Experience
This epic builds the main feature of the application.

Story 2.1: Basic Chat Interface Setup

Story 2.2: Conversational AI Integration

Story 2.3: AI Confirmation Brief

Story 2.4: Final JSON Generation and Display

Epic 3: Advanced Generation & Workflow Management
This epic adds the advanced "wow" feature and user convenience.

Story 3.1: Save Workflow to Dashboard

Story 3.2: Video Link Submission Interface

Story 3.3: Backend Video Analysis and Summary