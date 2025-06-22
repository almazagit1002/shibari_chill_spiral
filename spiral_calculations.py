import numpy as np
from scipy.integrate import quad
import math

class DoubleConicalSpiral:
    def __init__(self, outer_radius=15, inner_radius=5, height=20, num_turns=5, phase_offset=0,
                  target_spacing=0.3, arc_span_deg=30, arc_density=5,struct_lines=1 ):
        """
        Initialize double conical spiral parameters (like spiral stairs)
        
        Parameters:
        outer_radius: radius of outer spiral at the base
        inner_radius: radius of inner spiral at the base
        height: height of the cone
        num_turns: number of complete turns around the cone
        phase_offset: angular offset between spirals (0 = aligned, π = opposite)
        """
        self.R_outer = outer_radius
        self.R_inner = inner_radius
        self.h = height
        self.n = num_turns * 2 * np.pi / height  # angular frequency
        self.phase_offset = phase_offset
        self.target_spacing= target_spacing
        self.arc_span_deg=arc_span_deg
        self.arc_density = arc_density
        
    def radius_outer(self, z):
        """Outer spiral radius as a function of height"""
        return self.R_outer * (1 - z / self.h)
    
    def radius_inner(self, z):
        """Inner spiral radius as a function of height"""
        return self.R_inner * (1 - z / self.h)
    
    def theta(self, z, is_inner=False):
        """Angular position as a function of height"""
        base_theta = self.n * z
        if is_inner:
            return base_theta + self.phase_offset
        return base_theta
    
    def parametric_coords_outer(self, z_values):
        """Calculate x, y, z coordinates for outer spiral"""
        z = z_values
        r = self.radius_outer(z)
        theta = self.theta(z, is_inner=False)
        
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        return x, y, z
    
    def parametric_coords_inner(self, z_values):
        """Calculate x, y, z coordinates for inner spiral"""
        z = z_values
        r = self.radius_inner(z)
        theta = self.theta(z, is_inner=True)
        
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        return x, y, z
    
    def arc_length_integrand(self, z, is_inner=False):
        """Integrand for arc length calculation"""
        if is_inner:
            R0 = self.R_inner
        else:
            R0 = self.R_outer
            
        # dR/dz
        dR_dz = -R0 / self.h
        
        # dθ/dz
        dtheta_dz = self.n
        
        # R(z)
        R = R0 * (1 - z / self.h)
        
        # Arc length element: sqrt((dR/dz)² + (R*dθ/dz)² + 1)
        return np.sqrt(dR_dz**2 + (R * dtheta_dz)**2 + 1)
    
    def calculate_perimeter_analytical(self):
        """Calculate perimeter for both spirals using numerical integration"""
        outer_perimeter, outer_error = quad(lambda z: self.arc_length_integrand(z, False), 0, self.h)
        inner_perimeter, inner_error = quad(lambda z: self.arc_length_integrand(z, True), 0, self.h)
        
        total_perimeter = outer_perimeter + inner_perimeter
        total_error = np.sqrt(outer_error**2 + inner_error**2)
        
        return {
            'outer': outer_perimeter,
            'inner': inner_perimeter,
            'total': total_perimeter,
            'error': total_error
        }
    
    def calculate_perimeter_numerical(self, num_points=1000):
        """Calculate perimeter using discrete approximation"""
        z_values = np.linspace(0, self.h, num_points)
        
        # Outer spiral
        x_outer, y_outer, z_outer = self.parametric_coords_outer(z_values)
        dx_outer = np.diff(x_outer)
        dy_outer = np.diff(y_outer)
        dz_outer = np.diff(z_outer)
        distances_outer = np.sqrt(dx_outer**2 + dy_outer**2 + dz_outer**2)
        perimeter_outer = np.sum(distances_outer)
        
        # Inner spiral
        x_inner, y_inner, z_inner = self.parametric_coords_inner(z_values)
        dx_inner = np.diff(x_inner)
        dy_inner = np.diff(y_inner)
        dz_inner = np.diff(z_inner)
        distances_inner = np.sqrt(dx_inner**2 + dy_inner**2 + dz_inner**2)
        perimeter_inner = np.sum(distances_inner)
        
        return {
            'outer': perimeter_outer,
            'inner': perimeter_inner,
            'total': perimeter_outer + perimeter_inner
        }
    
    def calculate_perimeter_xy_plane_circles(self):
        """
        Approximate perimeter by treating each spiral as a series of flat circles in the XY plane.
        Ignores vertical height changes.
        
        Total perimeter is just the sum of 2πr for each turn.
        """
        num_turns = int(round(self.n * self.h / (2 * np.pi)))  # full turns
        
        if num_turns == 0:
            num_turns = 1
        
        # Heights where circles would be centered (not actually used here)
        z_values = np.linspace(0, self.h, num_turns + 1)[:-1]
        z_values += self.h / (2 * num_turns)
        
        outer_length = 0
        inner_length = 0
        
        for z in z_values:
            r_outer = self.radius_outer(z)
            r_inner = self.radius_inner(z)
            outer_length += 2 * np.pi * r_outer
            inner_length += 2 * np.pi * r_inner

        return {
            'outer': outer_length,
            'inner': inner_length,
            'total': outer_length + inner_length,
            'turns': num_turns
        }

    
    def get_xy_circles_for_visualization(self, num_turns=None):
        """
        Returns radii of flat XY circles to approximate the spirals (ignores height).
        
        Each circle represents one full turn of the spiral.
        """
        if num_turns is None:
            num_turns = int(round(self.n * self.h / (2 * np.pi)))

        if num_turns == 0:
            num_turns = 1

        z_values = np.linspace(0, self.h, num_turns + 1)[:-1]
        z_values += self.h / (2 * num_turns)  # midpoint per slice

        circles = []
        for z in z_values:
            circles.append({
                'r_outer': self.radius_outer(z),
                'r_inner': self.radius_inner(z),
            })
        return circles
    

    def calculate_net_length_angles(self, circles):
        """
        Connect each outer point to multiple inner points within a small angular arc (not through center).
        Point density is adapted to arc length for more uniform spacing.
        """

        total_length = 0.0
        arc_span_rad = np.deg2rad(self.arc_span_deg)

        for circle in circles:
            R = circle['r_outer']
            r = circle['r_inner']
            avg_radius = 0.5 * (R + r)
            avg_circumference = 2 * np.pi * avg_radius

            # Dynamically compute number of points for roughly uniform spacing
            num_points = max(4, int(avg_circumference / self.target_spacing))
            angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)

            angle_offsets = np.linspace(-arc_span_rad/2, arc_span_rad/2, self.arc_density)

            for angle in angles:
                x_outer = R * math.cos(angle)
                y_outer = R * math.sin(angle)

                for offset in angle_offsets:
                    theta_inner = angle + offset
                    x_inner = r * math.cos(theta_inner)
                    y_inner = r * math.sin(theta_inner)

                    dx = x_outer - x_inner
                    dy = y_outer - y_inner
                    total_length += math.sqrt(dx*dx + dy*dy)

        return total_length


   

    def compare_all_methods(self, num_points_numerical=1000, num_slices_circular=100):
        """
        Compare all three perimeter calculation methods
        
        Returns a comprehensive comparison of analytical, numerical, and circular approximation methods
        """
        # Calculate using all methods
        analytical = self.calculate_perimeter_analytical()
        numerical = self.calculate_perimeter_numerical(num_points_numerical)
        circular = self.calculate_perimeter_xy_plane_circles()


        
        # Calculate differences
        analytical_vs_numerical = abs(analytical['total'] - numerical['total'])
        analytical_vs_circular = abs(analytical['total'] - circular['total'])
        numerical_vs_circular = abs(numerical['total'] - circular['total'])
        
        return {
            'analytical': analytical,
            'numerical': numerical,
            'circular_approximation': circular,
            'differences': {
                'analytical_vs_numerical': analytical_vs_numerical,
                'analytical_vs_circular': analytical_vs_circular,
                'numerical_vs_circular': numerical_vs_circular
            },
            'parameters': {
                'numerical_points': num_points_numerical,
                'circular_slices': num_slices_circular
            }
        }