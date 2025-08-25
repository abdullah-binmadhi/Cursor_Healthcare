# Healthcare Analytics Website

A comprehensive healthcare cost estimation and doctor finder platform built with modern web technologies.

## 🏥 Features

### 1. Healthcare Cost Estimator
- **Patient Information Input**: Age, insurance type, department, and procedure selection
- **Transparent Pricing**: Real-time cost calculations based on healthcare data
- **Insurance Coverage**: Detailed breakdown of insurance coverage and patient costs
- **Length of Stay Predictions**: Estimated hospital stay duration
- **Cost Factors**: Clear explanation of factors affecting final costs

### 2. Doctor Finder & Rating System
- **Searchable Physician Directory**: Filter by specialty, hospital, and availability
- **Performance Metrics**: Patient satisfaction scores, success rates, and experience years
- **Availability Tracking**: Real-time appointment availability status
- **Specialty Recommendations**: Find doctors based on medical needs
- **Comprehensive Profiles**: Detailed doctor information with patient feedback across 8 hospitals

## 🛠 Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Modern CSS Grid and Flexbox layouts
- **Data**: CSV-based data storage for easy maintenance
- **Icons**: Font Awesome 6.0
- **Fonts**: Inter font family for modern typography
- **Responsive**: Mobile-first responsive design

## 📁 Project Structure

```
healthcare-website/
├── index.html              # Main HTML file with all sections
├── style.css               # Comprehensive CSS styling
├── script.js               # JavaScript functionality
├── data/                   # Healthcare data files
│   ├── physician_performance.csv    # Doctor profiles and ratings
│   ├── department_metrics.csv       # Department performance data
│   ├── financial_performance.csv    # Cost estimation data
│   ├── patient_demographics.csv     # Patient population statistics
│   └── quality_metrics.csv          # Healthcare quality indicators
└── README.md               # This file
```

## 🚀 Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Local web server (recommended for CSV file loading)

### Installation

1. **Clone or download** the healthcare website files
2. **Set up a local server** (required for CSV file access):

   **Option 1: Python HTTP Server**
   ```bash
   cd healthcare-website
   python -m http.server 8000
   ```

   **Option 2: Node.js HTTP Server**
   ```bash
   cd healthcare-website
   npx http-server -p 8000
   ```

   **Option 3: VS Code Live Server**
   - Install Live Server extension
   - Right-click on index.html → "Open with Live Server"

3. **Open your browser** and navigate to:
   - `http://localhost:8000` (for Python/Node.js servers)
   - Or the URL provided by Live Server

## 💡 How to Use

### Healthcare Cost Estimator

1. **Navigate** to the "Cost Estimator" section
2. **Enter patient information**:
   - Age (affects cost calculations)
   - Insurance type (Medicare, Medicaid, Private, etc.)
   - Department (Cardiology, Emergency, Surgery, etc.)
   - Procedure type (Consultation, Surgery, etc.)
3. **Click "Calculate Estimate"** to get:
   - Total estimated cost
   - Insurance coverage amount
   - Patient out-of-pocket cost
   - Expected length of stay
   - Factors affecting the cost

### Doctor Finder

1. **Navigate** to the "Find Doctors" section
2. **Use filters** to narrow your search:
   - Specialty (Cardiology, Surgery, etc.)
   - Hospital (8 different hospital locations)
   - Minimum rating (3+, 4+, 4.5+ stars)
   - Availability status
3. **Browse results** showing:
   - Doctor names and credentials
   - Patient satisfaction ratings
   - Success rates and experience
   - Hospital affiliation
   - Current availability status

## 📊 Data Sources

The website uses realistic sample data including:

- **150 physician profiles** with performance metrics across 8 hospitals
- **210 cost combinations** across departments, insurance types, and procedures
- **7 department categories** with capacity and quality metrics
- **8 hospital locations** for comprehensive physician search
- **Patient demographics** across age groups and insurance types
- **Quality indicators** for healthcare performance tracking

## 🎨 Design Features

- **Modern Healthcare Theme**: Professional blue and white color scheme
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Intuitive Navigation**: Smooth scrolling and clear section organization
- **Interactive Elements**: Hover effects, transitions, and loading states
- **Accessibility**: Semantic HTML and proper contrast ratios
- **Professional Typography**: Clean, readable font choices

## 🔧 Customization

### Adding New Data
1. **Edit CSV files** in the `data/` directory
2. **Follow existing column structure** for compatibility
3. **Refresh the page** to load new data

### Styling Changes
- **Colors**: Update CSS custom properties in `style.css`
- **Layout**: Modify Grid and Flexbox properties
- **Typography**: Change font families and sizes

### Functionality Extensions
- **Add new filters**: Extend the JavaScript filter functions
- **New calculations**: Modify cost estimation algorithms
- **Additional metrics**: Include more doctor performance indicators

## 🌐 Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## 📱 Mobile Responsiveness

The website is fully responsive with:
- **Flexible layouts** that adapt to screen sizes
- **Touch-friendly buttons** and form elements
- **Optimized navigation** for mobile devices
- **Readable text** at all screen sizes

## 🔒 Security & Privacy

- **No server-side processing**: All calculations done in browser
- **No data collection**: Patient information is not stored
- **Local data only**: CSV files contain sample, non-sensitive data
- **HTTPS ready**: Works with secure connections

## 🚀 Performance

- **Fast loading**: Minimal external dependencies
- **Efficient filtering**: Optimized search algorithms
- **Smooth animations**: Hardware-accelerated CSS transitions
- **Lazy loading**: Data loaded only when needed

## 📈 Future Enhancements

Potential improvements:
- **Real-time appointments**: Integration with booking systems
- **Patient reviews**: User-generated doctor feedback
- **Advanced filtering**: More granular search options
- **Cost comparisons**: Multi-hospital price comparisons
- **Insurance verification**: Real-time coverage checks

## 🤝 Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For questions or issues:
- Check the browser console for error messages
- Ensure you're running a local server for CSV file access
- Verify all files are in the correct directory structure

---

**Built with healthcare analytics data from the Cursor Healthcare project**