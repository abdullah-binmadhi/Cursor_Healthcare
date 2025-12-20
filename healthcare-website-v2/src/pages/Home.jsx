import { ArrowRight, Shield, Users, FileText } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';

export default function Home() {
    return (
        <div className="min-h-screen">
            {/* Hero - Asymmetric, purposeful */}
            <section className="py-24 md:py-32">
                <div className="container-asymmetric">
                    <div className="max-w-2xl">
                        <h1 className="font-display text-4xl md:text-6xl font-semibold text-ink tracking-tight leading-[1.1] text-balance">
                            Healthcare costs
                            <br />
                            <span className="text-stone-400">shouldn't be a mystery</span>
                        </h1>

                        <p className="mt-6 text-lg text-stone-500 max-w-lg">
                            Transparent pricing. Real physician data.
                            Make informed decisions about your care.
                        </p>

                        <div className="mt-10 flex flex-wrap gap-4">
                            <Button asChild size="lg" className="bg-accent hover:bg-accent-dark text-white">
                                <Link to="/cost">
                                    Estimate Costs
                                    <ArrowRight className="ml-2 w-4 h-4" />
                                </Link>
                            </Button>
                            <Button asChild variant="outline" size="lg">
                                <Link to="/doctors">Find Physicians</Link>
                            </Button>
                        </div>
                    </div>
                </div>
            </section>

            {/* Value Props - 3 only, minimal */}
            <section className="py-20 border-t border-stone-100">
                <div className="container-asymmetric">
                    <div className="grid md:grid-cols-3 gap-12 md:gap-16">
                        <ValueProp
                            icon={<FileText className="w-5 h-5" />}
                            title="Transparent Pricing"
                            description="See exact costs before any procedure. No hidden fees, no surprises."
                        />
                        <ValueProp
                            icon={<Users className="w-5 h-5" />}
                            title="Physician Metrics"
                            description="Access real performance data and patient satisfaction scores."
                        />
                        <ValueProp
                            icon={<Shield className="w-5 h-5" />}
                            title="Private & Secure"
                            description="HIPAA-compliant platform with bank-level encryption."
                        />
                    </div>
                </div>
            </section>

            {/* Mission - Single statement */}
            <section className="py-20 bg-stone-50">
                <div className="container-asymmetric">
                    <div className="max-w-2xl">
                        <p className="text-2xl md:text-3xl font-display text-ink leading-relaxed">
                            We believe every patient deserves to know exactly what they're paying for,
                            who they're seeing, and what outcomes to expect.
                        </p>
                        <Link
                            to="/about"
                            className="inline-flex items-center gap-2 mt-8 text-accent font-medium hover:underline"
                        >
                            Learn about our mission
                            <ArrowRight className="w-4 h-4" />
                        </Link>
                    </div>
                </div>
            </section>
        </div>
    );
}

function ValueProp({ icon, title, description }) {
    return (
        <div>
            <div className="w-10 h-10 rounded-full bg-accent/10 flex items-center justify-center text-accent mb-4">
                {icon}
            </div>
            <h3 className="font-display font-semibold text-ink text-lg mb-2">{title}</h3>
            <p className="text-stone-500 text-sm leading-relaxed">{description}</p>
        </div>
    );
}
