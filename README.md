# shibari_chill_spiral

A Python application for analyzing and visualizing double conical spiral configurations with multiple calculation methods, comprehensive plotting capabilities, and professional LaTeX report generation.

## Features

- **Multiple Calculation Methods**: Analytical, numerical, and circular approximation methods for spiral perimeter calculations
- **3D Visualization**: Combined 3D plots showing spiral geometry, cone structures, and projections
- **Annular Net Visualization**: Flat representation of spiral segments for practical applications
- **LaTeX Report Generation**: Professional PDF reports with narrative-driven analysis
- **Configuration Management**: YAML-based configuration system for easy parameter adjustment
- **Comprehensive Analysis**: Detailed comparison of calculation methods with accuracy metrics
- **Structural Analysis**: Integration of structural lines and net length calculations

## Prerequisites

### Python Installation

This project requires Python 3.13.1 or higher. 

#### Installing Python 3.13.1

**Windows:**
1. Download Python 3.13.1 from [python.org](https://www.python.org/downloads/)
2. Run the installer and make sure to check "Add Python to PATH"
3. Verify installation: `python --version`

**macOS:**
```bash
# Using Homebrew
brew install python@3.13

# Or download from python.org
```

**Linux (Ubuntu/Debian):**
```bash
# Add deadsnakes PPA for latest Python versions
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-pip
```

### LaTeX Installation (Required for PDF Reports)

#### Windows
1. Install [MiKTeX](https://miktex.org/download) or [TeX Live](https://www.tug.org/texlive/)
2. Ensure `pdflatex` and `latexmk` are in your system PATH
3. Verify installation: `pdflatex --version`

#### macOS
```bash
# Install MacTeX (recommended)
brew install --cask mactex

# Or install BasicTeX (smaller)
brew install --cask basictex
sudo tlmgr update --self
sudo tlmgr install latexmk
```

#### Linux (Ubuntu/Debian)
```bash
# Full installation (recommended)
sudo apt-get install texlive-full

# Or minimal installation
sudo apt-get install texlive-latex-base texlive-latex-recommended texlive-latex-extra
sudo apt-get install texlive-fonts-recommended latexmk
```

## Installation

### 1. Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd double-conical-spiral

# Or download and extract the project files
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3.13 -m venv spiral_env

# Alternative if python3.13 is your default python
python -m venv spiral_env
```

### 3. Activate Virtual Environment

**Windows:**
```bash
# Command Prompt
spiral_env\Scripts\activate

# PowerShell
spiral_env\Scripts\Activate.ps1

# Git Bash
source spiral_env/Scripts/activate
```

**macOS/Linux:**
```bash
source spiral_env/bin/activate
```

You should see `(spiral_env)` at the beginning of your command prompt.

### 4. Install Requirements

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install dependencies manually:

```bash
pip install numpy matplotlib pyyaml scipy pylatex
```

### 5. Verify LaTeX Installation

Run the diagnostic tool to check your LaTeX setup:

```bash
python latex_troubleshooter.py
```

This will verify that LaTeX is properly installed and configured.

## Project Structure

```
double-conical-spiral/
├── main.py                          # Main analysis script
├── spiral_calculations.py           # Core calculation classes
├── spiral_plots.py                  # Visualization classes
├── story_driven_latex_report.py     # LaTeX report generator
├── latex_troubleshooter.py          # LaTeX diagnostic tool
├── config.yaml                      # Configuration file
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── reports/                         # Generated LaTeX reports
│   ├── spiral_design_story_*.pdf    # Story-driven reports
│   └── *.png                        # Generated plot images
└── output/                          # Generated plots and results
    ├── Combined_visuals.pdf
    └── net_approx.pdf
```

## Configuration

### Creating config.yaml

Create a `config.yaml` file in the project root with your spiral configurations:

```yaml
configurations:
  - name: "1. Aligned Spirals (0° phase offset)"
    params:
      outer_radius: 15
      inner_radius: 5
      height: 20
      num_turns: 4
      phase_offset: 0
      struct_lines: 1.0
      target_spacing: 1.0
      arc_span_deg: 180
      arc_density: 50

  - name: "2. Offset Spirals (90° phase offset)"
    params:
      outer_radius: 15
      inner_radius: 5
      height: 20
      num_turns: 4
      phase_offset: 1.5708  # π/2 radians = 90°
      struct_lines: 1.0
      target_spacing: 1.0
      arc_span_deg: 180
      arc_density: 50

  - name: "3. Complex Configuration"
    params:
      outer_radius: 12
      inner_radius: 3
      height: 25
      num_turns: 5.5
      phase_offset: 3.14159  # π radians = 180°
      struct_lines: 0.8
      target_spacing: 0.8
      arc_span_deg: 120
      arc_density: 40
```

### Configuration Parameters

- **outer_radius**: Outer radius of the conical spiral
- **inner_radius**: Inner radius of the conical spiral
- **height**: Total height of the cone
- **num_turns**: Number of spiral turns
- **phase_offset**: Phase offset in radians (0 = aligned spirals)
- **struct_lines**: Structural line density factor
- **target_spacing**: Target spacing for visualization
- **arc_span_deg**: Arc span in degrees for annular net
- **arc_density**: Density of points for arc generation

## Usage

### Basic Analysis

1. **Activate your virtual environment** (if not already active):
   ```bash
   # Windows
   spiral_env\Scripts\activate
   
   # macOS/Linux
   source spiral_env/bin/activate
   ```

2. **Run the basic analysis**:
   ```bash
   python main.py
   ```

### Generate LaTeX Reports

#### Story-Driven Report (Recommended)

Generate a comprehensive narrative-driven PDF report:

```bash
python story_driven_latex_report.py
```

This creates a professional report with:
- **Chapter 1**: Understanding the Spiral Geometry
- **Chapter 2**: Calculating the True Perimeter
- **Chapter 3**: Discovering the Circular Approximation
- **Chapter 4**: Creating the Annular Net
- **Chapter 5**: Validation and Results

#### Robust Report (If LaTeX Issues)

If you encounter LaTeX compilation issues, use the robust version:

```bash
python -c "from robust_latex_report import generate_robust_report; generate_robust_report()"
```

#### LaTeX Troubleshooting

If reports fail to generate:

```bash
python latex_troubleshooter.py
```

This diagnostic tool will:
- Check LaTeX installation
- Verify Python packages
- Test minimal LaTeX compilation
- Suggest specific fixes

### Advanced Usage

#### Custom Analysis Scripts

```python
from spiral_calculations import DoubleConicalSpiral
from spiral_plots import SpiralPlotter

# Create spiral instance
spiral = DoubleConicalSpiral(
    outer_radius=15,
    inner_radius=5,
    height=20,
    num_turns=4,
    phase_offset=0
)

# Generate analysis
comparison = spiral.compare_all_methods()
print(f"Analytical length: {comparison['analytical']['total']:.2f}")

# Create visualizations
plotter = SpiralPlotter(spiral)
fig, axes = plotter.plot_combined(show_cone=True)
plt.show()
```

#### Batch Processing

Process multiple configurations programmatically:

```python
import yaml
from story_driven_latex_report import StoryDrivenLatexReportGenerator

# Load configurations
with open('config.yaml', 'r') as f:
    data = yaml.safe_load(f)

# Generate report
generator = StoryDrivenLatexReportGenerator()
report_file = generator.generate_story_report()
print(f"Report saved: {report_file}")
```

## What the Scripts Do

### main.py
1. **Loads configurations** from `config.yaml`
2. **Calculates spiral perimeters** using three methods:
   - Analytical (exact mathematical solution)
   - Numerical (discrete approximation)
   - Circular approximation
3. **Generates comprehensive analysis** including:
   - Configuration parameters
   - Perimeter calculations
   - Method accuracy comparisons
4. **Creates visualizations**:
   - 3D spiral plots with cone structure
   - XZ and XY projections
   - Annular net approximations
5. **Exports results** as PDF files

### story_driven_latex_report.py
1. **Creates professional LaTeX documents** with narrative structure
2. **Generates mathematical analysis** with proper equations
3. **Includes high-quality plots** embedded in the document
4. **Provides manufacturing insights** with net length calculations
5. **Outputs publication-ready PDFs**

## Output Files

### Standard Output
- `Combined_visuals.pdf`: 3D visualizations and projections
- `net_approx.pdf`: Annular net approximations
- Console output with detailed numerical analysis

### LaTeX Reports
- `reports/spiral_design_story_YYYYMMDD_HHMMSS.pdf`: Complete narrative report
- `reports/3d_plot_*.png`: Generated 3D visualization images
- `reports/net_plot_*.png`: Generated net pattern images

## Example Output

### Console Analysis
```
DOUBLE CONICAL SPIRAL ANALYSIS
============================================================

1. Aligned Spirals (0° phase offset)
====================================

CONFIGURATION PARAMETERS:
----------------------------------------
Outer Radius:           15.00
Inner Radius:            5.00
Height:                 20.00
Number of Turns:         4.00
Phase Offset:              0°

PERIMETER CALCULATIONS:
==================================================
Analytical Method (Exact):
-------------------------
  Outer Spiral:       251.3274
  Inner Spiral:        83.7758
  Total Length:       335.1032

Numerical Method (1000 points):
------------------------------
  Outer Spiral:       251.2156
  Inner Spiral:        83.7384
  Total Length:       334.9540

CIRCULAR APPROXIMATION (100 slices):
====================================
  Outer Spiral:       235.6194
  Inner Spiral:        78.5398
  Total Length:       314.1592

ACCURACY ANALYSIS:
==================
Numerical vs Analytical:
  Error: -0.0447% (excellent)
  
Circular vs Analytical:
  Error: -6.2651% (underestimate)
```

### LaTeX Report Content

The generated LaTeX report includes:

1. **Professional Title Page** with design process overview
2. **Technical Analysis** with mathematical equations and derivations
3. **High-Quality Visualizations** embedded directly in the document
4. **Manufacturing Specifications** with material requirements
5. **Comprehensive Tables** comparing all calculation methods
6. **Executive Summary** with key findings and recommendations

## Troubleshooting

### Common Issues

1. **Python version error**:
   ```
   Error: Python 3.13.1 required
   ```
   Solution: Install Python 3.13.1 as described in prerequisites

2. **LaTeX compilation errors**:
   ```
   Error generating PDF: Command [...] returned non-zero exit status
   ```
   Solution: 
   - Run `python latex_troubleshooter.py`
   - Install missing LaTeX packages
   - Use the robust report generator

3. **Missing LaTeX packages**:
   ```
   ! LaTeX Error: File `package.sty' not found
   ```
   Solution:
   ```bash
   # MiKTeX (Windows)
   mpm --install package-name
   
   # TeX Live (macOS/Linux)
   sudo tlmgr install package-name
   ```

4. **Virtual environment activation fails**:
   - Windows: Try different terminal (Command Prompt vs PowerShell)
   - macOS/Linux: Ensure you're in the correct directory

5. **Import errors**:
   ```
   ModuleNotFoundError: No module named 'numpy'
   ```
   Solution: Ensure virtual environment is activated and run `pip install -r requirements.txt`

6. **YAML configuration errors**:
   ```
   Error parsing YAML file
   ```
   Solution: Check `config.yaml` syntax and indentation

7. **Missing spiral_calculations.py or spiral_plots.py**:
   - Ensure all project files are in the same directory
   - Verify file names match exactly

### LaTeX-Specific Troubleshooting

#### Windows (MiKTeX)
```bash
# Update package database
mpm --update-db

# Install commonly needed packages
mpm --install xcolor graphicx booktabs tcolorbox titlesec enumitem
```

#### macOS (MacTeX)
```bash
# Update TeX Live
sudo tlmgr update --self --all

# Install packages if needed
sudo tlmgr install collection-latexextra
```

#### Linux (TeX Live)
```bash
# Install additional packages
sudo apt-get install texlive-science texlive-pictures

# Or use tlmgr
sudo tlmgr install xcolor tcolorbox titlesec
```

### Dependencies Issues

If you encounter issues with specific packages:

```bash
# Upgrade pip first
pip install --upgrade pip

# Install packages individually
pip install numpy>=1.21.0
pip install matplotlib>=3.5.0
pip install pyyaml>=6.0
pip install scipy>=1.7.0
pip install pylatex>=1.4.0
```

## Development

### Adding New Configurations

1. Edit `config.yaml` to add new spiral configurations
2. Modify parameters as needed
3. Run analysis: `python main.py`
4. Generate report: `python story_driven_latex_report.py`

### Extending Functionality

- **New calculation methods**: Add to `spiral_calculations.py`
- **Additional visualizations**: Extend `spiral_plots.py`
- **Custom LaTeX reports**: Modify `story_driven_latex_report.py`
- **Custom analysis**: Modify `main.py`

### Report Customization

The LaTeX report generator supports:
- Custom styling and colors
- Additional mathematical sections
- Custom plot generation
- Flexible narrative structure

Example customization:
```python
from story_driven_latex_report import StoryDrivenLatexReportGenerator

# Create custom generator
generator = StoryDrivenLatexReportGenerator(output_dir="custom_reports")

# Generate with custom configuration
report = generator.generate_story_report("my_config.yaml")
```

## Requirements

### Python Packages

Create a `requirements.txt` file with:

```
numpy>=1.21.0
matplotlib>=3.5.0
pyyaml>=6.0
scipy>=1.7.0
pylatex>=1.4.0
```

### System Requirements

- Python 3.13.1+
- LaTeX distribution (MiKTeX, TeX Live, or MacTeX)
- 2GB RAM minimum
- Graphics capability for matplotlib visualizations
- 500MB disk space for LaTeX installation

### Optional but Recommended

- Git (for version control)
- VS Code or PyCharm (for development)
- PDF viewer (for viewing generated reports)

## Performance Notes

- **Large configurations** (>10 spirals): May take several minutes for LaTeX compilation
- **High-resolution plots**: Increase generation time but improve quality
- **Complex equations**: LaTeX compilation is CPU-intensive

## Advanced Features

### Batch Report Generation

```python
# Generate reports for multiple configuration files
configs = ['config_v1.yaml', 'config_v2.yaml', 'config_v3.yaml']
for config in configs:
    generator = StoryDrivenLatexReportGenerator()
    generator.generate_story_report(config)
```

### Custom Plot Integration

```python
# Add custom plots to reports
from spiral_plots import SpiralPlotter

def custom_analysis_plot(spiral):
    # Your custom analysis here
    fig, ax = plt.subplots()
    # ... plotting code ...
    return fig

# Integrate with report generator
# (modify _generate_and_include_3d_plot method)
```

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Citation

If you use this software in academic work, please cite:

```
@software{shibari_chill_spiral,
  title={Double Conical Spiral Analysis and Visualization},
  author={[Your Name]},
  year={2025},
  url={[Your Repository URL]}
}
```

## Support

For issues or questions:
1. Check the troubleshooting section
2. Run `python latex_troubleshooter.py` for LaTeX issues
3. Verify all dependencies are installed
4. Ensure config.yaml is properly formatted
5. Check that all Python files are in the same directory

### Quick Diagnosis Commands

```bash
# Check Python installation
python --version

# Check LaTeX installation  
pdflatex --version
latexmk --version

# Test LaTeX compilation
python latex_troubleshooter.py

# Verify Python packages
pip list | grep -E "(numpy|matplotlib|pylatex|yaml)"

# Generate test report
python -c "from story_driven_latex_report import generate_story_report; generate_story_report()"
```

## Changelog

### Version 2.0.0
- Added LaTeX report generation
- Integrated narrative-driven analysis
- Enhanced visualization pipeline
- Added diagnostic tools
- Improved error handling

### Version 1.0.0
- Initial release
- Basic spiral analysis
- 3D visualization
- Configuration management