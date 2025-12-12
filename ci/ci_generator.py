import math


class CIGenerator:
    def __init__(self, stroke_width=2.2, diameter=12.0, padding=5.0):
        self.stroke_w = stroke_width
        self.diameter = diameter
        self.r = diameter / 2.0
        self.padding = padding
        
        self.left_quad = [(67, 12), (82, 12), (39, 118), (24, 118)]
        self.right_quad = [(67, 12), (82, 12), (129, 118), (112, 118)]
        self.mid_trap = [(50, 82), (98, 82), (101, 88), (50, 88)]
        
        self._calculate_coordinates()
    
    def _poly_path(self, points):
        return "M " + " ".join(f"{x},{y}" for x, y in points) + " Z"
    
    def _calculate_coordinates(self):
        x1_slant, y1_slant = 63.0, 82.0
        x2_slant, y2_slant = 66.75908020522317, 72.73343019177543
        x1_h, y1_h = x2_slant, y2_slant
        x2_h, y2_h = x1_h + 10, y1_h
        self.cx_left, self.cy_left = x2_h + self.r, y2_h
        
        vx, vy = 45.0, 106.0
        norm = math.hypot(vx, vy)
        ux, uy = vx / norm, vy / norm
        
        length_new = 10.0
        dx_new, dy_new = ux * length_new, uy * length_new
        
        x1_green, y1_green = 70.0, 88.0
        x2_green, y2_green = x1_green + dx_new, y1_green + dy_new
        
        shift = 17.0
        x1_purple, y1_purple = x1_green + shift, y1_green
        x2_purple, y2_purple = x2_green + shift, y2_green
        
        s_old = self.r
        s_new = s_old - 3.0 / uy
        
        self.cx_green, self.cy_green = x2_green + ux * s_new, y2_green + uy * s_new
        self.cx_purple, self.cy_purple = x2_purple + ux * s_new, y2_purple + uy * s_new
        
        self.x1_slant, self.y1_slant = x1_slant, y1_slant
        self.x2_slant, self.y2_slant = x2_slant, y2_slant
        self.x1_h, self.y1_h = x1_h, y1_h
        self.x2_h, self.y2_h = x2_h, y2_h
        self.x1_green, self.y1_green = x1_green, y1_green
        self.x2_green, self.y2_green = x2_green, y2_green
        self.x1_purple, self.y1_purple = x1_purple, y1_purple
        self.x2_purple, self.y2_purple = x2_purple, y2_purple
    
    def _get_all_points(self):
        points = []
        points.extend(self.left_quad)
        points.extend(self.right_quad)
        points.extend(self.mid_trap)
        points.extend([
            (self.x1_slant, self.y1_slant),
            (self.x2_slant, self.y2_slant),
            (self.x1_h, self.y1_h),
            (self.x2_h, self.y2_h)
        ])
        points.extend([
            (self.x1_green, self.y1_green),
            (self.x2_green, self.y2_green),
            (self.x1_purple, self.y1_purple),
            (self.x2_purple, self.y2_purple)
        ])
        points.extend([
            (self.cx_left, self.cy_left),
            (self.cx_green, self.cy_green),
            (self.cx_purple, self.cy_purple)
        ])
        return points
    
    def _calculate_bounds(self):
        all_points = self._get_all_points()
        min_x = min(p[0] for p in all_points) - self.r
        min_y = min(p[1] for p in all_points) - self.r
        max_x = max(p[0] for p in all_points) + self.r
        max_y = max(p[1] for p in all_points) + self.r
        
        min_x -= self.padding
        min_y -= self.padding
        max_x += self.padding
        max_y += self.padding
        
        svg_w = max_x - min_x
        svg_h = max_y - min_y
        svg_size = max(svg_w, svg_h)
        
        return min_x, min_y, svg_w, svg_h, svg_size
    
    def generate_svg_content(self):
        min_x, min_y, svg_w, svg_h, svg_size = self._calculate_bounds()
        
        left_path = self._poly_path(self.left_quad)
        right_path = self._poly_path(self.right_quad)
        trap_path = self._poly_path(self.mid_trap)
        
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{svg_size:.1f}" height="{svg_size:.1f}" viewBox="{min_x:.1f} {min_y:.1f} {svg_w:.1f} {svg_h:.1f}">
  <path d="{left_path}" fill="black"/>
  <path d="{right_path}" fill="black"/>
  <path d="{trap_path}" fill="black"/>
  <line x1="{self.x1_slant:.3f}" y1="{self.y1_slant:.3f}" x2="{self.x2_slant:.3f}" y2="{self.y2_slant:.3f}" stroke="black" stroke-width="{self.stroke_w}" stroke-linecap="round"/>
  <line x1="{self.x1_h:.3f}" y1="{self.y1_h:.3f}" x2="{self.x2_h:.3f}" y2="{self.y2_h:.3f}" stroke="black" stroke-width="{self.stroke_w}" stroke-linecap="round"/>
  <circle cx="{self.cx_left:.3f}" cy="{self.cy_left:.3f}" r="{self.r:.3f}" fill="black"/>
  <line x1="{self.x1_green:.3f}" y1="{self.y1_green:.3f}" x2="{self.x2_green:.3f}" y2="{self.y2_green:.3f}" stroke="black" stroke-width="{self.stroke_w}" stroke-linecap="round"/>
  <line x1="{self.x1_purple:.3f}" y1="{self.y1_purple:.3f}" x2="{self.x2_purple:.3f}" y2="{self.y2_purple:.3f}" stroke="black" stroke-width="{self.stroke_w}" stroke-linecap="round"/>
  <circle cx="{self.cx_green:.3f}" cy="{self.cy_green:.3f}" r="{self.r:.3f}" fill="black"/>
  <circle cx="{self.cx_purple:.3f}" cy="{self.cy_purple:.3f}" r="{self.r:.3f}" fill="black"/>
</svg>'''
    
    def save(self, output_path="ci.svg"):
        svg_content = self.generate_svg_content()
        with open(output_path, "w") as f:
            f.write(svg_content)


if __name__ == "__main__":
    generator = CIGenerator()
    generator.save("ci.svg")

