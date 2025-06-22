import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from spiral_calculations import DoubleConicalSpiral

class SpiralPlotter:
    def __init__(self, spiral: DoubleConicalSpiral):
        """Initialize plotter with a DoubleConicalSpiral instance"""
        self.spiral = spiral
    
    def plot_xz_plane(self, num_points=1000):
        """Create XZ plane plot showing side view of the spiral"""
        # Generate spiral points
        z_values = np.linspace(0, self.spiral.h, num_points)
        
        # Outer spiral
        x_outer, y_outer, z_outer = self.spiral.parametric_coords_outer(z_values)
        
        # Inner spiral
        x_inner, y_inner, z_inner = self.spiral.parametric_coords_inner(z_values)
        
        # Create the plot
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        
        # Plot the spirals in XZ plane
        ax.plot(x_outer, z_outer, 'b-', linewidth=2, label='Outer Spiral', alpha=0.8)
        ax.plot(x_inner, z_inner, 'r-', linewidth=2, label='Inner Spiral', alpha=0.8)
        
        # Add cone boundary lines for reference
        z_boundary = np.linspace(0, self.spiral.h, 100)
        r_outer_boundary = self.spiral.radius_outer(z_boundary)
        r_inner_boundary = self.spiral.radius_inner(z_boundary)
        
        # Plot cone boundaries (positive and negative x)
        ax.plot(r_outer_boundary, z_boundary, 'b--', alpha=0.3, linewidth=1, label='Outer Cone Boundary')
        ax.plot(-r_outer_boundary, z_boundary, 'b--', alpha=0.3, linewidth=1)
        ax.plot(r_inner_boundary, z_boundary, 'r--', alpha=0.3, linewidth=1, label='Inner Cone Boundary')
        ax.plot(-r_inner_boundary, z_boundary, 'r--', alpha=0.3, linewidth=1)
        
        # Add some sample points for clarity
        sample_indices = np.linspace(0, len(z_values)-1, 20, dtype=int)
        ax.scatter(x_outer[sample_indices], z_outer[sample_indices], 
                  c='blue', s=30, alpha=0.8, zorder=5)
        ax.scatter(x_inner[sample_indices], z_inner[sample_indices], 
                  c='red', s=30, alpha=0.8, zorder=5)
        
        # Formatting
        ax.set_xlabel('X Position', fontsize=12)
        ax.set_ylabel('Z (Height)', fontsize=12)
        ax.set_title(f'XZ Plane View - Double Conical Spiral\n'
                    f'Outer R: {self.spiral.R_outer}, Inner R: {self.spiral.R_inner}, Height: {self.spiral.h}, '
                    f'Turns: {self.spiral.n*self.spiral.h/(2*np.pi):.1f}, Phase: {self.spiral.phase_offset*180/np.pi:.0f}°', 
                    fontsize=14)
        
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
        
        # Set axis limits
        ax.set_xlim([-self.spiral.R_outer*1.1, self.spiral.R_outer*1.1])
        ax.set_ylim([0, self.spiral.h*1.05])
        
        plt.tight_layout()
        return fig, ax
    
    def plot_3d(self, num_points=1000, show_cone=True):
        """Create 3D plot of the double conical spiral structure"""
        # Generate spiral points
        z_values = np.linspace(0, self.spiral.h, num_points)
        
        # Outer spiral
        x_outer, y_outer, z_outer = self.spiral.parametric_coords_outer(z_values)
        
        # Inner spiral
        x_inner, y_inner, z_inner = self.spiral.parametric_coords_inner(z_values)
        
        # Create 3D plot
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot the spirals
        ax.plot(x_outer, y_outer, z_outer, 'b-', linewidth=3, label='Outer Spiral')
        ax.plot(x_inner, y_inner, z_inner, 'r-', linewidth=3, label='Inner Spiral')
        
        # Optionally show the cone surfaces
        if show_cone:
            # Create outer cone surface
            theta_cone = np.linspace(0, 2*np.pi, 50)
            z_cone = np.linspace(0, self.spiral.h, 50)
            Z_cone, Theta_cone = np.meshgrid(z_cone, theta_cone)
            
            # Outer cone
            R_outer_cone = self.spiral.R_outer * (1 - Z_cone / self.spiral.h)
            X_outer_cone = R_outer_cone * np.cos(Theta_cone)
            Y_outer_cone = R_outer_cone * np.sin(Theta_cone)
            ax.plot_surface(X_outer_cone, Y_outer_cone, Z_cone, alpha=0.1, color='blue')
            
            # Inner cone
            R_inner_cone = self.spiral.R_inner * (1 - Z_cone / self.spiral.h)
            X_inner_cone = R_inner_cone * np.cos(Theta_cone)
            Y_inner_cone = R_inner_cone * np.sin(Theta_cone)
            ax.plot_surface(X_inner_cone, Y_inner_cone, Z_cone, alpha=0.1, color='red')
        
        # Add some sample points for clarity
        sample_indices = np.linspace(0, len(z_values)-1, 15, dtype=int)
        ax.scatter(x_outer[sample_indices], y_outer[sample_indices], z_outer[sample_indices], 
                  c='blue', s=40, alpha=0.8, label='Outer Points')
        ax.scatter(x_inner[sample_indices], y_inner[sample_indices], z_inner[sample_indices], 
                  c='red', s=40, alpha=0.8, label='Inner Points')
        
        # Formatting
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z (Height)')
        
        phase_deg = self.spiral.phase_offset * 180 / np.pi
        ax.set_title(f'Double Conical Spiral\n'
                    f'Outer R: {self.spiral.R_outer}, Inner R: {self.spiral.R_inner}, Height: {self.spiral.h}\n'
                    f'Turns: {self.spiral.n*self.spiral.h/(2*np.pi):.1f}, Phase Offset: {phase_deg:.0f}°')
        
        ax.legend()
        
        # Make axes equal
        max_range = max(self.spiral.R_outer, self.spiral.h)
        ax.set_xlim([-max_range, max_range])
        ax.set_ylim([-max_range, max_range])
        ax.set_zlim([0, self.spiral.h])
        
        plt.tight_layout()
        return fig, ax
    
    def plot_combined(self, num_points=1000, show_cone=True):
        """Create combined plot with 3D, XZ, XY spiral views and flat XY circle approximation."""

        # Create 2x2 grid
        fig = plt.figure(figsize=(25, 20))  # Adjusted size for better 2x2 layout

        # 3D plot - Top Left
        ax1 = fig.add_subplot(221, projection='3d')

        # Generate spiral points
        z_values = np.linspace(0, self.spiral.h, num_points)
        x_outer, y_outer, z_outer = self.spiral.parametric_coords_outer(z_values)
        x_inner, y_inner, z_inner = self.spiral.parametric_coords_inner(z_values)

        ax1.plot(x_outer, y_outer, z_outer, 'b-', linewidth=3, label='Outer Spiral')
        ax1.plot(x_inner, y_inner, z_inner, 'r-', linewidth=3, label='Inner Spiral')

        if show_cone:
            theta_cone = np.linspace(0, 2*np.pi, 50)
            z_cone = np.linspace(0, self.spiral.h, 50)
            Z_cone, Theta_cone = np.meshgrid(z_cone, theta_cone)

            # Outer cone
            R_outer_cone = self.spiral.R_outer * (1 - Z_cone / self.spiral.h)
            X_outer_cone = R_outer_cone * np.cos(Theta_cone)
            Y_outer_cone = R_outer_cone * np.sin(Theta_cone)
            ax1.plot_surface(X_outer_cone, Y_outer_cone, Z_cone, alpha=0.1, color='blue')

            # Inner cone
            R_inner_cone = self.spiral.R_inner * (1 - Z_cone / self.spiral.h)
            X_inner_cone = R_inner_cone * np.cos(Theta_cone)
            Y_inner_cone = R_inner_cone * np.sin(Theta_cone)
            ax1.plot_surface(X_inner_cone, Y_inner_cone, Z_cone, alpha=0.1, color='red')

        sample_indices = np.linspace(0, len(z_values)-1, 15, dtype=int)
        ax1.scatter(x_outer[sample_indices], y_outer[sample_indices], z_outer[sample_indices],
                    c='blue', s=40, alpha=0.8)
        ax1.scatter(x_inner[sample_indices], y_inner[sample_indices], z_inner[sample_indices],
                    c='red', s=40, alpha=0.8)

        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z (Height)')
        ax1.set_title('3D View')
        ax1.legend()

        max_range = max(self.spiral.R_outer, self.spiral.h)
        ax1.set_xlim([-max_range, max_range])
        ax1.set_ylim([-max_range, max_range])
        ax1.set_zlim([0, self.spiral.h])

        # XY plane spiral - top right
        ax2 = fig.add_subplot(222)
        ax2.plot(x_outer, y_outer, 'b-', linewidth=2, label='Outer Spiral', alpha=0.8)
        ax2.plot(x_inner, y_inner, 'r-', linewidth=2, label='Inner Spiral', alpha=0.8)

        sample_indices_xy = np.linspace(0, len(z_values)-1, 20, dtype=int)
        ax2.scatter(x_outer[sample_indices_xy], y_outer[sample_indices_xy],
                    c='blue', s=30, alpha=0.8)
        ax2.scatter(x_inner[sample_indices_xy], y_inner[sample_indices_xy],
                    c='red', s=30, alpha=0.8)

        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.set_title('XY Plane View (Top View)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_aspect('equal')
        ax2.set_xlim([-self.spiral.R_outer*1.1, self.spiral.R_outer*1.1])
        ax2.set_ylim([-self.spiral.R_outer*1.1, self.spiral.R_outer*1.1])

        # XZ plane spiral - bottom left Right
        ax3 = fig.add_subplot(223)
        ax3.plot(x_outer, z_outer, 'b-', linewidth=2, label='Outer Spiral', alpha=0.8)
        ax3.plot(x_inner, z_inner, 'r-', linewidth=2, label='Inner Spiral', alpha=0.8)

        z_boundary = np.linspace(0, self.spiral.h, 100)
        r_outer_boundary = self.spiral.radius_outer(z_boundary)
        r_inner_boundary = self.spiral.radius_inner(z_boundary)
        ax3.plot(r_outer_boundary, z_boundary, 'b--', alpha=0.3, linewidth=1, label='Outer Cone')
        ax3.plot(-r_outer_boundary, z_boundary, 'b--', alpha=0.3, linewidth=1)
        ax3.plot(r_inner_boundary, z_boundary, 'r--', alpha=0.3, linewidth=1, label='Inner Cone')
        ax3.plot(-r_inner_boundary, z_boundary, 'r--', alpha=0.3, linewidth=1)

        sample_indices_xz = np.linspace(0, len(z_values)-1, 20, dtype=int)
        ax3.scatter(x_outer[sample_indices_xz], z_outer[sample_indices_xz],
                    c='blue', s=30, alpha=0.8, zorder=5)
        ax3.scatter(x_inner[sample_indices_xz], z_inner[sample_indices_xz],
                    c='red', s=30, alpha=0.8, zorder=5)

        ax3.set_xlabel('X')
        ax3.set_ylabel('Z (Height)')
        ax3.set_title('XZ Plane View (Side View)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.set_aspect('equal')
        ax3.set_xlim([-self.spiral.R_outer*1.1, self.spiral.R_outer*1.1])
        ax3.set_ylim([0, self.spiral.h*1.05])

        
        # Flat XY Circles - Bottom Right
        ax4 = fig.add_subplot(224)
        circles = self.spiral.get_xy_circles_for_visualization()
        for c in circles:
            outer = plt.Circle((0, 0), c['r_outer'], fill=False, color='blue', linestyle='--')
            inner = plt.Circle((0, 0), c['r_inner'], fill=False, color='red', linestyle=':')
            ax4.add_patch(outer)
            ax4.add_patch(inner)

        ax4.set_aspect('equal')
        ax4.set_title("XY Circle Approximation")
        ax4.set_xlabel("X")
        ax4.set_ylabel("Y")
        max_radius = self.spiral.R_outer
        ax4.set_xlim(-max_radius - 1, max_radius + 1)
        ax4.set_ylim(-max_radius - 1, max_radius + 1)
        ax4.grid(True, alpha=0.3)

        # Overall Title
        phase_deg = self.spiral.phase_offset * 180 / np.pi
        fig.suptitle(f'Double Conical Spiral - Outer R: {self.spiral.R_outer}, Inner R: {self.spiral.R_inner}, '
                    f'Height: {self.spiral.h}, Turns: {self.spiral.n*self.spiral.h/(2*np.pi):.1f}, Phase: {phase_deg:.0f}°',
                    fontsize=16)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.subplots_adjust(hspace=0.4)
        return fig, (ax1, ax2, ax3, ax4)

    
    def plot_flat_xy_circles(self):


        print("\n" + "="*100)
        circles = self.spiral.get_xy_circles_for_visualization()
        print(circles)
        print("\n" + "="*100)

        fig, ax = plt.subplots()

        for c in circles:
            outer = plt.Circle((0, 0), c['r_outer'], fill=False, color='blue', linestyle='--')
            inner = plt.Circle((0, 0), c['r_inner'], fill=False, color='red', linestyle=':')
            ax.add_patch(outer)
            ax.add_patch(inner)

        # Get the max radius to set appropriate limits
        max_radius = max(c['r_outer'] for c in circles)
        ax.set_xlim(-max_radius - 1, max_radius + 1)
        ax.set_ylim(-max_radius - 1, max_radius + 1)

        ax.set_aspect('equal')
        ax.set_title("Flat XY Circle Approximation")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        plt.grid(True)

        return fig
    def plot_all_annular_regions_net(self, circles, target_spacing=0.35, arc_span_deg=30, arc_density=5):
        """
        Plot each annular region and draw net lines using adaptive point density based on arc length.
        """
        arc_span_rad = np.deg2rad(arc_span_deg)
        angle_offsets = np.linspace(-arc_span_rad/2, arc_span_rad/2, arc_density)

        y_offset = 0
        gap = 0.2  # space between rings in y-direction

        fig, ax = plt.subplots(figsize=(10, len(circles) * 0.7))

        for idx, circle in enumerate(circles):
            R = circle['r_outer']
            r = circle['r_inner']
            avg_radius = 0.5 * (R + r)
            avg_circumference = 2 * np.pi * avg_radius

            # Compute number of points dynamically
            num_points = max(4, int(avg_circumference / target_spacing))
            angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)

            # Outer and inner boundaries
            outer_x = R * np.cos(angles)
            outer_y = R * np.sin(angles) + y_offset
            inner_x = r * np.cos(angles)
            inner_y = r * np.sin(angles) + y_offset

            # Draw boundaries
            ax.plot(outer_x, outer_y, 'r-', linewidth=1)
            ax.plot(inner_x, inner_y, 'b-', linewidth=1)

            # Net connections (arc pattern from outer to inner circle)
            for angle in angles:
                x_outer = R * np.cos(angle)
                y_outer = R * np.sin(angle) + y_offset

                for offset in angle_offsets:
                    theta_inner = angle + offset
                    x_inner = r * np.cos(theta_inner)
                    y_inner = r * np.sin(theta_inner) + y_offset

                    ax.plot([x_outer, x_inner], [y_outer, y_inner], 'g-', linewidth=0.4)

            y_offset += R + gap

        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(f"Annular Regions with {arc_span_deg}° Arc Net Pattern", fontsize=14)

        return fig

