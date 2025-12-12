# Healthcare Analytics Website

## How to Run

This website requires a local web server to function properly because it loads CSV data files using the Fetch API, which doesn't work with the `file://` protocol.

### Quick Start

1. **Open Terminal** in the `healthcare-website` folder

2. **Start the web server:**
   ```bash
   python3 -m http.server 8080
   ```

3. **Open your browser** and navigate to:
   ```
   http://localhost:8080
   ```

4. **To stop the server**, press `Ctrl+C` in the terminal

### Alternative Ports

If port 8080 is already in use, you can use a different port:
```bash
python3 -m http.server 3000
```
Then open: `http://localhost:3000`

### Required Files

The following files must be present in the `healthcare-website` folder:
- `index.html` - Main application file
- `physician_registry.csv` - Physician data (110 doctors)
- `style.css` - Styling
- `script.js` - Additional JavaScript
- `data/` folder with CSV files for analytics

### Features

- **Cost Estimator** - Calculate healthcare procedure costs
- **Find Doctors** - Browse and filter 110 physicians across 17 specialties
- **Analytics Dashboard** - View healthcare performance metrics
- **Filters**:
  - Specialty (17 medical specialties)
  - Hospital (8 locations)
  - Minimum Rating (3+, 4+, 4.5+)
  - Availability (Available This Week, Limited)

### Troubleshooting

**Problem:** "Error loading physicians: Failed to load CSV: 404"

**Solution:** You're opening the HTML file directly. Use the HTTP server method above.

**Problem:** Port 8080 already in use

**Solution:** Try a different port number (e.g., 3000, 5000, 8000)

### Data Files

- `physician_registry.csv` - 110 physicians with specialties and hospitals
- `data/physician_performance.csv` - Performance metrics (3,960 records)
- `data/department_metrics.csv` - Department statistics
- `data/financial_performance.csv` - Financial data
- `data/patient_demographics.csv` - Patient demographics (1,000 segments)

### Browser Compatibility

- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

All modern browsers with ES6+ support.
