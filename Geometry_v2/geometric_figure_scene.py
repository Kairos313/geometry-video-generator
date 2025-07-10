import json
from manim import *
from geometric_figure_output import create_base_diagram_main, create_base_diagram_triangles
import os

# Load the solution steps JSON
with open("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/math_solution_2.json", "r", encoding="utf-8") as f:
    solution = json.load(f)

# Load the solution steps JSON for the new scene
with open("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/math_solution.json", "r", encoding="utf-8") as f:
    solution_steps = json.load(f)

class GeometricFigureSceneA(Scene):
    def construct(self):
        diagram_a = create_base_diagram_pentagon(solution["solution"])
        self.add(diagram_a)
        self.wait(3)

class GeometricFigureSceneB(Scene):
    def construct(self):
        diagram_b = create_base_diagram_triangles(solution["solution"])
        self.add(diagram_b)
        self.wait(3)

class GeometricFigureSceneC(Scene):
    def construct(self):
        # Pass the solution_steps dict to the diagram function
        diagram = create_base_diagram_pentagon(solution_steps)
        self.add(diagram)
        self.wait(3)

class GeometricFigureSceneMain(Scene):
    def construct(self):
        diagram = create_base_diagram_main(solution["solution"])
        self.add(diagram)
        self.wait(3) 