import { useState, useMemo } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue
} from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    LineElement,
    PointElement,
    ArcElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Bar, Doughnut } from 'react-chartjs-2';
import {
    healthcareDataByYear,
    hospitals,
    physicians,
    patientsByCondition,
    billingByCondition,
    patientsByInsurance,
    admissionTypes,
    ageDistribution
} from '@/data/healthcareData';
import { formatCurrency } from '@/utils/helpers';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    LineElement,
    PointElement,
    ArcElement,
    Title,
    Tooltip,
    Legend
);

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { display: false },
    },
    scales: {
        x: {
            grid: { display: false },
            ticks: { font: { size: 11 } }
        },
        y: {
            grid: { color: '#f5f5f4' },
            ticks: { font: { size: 11 } }
        }
    }
};

const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'bottom',
            labels: { font: { size: 11 }, padding: 15 }
        },
    }
};

// Color palettes
const conditionColors = ['#115e59', '#14b8a6', '#0d9488', '#2dd4bf', '#5eead4', '#99f6e4'];
const insuranceColors = ['#1e3a5f', '#2563eb', '#3b82f6', '#60a5fa', '#93c5fd'];
const admissionColors = ['#dc2626', '#f59e0b', '#16a34a'];

export default function Analytics() {
    const [selectedYear, setSelectedYear] = useState(2024);
    const [selectedHospital, setSelectedHospital] = useState('all');
    const [activeTab, setActiveTab] = useState('overview'); // overview, patients, billing

    const yearData = healthcareDataByYear[selectedYear];

    const departments = useMemo(() => {
        if (!yearData?.departments) return [];
        return yearData.departments['all'] || [];
    }, [yearData]);

    const filteredPhysicians = useMemo(() => {
        if (selectedHospital === 'all') return physicians;
        return physicians.filter(p => p.hospital === selectedHospital);
    }, [selectedHospital]);

    // Top Physicians by rating
    const topPhysicians = [...filteredPhysicians]
        .sort((a, b) => b.rating - a.rating)
        .slice(0, 6);

    // ============= CHARTS DATA =============

    // Patients by Medical Condition
    const conditionChartData = {
        labels: Object.keys(patientsByCondition),
        datasets: [{
            data: Object.values(patientsByCondition),
            backgroundColor: conditionColors,
            borderWidth: 0,
        }]
    };

    // Billing by Condition (bar chart)
    const billingChartData = {
        labels: Object.keys(billingByCondition),
        datasets: [{
            data: Object.values(billingByCondition),
            backgroundColor: '#115e59',
            borderRadius: 4,
        }]
    };

    // Insurance Distribution
    const insuranceChartData = {
        labels: Object.keys(patientsByInsurance),
        datasets: [{
            data: Object.values(patientsByInsurance),
            backgroundColor: insuranceColors,
            borderWidth: 0,
        }]
    };

    // Admission Types
    const admissionChartData = {
        labels: Object.keys(admissionTypes),
        datasets: [{
            data: Object.values(admissionTypes),
            backgroundColor: admissionColors,
            borderWidth: 0,
        }]
    };

    // Age Distribution
    const ageChartData = {
        labels: Object.keys(ageDistribution),
        datasets: [{
            data: Object.values(ageDistribution),
            backgroundColor: '#14b8a6',
            borderRadius: 4,
        }]
    };

    // Department Performance
    const deptChartData = {
        labels: departments.map(d => d.department_name),
        datasets: [{
            data: departments.map(d => d.patient_satisfaction),
            backgroundColor: '#115e59',
            borderRadius: 4,
        }]
    };

    // Top Physicians Chart
    const physChartData = {
        labels: topPhysicians.map(p => `Dr. ${p.lastName}`),
        datasets: [{
            data: topPhysicians.map(p => p.rating),
            backgroundColor: '#14b8a6',
            borderRadius: 4,
        }]
    };

    return (
        <div className="py-16 md:py-24">
            <div className="container-asymmetric">
                {/* Header */}
                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
                    <div>
                        <h1 className="font-display text-3xl md:text-4xl font-semibold text-ink tracking-tight">
                            Analytics Dashboard
                        </h1>
                        <p className="mt-2 text-stone-500">
                            55,500 patient records • 52 physicians
                        </p>
                    </div>
                </div>

                {/* Tab Navigation */}
                <div className="flex gap-2 mb-8 border-b border-stone-200 pb-2">
                    {[
                        { id: 'overview', label: 'Overview' },
                        { id: 'patients', label: 'Patient Data' },
                        { id: 'billing', label: 'Billing & Insurance' },
                    ].map(tab => (
                        <Button
                            key={tab.id}
                            variant="ghost"
                            size="sm"
                            onClick={() => setActiveTab(tab.id)}
                            className={activeTab === tab.id ? 'text-stone-900 font-semibold' : 'text-stone-500'}
                        >
                            {tab.label}
                        </Button>
                    ))}
                </div>

                {/* Overview Tab - Enhanced Dashboard */}
                {activeTab === 'overview' && (
                    <div className="space-y-6">
                        {/* KPI Summary Cards */}
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            <Card className="border-stone-200 bg-gradient-to-br from-emerald-50 to-white">
                                <CardContent className="pt-6">
                                    <p className="text-sm text-stone-500 font-medium">Total Patients</p>
                                    <p className="text-2xl md:text-3xl font-bold text-ink mt-1">55,500</p>
                                    <p className="text-xs text-emerald-600 mt-2">↑ 8.3% vs last year</p>
                                </CardContent>
                            </Card>
                            <Card className="border-stone-200 bg-gradient-to-br from-blue-50 to-white">
                                <CardContent className="pt-6">
                                    <p className="text-sm text-stone-500 font-medium">Active Physicians</p>
                                    <p className="text-2xl md:text-3xl font-bold text-ink mt-1">52</p>
                                    <p className="text-xs text-stone-500 mt-2">Across 8 hospitals</p>
                                </CardContent>
                            </Card>
                            <Card className="border-stone-200 bg-gradient-to-br from-amber-50 to-white">
                                <CardContent className="pt-6">
                                    <p className="text-sm text-stone-500 font-medium">Avg. Satisfaction</p>
                                    <p className="text-2xl md:text-3xl font-bold text-ink mt-1">4.3/5</p>
                                    <p className="text-xs text-emerald-600 mt-2">↑ 0.2 improvement</p>
                                </CardContent>
                            </Card>
                            <Card className="border-stone-200 bg-gradient-to-br from-rose-50 to-white">
                                <CardContent className="pt-6">
                                    <p className="text-sm text-stone-500 font-medium">Avg. Occupancy</p>
                                    <p className="text-2xl md:text-3xl font-bold text-ink mt-1">76%</p>
                                    <p className="text-xs text-amber-600 mt-2">Optimal range</p>
                                </CardContent>
                            </Card>
                        </div>

                        {/* Static Charts Row - Top Physicians & Admission Types */}
                        <div className="grid md:grid-cols-2 gap-6">
                            {/* Top Physicians */}
                            <Card className="border-stone-200">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-base font-display">Top Rated Physicians</CardTitle>
                                    <p className="text-sm text-stone-500">52 physicians in network</p>
                                </CardHeader>
                                <CardContent>
                                    <div className="h-72">
                                        <Bar
                                            data={physChartData}
                                            options={{
                                                ...chartOptions,
                                                indexAxis: 'y',
                                                scales: {
                                                    ...chartOptions.scales,
                                                    x: { ...chartOptions.scales.x, max: 5 }
                                                }
                                            }}
                                        />
                                    </div>
                                </CardContent>
                            </Card>

                            {/* Admission Types */}
                            <Card className="border-stone-200">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-base font-display">Admission Types</CardTitle>
                                    <p className="text-sm text-stone-500">Patient intake distribution</p>
                                </CardHeader>
                                <CardContent>
                                    <div className="h-72">
                                        <Doughnut data={admissionChartData} options={doughnutOptions} />
                                    </div>
                                </CardContent>
                            </Card>
                        </div>

                        {/* Hospital Distribution */}
                        <Card className="border-stone-200">
                            <CardHeader className="pb-2">
                                <CardTitle className="text-base font-display">Physicians by Hospital</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
                                    {[
                                        { name: 'City General Hospital', count: 8, rating: 4.7 },
                                        { name: "St. Mary's Medical Center", count: 7, rating: 4.5 },
                                        { name: 'University Health System', count: 8, rating: 4.8 },
                                        { name: 'Memorial Hospital', count: 6, rating: 4.4 },
                                        { name: 'Regional Medical Center', count: 7, rating: 4.6 },
                                        { name: 'Community Health Hospital', count: 6, rating: 4.5 },
                                        { name: 'Metropolitan Medical Center', count: 7, rating: 4.7 },
                                        { name: 'Riverside Hospital', count: 5, rating: 4.4 },
                                    ].map((hospital, i) => (
                                        <div key={i} className="p-3 bg-stone-50 rounded-lg">
                                            <p className="font-medium text-ink text-sm truncate">{hospital.name}</p>
                                            <div className="flex justify-between mt-2 text-sm">
                                                <span className="text-stone-500">{hospital.count} doctors</span>
                                                <span className="font-semibold text-amber-600">★ {hospital.rating}</span>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </CardContent>
                        </Card>

                        {/* Department Analytics Section - Year Dependent */}
                        <div className="border-t border-stone-200 pt-6">
                            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
                                <div>
                                    <h2 className="font-display text-xl font-semibold text-ink">Department Analytics</h2>
                                    <p className="text-sm text-stone-500">Performance metrics by year</p>
                                </div>
                                <div className="flex gap-1 bg-stone-100 p-1 rounded-lg">
                                    {[2024, 2023, 2022].map(year => (
                                        <Button
                                            key={year}
                                            variant={selectedYear === year ? 'default' : 'ghost'}
                                            size="sm"
                                            onClick={() => setSelectedYear(year)}
                                            className={selectedYear === year ? 'bg-stone-900 hover:bg-stone-800' : 'hover:bg-stone-200'}
                                        >
                                            {year}
                                        </Button>
                                    ))}
                                </div>
                            </div>

                            {/* Year-dependent Charts */}
                            <div className="grid md:grid-cols-2 gap-6">
                                {/* Department Satisfaction */}
                                <Card className="border-stone-200">
                                    <CardHeader className="pb-2">
                                        <CardTitle className="text-base font-display">Patient Satisfaction by Department</CardTitle>
                                        <p className="text-sm text-stone-500">Rating out of 5.0 • {selectedYear}</p>
                                    </CardHeader>
                                    <CardContent>
                                        <div className="h-72">
                                            <Bar data={deptChartData} options={{
                                                ...chartOptions,
                                                scales: {
                                                    ...chartOptions.scales,
                                                    y: { ...chartOptions.scales.y, max: 5 }
                                                }
                                            }} />
                                        </div>
                                    </CardContent>
                                </Card>

                                {/* Department Occupancy */}
                                <Card className="border-stone-200">
                                    <CardHeader className="pb-2">
                                        <CardTitle className="text-base font-display">Department Occupancy</CardTitle>
                                        <p className="text-sm text-stone-500">Capacity utilization • {selectedYear}</p>
                                    </CardHeader>
                                    <CardContent>
                                        <div className="h-72">
                                            <Bar
                                                data={{
                                                    labels: departments.map(d => d.department_name),
                                                    datasets: [{
                                                        data: departments.map(d => Math.round(d.current_occupancy * 100)),
                                                        backgroundColor: departments.map(d =>
                                                            d.current_occupancy > 0.85 ? '#dc2626' :
                                                                d.current_occupancy > 0.7 ? '#f59e0b' : '#16a34a'
                                                        ),
                                                        borderRadius: 4,
                                                    }]
                                                }}
                                                options={{
                                                    ...chartOptions,
                                                    scales: {
                                                        ...chartOptions.scales,
                                                        y: { ...chartOptions.scales.y, max: 100 }
                                                    },
                                                    plugins: {
                                                        ...chartOptions.plugins,
                                                        tooltip: {
                                                            callbacks: {
                                                                label: (ctx) => `${ctx.raw}%`
                                                            }
                                                        }
                                                    }
                                                }}
                                            />
                                        </div>
                                    </CardContent>
                                </Card>
                            </div>

                            {/* Department Performance Table */}
                            <Card className="border-stone-200 mt-6">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-base font-display">Department Performance Summary • {selectedYear}</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <div className="overflow-x-auto">
                                        <table className="w-full text-sm">
                                            <thead>
                                                <tr className="border-b border-stone-200">
                                                    <th className="text-left py-3 font-medium text-stone-500">Department</th>
                                                    <th className="text-right py-3 font-medium text-stone-500">Patients</th>
                                                    <th className="text-right py-3 font-medium text-stone-500">Satisfaction</th>
                                                    <th className="text-right py-3 font-medium text-stone-500">Occupancy</th>
                                                    <th className="text-right py-3 font-medium text-stone-500">Quality</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {departments.map((dept, i) => (
                                                    <tr key={i} className="border-b border-stone-100 last:border-0">
                                                        <td className="py-3">
                                                            <div className="flex items-center gap-2">
                                                                <div className="w-2 h-2 rounded-full" style={{
                                                                    backgroundColor: dept.quality_score >= 90 ? '#16a34a' :
                                                                        dept.quality_score >= 85 ? '#f59e0b' : '#dc2626'
                                                                }}></div>
                                                                <span className="font-medium text-ink">{dept.department_name}</span>
                                                            </div>
                                                        </td>
                                                        <td className="text-right py-3 text-stone-600">{dept.total_patients.toLocaleString()}</td>
                                                        <td className="text-right py-3 font-medium text-ink">{dept.patient_satisfaction}/5</td>
                                                        <td className="text-right py-3">
                                                            <span className={`font-medium ${dept.current_occupancy > 0.85 ? 'text-red-600' : dept.current_occupancy > 0.7 ? 'text-amber-600' : 'text-green-600'}`}>
                                                                {Math.round(dept.current_occupancy * 100)}%
                                                            </span>
                                                        </td>
                                                        <td className="text-right py-3 font-semibold text-ink">{dept.quality_score}%</td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                </CardContent>
                            </Card>
                        </div>
                    </div>
                )}

                {/* Patients Tab - Enhanced Dashboard */}
                {activeTab === 'patients' && (
                    <div className="space-y-6">
                        {/* KPI Summary Cards */}
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            <Card className="border-stone-200 bg-gradient-to-br from-violet-50 to-white">
                                <CardContent className="pt-6">
                                    <p className="text-sm text-stone-500 font-medium">Total Records</p>
                                    <p className="text-2xl md:text-3xl font-bold text-ink mt-1">55,500</p>
                                    <p className="text-xs text-emerald-600 mt-2">All conditions</p>
                                </CardContent>
                            </Card>
                            <Card className="border-stone-200 bg-gradient-to-br from-pink-50 to-white">
                                <CardContent className="pt-6">
                                    <p className="text-sm text-stone-500 font-medium">Avg. Patient Age</p>
                                    <p className="text-2xl md:text-3xl font-bold text-ink mt-1">52.3</p>
                                    <p className="text-xs text-stone-500 mt-2">Years old</p>
                                </CardContent>
                            </Card>
                            <Card className="border-stone-200 bg-gradient-to-br from-cyan-50 to-white">
                                <CardContent className="pt-6">
                                    <p className="text-sm text-stone-500 font-medium">Gender Ratio</p>
                                    <p className="text-2xl md:text-3xl font-bold text-ink mt-1">50/50</p>
                                    <p className="text-xs text-stone-500 mt-2">Male/Female</p>
                                </CardContent>
                            </Card>
                            <Card className="border-stone-200 bg-gradient-to-br from-orange-50 to-white">
                                <CardContent className="pt-6">
                                    <p className="text-sm text-stone-500 font-medium">Avg. Stay</p>
                                    <p className="text-2xl md:text-3xl font-bold text-ink mt-1">15.5</p>
                                    <p className="text-xs text-stone-500 mt-2">Days</p>
                                </CardContent>
                            </Card>
                        </div>

                        {/* Main Charts Row */}
                        <div className="grid md:grid-cols-3 gap-6">
                            {/* Patients by Condition - Larger Card */}
                            <Card className="border-stone-200 md:col-span-2">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-base font-display">Patients by Medical Condition</CardTitle>
                                    <p className="text-sm text-stone-500">Distribution across 55,500 records</p>
                                </CardHeader>
                                <CardContent>
                                    <div className="h-80">
                                        <Bar
                                            data={{
                                                labels: Object.keys(patientsByCondition),
                                                datasets: [{
                                                    data: Object.values(patientsByCondition),
                                                    backgroundColor: conditionColors,
                                                    borderRadius: 4,
                                                }]
                                            }}
                                            options={chartOptions}
                                        />
                                    </div>
                                </CardContent>
                            </Card>

                            {/* Gender Distribution */}
                            <Card className="border-stone-200">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-base font-display">Gender Distribution</CardTitle>
                                    <p className="text-sm text-stone-500">Patient demographics</p>
                                </CardHeader>
                                <CardContent>
                                    <div className="h-80">
                                        <Doughnut
                                            data={{
                                                labels: ['Male', 'Female'],
                                                datasets: [{
                                                    data: [27750, 27750],
                                                    backgroundColor: ['#3b82f6', '#ec4899'],
                                                    borderWidth: 0,
                                                }]
                                            }}
                                            options={doughnutOptions}
                                        />
                                    </div>
                                </CardContent>
                            </Card>
                        </div>

                        {/* Secondary Charts Row */}
                        <div className="grid md:grid-cols-2 gap-6">
                            {/* Age Distribution */}
                            <Card className="border-stone-200">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-base font-display">Age Distribution</CardTitle>
                                    <p className="text-sm text-stone-500">Patient age groups</p>
                                </CardHeader>
                                <CardContent>
                                    <div className="h-72">
                                        <Bar data={ageChartData} options={chartOptions} />
                                    </div>
                                </CardContent>
                            </Card>

                            {/* Test Results */}
                            <Card className="border-stone-200">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-base font-display">Test Results Distribution</CardTitle>
                                    <p className="text-sm text-stone-500">Lab test outcomes</p>
                                </CardHeader>
                                <CardContent>
                                    <div className="h-72">
                                        <Doughnut
                                            data={{
                                                labels: ['Normal', 'Abnormal', 'Inconclusive'],
                                                datasets: [{
                                                    data: [18620, 18440, 18440],
                                                    backgroundColor: ['#16a34a', '#dc2626', '#f59e0b'],
                                                    borderWidth: 0,
                                                }]
                                            }}
                                            options={doughnutOptions}
                                        />
                                    </div>
                                </CardContent>
                            </Card>
                        </div>

                        {/* Bottom Row - Detailed Tables */}
                        <div className="grid md:grid-cols-2 gap-6">
                            {/* Condition Breakdown */}
                            <Card className="border-stone-200">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-base font-display">Condition Patient Summary</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <div className="space-y-3">
                                        {[
                                            { name: 'Arthritis', count: 9308, pct: '16.8%', color: '#115e59' },
                                            { name: 'Diabetes', count: 9304, pct: '16.8%', color: '#14b8a6' },
                                            { name: 'Hypertension', count: 9245, pct: '16.7%', color: '#0d9488' },
                                            { name: 'Obesity', count: 9231, pct: '16.6%', color: '#2dd4bf' },
                                            { name: 'Cancer', count: 9227, pct: '16.6%', color: '#5eead4' },
                                            { name: 'Asthma', count: 9185, pct: '16.5%', color: '#99f6e4' },
                                        ].map((cond, i) => (
                                            <div key={i} className="flex items-center justify-between py-2 border-b border-stone-100 last:border-0">
                                                <div className="flex items-center gap-3">
                                                    <div className="w-3 h-3 rounded-full" style={{ backgroundColor: cond.color }}></div>
                                                    <span className="font-medium text-ink">{cond.name}</span>
                                                </div>
                                                <div className="flex gap-4 text-sm">
                                                    <span className="text-stone-500">{cond.count.toLocaleString()} patients</span>
                                                    <span className="font-semibold text-ink w-14 text-right">{cond.pct}</span>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </CardContent>
                            </Card>

                            {/* Age Group Analysis */}
                            <Card className="border-stone-200">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-base font-display">Age Group Analysis</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <div className="space-y-3">
                                        {[
                                            { group: '18-30', count: 9250, pct: '16.7%', trend: 'Young Adults' },
                                            { group: '31-45', count: 11100, pct: '20.0%', trend: 'Working Age' },
                                            { group: '46-60', count: 13850, pct: '24.9%', trend: 'Middle Age' },
                                            { group: '61-75', count: 14200, pct: '25.6%', trend: 'Senior' },
                                            { group: '76+', count: 7100, pct: '12.8%', trend: 'Elderly' },
                                        ].map((age, i) => (
                                            <div key={i} className="flex items-center justify-between py-2 border-b border-stone-100 last:border-0">
                                                <div className="flex items-center gap-3">
                                                    <span className="font-bold text-ink w-14">{age.group}</span>
                                                    <span className="text-stone-400 text-sm">{age.trend}</span>
                                                </div>
                                                <div className="flex gap-4 text-sm">
                                                    <span className="text-stone-500">{age.count.toLocaleString()}</span>
                                                    <span className="font-semibold text-ink w-14 text-right">{age.pct}</span>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </CardContent>
                            </Card>
                        </div>
                    </div>
                )}

                {/* Billing Tab - Enhanced Dashboard */}
                {activeTab === 'billing' && (
                    <div className="space-y-6">
                        {/* KPI Summary Cards */}
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            <Card className="border-stone-200 bg-gradient-to-br from-teal-50 to-white">
                                <CardContent className="pt-6">
                                    <p className="text-sm text-stone-500 font-medium">Total Revenue</p>
                                    <p className="text-2xl md:text-3xl font-bold text-ink mt-1">$1.38B</p>
                                    <p className="text-xs text-emerald-600 mt-2">↑ 12.5% vs last year</p>
                                </CardContent>
                            </Card>
                            <Card className="border-stone-200 bg-gradient-to-br from-blue-50 to-white">
                                <CardContent className="pt-6">
                                    <p className="text-sm text-stone-500 font-medium">Avg. Bill Amount</p>
                                    <p className="text-2xl md:text-3xl font-bold text-ink mt-1">$24,938</p>
                                    <p className="text-xs text-stone-500 mt-2">Per patient visit</p>
                                </CardContent>
                            </Card>
                            <Card className="border-stone-200 bg-gradient-to-br from-amber-50 to-white">
                                <CardContent className="pt-6">
                                    <p className="text-sm text-stone-500 font-medium">Insurance Claims</p>
                                    <p className="text-2xl md:text-3xl font-bold text-ink mt-1">55,500</p>
                                    <p className="text-xs text-emerald-600 mt-2">98.2% processed</p>
                                </CardContent>
                            </Card>
                            <Card className="border-stone-200 bg-gradient-to-br from-purple-50 to-white">
                                <CardContent className="pt-6">
                                    <p className="text-sm text-stone-500 font-medium">Collection Rate</p>
                                    <p className="text-2xl md:text-3xl font-bold text-ink mt-1">94.8%</p>
                                    <p className="text-xs text-emerald-600 mt-2">↑ 2.1% improvement</p>
                                </CardContent>
                            </Card>
                        </div>

                        {/* Main Charts Row */}
                        <div className="grid md:grid-cols-3 gap-6">
                            {/* Billing by Condition - Larger Card */}
                            <Card className="border-stone-200 md:col-span-2">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-base font-display">Average Billing by Medical Condition</CardTitle>
                                    <p className="text-sm text-stone-500">Revenue analysis across 6 conditions</p>
                                </CardHeader>
                                <CardContent>
                                    <div className="h-80">
                                        <Bar
                                            data={billingChartData}
                                            options={{
                                                ...chartOptions,
                                                plugins: {
                                                    ...chartOptions.plugins,
                                                    tooltip: {
                                                        callbacks: {
                                                            label: (ctx) => formatCurrency(ctx.raw)
                                                        }
                                                    }
                                                }
                                            }}
                                        />
                                    </div>
                                </CardContent>
                            </Card>

                            {/* Insurance Distribution - Doughnut */}
                            <Card className="border-stone-200">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-base font-display">Patient Distribution</CardTitle>
                                    <p className="text-sm text-stone-500">By insurance provider</p>
                                </CardHeader>
                                <CardContent>
                                    <div className="h-80">
                                        <Doughnut data={insuranceChartData} options={doughnutOptions} />
                                    </div>
                                </CardContent>
                            </Card>
                        </div>

                        {/* Secondary Charts Row */}
                        <div className="grid md:grid-cols-2 gap-6">
                            {/* Billing by Insurance Provider */}
                            <Card className="border-stone-200">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-base font-display">Average Billing by Insurance</CardTitle>
                                    <p className="text-sm text-stone-500">Revenue per insurance provider</p>
                                </CardHeader>
                                <CardContent>
                                    <div className="h-72">
                                        <Bar
                                            data={{
                                                labels: ['Blue Cross', 'UnitedHealthcare', 'Aetna', 'Cigna', 'Medicare'],
                                                datasets: [{
                                                    data: [26200, 25800, 24900, 24100, 22400],
                                                    backgroundColor: insuranceColors,
                                                    borderRadius: 4,
                                                }]
                                            }}
                                            options={{
                                                ...chartOptions,
                                                indexAxis: 'y',
                                                plugins: {
                                                    ...chartOptions.plugins,
                                                    tooltip: {
                                                        callbacks: {
                                                            label: (ctx) => formatCurrency(ctx.raw)
                                                        }
                                                    }
                                                }
                                            }}
                                        />
                                    </div>
                                </CardContent>
                            </Card>

                            {/* Billing Comparison by Condition & Insurance */}
                            <Card className="border-stone-200">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-base font-display">Claims by Admission Type</CardTitle>
                                    <p className="text-sm text-stone-500">Emergency, Elective & Urgent cases</p>
                                </CardHeader>
                                <CardContent>
                                    <div className="h-72">
                                        <Doughnut
                                            data={{
                                                labels: ['Emergency', 'Elective', 'Urgent'],
                                                datasets: [{
                                                    data: [18520, 18490, 18490],
                                                    backgroundColor: ['#dc2626', '#16a34a', '#f59e0b'],
                                                    borderWidth: 0,
                                                }]
                                            }}
                                            options={doughnutOptions}
                                        />
                                    </div>
                                </CardContent>
                            </Card>
                        </div>

                        {/* Bottom Row - Detailed Table-like Cards */}
                        <div className="grid md:grid-cols-2 gap-6">
                            {/* Insurance Provider Breakdown */}
                            <Card className="border-stone-200">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-base font-display">Insurance Provider Summary</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <div className="space-y-3">
                                        {[
                                            { name: 'Medicare', patients: '11,180', avgBill: '$22,400', color: '#1e3a5f' },
                                            { name: 'Blue Cross', patients: '11,150', avgBill: '$26,200', color: '#2563eb' },
                                            { name: 'Aetna', patients: '11,100', avgBill: '$24,900', color: '#3b82f6' },
                                            { name: 'Cigna', patients: '11,050', avgBill: '$24,100', color: '#60a5fa' },
                                            { name: 'UnitedHealthcare', patients: '11,020', avgBill: '$25,800', color: '#93c5fd' },
                                        ].map((ins, i) => (
                                            <div key={i} className="flex items-center justify-between py-2 border-b border-stone-100 last:border-0">
                                                <div className="flex items-center gap-3">
                                                    <div className="w-3 h-3 rounded-full" style={{ backgroundColor: ins.color }}></div>
                                                    <span className="font-medium text-ink">{ins.name}</span>
                                                </div>
                                                <div className="flex gap-6 text-sm">
                                                    <span className="text-stone-500">{ins.patients} patients</span>
                                                    <span className="font-semibold text-ink">{ins.avgBill}</span>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </CardContent>
                            </Card>

                            {/* Condition Billing Breakdown */}
                            <Card className="border-stone-200">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-base font-display">Billing by Condition Summary</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <div className="space-y-3">
                                        {[
                                            { name: 'Cancer', patients: '9,227', avgBill: '$26,850', trend: '↑ 5.2%', color: '#115e59' },
                                            { name: 'Diabetes', patients: '9,304', avgBill: '$25,420', trend: '↑ 3.8%', color: '#14b8a6' },
                                            { name: 'Hypertension', patients: '9,245', avgBill: '$24,180', trend: '↑ 2.1%', color: '#0d9488' },
                                            { name: 'Arthritis', patients: '9,308', avgBill: '$23,950', trend: '↓ 1.4%', color: '#2dd4bf' },
                                            { name: 'Obesity', patients: '9,231', avgBill: '$22,780', trend: '↑ 4.5%', color: '#5eead4' },
                                            { name: 'Asthma', patients: '9,185', avgBill: '$21,450', trend: '↑ 1.8%', color: '#99f6e4' },
                                        ].map((cond, i) => (
                                            <div key={i} className="flex items-center justify-between py-2 border-b border-stone-100 last:border-0">
                                                <div className="flex items-center gap-3">
                                                    <div className="w-3 h-3 rounded-full" style={{ backgroundColor: cond.color }}></div>
                                                    <span className="font-medium text-ink">{cond.name}</span>
                                                </div>
                                                <div className="flex gap-4 text-sm">
                                                    <span className="text-stone-500">{cond.patients}</span>
                                                    <span className="font-semibold text-ink w-20 text-right">{cond.avgBill}</span>
                                                    <span className={`w-14 text-right ${cond.trend.startsWith('↑') ? 'text-emerald-600' : 'text-red-500'}`}>{cond.trend}</span>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </CardContent>
                            </Card>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
