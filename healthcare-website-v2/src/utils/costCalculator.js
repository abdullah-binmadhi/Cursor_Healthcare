/**
 * Cost Calculator - Extracted from existing autoCalculateCost()
 */

const PROCEDURE_COSTS = {
    consultation: 250,
    diagnostic: 800,
    'minor-surgery': 3500,
    'major-surgery': 25000,
    'emergency-visit': 1500,
    'follow-up': 150
};

const DEPARTMENT_MULTIPLIERS = {
    Cardiology: 1.3,
    Emergency: 1.2,
    Surgery: 1.4,
    Orthopedics: 1.25,
    Neurology: 1.35,
    Pediatrics: 0.9,
    Oncology: 1.5
};

const INSURANCE_COVERAGE = {
    medicare: 0.80,
    medicaid: 0.85,
    private: 0.75,
    commercial: 0.70,
    'self-pay': 0
};

const LENGTH_OF_STAY = {
    consultation: 'Same day',
    diagnostic: 'Same day',
    'minor-surgery': '1-2 days',
    'major-surgery': '5-7 days',
    'emergency-visit': '1-3 days',
    'follow-up': 'Same day'
};

export function calculateCostEstimate({ age, insuranceType, department, procedure }) {
    // Validate inputs
    if (!age || !insuranceType || !department || !procedure) {
        return null;
    }

    // Base cost from procedure
    let baseCost = PROCEDURE_COSTS[procedure] || 500;

    // Department multiplier
    baseCost *= DEPARTMENT_MULTIPLIERS[department] || 1.0;

    // Age adjustment
    if (age > 65) baseCost *= 1.15;
    if (age < 18) baseCost *= 0.85;

    // Insurance coverage
    const coverageRate = INSURANCE_COVERAGE[insuranceType] || 0;
    const insuranceCoverage = baseCost * coverageRate;
    const outOfPocket = baseCost - insuranceCoverage;

    // Get estimated length of stay
    const lengthOfStay = LENGTH_OF_STAY[procedure] || 'Varies';

    // Generate cost factors
    const factors = [];
    if (age > 65) factors.push('Age adjustment (+15% for patients over 65)');
    if (age < 18) factors.push('Pediatric discount (-15% for patients under 18)');
    if (DEPARTMENT_MULTIPLIERS[department] > 1.2) {
        factors.push(`${department} specialty premium`);
    }
    if (insuranceType === 'self-pay') {
        factors.push('No insurance coverage - payment plans available');
    }

    return {
        estimatedCost: baseCost,
        insuranceCoverage,
        outOfPocket,
        lengthOfStay,
        factors
    };
}

export const procedures = [
    { value: 'consultation', label: 'Consultation' },
    { value: 'diagnostic', label: 'Diagnostic Test' },
    { value: 'minor-surgery', label: 'Minor Surgery' },
    { value: 'major-surgery', label: 'Major Surgery' },
    { value: 'emergency-visit', label: 'Emergency Visit' },
    { value: 'follow-up', label: 'Follow-up Visit' }
];

export const insuranceTypes = [
    { value: 'medicare', label: 'Medicare' },
    { value: 'medicaid', label: 'Medicaid' },
    { value: 'private', label: 'Private Insurance' },
    { value: 'commercial', label: 'Commercial' },
    { value: 'self-pay', label: 'Self-Pay' }
];

export const departments = [
    { value: 'Cardiology', label: 'Cardiology' },
    { value: 'Emergency', label: 'Emergency' },
    { value: 'Surgery', label: 'Surgery' },
    { value: 'Orthopedics', label: 'Orthopedics' },
    { value: 'Neurology', label: 'Neurology' },
    { value: 'Pediatrics', label: 'Pediatrics' },
    { value: 'Oncology', label: 'Oncology' }
];
