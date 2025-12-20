import { Card, CardContent } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';

export default function About() {
    return (
        <div className="py-16 md:py-24">
            <div className="container-asymmetric">
                {/* Header */}
                <div className="max-w-2xl mb-16">
                    <h1 className="font-display text-3xl md:text-4xl font-semibold text-ink tracking-tight">
                        About
                    </h1>
                    <p className="mt-6 text-lg text-stone-600 leading-relaxed">
                        We believe healthcare should be transparent, accessible, and data-driven.
                        Our platform empowers patients and providers with real-time insights,
                        accurate cost estimates, and performance analytics.
                    </p>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-16">
                    <Stat value="500+" label="Healthcare Providers" />
                    <Stat value="10K+" label="Cost Estimates" />
                    <Stat value="98%" label="Accuracy Rate" />
                    <Stat value="24/7" label="Live Analytics" />
                </div>

                <Separator className="my-16" />

                {/* Mission */}
                <div className="max-w-2xl">
                    <h2 className="font-display text-xl font-semibold text-ink mb-4">Our Mission</h2>
                    <p className="text-stone-600 leading-relaxed mb-6">
                        Healthcare has been shrouded in secrecy for too long. We believe every patient
                        deserves to know exactly what they're paying for, who they're seeing, and what
                        outcomes to expect.
                    </p>
                    <p className="text-stone-600 leading-relaxed">
                        Our platform tears down the walls of healthcare opacity, putting transparent
                        data and clear pricing directly in your hands.
                    </p>
                </div>

                <Separator className="my-16" />

                {/* Contact */}
                <Card className="max-w-md border-stone-200">
                    <CardContent className="p-6">
                        <h2 className="font-display font-semibold text-ink mb-4">Contact</h2>
                        <div className="space-y-2 text-sm text-stone-600">
                            <p><span className="text-stone-400">Email:</span> support@healthcareanalytics.com</p>
                            <p><span className="text-stone-400">Phone:</span> (555) 123-4567</p>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}

function Stat({ value, label }) {
    return (
        <div className="text-center">
            <div className="font-display text-3xl md:text-4xl font-semibold text-accent mb-1">
                {value}
            </div>
            <div className="text-sm text-stone-500">{label}</div>
        </div>
    );
}
