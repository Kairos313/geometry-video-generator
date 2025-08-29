#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from functions import *

def create_complete_diagram_main():
    import math
    
    coord_Q = np.array([0.000, 0.000, 0.000])
    coord_S = np.array([14.512, 0.000, 0.000])
    coord_P = np.array([8.772, 8.188, 0.000])
    coord_R = np.array([6.362, -11.337, 0.000])
    
    dots = VGroup(
        Dot(coord_P, radius=0.08, color="#FFFFFF"),
        Dot(coord_Q, radius=0.08, color="#FFFFFF"),
        Dot(coord_S, radius=0.08, color="#FFFFFF"),
        Dot(coord_R, radius=0.08, color="#FFFFFF")
    )
    
    lines = VGroup(
        Line(coord_P, coord_Q, color="#FFFFFF", stroke_width=2),
        Line(coord_P, coord_S, color="#FFFFFF", stroke_width=2),
        Line(coord_Q, coord_S, color="#FFFF00", stroke_width=3),
        Line(coord_Q, coord_R, color="#FFFFFF", stroke_width=2),
        Line(coord_R, coord_S, color="#FFFFFF", stroke_width=2)
    )
    
    labels = VGroup(
        MathTex("P", font_size=72, color="#FFFFFF").move_to(coord_P + np.array([-0.3, 0.3, 0])),
        MathTex("Q", font_size=72, color="#FFFFFF").move_to(coord_Q + np.array([-0.3, -0.3, 0])),
        MathTex("S", font_size=72, color="#FFFFFF").move_to(coord_S + np.array([0.3, -0.3, 0])),
        MathTex("R", font_size=72, color="#FFFFFF").move_to(coord_R + np.array([0.3, -0.3, 0]))
    )
    
    triangle_PQS = Polygon(coord_P, coord_Q, coord_S, 
                          fill_opacity=0.2, fill_color="#0000FF", 
                          stroke_width=2, stroke_color="#0000FF")
    triangle_QRS = Polygon(coord_Q, coord_R, coord_S, 
                          fill_opacity=0.2, fill_color="#00FF00", 
                          stroke_width=2, stroke_color="#00FF00")
    
    complete_figure = VGroup(
        dots, lines, labels, triangle_PQS, triangle_QRS
    )
    
    complete_figure.set_opacity(0)
    
    return {
        "complete_figure": complete_figure,
        "elements": {
            "point_P": dots[0],
            "point_Q": dots[1],
            "point_S": dots[2],
            "point_R": dots[3],
            "point_P_label": labels[0],
            "point_Q_label": labels[1],
            "point_S_label": labels[2],
            "point_R_label": labels[3],
            "line_PQ": lines[0],
            "line_PS": lines[1],
            "line_QS": lines[2],
            "line_QR": lines[3],
            "line_RS": lines[4],
            "region_triangle_PQS_interior": triangle_PQS,
            "region_triangle_QRS_interior": triangle_QRS
        }
    }

def create_complete_diagram_b():
    import math
    
    coord_Q = np.array([0.000, 0.000, 0.000])
    coord_S = np.array([14.512, 0.000, 0.000])
    coord_P = np.array([8.772, 8.188, 0.000])
    coord_R = np.array([6.362, -1.969, 11.165])
    coord_H_R = np.array([6.362, 0.000, 0.000])
    coord_R_proj = np.array([6.362, -1.969, 0.000])
    coord_H_P = np.array([8.772, 0.000, 0.000])
    coord_P_proj = np.array([8.772, 0.247, -1.400])
    
    dots = VGroup(
        Dot3D(coord_P, radius=0.08, color="#FFFFFF"),
        Dot3D(coord_Q, radius=0.08, color="#FFFFFF"),
        Dot3D(coord_S, radius=0.08, color="#FFFFFF"),
        Dot3D(coord_R, radius=0.08, color="#FFFF00"),
        Dot3D(coord_H_R, radius=0.06, color="#00FF00"),
        Dot3D(coord_H_P, radius=0.06, color="#0000FF")
    )
    
    lines = VGroup(
        Line3D(coord_P, coord_Q, color="#FFFFFF", thickness=0.02),
        Line3D(coord_P, coord_S, color="#FFFFFF", thickness=0.02),
        Line3D(coord_Q, coord_S, color="#FFFF00", thickness=0.03),
        Line3D(coord_Q, coord_R, color="#FFFFFF", thickness=0.02),
        Line3D(coord_R, coord_S, color="#FFFFFF", thickness=0.02)
    )
    
    construction_lines = VGroup(
        Line3D(coord_R, coord_H_R, color="#00FF00", thickness=0.02),
        Line3D(coord_R, coord_R_proj, color="#FF0000", thickness=0.03),
        Line3D(coord_P, coord_H_P, color="#0000FF", thickness=0.02),
        Line3D(coord_P, coord_P_proj, color="#FF00FF", thickness=0.03)
    )
    
    labels = VGroup(
        MathTex("P", font_size=72, color="#FFFFFF").move_to(coord_P + np.array([-0.5, 0.5, 0])),
        MathTex("Q", font_size=72, color="#FFFFFF").move_to(coord_Q + np.array([-0.5, -0.5, 0])),
        MathTex("S", font_size=72, color="#FFFFFF").move_to(coord_S + np.array([0.5, -0.5, 0])),
        MathTex("R", font_size=72, color="#FFFF00").move_to(coord_R + np.array([0.5, 0.5, 0.5]))
    )
    
    complete_figure = VGroup(
        dots, lines, construction_lines, labels
    )
    
    complete_figure.set_opacity(0)
    
    return {
        "complete_figure": complete_figure,
        "elements": {
            "point_P": dots[0],
            "point_Q": dots[1],
            "point_S": dots[2],
            "point_R": dots[3],
            "point_P_label": labels[0],
            "point_Q_label": labels[1],
            "point_S_label": labels[2],
            "point_R_label": labels[3],
            "line_PQ": lines[0],
            "line_PS": lines[1],
            "line_QS": lines[2],
            "line_QR": lines[3],
            "line_RS": lines[4],
            "construction_line_R_to_plane": construction_lines[1],
            "altitude_R_to_QS": construction_lines[0],
            "construction_line_P_to_plane": construction_lines[3],
            "altitude_P_to_QS": construction_lines[2]
        }
    }

class FindLengthQSUsingCosineRuleScene(Scene):
    def construct(self):
        self.camera.background_color = "#0C0C0C"
        
        complete_diagram = create_complete_diagram_main()
        complete_figure = complete_diagram["complete_figure"]
        elements = complete_diagram["elements"]
        
        auto_scale_to_left_screen(complete_figure, is_3d=False)
        self.add(complete_figure)
        
        try:
            self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Full_Pipeline/Scene/find_length_QS_using_cosine_rule_scene.mp3")
        except Exception as e:
            print(f"Warning: Could not add audio file: {e}")
        
        add_explanation_text(self, MathTex(r"\text{In } \triangle PQS:"))
        
        elements["point_P"].set_opacity(1.0)
        elements["point_Q"].set_opacity(1.0)
        elements["point_S"].set_opacity(1.0)
        elements["point_P_label"].set_opacity(1.0)
        elements["point_Q_label"].set_opacity(1.0)
        elements["point_S_label"].set_opacity(1.0)
        elements["line_PQ"].set_opacity(1.0)
        elements["line_PS"].set_opacity(1.0)
        elements["line_QS"].set_opacity(1.0)
        elements["region_triangle_PQS_interior"].set_opacity(0.2)
        
        self.play(Create(elements["point_P"]), Create(elements["point_Q"]), Create(elements["point_S"]),
                 Create(elements["point_P_label"]), Create(elements["point_Q_label"]), Create(elements["point_S_label"]),
                 Create(elements["line_PQ"]), Create(elements["line_PS"]), Create(elements["line_QS"]))
        
        num_indicates = int(6.71 / 2.5)
        total_indicate_time = num_indicates * 0.5
        total_animation_time = 0.5 + 1.0
        remaining_wait_time = 6.71 - total_animation_time - total_indicate_time
        
        self.play(Indicate(elements["region_triangle_PQS_interior"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["region_triangle_PQS_interior"], color="#FFFF00"))
        self.wait(max(0.1, remaining_wait_time - 2.0))
        
        add_explanation_text(self, MathTex(r"\text{Given: } PQ = 12 \text{ cm, } PS = 10 \text{ cm, } \angle QPS = 82^\circ"))
        add_explanation_text(self, MathTex(r"\text{Use Cosine Rule.}"))
        
        num_indicates = int(9.27 / 2.5)
        total_indicate_time = num_indicates * 0.5
        total_animation_time = 1.0
        remaining_wait_time = 9.27 - total_animation_time - total_indicate_time
        
        self.play(Indicate(elements["line_PQ"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["line_PS"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["point_P"], color="#FFFF00"))
        self.wait(max(0.1, remaining_wait_time - 4.0))
        
        add_explanation_text(self, MathTex(r"QS^2 = PQ^2 + PS^2 - 2(PQ)(PS)\cos(\angle QPS)"))
        
        num_indicates = int(11.65 / 2.5)
        total_indicate_time = num_indicates * 0.5
        total_animation_time = 0.5
        remaining_wait_time = 11.65 - total_animation_time - total_indicate_time
        
        self.wait(max(0.1, 0.5))
        self.wait(max(0.1, 2.0))
        self.wait(max(0.1, 2.0))
        self.wait(max(0.1, 2.0))
        self.wait(max(0.1, remaining_wait_time - 6.5))
        
        add_explanation_text(self, MathTex(r"QS^2 = 12^2 + 10^2 - 2(12)(10)\cos(82^\circ) \approx 210.598"))
        add_explanation_text(self, MathTex(r"\implies QS \approx 14.51 \text{ cm}"))
        
        num_indicates = int(9.98 / 2.5)
        total_indicate_time = num_indicates * 0.5
        total_animation_time = 1.0
        remaining_wait_time = 9.98 - total_animation_time - total_indicate_time
        
        self.play(Indicate(elements["line_QS"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["line_QS"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["line_QS"], color="#FFFF00"))
        self.wait(max(0.1, remaining_wait_time - 4.0))

class FindAngleRQSUsingSineRuleScene(Scene):
    def construct(self):
        self.camera.background_color = "#0C0C0C"
        
        complete_diagram = create_complete_diagram_main()
        complete_figure = complete_diagram["complete_figure"]
        elements = complete_diagram["elements"]
        
        auto_scale_to_left_screen(complete_figure, is_3d=False)
        self.add(complete_figure)
        
        try:
            self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Full_Pipeline/Scene/find_angle_RQS_using_sine_rule_scene.mp3")
        except Exception as e:
            print(f"Warning: Could not add audio file: {e}")
        
        elements["point_P"].set_opacity(1.0)
        elements["point_P_label"].set_opacity(1.0)
        elements["point_Q"].set_opacity(1.0)
        elements["point_Q_label"].set_opacity(1.0)
        elements["point_S"].set_opacity(1.0)
        elements["point_S_label"].set_opacity(1.0)
        elements["line_PQ"].set_opacity(1.0)
        elements["line_PS"].set_opacity(1.0)
        elements["line_QS"].set_opacity(1.0)
        
        add_explanation_text(self, MathTex(r"\text{In } \triangle QRS: QR = 13 \text{ cm, } QS \approx 14.51 \text{ cm, } \angle QRS = 65^\circ"))
        
        elements["point_R"].set_opacity(1.0)
        elements["point_R_label"].set_opacity(1.0)
        elements["line_QR"].set_opacity(1.0)
        elements["line_RS"].set_opacity(1.0)
        elements["region_triangle_QRS_interior"].set_opacity(0.2)
        
        self.play(Create(elements["point_R"]), Create(elements["point_R_label"]),
                 Create(elements["line_QR"]), Create(elements["line_RS"]))
        
        num_indicates = int(8.26 / 2.5)
        total_indicate_time = num_indicates * 0.5
        total_animation_time = 0.5 + 1.0
        remaining_wait_time = 8.26 - total_animation_time - total_indicate_time
        
        self.play(Indicate(elements["region_triangle_QRS_interior"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["line_QR"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["point_R"], color="#FFFF00"))
        self.wait(max(0.1, remaining_wait_time - 4.0))
        
        add_explanation_text(self, MathTex(r"\text{Use Sine Rule: } \frac{\sin(\angle RSQ)}{QR} = \frac{\sin(\angle QRS)}{QS}"))
        
        num_indicates = int(7.76 / 2.5)
        total_indicate_time = num_indicates * 0.5
        total_animation_time = 0.5
        remaining_wait_time = 7.76 - total_animation_time - total_indicate_time
        
        self.play(Indicate(elements["line_QR"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["point_S"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["point_R"], color="#FFFF00"))
        self.wait(max(0.1, remaining_wait_time - 4.0))
        
        add_explanation_text(self, MathTex(r"\sin(\angle RSQ) = \frac{13 \times \sin(65^\circ)}{14.51} \approx 0.8119"))
        add_explanation_text(self, MathTex(r"\implies \angle RSQ \approx 54.3^\circ"))
        
        num_indicates = int(10.53 / 2.5)
        total_indicate_time = num_indicates * 0.5
        total_animation_time = 1.0
        remaining_wait_time = 10.53 - total_animation_time - total_indicate_time
        
        self.play(Indicate(elements["point_S"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["point_S"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["point_S"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["point_S"], color="#FFFF00"))
        self.wait(max(0.1, remaining_wait_time - 6.0))
        
        add_explanation_text(self, MathTex(r"\angle RQS = 180^\circ - 65^\circ - 54.3^\circ \approx 60.7^\circ"))
        
        num_indicates = int(9.09 / 2.5)
        total_indicate_time = num_indicates * 0.5
        total_animation_time = 0.5
        remaining_wait_time = 9.09 - total_animation_time - total_indicate_time
        
        self.play(Indicate(elements["point_Q"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["point_Q"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["point_Q"], color="#FFFF00"))
        self.wait(max(0.1, remaining_wait_time - 4.0))

class FindShortestDistanceFromRToPlanePQSScene(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#0C0C0C"
        
        complete_diagram = create_complete_diagram_b()
        complete_figure = complete_diagram["complete_figure"]
        elements = complete_diagram["elements"]
        
        auto_scale_to_left_screen(complete_figure, is_3d=True)
        self.add(complete_figure)
        
        try:
            self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Full_Pipeline/Scene/find_shortest_distance_from_R_to_plane_PQS_scene.mp3")
        except Exception as e:
            print(f"Warning: Could not add audio file: {e}")
        
        elements["point_P"].set_opacity(1.0)
        elements["point_P_label"].set_opacity(1.0)
        elements["point_Q"].set_opacity(1.0)
        elements["point_Q_label"].set_opacity(1.0)
        elements["point_S"].set_opacity(1.0)
        elements["point_S_label"].set_opacity(1.0)
        elements["point_R"].set_opacity(1.0)
        elements["point_R_label"].set_opacity(1.0)
        elements["line_PQ"].set_opacity(1.0)
        elements["line_PS"].set_opacity(1.0)
        elements["line_QS"].set_opacity(1.0)
        elements["line_QR"].set_opacity(1.0)
        elements["line_RS"].set_opacity(1.0)
        
        self.play(Rotate(complete_figure, angle=2*PI, axis=UP), run_time=3)
        
        add_explanation_text(self, MathTex(r"\text{Find shortest distance from R to plane PQS.}"))
        
        elements["construction_line_R_to_plane"].set_opacity(1.0)
        self.play(Create(elements["construction_line_R_to_plane"]))
        
        num_indicates = int(7.24 / 2.5)
        total_indicate_time = num_indicates * 0.5
        total_animation_time = 0.5 + 1.0
        remaining_wait_time = 7.24 - total_animation_time - total_indicate_time
        
        self.play(Indicate(elements["construction_line_R_to_plane"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["point_R"], color="#FFFF00"))
        self.wait(max(0.1, remaining_wait_time - 2.0))
        
        add_explanation_text(self, MathTex(r"\text{Dihedral angle between planes} = 80^\circ"))
        
        num_indicates = int(6.45 / 2.5)
        total_indicate_time = num_indicates * 0.5
        total_animation_time = 0.5
        remaining_wait_time = 6.45 - total_animation_time - total_indicate_time
        
        self.play(Indicate(elements["line_QS"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["line_QS"], color="#FFFF00"))
        self.wait(max(0.1, remaining_wait_time - 2.0))
        
        add_explanation_text(self, MathTex(r"\text{Altitude } h_{R \to QS} = \frac{2 \times \text{Area}(\triangle QRS)}{QS}"))
        add_explanation_text(self, MathTex(r"= 13 \sin(60.7^\circ) \approx 11.35 \text{ cm}"))
        
        elements["altitude_R_to_QS"].set_opacity(1.0)
        self.play(Create(elements["altitude_R_to_QS"]))
        
        num_indicates = int(10.53 / 2.5)
        total_indicate_time = num_indicates * 0.5
        total_animation_time = 1.0 + 1.0
        remaining_wait_time = 10.53 - total_animation_time - total_indicate_time
        
        self.play(Indicate(elements["altitude_R_to_QS"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["altitude_R_to_QS"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["altitude_R_to_QS"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["altitude_R_to_QS"], color="#FFFF00"))
        self.wait(max(0.1, remaining_wait_time - 6.0))
        
        add_explanation_text(self, MathTex(r"\text{Distance} = h_{R \to QS} \times \sin(80^\circ)"))
        add_explanation_text(self, MathTex(r"\approx 11.35 \times 0.9848 \approx 11.2 \text{ cm}"))
        
        num_indicates = int(11.23 / 2.5)
        total_indicate_time = num_indicates * 0.5
        total_animation_time = 1.0
        remaining_wait_time = 11.23 - total_animation_time - total_indicate_time
        
        self.play(Indicate(elements["construction_line_R_to_plane"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["construction_line_R_to_plane"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["construction_line_R_to_plane"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["construction_line_R_to_plane"], color="#FFFF00"))
        self.wait(max(0.1, remaining_wait_time - 6.0))
        
        clear_explanation_text(self)
        self.play(Rotate(complete_figure, angle=2*PI, axis=UP), run_time=3)
        self.play(FadeOut(complete_figure), run_time=2.0)

class EvaluateClaimAboutDistancePXScene(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#0C0C0C"
        
        complete_diagram = create_complete_diagram_b()
        complete_figure = complete_diagram["complete_figure"]
        elements = complete_diagram["elements"]
        
        auto_scale_to_left_screen(complete_figure, is_3d=True)
        self.add(complete_figure)
        
        try:
            self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Full_Pipeline/Scene/evaluate_claim_about_distance_PX_scene.mp3")
        except Exception as e:
            print(f"Warning: Could not add audio file: {e}")
        
        elements["point_P"].set_opacity(1.0)
        elements["point_P_label"].set_opacity(1.0)
        elements["point_Q"].set_opacity(1.0)
        elements["point_Q_label"].set_opacity(1.0)
        elements["point_S"].set_opacity(1.0)
        elements["point_S_label"].set_opacity(1.0)
        elements["point_R"].set_opacity(1.0)
        elements["point_R_label"].set_opacity(1.0)
        elements["line_PQ"].set_opacity(1.0)
        elements["line_PS"].set_opacity(1.0)
        elements["line_QS"].set_opacity(1.0)
        elements["line_QR"].set_opacity(1.0)
        elements["line_RS"].set_opacity(1.0)
        
        self.play(Rotate(complete_figure, angle=2*PI, axis=UP), run_time=3)
        
        add_explanation_text(self, MathTex(r"\text{Is } PX > 8 \text{ cm for any point X on plane QRS?}"))
        
        num_indicates = int(9.93 / 2.5)
        total_indicate_time = num_indicates * 0.5
        total_animation_time = 0.5
        remaining_wait_time = 9.93 - total_animation_time - total_indicate_time
        
        self.play(Indicate(elements["point_P"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["point_P"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["point_P"], color="#FFFF00"))
        self.wait(max(0.1, remaining_wait_time - 4.0))
        
        add_explanation_text(self, MathTex(r"\text{Find shortest distance from P to plane QRS.}"))
        
        elements["construction_line_P_to_plane"].set_opacity(1.0)
        self.play(Create(elements["construction_line_P_to_plane"]))
        
        num_indicates = int(7.29 / 2.5)
        total_indicate_time = num_indicates * 0.5
        total_animation_time = 0.5 + 1.0
        remaining_wait_time = 7.29 - total_animation_time - total_indicate_time
        
        self.play(Indicate(elements["construction_line_P_to_plane"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["point_P"], color="#FFFF00"))
        self.wait(max(0.1, remaining_wait_time - 2.0))
        
        add_explanation_text(self, MathTex(r"\text{Altitude } h_{P \to QS} = \frac{PQ \times PS \times \sin(\angle QPS)}{QS}"))
        add_explanation_text(self, MathTex(r"= \frac{12 \times 10 \times \sin(82^\circ)}{14.51} \approx 8.19 \text{ cm}"))
        
        elements["altitude_P_to_QS"].set_opacity(1.0)
        self.play(Create(elements["altitude_P_to_QS"]))
        
        num_indicates = int(10.58 / 2.5)
        total_indicate_time = num_indicates * 0.5
        total_animation_time = 1.0 + 1.0
        remaining_wait_time = 10.58 - total_animation_time - total_indicate_time
        
        self.play(Indicate(elements["altitude_P_to_QS"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["altitude_P_to_QS"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["altitude_P_to_QS"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["altitude_P_to_QS"], color="#FFFF00"))
        self.wait(max(0.1, remaining_wait_time - 6.0))
        
        add_explanation_text(self, MathTex(r"\text{Shortest Distance} = h_{P \to QS} \times \sin(80^\circ)"))
        add_explanation_text(self, MathTex(r"\approx 8.19 \times 0.9848 \approx 8.06 \text{ cm}"))
        
        num_indicates = int(8.86 / 2.5)
        total_indicate_time = num_indicates * 0.5
        total_animation_time = 1.0
        remaining_wait_time = 8.86 - total_animation_time - total_indicate_time
        
        self.play(Indicate(elements["construction_line_P_to_plane"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["construction_line_P_to_plane"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["construction_line_P_to_plane"], color="#FFFF00"))
        self.wait(max(0.1, remaining_wait_time - 4.0))
        
        add_explanation_text(self, MathTex(r"8.06 \text{ cm} > 8 \text{ cm. The claim is correct.}"))
        
        num_indicates = int(13.38 / 2.5)
        total_indicate_time = num_indicates * 0.5
        total_animation_time = 0.5
        remaining_wait_time = 13.38 - total_animation_time - total_indicate_time
        
        self.play(Indicate(elements["construction_line_P_to_plane"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["construction_line_P_to_plane"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["construction_line_P_to_plane"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["construction_line_P_to_plane"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["construction_line_P_to_plane"], color="#FFFF00"))
        self.wait(max(0.1, remaining_wait_time - 8.0))
        
        clear_explanation_text(self)
        self.play(Rotate(complete_figure, angle=2*PI, axis=UP), run_time=3)
        self.play(FadeOut(complete_figure), run_time=2.0)

class KeyTakeawaysScene(Scene):
    def construct(self):
        self.camera.background_color = "#0C0C0C"
        
        complete_diagram = create_complete_diagram_main()
        complete_figure = complete_diagram["complete_figure"]
        elements = complete_diagram["elements"]
        
        auto_scale_to_left_screen(complete_figure, is_3d=False)
        self.add(complete_figure)
        
        try:
            self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Full_Pipeline/Scene/key_takeaways_scene.mp3")
        except Exception as e:
            print(f"Warning: Could not add audio file: {e}")
        
        elements["point_P"].set_opacity(1.0)
        elements["point_P_label"].set_opacity(1.0)
        elements["point_Q"].set_opacity(1.0)
        elements["point_Q_label"].set_opacity(1.0)
        elements["point_S"].set_opacity(1.0)
        elements["point_S_label"].set_opacity(1.0)
        elements["point_R"].set_opacity(1.0)
        elements["point_R_label"].set_opacity(1.0)
        elements["line_PQ"].set_opacity(1.0)
        elements["line_PS"].set_opacity(1.0)
        elements["line_QS"].set_opacity(1.0)
        elements["line_QR"].set_opacity(1.0)
        elements["line_RS"].set_opacity(1.0)
        
        add_explanation_text(self, MathTex(r"\text{Key Method 1: Cosine Rule for Side-Angle-Side (SAS)}"))
        
        elements["region_triangle_PQS_interior"].set_opacity(0.2)
        
        num_indicates = int(6.4 / 2.5)
        total_indicate_time = num_indicates * 0.5
        total_animation_time = 0.5
        remaining_wait_time = 6.4 - total_animation_time - total_indicate_time
        
        self.play(Indicate(elements["region_triangle_PQS_interior"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["region_triangle_PQS_interior"], color="#FFFF00"))
        self.wait(max(0.1, remaining_wait_time - 2.0))
        
        add_explanation_text(self, MathTex(r"\text{Key Method 2: Sine Rule for a known side-angle pair}"))
        
        elements["region_triangle_QRS_interior"].set_opacity(0.2)
        
        num_indicates = int(4.44 / 2.5)
        total_indicate_time = num_indicates * 0.5
        total_animation_time = 0.5
        remaining_wait_time = 4.44 - total_animation_time - total_indicate_time
        
        self.play(Indicate(elements["region_triangle_QRS_interior"], color="#FFFF00"))
        self.wait(max(0.1, remaining_wait_time))
        
        add_explanation_text(self, MathTex(r"\text{Key Method 3: 3D Trigonometry using 2D cross-sections}"))
        
        num_indicates = int(10.11 / 2.5)
        total_indicate_time = num_indicates * 0.5
        total_animation_time = 0.5
        remaining_wait_time = 10.11 - total_animation_time - total_indicate_time
        
        self.play(Indicate(elements["region_triangle_PQS_interior"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["region_triangle_QRS_interior"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["line_QS"], color="#FFFF00"))
        self.wait(max(0.1, 2.0))
        self.play(Indicate(elements["line_QS"], color="#FFFF00"))
        self.wait(max(0.1, remaining_wait_time - 6.0))
        
        self.play(FadeOut(complete_figure), run_time=2.0)