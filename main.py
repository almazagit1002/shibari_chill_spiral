#!/usr/bin/env python3
"""
Enhanced main script with automated report generation
Combines spiral analysis with comprehensive PDF reporting
"""

import yaml
import numpy as np
import argparse
import os
from spiral_calculations import DoubleConicalSpiral
from spiral_plots import SpiralPlotter
from report_generator import SpiralReportGenerator

def analyze_spiral_configuration(spiral, config_name, config_params):
    """Analyze a spiral configuration and print results"""
    print(f"\n{config_name}")
    print("=" * len(config_name))
    
    # Calculate perimeters using all methods
    comparison = spiral.compare_all_methods(num_points_numerical=1000, num_slices_circular=100)
    
    # Print configuration details in a more organized way
    print("CONFIGURATION PARAMETERS:")
    print("-" * 40)
    print(f"{'Outer Radius:':<20} {spiral.R_outer:>8.2f}")
    print(f"{'Inner Radius:':<20} {spiral.R_inner:>8.2f}")
    print(f"{'Height:':<20} {spiral.h:>8.2f}")
    print(f"{'Number of Turns:':<20} {spiral.n * spiral.h / (2 * np.pi):>8.2f}")
    print(f"{'Phase Offset:':<20} {spiral.phase_offset * 180 / np.pi:>8.0f}°")
    
    # Add structural lines if available
    if 'struct_lines' in config_params:
        struct_lines = config_params['height'] * config_params['struct_lines']
        print(f"{'Structural Lines:':<20} {struct_lines:>8.2f}")
    
    # Print all method results in organized format
    print("\nPERIMETER CALCULATIONS:")
    print("=" * 50)
    
    print("Analytical Method (Exact):")
    print("-" * 25)
    analytical = comparison['analytical']
    print(f"  {'Outer Spiral:':<15} {analytical['outer']:>10.4f}")
    print(f"  {'Inner Spiral:':<15} {analytical['inner']:>10.4f}")
    print(f"  {'Total Length:':<15} {analytical['total']:>10.4f}")
    print(f"  {'Error Margin:':<15} {analytical['error']:>10.6f}")
    
    print("\nNumerical Method (Discrete Approximation):")
    print("-" * 40)
    numerical = comparison['numerical']
    print(f"  {'Outer Spiral:':<15} {numerical['outer']:>10.4f}")
    print(f"  {'Inner Spiral:':<15} {numerical['inner']:>10.4f}")
    print(f"  {'Total Length:':<15} {numerical['total']:>10.4f}")
    
    print("\nCircular Approximation Method:")
    print("-" * 30)
    circular = comparison['circular_approximation']
    print(f"  {'Outer Spiral:':<15} {circular['outer']:>10.4f}")
    print(f"  {'Inner Spiral:':<15} {circular['inner']:>10.4f}")
    print(f"  {'Total Length:':<15} {circular['total']:>10.4f}")
    print(f"  {'Turns Used:':<15} {circular['turns']:>10.0f}")
    
    # Print differences in organized format
    print("\nMETHOD ACCURACY COMPARISON:")
    print("=" * 40)
    differences = comparison['differences']
    print(f"{'Analytical vs Numerical:':<25} {differences['analytical_vs_numerical']:>10.6f}")
    print(f"{'Analytical vs Circular:':<25} {differences['analytical_vs_circular']:>10.6f}")
    print(f"{'Numerical vs Circular:':<25} {differences['numerical_vs_circular']:>10.6f}")
    
    return comparison

def create_visualizations(spiral, circles, config_name, config_params, save_individual=True):
    """Create all visualizations for a spiral configuration"""
    print(f"\nGenerating visualizations for {config_name}...")
    
    # Create plotter
    plotter = SpiralPlotter(spiral)
    
    # Create all plots
    fig_combined, (ax_3d, ax_xz, ax_xy, ax_aprox) = plotter.plot_combined(show_cone=True)
    anular_net = plotter.plot_all_annular_regions_net(circles, config_params.get('target_spacing', 1.0),
                                                      config_params.get('arc_span_deg', 180), 
                                                      config_params.get('arc_density', 50))

    # Save individual plots if requested
    if save_individual:
        os.makedirs("plots", exist_ok=True)
        safe_name = config_name.replace(" ", "_").replace("(", "").replace(")", "").replace("°", "deg")
        fig_combined.savefig(f"plots/{safe_name}_combined.pdf", bbox_inches='tight')
        anular_net.savefig(f"plots/{safe_name}_net.pdf", bbox_inches='tight')

    return fig_combined, anular_net

def load_configurations(config_file='config.yaml'):
    """Load spiral configurations from YAML file"""
    try:
        with open(config_file, 'r') as f:
            data = yaml.safe_load(f)
        return data['configurations']
    except FileNotFoundError:
        print(f"Configuration file '{config_file}' not found!")
        print("Using default configuration...")
        # Fallback configuration
        return [
            {
                'name': '1. Aligned Spirals (0° phase offset)',
                'params': {
                    'outer_radius': 15,
                    'inner_radius': 5,
                    'height': 20,
                    'num_turns': 4,
                    'phase_offset': 0,
                    'struct_lines': 1.0,
                    'target_spacing': 1.0,
                    'arc_span_deg': 180,
                    'arc_density': 50
                }
            }
        ]
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return []

def print_summary_tables(all_results, configurations):
    """Print comprehensive summary tables"""
    print("\n" + "="*140)
    print("CONFIGURATION COMPARISON SUMMARY")
    print("="*140)
    
    # Header for main comparison
    header = f"{'Configuration':<30} {'Analytical':<12} {'Numerical':<12} {'Circular':<12} {'Best Match':<15} {'Struct Lines':<12} {'Net Length':<12}"
    print(header)
    print("-" * 140)

    for i, (name, comparison, net_angles) in enumerate(all_results):
        short_name = name.split('.')[1].strip() if '.' in name else name
        analytical_total = comparison['analytical']['total']
        numerical_total = comparison['numerical']['total']
        circular_total = comparison['circular_approximation']['total']
        
        # Calculate structural lines
        config_params = configurations[i]['params']
        struct_lines = config_params['height'] * config_params.get('struct_lines', 0)
        
        # Find which approximation is closest to analytical
        num_diff = abs(analytical_total - numerical_total)
        circ_diff = abs(analytical_total - circular_total)
        best_match = "Numerical" if num_diff < circ_diff else "Circular"
        
        print(f"{short_name:<30} {analytical_total:>9.2f}   {numerical_total:>9.2f}   {circular_total:>9.2f}   {best_match:<15} {struct_lines:>9.2f}   {net_angles:>9.4f}")

    # Structural Configuration Summary
    print("\n" + "="*100)
    print("STRUCTURAL CONFIGURATION SUMMARY (Spiral + Structural Lines)")
    print("="*100)
    print(f"{'Configuration':<30} {'Spiral Length':<15} {'Struct Lines':<15} {'Total Length':<15}")
    print("-" * 100)
    
    for i, (name, comparison, net_angles) in enumerate(all_results):
        short_name = name.split('.')[1].strip() if '.' in name else name
        spiral_length = comparison['analytical']['total']
        config_params = configurations[i]['params']
        struct_lines = config_params['height'] * config_params.get('struct_lines', 0)
        total_length = spiral_length + struct_lines
        
        print(f"{short_name:<30} {spiral_length:>12.2f}   {struct_lines:>12.2f}   {total_length:>12.2f}")

    # Net Length Configuration Summary
    print("\n" + "="*80)
    print("NET LENGTH CONFIGURATION SUMMARY")
    print("="*80)
    print(f"{'Configuration':<30} {'Net Length':<15}")
    print("-" * 80)
    
    for name, comparison, net_length in all_results:
        short_name = name.split('.')[1].strip() if '.' in name else name
        print(f"{short_name:<30} {net_length:>12.4f}")

def main():
    """Main function to run the analysis with optional report generation"""
    parser = argparse.ArgumentParser(description='Double Conical Spiral Analysis with Report Generation')
    parser.add_argument('--report', '-r', action='store_true', 
                       help='Generate comprehensive PDF report')
    parser.add_argument('--config', '-c', default='config.yaml',
                       help='Configuration file (default: config.yaml)')
    parser.add_argument('--output-dir', '-o', default='reports',
                       help='Output directory for reports (default: reports)')
    parser.add_argument('--no-plots', action='store_true',
                       help='Skip individual plot generation')
    parser.add_argument('--console-only', action='store_true',
                       help='Run console analysis only (no visualizations)')
    
    args = parser.parse_args()
    
    print("DOUBLE CONICAL SPIRAL ANALYSIS")
    print("=" * 60)
    
    # Load configurations from YAML file
    configurations = load_configurations(args.config)
    
    if not configurations:
        print("No valid configurations found!")
        return
    
    # Store results for comparison
    all_results = []

    for config in configurations:
        spiral = DoubleConicalSpiral(**config['params'])

        # Analyze
        comparison = analyze_spiral_configuration(spiral, config['name'], config['params'])

        # Visualize flat XY circles
        flat_circles = spiral.get_xy_circles_for_visualization()
        print("\nFLAT XY CIRCLES (Approximation):")
        print("-" * 35)
        for i, c in enumerate(flat_circles):
            print(f"  Circle {i+1:>2}: r_outer={c['r_outer']:>6.2f}, r_inner={c['r_inner']:>6.2f}")

        net_length_angles = spiral.calculate_net_length_angles(flat_circles)  
        
        # Store results
        all_results.append((config['name'], comparison, net_length_angles))
        
        # Create visualizations unless console-only mode
        if not args.console_only:
            fig_combined, anular_net = create_visualizations(
                spiral, flat_circles, config['name'], config['params'], 
                save_individual=not args.no_plots
            )

    # Print comparison summaries
    print_summary_tables(all_results, configurations)

    # Generate comprehensive report if requested
    if args.report:
        print(f"\n{'='*60}")
        print("GENERATING COMPREHENSIVE PDF REPORT")
        print(f"{'='*60}")
        
        generator = SpiralReportGenerator(output_dir=args.output_dir)
        report_file = generator.generate_full_report(args.config)
        
        if report_file:
            print(f"\nReport generated successfully!")
            print(f"Location: {report_file}")
            print(f"Size: {os.path.getsize(report_file) / 1024 / 1024:.2f} MB")
            print("\nReport includes:")
            print("• Executive summary with key findings")
            print("• Detailed analysis for each configuration")
            print("• Comprehensive comparison tables")
            print("• 3D visualizations and projections")
            print("• Annular net approximations")
            print("• Professional formatting and styling")
        else:
            print("Report generation failed!")
    
    # Save basic visualizations if not in console-only mode
    if not args.console_only and not args.no_plots:
        print(f"\nSaving combined visualizations...")
        # Note: Individual plots already saved in create_visualizations
        print("Individual plots saved in 'plots/' directory")

    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE!")
    print(f"{'='*60}")
    
    if args.report:
        print(f"✓ Comprehensive PDF report generated")
    if not args.console_only:
        print(f"✓ Visualizations created")
        if not args.no_plots:
            print(f"✓ Individual plots saved")
    print(f"✓ Console analysis completed")

if __name__ == "__main__":
    main()