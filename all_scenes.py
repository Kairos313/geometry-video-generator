#!/usr/bin/env python3

import sys
import os
from manim import *
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from functions import *

def create_complete_diagram_a():
    import math
    
    coord_Y = np.array([0.000, 0.000, 0.000])
    coord_X = np.array([5.000, 0.000, 0.000])
    coord_W = np.array([1.861, 5.114, 0.000])
    
    dots = VGroup(
        Dot(coord_W, radius=0.08, color=WHITE),
        Dot(coord_X, radius=0.08, color=WHITE),
        Dot(coord_Y, radius=0.08, color=WHITE)
    )
    
    lines = VGroup(
        Line(coord_W, coord_X, color=WHITE, stroke_width=2),
        Line(coord_X, coord_Y, color=WHITE, stroke_width=2),
        Line(coord_W, coord_Y, color=WHITE, stroke_width=2)
    )
    
    labels = VGroup(
        MathTex("W", font_size=72, color=WHITE).move_to(coord_W + np.array([-0.3, 0.3, 0])),
        MathTex("X", font_size=72, color=WHITE).move_to(coord_X + np.array([0.3, -0.3, 0])),
        MathTex("Y", font_size=72, color=WHITE).move_to(coord_Y + np.array([-0.3, -0.3, 0]))
    )
    
    measurement_labels = VGroup(
        MathTex("6\\text{ cm}", font_size=48, color=YELLOW).move_to((coord_W + coord_X) / 2 + np.array([0, 0.4, 0])),
        MathTex("5\\text{ cm}", font_size=48, color=YELLOW).move_to((coord_X + coord_Y) / 2 + np.array([0, -0.4, 0])),
        MathTex("70^{\\circ}", font_size=48, color=YELLOW).move_to(coord_Y + np.array([0.8, 0.8, 0])),
        MathTex("51.5^{\\circ}", font_size=48, color=GREEN).move_to(coord_W + np.array([-0.8, -0.8, 0]))
    )
    
    angle_WYX = create_2d_angle_arc_geometric(
        center=coord_Y, point1=coord_W, point2=coord_X,
        radius=0.5, num_points=30, use_smaller_angle=True,
        show_connections=False, color=YELLOW
    )
    
    angle_XWY = create_2d_angle_arc_geometric(
        center=coord_W, point1=coord_X, point2=coord_Y,
        radius=0.5, num_points=30, use_smaller_angle=True,
        show_connections=False, color=GREEN
    )
    
    triangle_WXY = Polygon(coord_W, coord_X, coord_Y, 
                          fill_opacity=0.2, fill_color=BLUE, 
                          stroke_width=2, stroke_color=BLUE)
    
    complete_figure = VGroup(
        triangle_WXY, dots, lines, labels, measurement_labels,
        angle_WYX, angle_XWY
    )
    
    complete_figure.set_opacity(0)
    
    return {
        "complete_figure": complete_figure,
        "elements": {
            "region_triangle_WXY_interior": triangle_WXY,
            "point_W": dots[0],
            "point_X": dots[1],
            "point_Y": dots[2],
            "line_WX": lines[0],
            "line_XY": lines[1],
            "line_WY": lines[2],
            "label_W": labels[0],
            "label_X": labels[1],
            "label_Y": labels[2],
            "line_WX_measurement_label": measurement_labels[0],
            "line_XY_measurement_label": measurement_labels[1],
            "angle_WYX_measurement_label": measurement_labels[2],
            "angle_XWY_measurement_label": measurement_labels[3],
            "angle_WYX": angle_WYX,
            "angle_XWY": angle_XWY
        }
    }

def create_complete_diagram_b():
    import math
    
    coord_Y = np.array([0.000, 0.000, 0.000])
    coord_X = np.array([5.000, 0.000, 0.000])
    coord_W = np.array([1.861, 5.114, 0.000])
    coord_Z = np.array([2.500, 1.986, 1.843])
    coord_M = np.array([2.500, 1.986, 0.000])
    coord_N = np.array([2.500, 0.000, 0.000])
    
    dots = VGroup(
        Dot3D(coord_W, radius=0.08, color=WHITE),
        Dot3D(coord_X, radius=0.08, color=WHITE),
        Dot3D(coord_Y, radius=0.08, color=WHITE),
        Dot3D(coord_Z, radius=0.08, color=YELLOW),
        Dot3D(coord_M, radius=0.08, color=RED),
        Dot3D(coord_N, radius=0.08, color=GREEN)
    )
    
    lines = VGroup(
        Line3D(coord_W, coord_X, color=WHITE, thickness=0.02),
        Line3D(coord_X, coord_Y, color=WHITE, thickness=0.02),
        Line3D(coord_W, coord_Y, color=WHITE, thickness=0.02),
        Line3D(coord_W, coord_Z, color=WHITE, thickness=0.02),
        Line3D(coord_X, coord_Z, color=WHITE, thickness=0.02),
        Line3D(coord_Y, coord_Z, color=WHITE, thickness=0.02),
        Line3D(coord_Z, coord_M, color=RED, thickness=0.02),
        Line3D(coord_W, coord_M, color=RED, thickness=0.02),
        Line3D(coord_Z, coord_N, color=GREEN, thickness=0.02),
        Line3D(coord_M, coord_N, color=GREEN, thickness=0.02)
    )
    
    labels = VGroup(
        MathTex("W", font_size=72, color=WHITE).move_to(coord_W + np.array([-0.3, 0.3, 0])),
        MathTex("X", font_size=72, color=WHITE).move_to(coord_X + np.array([0.3, -0.3, 0])),
        MathTex("Y", font_size=72, color=WHITE).move_to(coord_Y + np.array([-0.3, -0.3, 0])),
        MathTex("Z", font_size=72, color=YELLOW).move_to(coord_Z + np.array([0, 0, 0.3])),
        MathTex("M", font_size=72, color=RED).move_to(coord_M + np.array([0.3, 0.3, 0])),
        MathTex("N", font_size=72, color=GREEN).move_to(coord_N + np.array([0, -0.3, 0]))
    )
    
    measurement_labels = VGroup(
        MathTex("6\\text{ cm}", font_size=48, color=YELLOW).move_to((coord_W + coord_X) / 2 + np.array([0, 0.4, 0])),
        MathTex("5\\text{ cm}", font_size=48, color=YELLOW).move_to((coord_X + coord_Y) / 2 + np.array([0, -0.4, 0])),
        MathTex("70^{\\circ}", font_size=48, color=YELLOW).move_to(coord_Y + np.array([0.8, 0.8, 0])),
        MathTex("51.5^{\\circ}", font_size=48, color=GREEN).move_to(coord_W + np.array([-0.8, -0.8, 0])),
        MathTex("30^{\\circ}", font_size=48, color=ORANGE).move_to(coord_W + np.array([0.5, -0.5, 0.5])),
        MathTex("3.19\\text{ cm}", font_size=48, color=RED).move_to((coord_W + coord_M) / 2 + np.array([0.3, 0, 0])),
        MathTex("1.84\\text{ cm}", font_size=48, color=RED).move_to((coord_Z + coord_M) / 2 + np.array([0.3, 0, 0])),
        MathTex("1.99\\text{ cm}", font_size=48, color=GREEN).move_to((coord_M + coord_N) / 2 + np.array([0.3, 0, 0])),
        MathTex("42.8^{\\circ}", font_size=48, color=BLUE).move_to(coord_N + np.array([0.5, 0.5, 0.5]))
    )
    
    angle_ZWM = create_3d_angle_arc_with_connections(
        center=coord_W, point1=coord_Z, point2=coord_M,
        radius=0.5, show_connections=False, color=ORANGE
    )
    
    angle_ZNM = create_3d_angle_arc_with_connections(
        center=coord_N, point1=coord_Z, point2=coord_M,
        radius=0.5, show_connections=False, color=BLUE
    )
    
    triangle_WXY = Polygon(coord_W, coord_X, coord_Y, 
                          fill_opacity=0.2, fill_color=BLUE, 
                          stroke_width=2, stroke_color=BLUE)
    triangle_XYZ = Polygon(coord_X, coord_Y, coord_Z, 
                          fill_opacity=0.2, fill_color=GREEN, 
                          stroke_width=2, stroke_color=GREEN)
    triangle_ZMW = Polygon(coord_Z, coord_M, coord_W, 
                          fill_opacity=0.2, fill_color=ORANGE, 
                          stroke_width=2, stroke_color=ORANGE)
    triangle_MNY = Polygon(coord_M, coord_N, coord_Y, 
                          fill_opacity=0.2, fill_color=RED, 
                          stroke_width=2, stroke_color=RED)
    triangle_ZMN = Polygon(coord_Z, coord_M, coord_N, 
                          fill_opacity=0.2, fill_color=PURPLE, 
                          stroke_width=2, stroke_color=PURPLE)
    
    complete_figure = VGroup(
        dots, lines, labels, measurement_labels,
        angle_ZWM, angle_ZNM, triangle_WXY, triangle_XYZ,
        triangle_ZMW, triangle_MNY, triangle_ZMN
    )
    
    complete_figure.set_opacity(0)
    
    return {
        "complete_figure": complete_figure,
        "elements": {
            "point_W": dots[0],
            "point_X": dots[1],
            "point_Y": dots[2],
            "point_Z": dots[3],
            "point_M": dots[4],
            "point_N": dots[5],
            "line_WX": lines[0],
            "line_XY": lines[1],
            "line_WY": lines[2],
            "line_WZ": lines[3],
            "line_XZ": lines[4],
            "line_YZ": lines[5],
            "line_ZM": lines[6],
            "line_WM": lines[7],
            "line_ZN": lines[8],
            "line_MN": lines[9],
            "label_W": labels[0],
            "label_X": labels[1],
            "label_Y": labels[2],
            "label_Z": labels[3],
            "label_M": labels[4],
            "label_N": labels[5],
            "line_WX_measurement_label": measurement_labels[0],
            "line_XY_measurement_label": measurement_labels[1],
            "angle_WYX_measurement_label": measurement_labels[2],
            "angle_XWY_measurement_label": measurement_labels[3],
            "angle_ZWM_measurement_label": measurement_labels[4],
            "line_WM_measurement_label": measurement_labels[5],
            "line_ZM_measurement_label": measurement_labels[6],
            "line_MN_measurement_label": measurement_labels[7],
            "angle_ZNM_measurement_label": measurement_labels[8],
            "angle_ZWM": angle_ZWM,
            "angle_ZNM": angle_ZNM,
            "region_triangle_WXY_interior": triangle_WXY,
            "region_triangle_XYZ_interior": triangle_XYZ,
            "region_triangle_ZMW_interior": triangle_ZMW,
            "region_triangle_MNY_interior": triangle_MNY,
            "region_triangle_ZMN_interior": triangle_ZMN
        }
    }

class PartAFindAngleXWYScene(Scene):
    def construct(self):
        self.camera.background_color = "#0C0C0C"
        
        complete_diagram = create_complete_diagram_a()
        complete_figure = complete_diagram["complete_figure"]
        elements = complete_diagram["elements"]
        
        auto_scale_to_left_screen(complete_figure, is_3d=False)
        self.add(complete_figure)
        
        try:
            self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Full_Pipeline/Scene/part_a_find_angle_XWY_scene.mp3")
        except Exception as e:
            print(f"Warning: Could not add audio file: {e}")
        
        add_explanation_text(self, MathTex(r"\text{Part (a): Find } \angle XWY"))
        
        elements["point_W"].set_opacity(1.0)
        elements["point_X"].set_opacity(1.0)
        elements["point_Y"].set_opacity(1.0)
        elements["label_W"].set_opacity(1.0)
        elements["label_X"].set_opacity(1.0)
        elements["label_Y"].set_opacity(1.0)
        elements["line_WX"].set_opacity(1.0)
        elements["line_XY"].set_opacity(1.0)
        elements["line_WY"].set_opacity(1.0)
        elements["region_triangle_WXY_interior"].set_opacity(0.2)
        
        self.play(Create(elements["point_W"]), Create(elements["point_X"]), Create(elements["point_Y"]),
                 Create(elements["label_W"]), Create(elements["label_X"]), Create(elements["label_Y"]),
                 Create(elements["line_WX"]), Create(elements["line_XY"]), Create(elements["line_WY"]),
                 Create(elements["region_triangle_WXY_interior"]))
        
        num_indicates = int(8.62 / 2.5)
        total_indicate_time = num_indicates * 0.5
        remaining_wait_time = 8.62 - 1.5 - total_indicate_time
        
        self.play(Indicate(elements["point_W"], color=YELLOW), 
                 Indicate(elements["point_X"], color=YELLOW),
                 Indicate(elements["point_Y"], color=YELLOW))
        self.wait(2.0)
        self.play(Indicate(elements["point_W"], color=YELLOW), 
                 Indicate(elements["point_X"], color=YELLOW),
                 Indicate(elements["point_Y"], color=YELLOW))
        self.wait(2.0)
        self.play(Indicate(elements["point_W"], color=YELLOW), 
                 Indicate(elements["point_X"], color=YELLOW),
                 Indicate(elements["point_Y"], color=YELLOW))
        self.wait(remaining_wait_time - 4.0)
        
        add_explanation_text(self, MathTex(r"WX = 6\text{ cm}"))
        add_explanation_text(self, MathTex(r"XY = 5\text{ cm}"))
        add_explanation_text(self, MathTex(r"\angle WYX = 70^\circ"))
        
        elements["line_WX_measurement_label"].set_opacity(1.0)
        elements["line_XY_measurement_label"].set_opacity(1.0)
        elements["angle_WYX"].set_opacity(1.0)
        elements["angle_WYX_measurement_label"].set_opacity(1.0)
        
        self.play(Create(elements["line_WX_measurement_label"]), Create(elements["line_XY_measurement_label"]),
                 Create(elements["angle_WYX"]), Create(elements["angle_WYX_measurement_label"]))
        
        num_indicates = int(9.93 / 2.5)
        total_indicate_time = num_indicates * 0.5
        remaining_wait_time = 9.93 - 2.5 - total_indicate_time
        
        self.play(Indicate(elements["line_WX"], color=YELLOW), 
                 Indicate(elements["line_XY"], color=YELLOW),
                 Indicate(elements["angle_WYX"], color=YELLOW))
        self.wait(2.0)
        self.play(Indicate(elements["line_WX"], color=YELLOW), 
                 Indicate(elements["line_XY"], color=YELLOW),
                 Indicate(elements["angle_WYX"], color=YELLOW))
        self.wait(2.0)
        self.play(Indicate(elements["line_WX"], color=YELLOW), 
                 Indicate(elements["line_XY"], color=YELLOW),
                 Indicate(elements["angle_WYX"], color=YELLOW))
        self.wait(remaining_wait_time - 4.0)
        
        add_explanation_text(self, MathTex(r"\text{Use the Law of Sines: } \frac{a}{\sin A} = \frac{b}{\sin B}"))
        
        num_indicates = int(7.0 / 2.5)
        total_indicate_time = num_indicates * 0.5
        remaining_wait_time = 7.0 - 0.5 - total_indicate_time
        
        self.play(Indicate(elements["region_triangle_WXY_interior"], color=YELLOW))
        self.wait(2.0)
        self.play(Indicate(elements["region_triangle_WXY_interior"], color=YELLOW))
        self.wait(remaining_wait_time - 2.0)
        
        add_explanation_text(self, MathTex(r"\frac{\sin(\angle XWY)}{XY} = \frac{\sin(\angle WYX)}{WX}"))
        
        elements["angle_XWY"].set_opacity(1.0)
        self.play(Create(elements["angle_XWY"]))
        
        num_indicates = int(9.61 / 2.5)
        total_indicate_time = num_indicates * 0.5
        remaining_wait_time = 9.61 - 1.5 - total_indicate_time
        
        self.play(Indicate(elements["angle_XWY"], color=YELLOW), 
                 Indicate(elements["line_XY"], color=YELLOW),
                 Indicate(elements["angle_WYX"], color=YELLOW),
                 Indicate(elements["line_WX"], color=YELLOW))
        self.wait(2.0)
        self.play(Indicate(elements["angle_XWY"], color=YELLOW), 
                 Indicate(elements["line_XY"], color=YELLOW),
                 Indicate(elements["angle_WYX"], color=YELLOW),
                 Indicate(elements["line_WX"], color=YELLOW))
        self.wait(2.0)
        self.play(Indicate(elements["angle_XWY"], color=YELLOW), 
                 Indicate(elements["line_XY"], color=YELLOW),
                 Indicate(elements["angle_WYX"], color=YELLOW),
                 Indicate(elements["line_WX"], color=YELLOW))
        self.wait(remaining_wait_time - 4.0)
        
        add_explanation_text(self, MathTex(r"\frac{\sin(\angle XWY)}{5} = \frac{\sin(70^\circ)}{6}"))
        self.wait(6.77)
        
        add_explanation_text(self, MathTex(r"\angle XWY = \arcsin\left(\frac{5 \times \sin(70^\circ)}{6}\right)"))
        self.wait(5.51)
        
        add_explanation_text(self, MathTex(r"\angle XWY \approx 51.5^\circ"))
        
        elements["angle_XWY_measurement_label"].set_opacity(1.0)
        self.play(Create(elements["angle_XWY_measurement_label"]))
        
        self.play(Indicate(elements["angle_XWY"], color=GREEN))
        self.wait(3.44)
        
        self.play(FadeOut(complete_figure), run_time=2.0)

class PartBPyramidSetupScene(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#0C0C0C"
        
        complete_diagram = create_complete_diagram_b()
        complete_figure = complete_diagram["complete_figure"]
        elements = complete_diagram["elements"]
        
        auto_scale_to_left_screen(complete_figure, is_3d=True)
        self.add(complete_figure)
        
        try:
            self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Full_Pipeline/Scene/part_b_pyramid_setup_scene.mp3")
        except Exception as e:
            print(f"Warning: Could not add audio file: {e}")
        
        elements["point_W"].set_opacity(1.0)
        elements["point_X"].set_opacity(1.0)
        elements["point_Y"].set_opacity(1.0)
        elements["label_W"].set_opacity(1.0)
        elements["label_X"].set_opacity(1.0)
        elements["label_Y"].set_opacity(1.0)
        elements["line_WX"].set_opacity(1.0)
        elements["line_XY"].set_opacity(1.0)
        elements["line_WY"].set_opacity(1.0)
        elements["region_triangle_WXY_interior"].set_opacity(0.2)
        elements["line_WX_measurement_label"].set_opacity(1.0)
        elements["line_XY_measurement_label"].set_opacity(1.0)
        elements["angle_WYX_measurement_label"].set_opacity(1.0)
        elements["angle_XWY_measurement_label"].set_opacity(1.0)
        
        add_explanation_text(self, MathTex(r"\text{Part (b): Pyramid } WXYZ"))
        
        elements["point_Z"].set_opacity(1.0)
        elements["label_Z"].set_opacity(1.0)
        elements["line_WZ"].set_opacity(1.0)
        elements["line_XZ"].set_opacity(1.0)
        elements["line_YZ"].set_opacity(1.0)
        
        self.play(Create(elements["point_Z"]), Create(elements["label_Z"]),
                 Create(elements["line_WZ"]), Create(elements["line_XZ"]), Create(elements["line_YZ"]))
        
        self.play(Indicate(elements["point_Z"], color=YELLOW))
        self.wait(4.7)
        
        add_explanation_text(self, MathTex(r"WZ = XZ = YZ \implies M = \text{circumcenter of } \triangle WXY"))
        
        elements["point_M"].set_opacity(1.0)
        elements["label_M"].set_opacity(1.0)
        elements["line_ZM"].set_opacity(1.0)
        
        self.play(Indicate(elements["line_WZ"], color=YELLOW))
        self.play(Indicate(elements["line_XZ"], color=YELLOW))
        self.play(Indicate(elements["line_YZ"], color=YELLOW))
        self.play(Create(elements["point_M"]), Create(elements["label_M"]), Create(elements["line_ZM"]))
        
        num_indicates = int(12.3 / 2.5)
        for i in range(num_indicates - 1):
            self.wait(2.0)
            self.play(Indicate(elements["line_WZ"], color=YELLOW),
                     Indicate(elements["line_XZ"], color=YELLOW),
                     Indicate(elements["line_YZ"], color=YELLOW))
        self.wait(1.3)
        
        add_explanation_text(self, MathTex(r"\angle ZWM = 30^\circ"))
        
        elements["line_WM"].set_opacity(1.0)
        elements["angle_ZWM"].set_opacity(1.0)
        elements["angle_ZWM_measurement_label"].set_opacity(1.0)
        
        self.play(Create(elements["line_WM"]), Create(elements["angle_ZWM"]), 
                 Create(elements["angle_ZWM_measurement_label"]))
        
        num_indicates = int(15.12 / 2.5)
        for i in range(num_indicates):
            self.play(Indicate(elements["angle_ZWM"], color=ORANGE))
            if i < num_indicates - 1:
                self.wait(2.0)
        self.wait(0.12)
        
        add_explanation_text(self, MathTex(r"\text{Find circumradius } R = WM"))
        
        self.play(Indicate(elements["region_triangle_WXY_interior"], color=BLUE))
        
        num_indicates = int(10.4 / 2.5)
        for i in range(num_indicates - 1):
            self.wait(2.0)
            self.play(Indicate(elements["region_triangle_WXY_interior"], color=BLUE))
        self.wait(0.4)
        
        add_explanation_text(self, MathTex(r"\frac{WX}{\sin(\angle WYX)} = 2R"))
        self.wait(7.29)
        
        add_explanation_text(self, MathTex(r"R = \frac{6}{2 \sin(70^\circ)} \approx 3.19\text{ cm}"))
        
        elements["line_WM_measurement_label"].set_opacity(1.0)
        self.play(Indicate(elements["line_WM"], color=RED), Create(elements["line_WM_measurement_label"]))
        
        num_indicates = int(9.46 / 2.5)
        for i in range(num_indicates - 1):
            self.wait(2.0)
            self.play(Indicate(elements["line_WM"], color=RED))
        self.wait(1.46)
        
        add_explanation_text(self, MathTex(r"\text{In } \triangle ZMW, \tan(30^\circ) = \frac{ZM}{WM}"))
        
        elements["region_triangle_ZMW_interior"].set_opacity(0.2)
        self.play(Indicate(elements["region_triangle_ZMW_interior"], color=ORANGE))
        
        num_indicates = int(8.86 / 2.5)
        for i in range(num_indicates - 1):
            self.wait(2.0)
            self.play(Indicate(elements["region_triangle_ZMW_interior"], color=ORANGE))
        self.wait(1.86)
        
        add_explanation_text(self, MathTex(r"ZM = WM \times \tan(30^\circ) \approx 3.19 \times 0.577 \approx 1.84\text{ cm}"))
        
        elements["line_ZM_measurement_label"].set_opacity(1.0)
        self.play(Indicate(elements["line_ZM"], color=RED), Create(elements["line_ZM_measurement_label"]))
        
        self.play(Indicate(elements["line_ZM"], color=RED))
        self.wait(4.9)
        
        clear_explanation_text(self)
        self.play(Rotate(complete_figure, angle=2*PI, axis=UP), run_time=3)
        self.play(FadeOut(complete_figure), run_time=2.0)

class PartBFindDihedralAngleScene(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#0C0C0C"
        
        complete_diagram = create_complete_diagram_b()
        complete_figure = complete_diagram["complete_figure"]
        elements = complete_diagram["elements"]
        
        auto_scale_to_left_screen(complete_figure, is_3d=True)
        self.add(complete_figure)
        
        try:
            self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Full_Pipeline/Scene/part_b_find_dihedral_angle_scene.mp3")
        except Exception as e:
            print(f"Warning: Could not add audio file: {e}")
        
        elements["point_W"].set_opacity(1.0)
        elements["point_X"].set_opacity(1.0)
        elements["point_Y"].set_opacity(1.0)
        elements["point_Z"].set_opacity(1.0)
        elements["point_M"].set_opacity(1.0)
        elements["label_W"].set_opacity(1.0)
        elements["label_X"].set_opacity(1.0)
        elements["label_Y"].set_opacity(1.0)
        elements["label_Z"].set_opacity(1.0)
        elements["label_M"].set_opacity(1.0)
        elements["line_WX"].set_opacity(1.0)
        elements["line_XY"].set_opacity(1.0)
        elements["line_WY"].set_opacity(1.0)
        elements["line_WZ"].set_opacity(1.0)
        elements["line_XZ"].set_opacity(1.0)
        elements["line_YZ"].set_opacity(1.0)
        elements["line_ZM"].set_opacity(1.0)
        elements["line_WM"].set_opacity(1.0)
        elements["region_triangle_WXY_interior"].set_opacity(0.2)
        elements["line_WX_measurement_label"].set_opacity(1.0)
        elements["line_XY_measurement_label"].set_opacity(1.0)
        elements["angle_WYX_measurement_label"].set_opacity(1.0)
        elements["angle_XWY_measurement_label"].set_opacity(1.0)
        elements["angle_ZWM_measurement_label"].set_opacity(1.0)
        elements["line_WM_measurement_label"].set_opacity(1.0)
        elements["line_ZM_measurement_label"].set_opacity(1.0)
        
        add_explanation_text(self, MathTex(r"\text{Find angle between plane } WXY \text{ and plane } XYZ"))
        
        elements["region_triangle_XYZ_interior"].set_opacity(0.2)
        self.play(Indicate(elements["region_triangle_WXY_interior"], color=BLUE))
        self.play(Indicate(elements["region_triangle_XYZ_interior"], color=GREEN))
        
        num_indicates = int(7.84 / 2.5)
        for i in range(num_indicates - 1):
            self.wait(2.0)
            self.play(Indicate(elements["region_triangle_WXY_interior"], color=BLUE),
                     Indicate(elements["region_triangle_XYZ_interior"], color=GREEN))
        self.wait(0.84)
        
        add_explanation_text(self, MathTex(r"\text{Angle is the dihedral angle along edge } XY"))
        
        self.play(Indicate(elements["line_XY"], color=YELLOW))
        
        num_indicates = int(11.05 / 2.5)
        for i in range(num_indicates - 1):
            self.wait(2.0)
            self.play(Indicate(elements["line_XY"], color=YELLOW))
        self.wait(1.05)
        
        add_explanation_text(self, MathTex(r"N = \text{midpoint of } XY"))
        add_explanation_text(self, MathTex(r"ZN \perp XY"))
        add_explanation_text(self, MathTex(r"MN \perp XY"))
        
        elements["point_N"].set_opacity(1.0)
        elements["label_N"].set_opacity(1.0)
        elements["line_ZN"].set_opacity(1.0)
        elements["line_MN"].set_opacity(1.0)
        
        self.play(Create(elements["point_N"]), Create(elements["label_N"]),
                 Create(elements["line_ZN"]), Create(elements["line_MN"]))
        
        num_indicates = int(14.99 / 2.5)
        for i in range(num_indicates):
            self.play(Indicate(elements["point_N"], color=GREEN),
                     Indicate(elements["line_ZN"], color=GREEN),
                     Indicate(elements["line_MN"], color=GREEN))
            if i < num_indicates - 1:
                self.wait(2.0)
        self.wait(0.49)
        
        add_explanation_text(self, MathTex(r"\text{Find } \angle ZNM \text{ in right } \triangle ZMN"))
        
        elements["region_triangle_ZMN_interior"].set_opacity(0.2)
        elements["angle_ZNM"].set_opacity(1.0)
        
        self.play(Indicate(elements["region_triangle_ZMN_interior"], color=PURPLE),
                 Indicate(elements["angle_ZNM"], color=BLUE))
        
        self.play(Indicate(elements["region_triangle_ZMN_interior"], color=PURPLE))
        self.wait(2.88)
        
        add_explanation_text(self, MathTex(r"\text{In right } \triangle MNY, MY = R, NY = \frac{5}{2} = 2.5"))
        
        elements["region_triangle_MNY_interior"].set_opacity(0.2)
        self.play(Indicate(elements["region_triangle_MNY_interior"], color=RED))
        
        num_indicates = int(13.38 / 2.5)
        for i in range(num_indicates - 1):
            self.wait(2.0)
            self.play(Indicate(elements["region_triangle_MNY_interior"], color=RED))
        self.wait(1.38)
        
        add_explanation_text(self, MathTex(r"MN = \sqrt{MY^2 - NY^2} = \sqrt{3.19^2 - 2.5^2} \approx 1.99\text{ cm}"))
        
        elements["line_MN_measurement_label"].set_opacity(1.0)
        self.play(Indicate(elements["line_MN"], color=GREEN), Create(elements["line_MN_measurement_label"]))
        
        num_indicates = int(8.26 / 2.5)
        for i in range(num_indicates - 1):
            self.wait(2.0)
            self.play(Indicate(elements["line_MN"], color=GREEN))
        self.wait(0.76)
        
        add_explanation_text(self, MathTex(r"\tan(\angle ZNM) = \frac{ZM}{MN} = \frac{1.84}{1.99}"))
        
        self.play(Indicate(elements["region_triangle_ZMN_interior"], color=PURPLE))
        
        self.play(Indicate(elements["region_triangle_ZMN_interior"], color=PURPLE))
        self.wait(4.21)
        
        add_explanation_text(self, MathTex(r"\angle ZNM = \arctan\left(\frac{1.84}{1.99}\right) \approx 42.8^\circ"))
        
        elements["angle_ZNM_measurement_label"].set_opacity(1.0)
        self.play(Indicate(elements["angle_ZNM"], color=BLUE), Create(elements["angle_ZNM_measurement_label"]))
        
        self.play(Indicate(elements["angle_ZNM"], color=BLUE))
        self.wait(2.75)
        
        add_explanation_text(self, MathTex(r"42.8^\circ < 45^\circ \implies \text{No, it does not exceed } 45^\circ."))
        self.wait(7.13)
        
        clear_explanation_text(self)
        self.play(Rotate(complete_figure, angle=2*PI, axis=UP), run_time=3)
        self.play(FadeOut(complete_figure), run_time=2.0)

class KeyTakeawaysScene(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#0C0C0C"
        
        complete_diagram = create_complete_diagram_b()
        complete_figure = complete_diagram["complete_figure"]
        elements = complete_diagram["elements"]
        
        auto_scale_to_left_screen(complete_figure, is_3d=True)
        self.add(complete_figure)
        
        try:
            self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Full_Pipeline/Scene/key_takeaways_scene.mp3")
        except Exception as e:
            print(f"Warning: Could not add audio file: {e}")
        
        elements["point_W"].set_opacity(1.0)
        elements["point_X"].set_opacity(1.0)
        elements["point_Y"].set_opacity(1.0)
        elements["point_Z"].set_opacity(1.0)
        elements["point_M"].set_opacity(1.0)
        elements["point_N"].set_opacity(1.0)
        elements["label_W"].set_opacity(1.0)
        elements["label_X"].set_opacity(1.0)
        elements["label_Y"].set_opacity(1.0)
        elements["label_Z"].set_opacity(1.0)
        elements["label_M"].set_opacity(1.0)
        elements["label_N"].set_opacity(1.0)
        elements["line_WX"].set_opacity(1.0)
        elements["line_XY"].set_opacity(1.0)
        elements["line_WY"].set_opacity(1.0)
        elements["line_WZ"].set_opacity(1.0)
        elements["line_XZ"].set_opacity(1.0)
        elements["line_YZ"].set_opacity(1.0)
        elements["line_ZM"].set_opacity(1.0)
        elements["line_WM"].set_opacity(1.0)
        elements["line_ZN"].set_opacity(1.0)
        elements["line_MN"].set_opacity(1.0)
        elements["region_triangle_WXY_interior"].set_opacity(0.2)
        elements["line_WX_measurement_label"].set_opacity(1.0)
        elements["line_XY_measurement_label"].set_opacity(1.0)
        elements["angle_WYX_measurement_label"].set_opacity(1.0)
        elements["angle_XWY_measurement_label"].set_opacity(1.0)
        elements["angle_ZWM_measurement_label"].set_opacity(1.0)
        elements["line_WM_measurement_label"].set_opacity(1.0)
        elements["line_ZM_measurement_label"].set_opacity(1.0)
        elements["line_MN_measurement_label"].set_opacity(1.0)
        elements["angle_ZNM_measurement_label"].set_opacity(1.0)
        
        add_explanation_text(self, MathTex(r"\text{Key Method 1: Law of Sines for SSA case}"))
        
        self.play(Indicate(elements["region_triangle_WXY_interior"], color=BLUE))
        
        num_indicates = int(8.49 / 2.5)
        for i in range(num_indicates - 1):
            self.wait(2.0)
            self.play(Indicate(elements["region_triangle_WXY_interior"], color=BLUE))
        self.wait(0.99)
        
        add_explanation_text(self, MathTex(r"\text{Key Insight: Equal slant edges } \implies \text{Apex above circumcenter}"))
        
        self.play(Indicate(elements["point_Z"], color=YELLOW),
                 Indicate(elements["point_M"], color=RED),
                 Indicate(elements["line_ZM"], color=RED))
        
        num_indicates = int(7.47 / 2.5)
        for i in range(num_indicates - 1):
            self.wait(2.0)
            self.play(Indicate(elements["point_Z"], color=YELLOW),
                     Indicate(elements["point_M"], color=RED),
                     Indicate(elements["line_ZM"], color=RED))
        self.wait(0.47)
        
        add_explanation_text(self, MathTex(r"\text{Key Strategy: Deconstruct 3D problem into 2D right triangles}"))
        
        elements["region_triangle_ZMW_interior"].set_opacity(0.2)
        elements["region_triangle_MNY_interior"].set_opacity(0.2)
        elements["region_triangle_ZMN_interior"].set_opacity(0.2)
        
        self.play(Indicate(elements["region_triangle_ZMW_interior"], color=ORANGE),
                 Indicate(elements["region_triangle_MNY_interior"], color=RED),
                 Indicate(elements["region_triangle_ZMN_interior"], color=PURPLE))
        
        num_indicates = int(9.51 / 2.5)
        for i in range(num_indicates - 1):
            self.wait(2.0)
            self.play(Indicate(elements["region_triangle_ZMW_interior"], color=ORANGE),
                     Indicate(elements["region_triangle_MNY_interior"], color=RED),
                     Indicate(elements["region_triangle_ZMN_interior"], color=PURPLE))
        self.wait(0.01)
        
        clear_explanation_text(self)
        self.play(Rotate(complete_figure, angle=2*PI, axis=UP), run_time=3)
        self.play(FadeOut(complete_figure), run_time=2.0)