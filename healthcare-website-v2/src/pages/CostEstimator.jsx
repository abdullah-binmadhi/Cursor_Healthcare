import { useState, useMemo } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue
} from '@/components/ui/select';
import { calculateCostEstimate, procedures, insuranceTypes, departments } from '@/utils/costCalculator';
import { formatCurrency } from '@/utils/helpers';

export default function CostEstimator() {
    const [formData, setFormData] = useState({
        age: '',
        insuranceType: '',
        department: '',
        procedure: ''
    });

    const estimate = useMemo(() => {
        if (!formData.age || !formData.insuranceType || !formData.department || !formData.procedure) {
            return null;
        }
        return calculateCostEstimate({
            age: parseInt(formData.age),
            insuranceType: formData.insuranceType,
            department: formData.department,
            procedure: formData.procedure
        });
    }, [formData]);

    const updateField = (field, value) => {
        setFormData(prev => ({ ...prev, [field]: value }));
    };

    return (
        <div className="py-16 md:py-24">
            <div className="container-asymmetric">
                {/* Header */}
                <div className="max-w-xl mb-12">
                    <h1 className="font-display text-3xl md:text-4xl font-semibold text-ink tracking-tight">
                        Cost Estimator
                    </h1>
                    <p className="mt-3 text-stone-500">
                        Get transparent pricing for medical procedures.
                    </p>
                </div>

                {/* Form + Results Grid */}
                <div className="grid lg:grid-cols-2 gap-8 lg:gap-16">
                    {/* Form */}
                    <Card className="border-stone-200">
                        <CardHeader className="pb-4">
                            <CardTitle className="text-lg font-display">Patient Information</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-6">
                            <div className="space-y-2">
                                <Label htmlFor="age">Age</Label>
                                <Input
                                    id="age"
                                    type="number"
                                    min="1"
                                    max="120"
                                    placeholder="Enter age"
                                    value={formData.age}
                                    onChange={(e) => updateField('age', e.target.value)}
                                />
                            </div>

                            <div className="space-y-2">
                                <Label>Insurance Type</Label>
                                <Select value={formData.insuranceType} onValueChange={(v) => updateField('insuranceType', v)}>
                                    <SelectTrigger>
                                        <SelectValue placeholder="Select insurance" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {insuranceTypes.map(type => (
                                            <SelectItem key={type.value} value={type.value}>
                                                {type.label}
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </div>

                            <div className="space-y-2">
                                <Label>Department</Label>
                                <Select value={formData.department} onValueChange={(v) => updateField('department', v)}>
                                    <SelectTrigger>
                                        <SelectValue placeholder="Select department" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {departments.map(dept => (
                                            <SelectItem key={dept.value} value={dept.value}>
                                                {dept.label}
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </div>

                            <div className="space-y-2">
                                <Label>Procedure</Label>
                                <Select value={formData.procedure} onValueChange={(v) => updateField('procedure', v)}>
                                    <SelectTrigger>
                                        <SelectValue placeholder="Select procedure" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {procedures.map(proc => (
                                            <SelectItem key={proc.value} value={proc.value}>
                                                {proc.label}
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Results */}
                    <div>
                        {estimate ? (
                            <Card className="bg-stone-900 border-0">
                                <CardHeader className="pb-4">
                                    <CardTitle className="text-lg font-display text-white">Estimated Costs</CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    <CostRow label="Total Estimated Cost" value={formatCurrency(estimate.estimatedCost)} />
                                    <CostRow label="Insurance Coverage" value={formatCurrency(estimate.insuranceCoverage)} />
                                    <div className="border-t border-stone-700 pt-4">
                                        <CostRow
                                            label="Your Out-of-Pocket"
                                            value={formatCurrency(estimate.outOfPocket)}
                                            highlight
                                        />
                                    </div>
                                    <CostRow label="Est. Length of Stay" value={estimate.lengthOfStay} />

                                    {estimate.factors.length > 0 && (
                                        <div className="pt-4 border-t border-stone-700">
                                            <p className="text-sm text-stone-400 mb-2">Cost Factors:</p>
                                            <ul className="space-y-1">
                                                {estimate.factors.map((factor, i) => (
                                                    <li key={i} className="text-sm text-stone-300">• {factor}</li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}
                                </CardContent>
                            </Card>
                        ) : (
                            <div className="h-full flex items-center justify-center text-stone-400 text-center p-12 border border-dashed border-stone-200 rounded-lg">
                                <p>Fill in all fields to see your cost estimate</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

function CostRow({ label, value, highlight }) {
    return (
        <div className="flex justify-between items-center">
            <span className={highlight ? 'font-semibold text-white' : 'text-stone-300'}>{label}</span>
            <span className={highlight ? 'text-xl font-bold text-teal-400' : 'font-medium text-white'}>{value}</span>
        </div>
    );
}
