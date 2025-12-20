import { useState } from 'react';
import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import { Menu, X, Activity } from 'lucide-react';
import Home from './pages/Home';
import CostEstimator from './pages/CostEstimator';
import DoctorFinder from './pages/DoctorFinder';
import Analytics from './pages/Analytics';
import './App.css';

function Navigation() {
  const [isOpen, setIsOpen] = useState(false);

  const navItems = [
    { path: '/', label: 'Home' },
    { path: '/cost', label: 'Cost Estimator' },
    { path: '/doctors', label: 'Find Doctors' },
    { path: '/analytics', label: 'Analytics' },
  ];

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-paper/80 backdrop-blur-lg border-b border-stone-100">
      <nav className="container-asymmetric">
        <div className="flex items-center justify-between h-16">
          {/* Logo - minimal mark */}
          <NavLink to="/" className="flex items-center gap-2 text-ink font-semibold">
            <Activity className="w-5 h-5 text-ink" strokeWidth={2.5} />
            <span className="font-display tracking-tight">Healthcare</span>
          </NavLink>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center gap-8">
            {navItems.map(item => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `text-sm font-medium transition-colors duration-200 ${isActive
                    ? 'text-ink border-b-2 border-accent pb-1'
                    : 'text-stone-500 hover:text-ink'
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden p-2 text-stone-500 hover:text-ink"
            aria-label="Toggle menu"
          >
            {isOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>

        {/* Mobile nav */}
        {isOpen && (
          <div className="md:hidden py-4 border-t border-stone-100 animate-fade-in">
            {navItems.map(item => (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={() => setIsOpen(false)}
                className={({ isActive }) =>
                  `block py-3 text-sm font-medium ${isActive ? 'text-ink font-bold border-l-4 border-accent pl-3' : 'text-stone-500'
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </div>
        )}
      </nav>
    </header>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-paper">
        <Navigation />
        <main className="pt-16">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/cost" element={<CostEstimator />} />
            <Route path="/doctors" element={<DoctorFinder />} />
            <Route path="/analytics" element={<Analytics />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
