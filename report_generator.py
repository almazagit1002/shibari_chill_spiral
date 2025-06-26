#!/usr/bin/env python3
"""
Simplified Automated Report Generator for Double Conical Spiral Analysis
Generates streamlined PDF reports with essential findings and visualizations
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
    """Generates simplified PDF reports for spiral analysis"""
    
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
        ax.text(0.5, 0.62, 'Simplified Analysis of Spiral Configurations', 
                fontsize=16, ha='center', style='italic',
                color=self.header_color, transform=ax.transAxes)
        
        # Date and time
        timestamp = datetime.now().strftime("%B %d, %Y at %H:%M")
        
        
        # Add decorative elements
        rect = Rectangle((0.1, 0.35), 0.8, 0.02, 
                        facecolor=self.accent_color, alpha=0.8)
        ax.add_patch(rect)
        
        # Analysis methods
        methods_text = """
        CONTENTS:
        
        • Configuration Parameters Summary
        • Configuration Comparison Table
        • 3D Visualization and Projections
        • Annular Net Approximations
        """
        
        ax.text(0.5, 0.25, methods_text, 
                fontsize=11, ha='center', va='top',
                color=self.header_color, transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.3", 
                         facecolor=self.bg_color, alpha=0.8))
        
        pdf_pages.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def create_configuration_parameters_page(self, pdf_pages, configurations):
        """Create configuration parameters summary page"""
        fig, ax = plt.subplots(figsize=(11, 8.5))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # Page title
        ax.text(0.5, 0.95, 'CONFIGURATION PARAMETERS', 
                fontsize=20, fontweight='bold', ha='center', 
                color=self.title_color, transform=ax.transAxes)
        
        # Create parameters table
        headers = ['Config', 'Outer R', 'Inner R', 'Height', 'Turns', 'Struct Lines']
        table_data = []
        
        for config in configurations:
            params = config['params']
            short_name = config['name'].split('.')[1].strip() if '.' in config['name'] else config['name']
            
            row = [
                short_name,
                f"{params['outer_radius']:.2f}",
                f"{params['inner_radius']:.2f}",
                f"{params['height']:.2f}",
                f"{params['num_turns']:.2f}",
                f"{params.get('struct_lines', 0):.2f}"
            ]
            table_data.append(row)
        
        # Create table
        # Create table
        table = ax.table(cellText=table_data,
                        colLabels=headers,
                        cellLoc='center',
                        loc='center',
                        bbox=[0.05, 0.2, 0.9, 0.6])
        
        # Style the table
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2.5)
        
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
        
        # Prepare table data
        headers = ['Configuration', 'Analytical', 'Numerical', 'Circular', 'Struct Lines', 'Net Length', 'Total w/ Struct']
        table_data = []
        analytical_totals = []
        
        for i, result_tuple in enumerate(all_results):
            if len(result_tuple) == 3:
                name, comparison, net_length = result_tuple
            elif len(result_tuple) == 6:
                name, comparison, net_length, spiral, flat_circles, config_params = result_tuple
            else:
                raise ValueError(f"Unexpected tuple structure in all_results: {len(result_tuple)} elements")
            
            short_name = name.split('.')[1].strip() if '.' in name else name
            analytical_total = comparison['analytical']['total']
            numerical_total = comparison['numerical']['total']
            circular_total = comparison['circular_approximation']['total']
            
            analytical_totals.append(analytical_total)
            
            config_params = configurations[i]['params']
            struct_lines = config_params['height'] * config_params.get('struct_lines', 0)
            total_with_struct = analytical_total + struct_lines
            
            row = [
                short_name,
                f"{analytical_total:.2f}",
                f"{numerical_total:.2f}",
                f"{circular_total:.2f}",
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
        
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 2)
        
        for i in range(len(headers)):
            table[(0, i)].set_facecolor('#34495e')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        for i in range(1, len(table_data) + 1):
            for j in range(len(headers)):
                table[(i, j)].set_facecolor('#f8f9fa' if i % 2 == 0 else 'white')
        
        # ✅ Save the page to the PDF
        pdf_pages.savefig(fig, bbox_inches='tight')
        plt.close(fig)

    
    def embed_visualization_pages(self, pdf_pages, config_name, spiral, flat_circles, config_params):
        """Embed visualization plots in the report with figure captions"""

        plotter = SpiralPlotter(spiral)

        # === 1. 3D Spiral Visualization ===
        fig_combined, axes = plotter.plot_combined(show_cone=True)
        fig_combined.set_size_inches(6.5, 5.0)  # Resize for report

        # Add a figure caption below the plot
        fig_combined.subplots_adjust(bottom=0.2)  # Make space for caption
        fig_combined.suptitle("")  # Remove original title
        
        pdf_pages.savefig(fig_combined, bbox_inches='tight')
        plt.close(fig_combined)

        # === 2. Annular Net Visualization ===
        fig_net = plotter.plot_all_annular_regions_net(
            flat_circles,
            config_params.get('target_spacing', 1.0),
            config_params.get('arc_span_deg', 180),
            config_params.get('arc_density', 50)
        )
        fig_net.set_size_inches(6.5, 5.0)  # Resize for report

        fig_net.subplots_adjust(bottom=0.2)
        fig_net.suptitle("")
        

        pdf_pages.savefig(fig_net, bbox_inches='tight')
        plt.close(fig_net)

    
    def generate_full_report(self, configurations_file='config.yaml'):
        """Generate simplified PDF report"""
        print("Generating simplified spiral analysis report...")
        
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
            
            # Configuration parameters page
            self.create_configuration_parameters_page(pdf_pages, configurations)
            
            # Comparison table
            self.create_comparison_table_page(pdf_pages, all_results, configurations)
            
            # Visualization pages for each configuration
            for name, comparison, net_length, spiral, flat_circles, config_params in all_results:
                self.embed_visualization_pages(pdf_pages, name, spiral, flat_circles, config_params)
        
        print(f"Report generated successfully: {report_filename}")
        return report_filename


def generate_report():
    """Main function to generate the simplified report"""
    generator = SpiralReportGenerator()
    report_file = generator.generate_full_report()
    
    if report_file:
        print(f"\n{'='*60}")
        print("SIMPLIFIED REPORT GENERATION COMPLETE")
        print(f"{'='*60}")
        print(f"Report saved as: {report_file}")
        print(f"Report size: {os.path.getsize(report_file) / 1024 / 1024:.2f} MB")
        print("\nReport includes:")
        print("• Configuration parameters summary")
        print("• Comprehensive comparison table")
        print("• 3D visualizations for each configuration")
        print("• Annular net approximations")


if __name__ == "__main__":
    generate_report()