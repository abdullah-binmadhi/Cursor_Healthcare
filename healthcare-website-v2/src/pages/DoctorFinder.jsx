import { useState, useMemo, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue
} from '@/components/ui/select';
import { Star, Users, Loader2, AlertCircle } from 'lucide-react';
import { fetchPhysicians } from '@/services/supabase';

export default function DoctorFinder() {
    // State for physicians from Supabase
    const [physicians, setPhysicians] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // State for filters
    const [filters, setFilters] = useState({
        specialty: '',
        hospital: '',
        minRating: ''
    });

    // Load physicians from Supabase on mount
    useEffect(() => {
        async function loadPhysicians() {
            try {
                setLoading(true);
                setError(null);
                const data = await fetchPhysicians();
                setPhysicians(data);
            } catch (err) {
                console.error('Error loading physicians:', err);
                setError(err.message || 'Failed to load physicians');
            } finally {
                setLoading(false);
            }
        }
        loadPhysicians();
    }, []);

    // Extract unique specialties and hospitals from database
    const specialties = useMemo(() => {
        const unique = [...new Set(physicians.map(p => p.specialty).filter(Boolean))];
        return ['All Specialties', ...unique.sort()];
    }, [physicians]);

    const hospitals = useMemo(() => {
        const unique = [...new Set(physicians.map(p => p.hospital).filter(Boolean))];
        return ['All Hospitals', ...unique.sort()];
    }, [physicians]);

    // Filter physicians based on selected criteria
    const filteredDoctors = useMemo(() => {
        return physicians.filter(doc => {
            if (filters.specialty && doc.specialty !== filters.specialty) return false;
            if (filters.hospital && doc.hospital !== filters.hospital) return false;
            if (filters.minRating && doc.rating < parseFloat(filters.minRating)) return false;
            return true;
        }).sort((a, b) => b.rating - a.rating);
    }, [physicians, filters]);

    const updateFilter = (field, value) => {
        setFilters(prev => ({ ...prev, [field]: value === 'all' ? '' : value }));
    };

    // Compute stats
    const avgRating = filteredDoctors.length > 0
        ? (filteredDoctors.reduce((sum, d) => sum + (d.rating || 0), 0) / filteredDoctors.length).toFixed(1)
        : 0;

    // Loading state
    if (loading) {
        return (
            <div className="py-16 md:py-24">
                <div className="container-asymmetric">
                    <div className="flex flex-col items-center justify-center py-20">
                        <Loader2 className="w-8 h-8 text-teal-600 animate-spin mb-4" />
                        <p className="text-stone-500">Loading physicians from database...</p>
                    </div>
                </div>
            </div>
        );
    }

    // Error state
    if (error) {
        return (
            <div className="py-16 md:py-24">
                <div className="container-asymmetric">
                    <div className="flex flex-col items-center justify-center py-20">
                        <AlertCircle className="w-8 h-8 text-red-500 mb-4" />
                        <p className="text-red-600 font-medium mb-2">Error loading physicians</p>
                        <p className="text-stone-500 text-sm">{error}</p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="py-16 md:py-24">
            <div className="container-asymmetric">
                {/* Header */}
                <div className="max-w-xl mb-8">
                    <h1 className="font-display text-3xl md:text-4xl font-semibold text-ink tracking-tight">
                        Find Physicians
                    </h1>
                    <p className="mt-3 text-stone-500">
                        {physicians.length} physicians across {hospitals.length - 1} hospitals and {specialties.length - 1} specialties
                    </p>
                </div>

                {/* Stats Bar */}
                <div className="flex flex-wrap gap-6 mb-8 p-4 bg-stone-50 rounded-lg">
                    <div className="flex items-center gap-2">
                        <Users className="w-4 h-4 text-stone-400" />
                        <span className="text-sm text-stone-600">
                            <strong>{filteredDoctors.length}</strong> physicians
                        </span>
                    </div>
                    <div className="flex items-center gap-2">
                        <Star className="w-4 h-4 text-amber-500 fill-current" />
                        <span className="text-sm text-stone-600">
                            <strong>{avgRating}</strong> avg rating
                        </span>
                    </div>
                    <div className="text-sm text-emerald-600 font-medium">
                        ✓ Live data from Supabase
                    </div>
                </div>

                <div className="grid lg:grid-cols-4 gap-8">
                    {/* Filters */}
                    <Card className="border-stone-200 h-fit">
                        <CardContent className="p-6 space-y-6">
                            <div className="space-y-2">
                                <Label>Specialty</Label>
                                <Select value={filters.specialty || 'all'} onValueChange={(v) => updateFilter('specialty', v)}>
                                    <SelectTrigger className="w-full truncate">
                                        <SelectValue className="truncate" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {specialties.map(spec => (
                                            <SelectItem key={spec} value={spec === 'All Specialties' ? 'all' : spec}>
                                                {spec}
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </div>

                            <div className="space-y-2">
                                <Label>Hospital</Label>
                                <Select value={filters.hospital || 'all'} onValueChange={(v) => updateFilter('hospital', v)}>
                                    <SelectTrigger className="w-full truncate">
                                        <SelectValue className="truncate" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {hospitals.map(hosp => (
                                            <SelectItem key={hosp} value={hosp === 'All Hospitals' ? 'all' : hosp}>
                                                {hosp}
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </div>

                            <div className="space-y-2">
                                <Label>Minimum Rating</Label>
                                <Select value={filters.minRating || 'all'} onValueChange={(v) => updateFilter('minRating', v)}>
                                    <SelectTrigger className="w-full">
                                        <SelectValue />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="all">Any Rating</SelectItem>
                                        <SelectItem value="4">4+ Stars</SelectItem>
                                        <SelectItem value="4.5">4.5+ Stars</SelectItem>
                                        <SelectItem value="4.7">4.7+ Stars</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Results */}
                    <div className="lg:col-span-3">
                        <div className="grid md:grid-cols-2 gap-4">
                            {filteredDoctors.map((doc) => (
                                <DoctorCard key={doc.id} doctor={doc} />
                            ))}
                        </div>

                        {filteredDoctors.length === 0 && (
                            <div className="text-center py-12 text-stone-400">
                                No physicians match your criteria
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

function DoctorCard({ doctor }) {
    // Format name - handle both API formats
    const displayName = doctor.physician_name ||
        (doctor.first_name && doctor.last_name ? `Dr. ${doctor.first_name} ${doctor.last_name}` : 'Unknown Physician');

    return (
        <Card className="border-stone-200 hover:border-teal-600/30 transition-colors">
            <CardContent className="p-5">
                <div className="flex justify-between items-start mb-3">
                    <div>
                        <h3 className="font-semibold text-ink">{displayName}</h3>
                        <p className="text-sm text-teal-700 font-medium">{doctor.specialty || 'General Medicine'}</p>
                    </div>
                    <div className="flex items-center gap-1 bg-amber-50 px-2 py-1 rounded">
                        <Star className="w-3.5 h-3.5 text-amber-500 fill-current" />
                        <span className="text-sm font-semibold text-amber-700">{(doctor.rating || 4.5).toFixed(1)}</span>
                    </div>
                </div>
                <div className="flex justify-between text-sm text-stone-500">
                    <span>{doctor.hospital || 'Multiple Locations'}</span>
                    <span className={`font-medium ${doctor.availability === 'available' ? 'text-green-600' : 'text-orange-600'}`}>
                        {doctor.availability === 'available' ? '● Available' : '○ Limited'}
                    </span>
                </div>
            </CardContent>
        </Card>
    );
}
