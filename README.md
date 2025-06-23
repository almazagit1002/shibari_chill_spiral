# shibari_chill_spiral


A Python application for analyzing and visualizing double conical spiral configurations with multiple calculation methods and comprehensive plotting capabilities.

## Features

- **Multiple Calculation Methods**: Analytical, numerical, and circular approximation methods for spiral perimeter calculations
- **3D Visualization**: Combined 3D plots showing spiral geometry, cone structures, and projections
- **Annular Net Visualization**: Flat representation of spiral segments for practical applications
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
pip install numpy matplotlib pyyaml scipy
```

## Project Structure

```
double-conical-spiral/
├── main.py                 # Main analysis script
├── spiral_calculations.py  # Core calculation classes
├── spiral_plots.py         # Visualization classes
├── config.yaml            # Configuration file
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── output/                # Generated plots and results
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

### Basic Usage

1. **Activate your virtual environment** (if not already active):
   ```bash
   # Windows
   spiral_env\Scripts\activate
   
   # macOS/Linux
   source spiral_env/bin/activate
   ```

2. **Run the analysis**:
   ```bash
   python main.py
   ```

### What the Script Does

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

### Output Files

- `Combined_visuals.pdf`: 3D visualizations and projections
- `net_approx.pdf`: Annular net approximations
- Console output with detailed numerical analysis

## Example Output

The script provides detailed console output including:

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
```

## Troubleshooting

### Common Issues

1. **Python version error**:
   ```
   Error: Python 3.13.1 required
   ```
   Solution: Install Python 3.13.1 as described in prerequisites

2. **Virtual environment activation fails**:
   - Windows: Try different terminal (Command Prompt vs PowerShell)
   - macOS/Linux: Ensure you're in the correct directory

3. **Import errors**:
   ```
   ModuleNotFoundError: No module named 'numpy'
   ```
   Solution: Ensure virtual environment is activated and run `pip install -r requirements.txt`

4. **YAML configuration errors**:
   ```
   Error parsing YAML file
   ```
   Solution: Check `config.yaml` syntax and indentation

5. **Missing spiral_calculations.py or spiral_plots.py**:
   - Ensure all project files are in the same directory
   - Verify file names match exactly

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
```

## Development

### Adding New Configurations

1. Edit `config.yaml` to add new spiral configurations
2. Modify parameters as needed
3. Run `python main.py` to analyze new configurations

### Extending Functionality

- **New calculation methods**: Add to `spiral_calculations.py`
- **Additional visualizations**: Extend `spiral_plots.py`
- **Custom analysis**: Modify `main.py`

## Requirements

### Python Packages

Create a `requirements.txt` file with:

```
numpy>=1.21.0
matplotlib>=3.5.0
pyyaml>=6.0
scipy>=1.7.0
```

### System Requirements

- Python 3.13.1+
- 2GB RAM minimum
- Graphics capability for matplotlib visualizations

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Ensure config.yaml is properly formatted
4. Check that all Python files are in the same directory