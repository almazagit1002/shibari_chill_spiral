import os
import yaml
import numpy as np
from pylatex import Document, Section, Subsection, Command, Package, NewPage, Itemize, Enumerate
from pylatex.base_classes import Environment
from pylatex.table import Tabular, Table
from pylatex.utils import bold, NoEscape
from pylatex import Figure, SubFigure
from pylatex.package import Package
from pylatex.tikz import TikZ, Axis, Plot
import matplotlib.pyplot as plt
from spiral_calculations import DoubleConicalSpiral
from spiral_plots import SpiralPlotter

class StoryDrivenLatexReportGenerator:
    """Generates narrative-focused LaTeX PDF reports for spiral analysis"""
    
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize LaTeX document with custom styling
        geometry_options = {
            "head": "40pt",
            "margin": "0.8in",
            "bottom": "0.8in",
            "includeheadfoot": True
        }
        
        self.doc = Document(geometry_options=geometry_options)
        self._setup_document()
        
    def _setup_document(self):
        """Setup LaTeX document with packages and styling"""
        # Add necessary packages
        self.doc.packages.append(Package('xcolor'))
        self.doc.packages.append(Package('graphicx'))
        self.doc.packages.append(Package('booktabs'))
        self.doc.packages.append(Package('array'))
        self.doc.packages.append(Package('longtable'))
        self.doc.packages.append(Package('fancyhdr'))
        self.doc.packages.append(Package('titlesec'))
        self.doc.packages.append(Package('tcolorbox'))
        self.doc.packages.append(Package('amsmath'))
        self.doc.packages.append(Package('enumitem'))
        
        # Define custom colors
        self.doc.preamble.append(Command('definecolor', arguments=['titlecolor', 'HTML', '2c3e50']))
        self.doc.preamble.append(Command('definecolor', arguments=['headercolor', 'HTML', '34495e']))
        self.doc.preamble.append(Command('definecolor', arguments=['accentcolor', 'HTML', '3498db']))
        self.doc.preamble.append(Command('definecolor', arguments=['storycolor', 'HTML', '27ae60']))
        self.doc.preamble.append(Command('definecolor', arguments=['bgcolor', 'HTML', 'f8f9fa']))
        
        # Custom title formatting
        self.doc.preamble.append(NoEscape(r'''
            \titleformat{\section}
              {\Large\bfseries\color{titlecolor}}
              {\thesection}{1em}{}
            \titleformat{\subsection}
              {\large\bfseries\color{headercolor}}
              {\thesubsection}{1em}{}
        '''))
        
        # Custom tcolorbox styles
        self.doc.preamble.append(NoEscape(r'''
            \newtcolorbox{storybox}[1][]{
              colback=bgcolor,
              colframe=storycolor,
              coltitle=white,
              fonttitle=\bfseries,
              title=#1,
              rounded corners
            }
            \newtcolorbox{chapterbox}[1][]{
              colback=white,
              colframe=accentcolor,
              coltitle=white,
              fonttitle=\bfseries,
              title=#1,
              rounded corners,
              boxrule=2pt
            }
        '''))
    
    def create_title_page(self):
        """Create professional title page"""
        self.doc.append(NoEscape(r'\begin{center}'))

        # Main title
        self.doc.append(NoEscape(r'\vspace*{2cm}'))
        self.doc.append(NoEscape(r'{\Huge\bfseries\color{titlecolor} DOUBLE CONICAL SPIRAL}'))
        self.doc.append(NoEscape(r'\\[0.5cm]'))
        # FIXED: Removed extra \\[1cm] that was causing the error
        
        # Subtitle
        self.doc.append(NoEscape(r'{\Large\itshape\color{headercolor} Mathematical Perimeter and Physical Net Design}'))
        self.doc.append(NoEscape(r'\\[2cm]'))

        #  outline in a box
        self.doc.append(NoEscape(r'\begin{chapterbox}[DESIGN PROCESS]'))
        with self.doc.create(Enumerate(options=[NoEscape(r'label=Section \arabic*:'), 'leftmargin=2cm'])) as enum:
            enum.add_item(NoEscape(r'\textbf{Understanding the Spiral Geometry} \\ Configuration parameters and mathematical foundation'))
            enum.add_item(NoEscape(r'\textbf{Calculating the True Perimeter} \\ Analytical integration vs numerical approximation'))
            enum.add_item(NoEscape(r'\textbf{Discovering the Circular Approximation} \\ From XZ projection to simplified circular regions'))
            enum.add_item(NoEscape(r'\textbf{Creating the Annular Net} \\ Transforming geometry into manufacturable nets'))
            enum.add_item(NoEscape(r'\textbf{Validation and Results} \\ Comparing all methods and final measurements'))
        self.doc.append(NoEscape(r'\end{chapterbox}'))

        self.doc.append(NoEscape(r'\vfill'))
        self.doc.append(NoEscape(r'\end{center}'))
        self.doc.append(NewPage())

    def create_chapter1_parameters(self, configurations):
        """ Understanding the Spiral Geometry"""
        with self.doc.create(Section('Understanding the Spiral Geometry')):

            # Introduction box
            self.doc.append(NoEscape(r'\begin{storybox}[Introduction]'))
            _text = """
            We start by establishing the mathematical basis for double conical spirals.
            Each configuration presents distinct geometric challenges, influenced by variations in radius, height, and structural complexity.
            These parameters will guide the design process throughout.
            """
            self.doc.append(_text.strip())
            self.doc.append(NoEscape(r'\end{storybox}'))

            self.doc.append(NoEscape(r'\vspace{1cm}'))

            # Parameters table
            with self.doc.create(Table(position='h!')) as table:
                table.add_caption('Configuration Parameters')

                # Open manual center environment
                table.append(NoEscape(r'\begin{center}'))

                with table.create(Tabular('|l|c|c|c|c|c|', booktabs=True)) as tabular:
                    # Header
                    tabular.add_hline()
                    tabular.add_row([
                        bold('Configuration'), bold('Outer R'), bold('Inner R'), 
                        bold('Height'), bold('Turns'), bold('Struct Lines')
                    ])
                    tabular.add_hline()

                    # Data rows
                    for config in configurations:
                        params = config['params']
                        short_name = config['name'].split('.')[1].strip() if '.' in config['name'] else config['name']
                        tabular.add_row([
                            short_name,
                            f"{params['outer_radius']:.2f}",
                            f"{params['inner_radius']:.2f}",
                            f"{params['height']:.2f}",
                            f"{params['num_turns']:.2f}",
                            f"{params.get('struct_lines', 0):.2f}"
                        ])

                    tabular.add_hline()

                # Close manual center environment
                table.append(NoEscape(r'\end{center}'))

            self.doc.append(NoEscape(r'\vspace{1cm}'))

    def create_chapter2_perimeter(self, all_results, configurations):
        """Calculating the True Perimeter"""
        with self.doc.create(Section('Calculating the True Perimeter')):

            #  narrative
            self.doc.append(NoEscape(r'\begin{storybox}[The Challenge]'))
            story_text = r"""
            A critical step in our structural design is calculating the true perimeter of each double conical spiral—
            that is, the actual length of material required to construct each spiral path. This perimeter is not trivial
            to compute due to the complex geometry involving conical tapering, variable radii, and helical motion.

            We apply three distinct methods to approach this problem, each offering a different balance of precision and complexity:

            \begin{itemize}
                \item \textbf{Analytical Method:} Based on the arc length of a 3D parametric curve, we compute the exact integral:
                \[
                    L = \int_0^h \sqrt{\left(\frac{dR}{dz}\right)^2 + \left(R(z) \frac{d\theta}{dz}\right)^2 + 1} \, dz
                \]
                where \( R(z) = R_0 \left(1 - \frac{z}{h} \right) \) defines the spiral's decreasing radius with height, and 
                \( \theta(z) = n z \) captures the angular rotation. This method yields the highest accuracy.

                \item \textbf{Numerical Method:} A discrete sampling approach where the spiral path is broken into thousands of small
                linear segments in 3D space. We compute the Euclidean distance between points:
                \[
                    L \approx \sum_{i=1}^{N-1} \sqrt{ \Delta x_i^2 + \Delta y_i^2 + \Delta z_i^2 }
                \]
                This provides a reliable approximation, especially for visual validation.

                \item \textbf{Circular Approximation:} A simplified model that treats each spiral as a series of flat circular arcs in the XY-plane, 
                ignoring vertical movement. The total length becomes:
                \[
                    L = \sum_{i=1}^{N} 2\pi R_i
                \]
                where \( R_i \) is the instantaneous radius at each step. This is useful for quick estimations but underestimates the actual path length.
            \end{itemize}

            Comparing these approaches not only validates our results but also highlights the geometric impact of vertical travel,
            radius tapering, and angular acceleration on material length.
            """
            self.doc.append(NoEscape(story_text.strip()))
            self.doc.append(NoEscape(r'\end{storybox}'))

            self.doc.append(NoEscape(r'\vspace{1cm}'))

            # Results table
            with self.doc.create(Table(position='h!')) as table:
                table.add_caption('Perimeter Calculation Results')
                table.append(NoEscape(r'\begin{center}'))

                with table.create(Tabular('|l|c|c|c|c|c|', booktabs=True)) as tabular:
                    tabular.add_hline()
                    tabular.add_row([
                        bold('Configuration'), bold('Analytical'), bold('Numerical'), 
                        bold('Circular'), bold('Struct Lines'), bold('Total Length')
                    ])
                    tabular.add_hline()

                    for i, result_tuple in enumerate(all_results):
                        if len(result_tuple) >= 6:
                            name, comparison, net_length, spiral, flat_circles, config_params = result_tuple[:6]
                        else:
                            continue

                        short_name = name.split('.')[1].strip() if '.' in name else name
                        analytical_total = comparison['analytical']['total']
                        numerical_total = comparison['numerical']['total']
                        circular_total = comparison['circular_approximation']['total']

                        config_params = configurations[i]['params']
                        struct_lines = config_params['height'] * config_params.get('struct_lines', 0)
                        total_with_struct = analytical_total + struct_lines

                        tabular.add_row([
                            short_name,
                            f"{analytical_total:.2f}",
                            f"{numerical_total:.2f}",
                            f"{circular_total:.2f}",
                            f"{struct_lines:.2f}",
                            f"{total_with_struct:.2f}"
                        ])

                    tabular.add_hline()

                table.append(NoEscape(r'\end{center}'))

            self.doc.append(NoEscape(r'\vspace{1cm}'))
    
    def create_chapter3_visualization_story(self, config_name, spiral, flat_circles, config_params):
        """the Circular Approximation"""
        with self.doc.create(Section('The Circular Approximation')):

            # Configuration identifier
            short_name = config_name.split('.')[1].strip() if '.' in config_name else config_name
            self.doc.append(NoEscape(f'{{\\large\\itshape\\color{{accentcolor}} Configuration: {short_name}}}'))
            self.doc.append(NoEscape(r'\\[0.5cm]'))

            # Discovery 
            self.doc.append(NoEscape(r'\begin{storybox}[The Breakthrough]'))
            discovery_text = f"""
            When we examine the XZ projection of our spiral geometry, what appears as a complex 3D curve 
            reveals itself as a series of concentric circles when viewed from the top.

            This insight allows us to:
            \\begin{{itemize}}
                \\item Simplify the 3D spiral into manageable circular sections
                \\item Create annular (ring-shaped) regions between inner and outer spirals
                \\item Design a flat net pattern that can be manufactured and assembled
            \\end{{itemize}}

            For \\textbf{{{short_name}}}, we identified \\textbf{{{len(flat_circles)} circular regions}} that approximate
            the original spiral geometry while maintaining structural integrity.

            By applying this simplification: complex 3D mathematics becomes
            straightforward 2D circular geometry, perfect for visualization with a close approximation to the spiral.
            """
            self.doc.append(NoEscape(discovery_text.strip()))
            self.doc.append(NoEscape(r'\end{storybox}'))

            self.doc.append(NoEscape(r'\vspace{1cm}'))

            # Technical parameters table
            with self.doc.create(Table(position='h!')) as table:
                table.add_caption(f'Technical Parameters for {short_name}')
                table.append(NoEscape(r'\begin{center}'))

                with table.create(Tabular('|l|c|', booktabs=True)) as tabular:
                    tabular.add_hline()
                    tabular.add_row([bold('Parameter'), bold('Value')])
                    tabular.add_hline()
                    tabular.add_row(['Target Spacing', f"{config_params.get('target_spacing', 1.0):.1f} units"])
                    tabular.add_row(['Arc Span', f"{config_params.get('arc_span_deg', 180)}°"])
                    tabular.add_row(['Arc Density', f"{config_params.get('arc_density', 50)} points"])
                    tabular.add_row(['Circular Regions', f"{len(flat_circles)} layers"])
                    tabular.add_hline()

                table.append(NoEscape(r'\end{center}'))

            # Generate and include 3D visualization
            self._generate_and_include_3d_plot(spiral, short_name)
            self.doc.append(NoEscape(r'\vspace{1cm}'))
    
    def create_chapter4_net_creation(self, config_name, spiral, flat_circles, config_params, net_length):
        """Chapter 4: Creating the Annular Net"""
        with self.doc.create(Section('Creating the Annular Net')):

            short_name = config_name.split('.')[1].strip() if '.' in config_name else config_name
            self.doc.append(NoEscape(f'{{\\large\\itshape\\color{{accentcolor}} Configuration: {short_name}}}'))
            self.doc.append(NoEscape(r'\\[0.5cm]'))

            # Net creation 
            self.doc.append(NoEscape(r'\begin{storybox}[The Practical Aproach]'))
            net_text = f"""
            Now comes the practical aproach: transforming our circular approximation into
            a manufacturable flat pattern -- the annular net.

            \\textbf{{THE NET CREATION PROCESS:}}
            \\begin{{enumerate}}
                \\item \\textbf{{ANNULAR REGIONS:}} Each circular layer becomes a ring (annulus) in the flat pattern
                \\item \\textbf{{CONNECTION PATTERN:}} We create a web of connections between outer and inner
                    edges within specific angular spans to maintain structural integrity
                \\item \\textbf{{OPTIMIZED SPACING:}} Points are distributed to achieve uniform material density
                    with our target spacing of {config_params.get('target_spacing', 1.0):.1f} units
                \\item \\textbf{{ANGULAR CONTROL:}} Each connection spans {config_params.get('arc_span_deg', 180)}° 
                    with {config_params.get('arc_density', 50)} connection points for precision
            \\end{{enumerate}}

            \\textbf{{RESULT:}} The net for {short_name} requires \\textbf{{{net_length:.2f} units}} of connecting
            material, creating a pattern that can be cut flat and assembled into the 3D spiral.

            This represents the final step from mathematical concept to physical reality.
            """
            self.doc.append(NoEscape(net_text.strip()))
            self.doc.append(NoEscape(r'\end{storybox}'))

            # Generate and include net visualization
            self._generate_and_include_net_plot(spiral, flat_circles, config_params, short_name, net_length)

            # Manufacturing note
            self.doc.append(NoEscape(r'\vspace{1cm}'))
            self.doc.append(NoEscape(r'\begin{center}'))
            self.doc.append(NoEscape(
                f'{{\\large\\bfseries\\color{{storycolor}} MANUFACTURING READY: {net_length:.2f} units of connecting material in optimized pattern}}'
            ))
            self.doc.append(NoEscape(r'\end{center}'))
    
    def create_chapter5_conclusion(self, all_results, configurations):
        """Chapter 5: Validation and Final Results"""
        with self.doc.create(Section('Validation and Final Results')):

            # Conclusion 
            self.doc.append(NoEscape(r'\begin{storybox}[Approximation Complete]'))
            conclusion_text = """
            Teh approxiamtion from mathematical spiral to manufacturable net is complete.
            The final validation compares all our methods and confirms the design integrity.

            This comprehensive table shows the complete material requirements for each configuration,
            validating our approach from theoretical calculation through practical implementation.
            """
            self.doc.append(NoEscape(conclusion_text.strip()))
            self.doc.append(NoEscape(r'\end{storybox}'))

            self.doc.append(NoEscape(r'\vspace{1cm}'))

            # Final comprehensive table
            with self.doc.create(Table(position='h!')) as table:
                table.add_caption('Complete Material Requirements Analysis')
                table.append(NoEscape(r'\begin{center}'))
                with table.create(Tabular('|l|c|c|c|c|c|c|', booktabs=True)) as tabular:
                    tabular.add_hline()
                    tabular.add_row([
                        bold('Config'), bold('Analytical'), bold('Numerical'), 
                        bold('Circular'), bold('Struct Lines'), bold('Net Length'), bold('Total Material')
                    ])
                    tabular.add_hline()

                    for i, result_tuple in enumerate(all_results):
                        if len(result_tuple) >= 6:
                            name, comparison, net_length, spiral, flat_circles, config_params = result_tuple[:6]
                        else:
                            continue

                        short_name = name.split('.')[1].strip() if '.' in name else name
                        analytical_total = comparison['analytical']['total']
                        numerical_total = comparison['numerical']['total']
                        circular_total = comparison['circular_approximation']['total']

                        config_params = configurations[i]['params']
                        struct_lines = config_params['height'] * config_params.get('struct_lines', 0)
                        total_material = analytical_total + struct_lines + net_length

                        tabular.add_row([
                            short_name,
                            f"{analytical_total:.2f}",
                            f"{numerical_total:.2f}",
                            f"{circular_total:.2f}",
                            f"{struct_lines:.2f}",
                            f"{net_length:.4f}",
                            f"{total_material:.2f}"
                        ])

                    tabular.add_hline()
                table.append(NoEscape(r'\end{center}'))

            # Success conclusion
            self.doc.append(NoEscape(r'\vspace{1cm}'))
            self.doc.append(NoEscape(r'\begin{storybox}[SUCCESS: Complete Design Validation Achieved!]'))
            success_text = """
            From mathematical perimeter through circular approximation to manufacturable nets,
            this demonstrates how complex 3D geometry can be transformed into
            practical manufacturing solutions while maintaining precision and integrity.

            \\textbf{The design is complete.}
            """
            self.doc.append(NoEscape(success_text.strip()))
            self.doc.append(NoEscape(r'\end{storybox}'))
    
    def _generate_and_include_3d_plot(self, spiral, short_name):
        """Generate 3D plot and include it in the document"""
        try:
            # Ensure matplotlib is using a non-interactive backend
            plt.switch_backend('Agg')
            
            plotter = SpiralPlotter(spiral)
            fig_3d, axes = plotter.plot_combined(show_cone=True)
            
            # Save plot with error handling
            plot_filename = os.path.join(self.output_dir,f'3d_plot_{short_name.replace(" ", "_").replace("/", "_")}.png')
            fig_3d.savefig(plot_filename, dpi=300, bbox_inches='tight')
            plt.close(fig_3d)
            
            # Verify file exists before including
            if os.path.exists(plot_filename):
                with self.doc.create(Figure(position='h!')) as fig:
                    fig.add_image(f'3d_plot_{short_name.replace(" ", "_").replace("/", "_")}.png', width=NoEscape(r'0.8\textwidth'))
                    fig.add_caption(f'3D Spiral Geometry - {short_name}. Observe the XZ projection (right) showing circular approximation.')
            else:
                self.doc.append(NoEscape(f"[3D Plot for {short_name}: Image file not created]"))
                
        except Exception as e:
            print(f"Error generating 3D plot for {short_name}: {str(e)}")
            self.doc.append(NoEscape(f"[3D Plot generation failed for {short_name}: {str(e)}]"))
    
    def _generate_and_include_net_plot(self, spiral, flat_circles, config_params, short_name, net_length):
        """Generate net plot and include it in the document"""
        try:
            # Ensure matplotlib is using a non-interactive backend
            plt.switch_backend('Agg')
            
            plotter = SpiralPlotter(spiral)
            fig_net = plotter.plot_all_annular_regions_net(
                flat_circles,
                config_params.get('target_spacing', 1.0),
                config_params.get('arc_span_deg', 180),
                config_params.get('arc_density', 50)
            )
            
            # Save plot with error handling
            plot_filename = os.path.join(self.output_dir,f'net_plot_{short_name.replace(" ", "_").replace("/", "_")}.png')
            fig_net.savefig(plot_filename, dpi=300, bbox_inches='tight')
            plt.close(fig_net)
            
            # Verify file exists before including
            if os.path.exists(plot_filename):
                with self.doc.create(Figure(position='h!')) as fig:
                    fig.add_image(f'net_plot_{short_name.replace(" ", "_").replace("/", "_")}.png', width=NoEscape(r'0.8\textwidth'))
                    fig.add_caption(f'Annular Net Pattern - {short_name}. Flat manufacturing pattern for 3D spiral assembly.')
            else:
                self.doc.append(NoEscape(f"[Net Plot for {short_name}: Image file not created]"))
                
        except Exception as e:
            print(f"Error generating net plot for {short_name}: {str(e)}")
            self.doc.append(NoEscape(f"[Net Plot generation failed for {short_name}: {str(e)}]"))
    
    def generate_story_report(self, configurations_file='config.yaml'):
        """Generate the complete  LaTeX report"""
        print("Generating LaTeX spiral analysis report...")
        
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
            try:
                spiral = DoubleConicalSpiral(**config['params'])
                comparison = spiral.compare_all_methods(num_points_numerical=1000, num_slices_circular=100)
                flat_circles = spiral.get_xy_circles_for_visualization()
                net_length = spiral.calculate_net_length_angles(flat_circles)
                
                all_results.append((config['name'], comparison, net_length, spiral, flat_circles, config['params']))
            except Exception as e:
                print(f"Error processing configuration {config['name']}: {str(e)}")
                continue
        
        if not all_results:
            print("No configurations were successfully processed!")
            return None
        
        # Generate report content
        self.create_title_page()
        self.create_chapter1_parameters(configurations)
        self.doc.append(NewPage())
        
        self.create_chapter2_perimeter(all_results, configurations)
        self.doc.append(NewPage())
        
        # Chapters 3 & 4 for each configuration
        for name, comparison, net_length, spiral, flat_circles, config_params in all_results:
            self.create_chapter3_visualization_story(name, spiral, flat_circles, config_params)
            self.doc.append(NewPage())
            self.create_chapter4_net_creation(name, spiral, flat_circles, config_params, net_length)
            self.doc.append(NewPage())
        
        self.create_chapter5_conclusion(all_results, configurations)
        
        # Generate PDF
        
        report_filename = f"spiral_design"
        
        try:
            self.doc.generate_pdf(os.path.join(self.output_dir, report_filename), clean_tex=False)
            print(f"Report generated successfully: {os.path.join(self.output_dir, report_filename)}.pdf")
            return f"{os.path.join(self.output_dir, report_filename)}.pdf"
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            # Save the .tex file for manual debugging
            try:
                tex_filename = os.path.join(self.output_dir, f"{report_filename}.tex")
                self.doc.generate_tex(tex_filename)
                print(f"LaTeX source saved as: {tex_filename}")
            except Exception as tex_e:
                print(f"Could not save LaTeX source: {str(tex_e)}")
            return None


def generate_story_report():
    """Main function to generate LaTeX report"""
    generator = StoryDrivenLatexReportGenerator()
    report_file = generator.generate_story_report()
    
    if report_file:
        print(f"\n{'='*70}")
        print(" LATEX REPORT GENERATION COMPLETE")
        print(f"{'='*70}")
        print(f"Report saved as: {report_file}")
        try:
            print(f"Report size: {os.path.getsize(report_file) / 1024 / 1024:.2f} MB")
        except:
            print("Report size: [File size unavailable]")
        print("\nThe File Includes:")
        print("📖 Chapter 1: Understanding the Spiral Geometry")
        print("🧮 Chapter 2: Calculating the True Perimeter") 
        print("🔍 Chapter 3: Discovering the Circular Approximation")
        print("🏭 Chapter 4: Creating the Annular Net")
        print("✅ Chapter 5: Validation and Final Results")
        print("\nNarrative Flow:")
        print("Mathematical Foundation → Perimeter Calculation → XZ Projection Analysis")
        print("→ Circular Approximation → Annular Net Design → Manufacturing Validation")
        print("\nNote: Requires LaTeX installation and pylatex package")
        print("Install with: pip install pylatex")
    else:
        print("\n" + "="*70)
        print("REPORT GENERATION FAILED")
        print("="*70)
        print("Check the error messages above for details.")
        print("Common issues:")
        print("- Missing dependencies (spiral_calculations, spiral_plots)")
        print("- LaTeX installation problems")
        print("- File permission issues")
        print("- Plot generation failures")


if __name__ == "__main__":
    generate_story_report()