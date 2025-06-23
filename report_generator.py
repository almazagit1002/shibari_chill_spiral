#!/usr/bin/env python3
"""
Automated Report Generator for Double Conical Spiral Analysis
Generates comprehensive PDF reports with findings and visualizations
"""

import os
import yaml
import numpy as np
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.patches as patches
from spiral_calculations import DoubleConicalSpiral
from spiral_plots import SpiralPlotter

class SpiralReportGenerator:
    """Generates comprehensive PDF reports for spiral analysis"""
    
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Report styling
        self.title_color = '#2c3e50'
        self.header_color = '#34495e'
        self.accent_color = '#3498db'
        self.bg_color = '#f8f9fa'
        
    def create_title_page(self, pdf_pages):
        """Create professional title page"""
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # Title
        ax.text(0.5, 0.75, 'DOUBLE CONICAL SPIRAL', 
                fontsize=28, fontweight='bold', ha='center', 
                color=self.title_color, transform=ax.transAxes)
        ax.text(0.5, 0.70, 'ANALYSIS REPORT', 
                fontsize=28, fontweight='bold', ha='center', 
                color=self.title_color, transform=ax.transAxes)
        
        # Subtitle
        ax.text(0.5, 0.62, 'Comprehensive Analysis of Spiral Configurations', 
                fontsize=16, ha='center', style='italic',
                color=self.header_color, transform=ax.transAxes)
        
        # Date and time
        timestamp = datetime.now().strftime("%B %d, %Y at %H:%M")
        ax.text(0.5, 0.45, f'Generated on {timestamp}', 
                fontsize=12, ha='center', 
                color=self.header_color, transform=ax.transAxes)
        
        # Add decorative elements
        rect = Rectangle((0.1, 0.35), 0.8, 0.02, 
                        facecolor=self.accent_color, alpha=0.8)
        ax.add_patch(rect)
        
        # Analysis methods
        methods_text = """
        ANALYSIS METHODS INCLUDED:
        
        • Analytical Calculations (Exact Mathematical Solutions)
        • Numerical Approximations (Discrete Point Analysis)
        • Circular Approximation Methods
        • 3D Visualization and Projections
        • Structural Analysis with Net Length Calculations
        • Comparative Accuracy Assessment
        """
        
        ax.text(0.5, 0.25, methods_text, 
                fontsize=11, ha='center', va='top',
                color=self.header_color, transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.3", 
                         facecolor=self.bg_color, alpha=0.8))
        
        pdf_pages.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def create_summary_page(self, pdf_pages, all_results, configurations):
        """Create executive summary page"""
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # Page title
        ax.text(0.5, 0.95, 'EXECUTIVE SUMMARY', 
                fontsize=20, fontweight='bold', ha='center', 
                color=self.title_color, transform=ax.transAxes)
        
        # Extract analytical totals for summary statistics
        analytical_totals = []
        for result_tuple in all_results:
            if len(result_tuple) >= 2:
                comparison = result_tuple[1]
                analytical_totals.append(comparison['analytical']['total'])
        
        # Summary statistics
        total_configs = len(all_results)
        avg_analytical = np.mean(analytical_totals)
        max_length = max(analytical_totals)
        min_length = min(analytical_totals)
        
        summary_stats = f"""
        ANALYSIS OVERVIEW:
        
        • Total Configurations Analyzed: {total_configs}
        • Average Spiral Length: {avg_analytical:.2f} units
        • Maximum Spiral Length: {max_length:.2f} units
        • Minimum Spiral Length: {min_length:.2f} units
        """
        
        ax.text(0.05, 0.85, summary_stats, 
                fontsize=12, va='top', transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.3", 
                         facecolor=self.bg_color, alpha=0.8))
        
        # Method accuracy analysis
        accuracy_text = """
        METHOD ACCURACY ASSESSMENT:
        
        All configurations were analyzed using three distinct calculation methods:
        
        1. ANALYTICAL METHOD: Provides exact mathematical solutions using integral calculus
        2. NUMERICAL METHOD: Discrete approximation using parametric equations
        3. CIRCULAR APPROXIMATION: Simplified circular arc approximation
        
        The analytical method serves as the baseline for accuracy comparison.
        """
        
        ax.text(0.05, 0.60, accuracy_text, 
                fontsize=10, va='top', transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.3", 
                         facecolor=self.bg_color, alpha=0.8))
        
        # Key findings
        findings_text = """
        KEY FINDINGS:
        
        • Analytical calculations provide the most accurate results
        • Numerical methods show excellent agreement with analytical solutions
        • Circular approximations are suitable for rapid estimation
        • Phase offset significantly affects spiral intersection patterns
        • Structural line integration enables complete system analysis
        """
        
        ax.text(0.05, 0.35, findings_text, 
                fontsize=11, va='top', transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.3", 
                         facecolor='#e8f5e8', alpha=0.8))
        
        pdf_pages.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def create_configuration_detail_page(self, pdf_pages, config_name, comparison, config_params, net_length):
        """Create detailed page for each configuration"""
        fig = plt.figure(figsize=(8.5, 11))
        
        # Main title
        fig.suptitle(f'CONFIGURATION ANALYSIS\n{config_name}', 
                    fontsize=16, fontweight='bold', color=self.title_color, y=0.95)
        
        # Create grid layout
        gs = fig.add_gridspec(4, 2, height_ratios=[1, 1, 1, 1], hspace=0.4, wspace=0.3)
        
        # Configuration parameters (top left)
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.axis('off')
        ax1.text(0.5, 0.9, 'CONFIGURATION PARAMETERS', 
                fontweight='bold', ha='center', fontsize=12, 
                color=self.header_color, transform=ax1.transAxes)
        
        params_text = f"""Outer Radius: {config_params['outer_radius']:.2f}
Inner Radius: {config_params['inner_radius']:.2f}
Height: {config_params['height']:.2f}
Number of Turns: {config_params['num_turns']:.2f}
Phase Offset: {config_params['phase_offset'] * 180 / np.pi:.1f}°
Structural Lines: {config_params.get('struct_lines', 0):.2f}"""
        
        ax1.text(0.1, 0.7, params_text, fontsize=10, va='top', 
                transform=ax1.transAxes, family='monospace',
                bbox=dict(boxstyle="round,pad=0.3", facecolor=self.bg_color))
        
        # Analytical results (top right)
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.axis('off')
        ax2.text(0.5, 0.9, 'ANALYTICAL RESULTS', 
                fontweight='bold', ha='center', fontsize=12, 
                color=self.header_color, transform=ax2.transAxes)
        
        analytical = comparison['analytical']
        analytical_text = f"""Outer Spiral: {analytical['outer']:.4f}
Inner Spiral: {analytical['inner']:.4f}
Total Length: {analytical['total']:.4f}
Error Margin: ±{analytical['error']:.6f}"""
        
        ax2.text(0.1, 0.7, analytical_text, fontsize=10, va='top', 
                transform=ax2.transAxes, family='monospace',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='#e8f5e8'))
        
        # Method comparison chart
        ax3 = fig.add_subplot(gs[1, :])
        methods = ['Analytical', 'Numerical', 'Circular\nApproximation']
        values = [
            comparison['analytical']['total'],
            comparison['numerical']['total'],
            comparison['circular_approximation']['total']
        ]
        colors = ['#2ecc71', '#3498db', '#e74c3c']
        
        bars = ax3.bar(methods, values, color=colors, alpha=0.7, edgecolor='black')
        ax3.set_ylabel('Total Length', fontweight='bold')
        ax3.set_title('METHOD COMPARISON', fontweight='bold', color=self.header_color)
        ax3.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # Accuracy differences (bottom left)
        ax4 = fig.add_subplot(gs[2, 0])
        ax4.axis('off')
        ax4.text(0.5, 0.9, 'ACCURACY DIFFERENCES', 
                fontweight='bold', ha='center', fontsize=12, 
                color=self.header_color, transform=ax4.transAxes)
        
        differences = comparison['differences']
        diff_text = f"""Analytical vs Numerical:
  {differences['analytical_vs_numerical']:.6f}

Analytical vs Circular:
  {differences['analytical_vs_circular']:.6f}

Numerical vs Circular:
  {differences['numerical_vs_circular']:.6f}"""
        
        ax4.text(0.1, 0.7, diff_text, fontsize=9, va='top', 
                transform=ax4.transAxes, family='monospace',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='#fff3cd'))
        
        # Additional metrics (bottom right)
        ax5 = fig.add_subplot(gs[2, 1])
        ax5.axis('off')
        ax5.text(0.5, 0.9, 'ADDITIONAL METRICS', 
                fontweight='bold', ha='center', fontsize=12, 
                color=self.header_color, transform=ax5.transAxes)
        
        struct_lines = config_params['height'] * config_params.get('struct_lines', 0)
        total_with_struct = comparison['analytical']['total'] + struct_lines
        
        metrics_text = f"""Net Length: {net_length:.4f}

Structural Lines: {struct_lines:.2f}

Total with Structure: {total_with_struct:.2f}

Turns Used (Circular): {comparison['circular_approximation']['turns']:.0f}"""
        
        ax5.text(0.1, 0.7, metrics_text, fontsize=9, va='top', 
                transform=ax5.transAxes, family='monospace',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='#d1ecf1'))
        
        # Performance indicator
        ax6 = fig.add_subplot(gs[3, :])
        
        # Calculate relative errors
        rel_error_num = abs(differences['analytical_vs_numerical']) / comparison['analytical']['total'] * 100
        rel_error_circ = abs(differences['analytical_vs_circular']) / comparison['analytical']['total'] * 100
        
        categories = ['Numerical\nAccuracy', 'Circular\nAccuracy']
        accuracies = [100 - rel_error_num, 100 - rel_error_circ]
        colors = ['#27ae60', '#e67e22']
        
        bars = ax6.barh(categories, accuracies, color=colors, alpha=0.7)
        ax6.set_xlabel('Accuracy (%)', fontweight='bold')
        ax6.set_title('METHOD ACCURACY RELATIVE TO ANALYTICAL', fontweight='bold', color=self.header_color)
        ax6.set_xlim(0, 100)
        ax6.grid(True, alpha=0.3, axis='x')
        
        # Add percentage labels
        for bar, accuracy in zip(bars, accuracies):
            width = bar.get_width()
            ax6.text(width - 5, bar.get_y() + bar.get_height()/2,
                    f'{accuracy:.3f}%', ha='right', va='center', 
                    fontweight='bold', color='white')
        
        pdf_pages.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def create_comparison_table_page(self, pdf_pages, all_results, configurations):
        """Create comprehensive comparison table"""
        fig, ax = plt.subplots(figsize=(11, 8.5))  # Landscape for table
        ax.axis('off')
        
        # Title
        ax.text(0.5, 0.95, 'CONFIGURATION COMPARISON TABLE', 
                fontsize=16, fontweight='bold', ha='center', 
                color=self.title_color, transform=ax.transAxes)
        
        # Prepare table data and extract analytical totals
        headers = ['Configuration', 'Analytical', 'Numerical', 'Circular', 'Best Match', 'Struct Lines', 'Net Length', 'Total w/ Struct']
        table_data = []
        analytical_totals = []  # Define this here to fix the NameError
        
        # Handle different tuple structures from main script vs generate_full_report
        for i, result_tuple in enumerate(all_results):
            if len(result_tuple) == 3:  # From main script: (name, comparison, net_length)
                name, comparison, net_length = result_tuple
            elif len(result_tuple) == 6:  # From generate_full_report: (name, comparison, net_length, spiral, flat_circles, config_params)
                name, comparison, net_length, spiral, flat_circles, config_params = result_tuple
            else:
                raise ValueError(f"Unexpected tuple structure in all_results: {len(result_tuple)} elements")
            
            short_name = name.split('.')[1].strip() if '.' in name else name
            analytical_total = comparison['analytical']['total']
            numerical_total = comparison['numerical']['total']
            circular_total = comparison['circular_approximation']['total']
            
            # Add to our list for summary statistics
            analytical_totals.append(analytical_total)
            
            config_params = configurations[i]['params']
            struct_lines = config_params['height'] * config_params.get('struct_lines', 0)
            total_with_struct = analytical_total + struct_lines
            
            # Find best match
            num_diff = abs(analytical_total - numerical_total)
            circ_diff = abs(analytical_total - circular_total)
            best_match = "Numerical" if num_diff < circ_diff else "Circular"
            
            row = [
                short_name,
                f"{analytical_total:.2f}",
                f"{numerical_total:.2f}",
                f"{circular_total:.2f}",
                best_match,
                f"{struct_lines:.2f}",
                f"{net_length:.4f}",
                f"{total_with_struct:.2f}"
            ]
            table_data.append(row)
        
        # Create table
        table = ax.table(cellText=table_data,
                        colLabels=headers,
                        cellLoc='center',
                        loc='center',
                        bbox=[0.05, 0.2, 0.9, 0.6])
        
        # Style the table
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 2)
        
        # Header styling
        for i in range(len(headers)):
            table[(0, i)].set_facecolor('#34495e')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        # Alternate row colors
        for i in range(1, len(table_data) + 1):
            for j in range(len(headers)):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#f8f9fa')
                else:
                    table[(i, j)].set_facecolor('white')
        
        # Add summary statistics below table (now using the correctly defined analytical_totals)
        summary_text = f"""
        TABLE SUMMARY:
        • Total Configurations: {len(all_results)}
        • Average Analytical Length: {np.mean(analytical_totals):.2f}
        • Standard Deviation: {np.std(analytical_totals):.2f}
        • Range: {min(analytical_totals):.2f} - {max(analytical_totals):.2f}
        """
        
        ax.text(0.5, 0.1, summary_text, fontsize=10, ha='center', va='top',
                transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.3", facecolor=self.bg_color))
        
        pdf_pages.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def embed_visualization_pages(self, pdf_pages, config_name, spiral, flat_circles, config_params):
        """Embed visualization plots in the report"""
        # Create plotter
        plotter = SpiralPlotter(spiral)
        
        # Combined visualization page
        fig_combined, axes = plotter.plot_combined(show_cone=True)
        fig_combined.suptitle(f'3D VISUALIZATION: {config_name}', 
                             fontsize=14, fontweight='bold', color=self.title_color)
        pdf_pages.savefig(fig_combined, bbox_inches='tight')
        plt.close(fig_combined)
        
        # Annular net page
        fig_net = plotter.plot_all_annular_regions_net(
            flat_circles, 
            config_params.get('target_spacing', 1.0),
            config_params.get('arc_span_deg', 180), 
            config_params.get('arc_density', 50)
        )
        fig_net.suptitle(f'ANNULAR NET APPROXIMATION: {config_name}', 
                        fontsize=14, fontweight='bold', color=self.title_color)
        pdf_pages.savefig(fig_net, bbox_inches='tight')
        plt.close(fig_net)
    
    def generate_full_report(self, configurations_file='config.yaml'):
        """Generate complete PDF report"""
        print("Generating comprehensive spiral analysis report...")
        
        # Load configurations
        try:
            with open(configurations_file, 'r') as f:
                data = yaml.safe_load(f)
            configurations = data['configurations']
        except FileNotFoundError:
            print(f"Configuration file '{configurations_file}' not found!")
            return None
        
        # Process all configurations
        all_results = []
        for config in configurations:
            spiral = DoubleConicalSpiral(**config['params'])
            comparison = spiral.compare_all_methods(num_points_numerical=1000, num_slices_circular=100)
            flat_circles = spiral.get_xy_circles_for_visualization()
            net_length = spiral.calculate_net_length_angles(flat_circles)
            
            # Store with 6-tuple structure for internal use
            all_results.append((config['name'], comparison, net_length, spiral, flat_circles, config['params']))
        
        # Generate report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = os.path.join(self.output_dir, f"spiral_analysis_report_{timestamp}.pdf")
        
        with PdfPages(report_filename) as pdf_pages:
            # Title page
            self.create_title_page(pdf_pages)
            
            # Executive summary
            self.create_summary_page(pdf_pages, all_results, configurations)
            
            # Comparison table
            self.create_comparison_table_page(pdf_pages, all_results, configurations)
            
            # Individual configuration pages
            for name, comparison, net_length, spiral, flat_circles, config_params in all_results:
                # Detailed analysis page
                self.create_configuration_detail_page(pdf_pages, name, comparison, config_params, net_length)
                
                # Visualization pages
                self.embed_visualization_pages(pdf_pages, name, spiral, flat_circles, config_params)
        
        print(f"Report generated successfully: {report_filename}")
        return report_filename


def generate_report():
    """Main function to generate the automated report"""
    generator = SpiralReportGenerator()
    report_file = generator.generate_full_report()
    
    if report_file:
        print(f"\n{'='*60}")
        print("AUTOMATED REPORT GENERATION COMPLETE")
        print(f"{'='*60}")
        print(f"Report saved as: {report_file}")
        print(f"Report size: {os.path.getsize(report_file) / 1024 / 1024:.2f} MB")
        print("\nReport includes:")
        print("• Executive summary with key findings")
        print("• Detailed analysis for each configuration")
        print("• Comprehensive comparison tables")
        print("• 3D visualizations and projections")
        print("• Annular net approximations")
        print("• Professional formatting and styling")


if __name__ == "__main__":
    generate_report()