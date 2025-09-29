"use client";

import { useAuth, SignInButton, SignUpButton } from "@clerk/nextjs";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Activity,
  BarChart3,
  CheckCircle,
  Clock,
  Globe,
  Package,
  Shield,
  TrendingUp,
  Users,
  Zap,
  ArrowRight,
  Sparkles,
  Lock,
  RefreshCw,
  Target,
  Layers,
} from "lucide-react";

export default function Home() {
  const { isSignedIn, isLoaded } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (isLoaded && isSignedIn) {
      router.push("/dashboard");
    }
  }, [isLoaded, isSignedIn, router]);

  if (!isLoaded) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <RefreshCw className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-blue-900">
      {/* Navigation */}
      <nav className="border-b bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-2">
              <Zap className="h-8 w-8 text-blue-600" />
              <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                SMM Drip Feed Pro
              </span>
            </div>
            <div className="flex gap-4">
              <SignInButton mode="modal">
                <Button variant="outline">Sign In</Button>
              </SignInButton>
              <SignUpButton mode="modal">
                <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                  Get Started
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </SignUpButton>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container mx-auto px-6 py-24">
        <div className="text-center max-w-4xl mx-auto">
          <Badge className="mb-4 bg-blue-100 text-blue-800">
            <Sparkles className="h-3 w-3 mr-1" />
            Powered by Parallel Processing & Real-time Analytics
          </Badge>
          <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-300 bg-clip-text text-transparent">
            Enterprise-Grade SMM
            <br />
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Drip Feed Automation
            </span>
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 mb-8 leading-relaxed">
            Transform your social media marketing with intelligent drip feeding.
            <br />
            Parallel workers, real-time monitoring, and 99.9% reliability.
          </p>
          <div className="flex gap-4 justify-center">
            <SignUpButton mode="modal">
              <Button size="lg" className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                Start Free Trial
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </SignUpButton>
            <Button size="lg" variant="outline">
              Watch Demo
            </Button>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="bg-white/60 dark:bg-gray-900/60 backdrop-blur-sm py-16">
        <div className="container mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-600 mb-2">99.9%</div>
              <div className="text-gray-600 dark:text-gray-400">Uptime SLA</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-purple-600 mb-2">10M+</div>
              <div className="text-gray-600 dark:text-gray-400">Orders Processed</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-green-600 mb-2">&lt;100ms</div>
              <div className="text-gray-600 dark:text-gray-400">Processing Time</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-orange-600 mb-2">24/7</div>
              <div className="text-gray-600 dark:text-gray-400">Parallel Processing</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="container mx-auto px-6 py-24">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">
            Everything You Need to Scale
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-400">
            Professional tools for serious SMM operations
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <FeatureCard
            icon={<Layers className="h-8 w-8" />}
            title="Parallel Workers"
            description="Process multiple campaigns simultaneously with our distributed worker architecture. No bottlenecks, just pure speed."
            gradient="from-blue-500 to-cyan-500"
          />
          <FeatureCard
            icon={<Target className="h-8 w-8" />}
            title="Smart Drip Patterns"
            description="6 intelligent delivery patterns including Natural Growth, Viral Spike, and Pulse. Mimic authentic engagement."
            gradient="from-purple-500 to-pink-500"
          />
          <FeatureCard
            icon={<BarChart3 className="h-8 w-8" />}
            title="Real-time Analytics"
            description="Monitor campaigns with live updates. Track delivery rates, success metrics, and performance in real-time."
            gradient="from-green-500 to-emerald-500"
          />
          <FeatureCard
            icon={<Shield className="h-8 w-8" />}
            title="Circuit Breakers"
            description="Automatic failure detection and recovery. Smart retry logic with exponential backoff keeps your campaigns running."
            gradient="from-orange-500 to-red-500"
          />
          <FeatureCard
            icon={<Package className="h-8 w-8" />}
            title="Service Packages"
            description="Bundle multiple services into reusable packages. Launch complex campaigns with a single click."
            gradient="from-indigo-500 to-purple-500"
          />
          <FeatureCard
            icon={<Lock className="h-8 w-8" />}
            title="Enterprise Security"
            description="Military-grade encryption for API keys. Row-level security, audit logs, and compliance-ready infrastructure."
            gradient="from-gray-600 to-gray-800"
          />
        </div>
      </section>

      {/* Drip Styles Showcase */}
      <section className="bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-900 dark:to-gray-800 py-24">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">
              Intelligent Drip Feed Algorithms
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400">
              Choose from 6 sophisticated delivery patterns
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <DripStyleCard
              name="Uniform Distribution"
              description="Steady, consistent delivery for maximum authenticity"
              pattern="━━━━━━━━━━"
            />
            <DripStyleCard
              name="Ramp Up"
              description="Start slow, accelerate gradually like viral growth"
              pattern="▁▂▃▄▅▆▇█"
            />
            <DripStyleCard
              name="Ramp Down"
              description="Fast start with natural decay over time"
              pattern="█▇▆▅▄▃▂▁"
            />
            <DripStyleCard
              name="Pulse Pattern"
              description="Oscillating waves mimicking daily activity cycles"
              pattern="▂█▂█▂█▂█"
            />
            <DripStyleCard
              name="Natural Growth"
              description="Sigmoid curve following organic growth patterns"
              pattern="▁▂▄█▇▅▃▂"
            />
            <DripStyleCard
              name="Viral Spike"
              description="Explosive growth with realistic tapering"
              pattern="▁▁█▇▅▃▂▁"
            />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-6 py-24">
        <Card className="bg-gradient-to-r from-blue-600 to-purple-600 text-white border-0">
          <CardContent className="p-12 text-center">
            <h2 className="text-4xl font-bold mb-4">
              Ready to Transform Your SMM Operations?
            </h2>
            <p className="text-xl mb-8 opacity-90">
              Join thousands of agencies achieving 10x growth with intelligent automation
            </p>
            <div className="flex gap-4 justify-center">
              <SignUpButton mode="modal">
                <Button size="lg" variant="secondary">
                  Start Free Trial
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </SignUpButton>
              <Button size="lg" variant="outline" className="text-white border-white hover:bg-white/20">
                Schedule Demo
              </Button>
            </div>
            <p className="mt-6 text-sm opacity-75">
              No credit card required • 14-day free trial • Cancel anytime
            </p>
          </CardContent>
        </Card>
      </section>

      {/* Footer */}
      <footer className="border-t bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm">
        <div className="container mx-auto px-6 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <Zap className="h-6 w-6 text-blue-600" />
                <span className="text-xl font-bold">SMM Drip Feed Pro</span>
              </div>
              <p className="text-gray-600 dark:text-gray-400">
                Enterprise-grade SMM automation platform
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Product</h3>
              <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                <li>Features</li>
                <li>Pricing</li>
                <li>API Docs</li>
                <li>Integrations</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                <li>About</li>
                <li>Blog</li>
                <li>Careers</li>
                <li>Contact</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Legal</h3>
              <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                <li>Privacy</li>
                <li>Terms</li>
                <li>Security</li>
                <li>Compliance</li>
              </ul>
            </div>
          </div>
          <div className="mt-12 pt-8 border-t text-center text-gray-600 dark:text-gray-400">
            <p>© 2025 SMM Drip Feed Pro. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, description, gradient }) {
  return (
    <Card className="hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
      <CardHeader>
        <div className={`inline-flex p-3 rounded-lg bg-gradient-to-br ${gradient} text-white mb-4`}>
          {icon}
        </div>
        <CardTitle className="text-xl">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <CardDescription className="text-base">{description}</CardDescription>
      </CardContent>
    </Card>
  );
}

function DripStyleCard({ name, description, pattern }) {
  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader>
        <CardTitle className="text-lg">{name}</CardTitle>
        <div className="text-3xl font-mono text-blue-600 my-2">{pattern}</div>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
    </Card>
  );
}