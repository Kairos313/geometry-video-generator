#!/usr/bin/env python3

from manim import *
import numpy as np
import os
import sys

# CRITICAL: Add grandparent directory to path to import helpers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from functions import *

class CompleteScene_a(Scene):
    def construct(self):
        self.camera.background_color = "#0C0C0C"
        
        # STEP 1: Create ALL geometric elements from JSON analysis (invisible)
        # Extract coordinates from blueprint tables
        coord_P = np.array([0.000, 0.000, 0.000])
        coord_Q = np.array([12.000, 0.000, 0.000])
        coord_S = np.array([1.392, 9.903, 0.000])
        coord_R = np.array([-0.386, -3.949, 0.000])
        
        # Create points identified in JSON geometric_elements arrays
        dots = VGroup(
            Dot(coord_P, radius=0.08, color="#FFFFFF"),
            Dot(coord_Q, radius=0.08, color="#FFFFFF"),
            Dot(coord_S, radius=0.08, color="#FFFFFF"),
            Dot(coord_R, radius=0.08, color="#FFFFFF")
        )
        
        # Create lines identified in JSON (structural elements)
        lines = VGroup(
            Line(coord_P, coord_Q, color="#FFFFFF", stroke_width=2),  # PQ
            Line(coord_P, coord_S, color="#FFFFFF", stroke_width=2),  # PS
            Line(coord_Q, coord_S, color="#FFFF00", stroke_width=3),  # QS - highlighted as main diagonal
            Line(coord_Q, coord_R, color="#FFFFFF", stroke_width=2),  # QR
            Line(coord_R, coord_S, color="#FFFFFF", stroke_width=2)   # RS
        )
        
        # Create labels (structural elements)
        labels = VGroup(
            MathTex("P", font_size=72, color="#FFFFFF").move_to(coord_P + np.array([-0.5, -0.5, 0])),
            MathTex("Q", font_size=72, color="#FFFFFF").move_to(coord_Q + np.array([0.5, -0.5, 0])),
            MathTex("S", font_size=72, color="#FFFFFF").move_to(coord_S + np.array([-0.5, 0.5, 0])),
            MathTex("R", font_size=72, color="#FFFFFF").move_to(coord_R + np.array([-0.5, -0.5, 0]))
        )
        
        # Create measurement labels
        measurement_labels = VGroup(
            MathTex("12\\text{ cm}", font_size=48, color="#00FF00").move_to((coord_P + coord_Q) / 2 + np.array([0, -0.8, 0])),
            MathTex("10\\text{ cm}", font_size=48, color="#00FF00").move_to((coord_P + coord_S) / 2 + np.array([-1.2, 0, 0])),
            MathTex("13\\text{ cm}", font_size=48, color="#00FF00").move_to((coord_Q + coord_R) / 2 + np.array([1.2, 0, 0])),
            MathTex("14.51\\text{ cm}", font_size=48, color="#FFFF00").move_to((coord_Q + coord_S) / 2 + np.array([1.5, 0, 0]))
        )
        
        # Create angle arcs using helper functions (structural elements)
        # Angle QPS = 82° (≤ 180°) → use_smaller_angle=True
        angle_QPS = create_2d_angle_arc_geometric(
            center=coord_P, point1=coord_Q, point2=coord_S,
            radius=0.8, num_points=30, use_smaller_angle=True,
            show_connections=False, connection_color="#FFFFFF",
            connection_opacity=0.2, connection_style="solid", color="#FFFF00"
        )
        
        # Angle QRS = 65° (≤ 180°) → use_smaller_angle=True
        angle_QRS = create_2d_angle_arc_geometric(
            center=coord_R, point1=coord_Q, point2=coord_S,
            radius=0.6, num_points=30, use_smaller_angle=True,
            show_connections=False, connection_color="#FFFFFF",
            connection_opacity=0.2, connection_style="solid", color="#00FF00"
        )
        
        # Angle RQS = 60.7° (≤ 180°) → use_smaller_angle=True
        angle_RQS = create_2d_angle_arc_geometric(
            center=coord_Q, point1=coord_R, point2=coord_S,
            radius=0.7, num_points=30, use_smaller_angle=True,
            show_connections=False, connection_color="#FFFFFF",
            connection_opacity=0.2, connection_style="solid", color="#FF0000"
        )
        
        # Angle QSR = 54.3° (≤ 180°) → use_smaller_angle=True
        angle_QSR = create_2d_angle_arc_geometric(
            center=coord_S, point1=coord_Q, point2=coord_R,
            radius=0.5, num_points=30, use_smaller_angle=True,
            show_connections=False, connection_color="#FFFFFF",
            connection_opacity=0.2, connection_style="solid", color="#0000FF"
        )
        
        # Create angle labels
        angle_labels = VGroup(
            MathTex("82^{\\circ}", font_size=48, color="#FFFF00").move_to(coord_P + np.array([1.5, 1.0, 0])),
            MathTex("65^{\\circ}", font_size=48, color="#00FF00").move_to(coord_R + np.array([1.0, 1.0, 0])),
            MathTex("60.7^{\\circ}", font_size=48, color="#FF0000").move_to(coord_Q + np.array([-1.5, 1.5, 0])),
            MathTex("54.3^{\\circ}", font_size=48, color="#0000FF").move_to(coord_S + np.array([1.0, -1.0, 0]))
        )
        
        # Create polygons for highlighting (shape/region elements)
        triangle_PQS = Polygon(coord_P, coord_Q, coord_S, fill_opacity=0.2, fill_color="#0000FF", stroke_width=2, stroke_color="#0000FF")
        triangle_QRS = Polygon(coord_Q, coord_R, coord_S, fill_opacity=0.2, fill_color="#00FF00", stroke_width=2, stroke_color="#00FF00")
        
        # Combine all elements
        complete_figure = VGroup(
            dots, lines, labels, measurement_labels,
            angle_QPS, angle_QRS, angle_RQS, angle_QSR, angle_labels,
            triangle_PQS, triangle_QRS
        )
        
        # STEP 2: Set all elements invisible initially
        complete_figure.set_opacity(0)
        
        # STEP 3: Auto-scale the complete figure
        auto_scale_to_left_screen(complete_figure, is_3d=False, margin_factor=0.85, pitch_angle=-40, yaw_angle=-20)
        self.add(complete_figure)
        
        # STEP 4: Follow sentence-by-sentence animation from JSON
        
        # Sentence 1: "Hello! Let's solve this problem step-by-step. First, we need to find the length of the diagonal QS. We'll focus on triangle PQS."
        dots.set_opacity(1)
        labels.set_opacity(1)
        lines[0].set_opacity(1)  # PQ
        lines[1].set_opacity(1)  # PS
        lines[2].set_opacity(1)  # QS
        triangle_PQS.set_opacity(0.2)
        self.play(FadeIn(dots), FadeIn(labels), Create(lines[0]), Create(lines[1]), Create(lines[2]))
        self.play(Indicate(triangle_PQS, color="#0000FF"))
        self.wait(0.5)
        
        # Sentence 2: "We are given two sides, PQ and PS, and the angle between them, angle QPS. This is a classic 'Side-Angle-Side' case, so we use the Cosine Rule."
        measurement_labels[0].set_opacity(1)  # PQ = 12 cm
        measurement_labels[1].set_opacity(1)  # PS = 10 cm
        angle_QPS.set_opacity(1)
        angle_labels[0].set_opacity(1)  # 82°
        self.play(FadeIn(measurement_labels[0]), FadeIn(measurement_labels[1]))
        self.play(Create(angle_QPS), FadeIn(angle_labels[0]))
        self.wait(0.5)
        
        # Sentence 3: "Plugging in the values, we get that QS squared is equal to 12 squared plus 10 squared, minus 2 times 12 times 10 times the cosine of 82 degrees."
        self.play(Indicate(lines[2], color="#FFFF00"))
        self.wait(0.5)
        
        # Sentence 4: "Solving this gives us QS squared as approximately 210.6. Taking the square root, we find that the length of QS is about 14.51 centimeters."
        measurement_labels[3].set_opacity(1)  # QS = 14.51 cm
        self.play(FadeIn(measurement_labels[3]))
        self.wait(0.5)
        
        # Sentence 5: "Next, let's find the measure of angle RQS. For this, we'll look at triangle QRS."
        dots[3].set_opacity(1)  # Point R
        lines[3].set_opacity(1)  # QR
        lines[4].set_opacity(1)  # RS
        triangle_QRS.set_opacity(0.2)
        self.play(FadeIn(dots[3]), Create(lines[3]), Create(lines[4]))
        self.play(Indicate(triangle_QRS, color="#00FF00"))
        self.wait(0.5)
        
        # Sentence 6: "We know side QR, angle QRS, and side QS from our previous calculation. Since we have a side and its opposite angle (QS and angle QRS), we can use the Sine Rule to find another angle."
        measurement_labels[2].set_opacity(1)  # QR = 13 cm
        angle_QRS.set_opacity(1)
        angle_labels[1].set_opacity(1)  # 65°
        self.play(FadeIn(measurement_labels[2]))
        self.play(Create(angle_QRS), FadeIn(angle_labels[1]))
        self.play(Indicate(lines[2], color="#FFFF00"))
        self.wait(0.5)
        
        # Sentence 7: "Let's first find angle QSR. Setting up the ratio, we find that the sine of angle QSR is approximately 0.812. This gives us an angle of about 54.3 degrees."
        angle_QSR.set_opacity(1)
        angle_labels[3].set_opacity(1)  # 54.3°
        self.play(Create(angle_QSR), FadeIn(angle_labels[3]))
        self.wait(0.5)
        
        # Sentence 8: "Finally, since the angles in a triangle add up to 180 degrees, we can find angle RQS by subtracting the two known angles from 180. This gives us approximately 60.7 degrees."
        angle_RQS.set_opacity(1)
        angle_labels[2].set_opacity(1)  # 60.7°
        self.play(Create(angle_RQS), FadeIn(angle_labels[2]))
        self.wait(0.5)
        
        # Final highlight of the complete solution
        self.play(Indicate(triangle_PQS, color="#0000FF"), Indicate(triangle_QRS, color="#00FF00"))
        self.wait(2)

class CompleteScene_b(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#0C0C0C"
        
        # STEP 1: Create ALL geometric elements from JSON analysis (invisible)
        # Extract coordinates from blueprint tables (varying Z-coordinates for 3D)
        coord_P = np.array([0.000, 0.000, 0.000])
        coord_Q = np.array([12.000, 0.000, 0.000])
        coord_S = np.array([1.392, 9.903, 0.000])
        coord_R = np.array([6.008, 2.900, 11.166])  # 3D position after folding
        coord_T = np.array([7.352, 4.339, 0.000])   # Foot of perpendicular from R to QS
        coord_U = np.array([5.588, 5.986, 0.000])   # Foot of perpendicular from P to QS
        coord_R_p = np.array([6.008, 2.900, 0.000]) # Projection of R onto plane PQS
        coord_P_p = np.array([-5.420, -5.806, -1.400]) # Projection of P onto plane QRS
        
        # Create 3D points (structural elements)
        dots = VGroup(
            Dot3D(coord_P, radius=0.08, color="#FFFFFF"),
            Dot3D(coord_Q, radius=0.08, color="#FFFFFF"),
            Dot3D(coord_S, radius=0.08, color="#FFFFFF"),
            Dot3D(coord_R, radius=0.08, color="#FFFF00"),
            Dot3D(coord_T, radius=0.06, color="#00FF00"),
            Dot3D(coord_U, radius=0.06, color="#0000FF")
        )
        
        # Create 3D lines (structural elements)
        lines = VGroup(
            Line3D(coord_P, coord_Q, color="#FFFFFF", thickness=0.02),
            Line3D(coord_P, coord_S, color="#FFFFFF", thickness=0.02),
            Line3D(coord_Q, coord_S, color="#FFFF00", thickness=0.03),  # Fold line
            Line3D(coord_Q, coord_R, color="#FFFFFF", thickness=0.02),
            Line3D(coord_R, coord_S, color="#FFFFFF", thickness=0.02)
        )
        
        # Create construction lines (structural elements)
        construction_lines = VGroup(
            Line3D(coord_R, coord_T, color="#00FF00", thickness=0.02),      # RT - altitude from R to QS
            Line3D(coord_R, coord_R_p, color="#FF0000", thickness=0.03),    # h - shortest distance from R to plane PQS
            Line3D(coord_P, coord_U, color="#0000FF", thickness=0.02),      # PU - altitude from P to QS
            Line3D(coord_P, coord_P_p, color="#FF00FF", thickness=0.03)     # d - shortest distance from P to plane QRS
        )
        
        # Create 3D labels (structural elements)
        labels = VGroup(
            MathTex("P", font_size=72, color="#FFFFFF").move_to(coord_P + np.array([-0.8, -0.8, 0])),
            MathTex("Q", font_size=72, color="#FFFFFF").move_to(coord_Q + np.array([0.8, -0.8, 0])),
            MathTex("S", font_size=72, color="#FFFFFF").move_to(coord_S + np.array([-0.8, 0.8, 0])),
            MathTex("R", font_size=72, color="#FFFF00").move_to(coord_R + np.array([0.8, 0.8, 0.8])),
            MathTex("T", font_size=48, color="#00FF00").move_to(coord_T + np.array([0, 0, -0.6])),
            MathTex("U", font_size=48, color="#0000FF").move_to(coord_U + np.array([0, 0, -0.6]))
        )
        
        # Create measurement labels
        measurement_labels = VGroup(
            MathTex("h = 11.17\\text{ cm}", font_size=48, color="#FF0000").move_to(coord_R + np.array([2.0, 0, -2.0])),
            MathTex("d = 8.07\\text{ cm}", font_size=48, color="#FF00FF").move_to(coord_P + np.array([-2.0, -2.0, 0])),
            MathTex("80^{\\circ}", font_size=48, color="#FFFF00").move_to((coord_P + coord_R) / 2 + np.array([0, 0, 2.0]))
        )
        
        # Create 3D faces/polyhedra (shape/region elements)
        face_PQS = Polygon(coord_P, coord_Q, coord_S, fill_opacity=0.2, fill_color="#0000FF", stroke_width=2, stroke_color="#0000FF")
        face_QRS = Polygon(coord_Q, coord_R, coord_S, fill_opacity=0.2, fill_color="#00FF00", stroke_width=2, stroke_color="#00FF00")
        
        # Create dihedral angle representation
        dihedral_angle = create_3d_angle_arc_with_connections(
            center=(coord_Q + coord_S) / 2, point1=coord_P, point2=coord_R,
            radius=1.0, num_points=30, show_connections=False,
            connection_color="#FFFFFF", connection_opacity=0.2,
            connection_style="solid", color="#FFFF00"
        )
        
        # Combine all elements
        complete_figure = VGroup(
            dots, lines, construction_lines, labels, measurement_labels,
            face_PQS, face_QRS, dihedral_angle
        )
        
        # STEP 2: Set all elements invisible initially
        complete_figure.set_opacity(0)
        
        # STEP 3: Auto-scale the complete figure FIRST
        auto_scale_to_left_screen(complete_figure, is_3d=True, margin_factor=0.85, pitch_angle=-40, yaw_angle=-20)
        self.add(complete_figure)
        
        # STEP 4: Follow sentence-by-sentence animation from JSON
        
        # Sentence 1: "Now for part (b). The sheet is folded along QS, and the angle between the two planes is 80 degrees. We need the shortest distance from point R to the plane PQS."
        dots[:4].set_opacity(1)      # P, Q, S, R
        labels[:4].set_opacity(1)    # P, Q, S, R labels
        lines.set_opacity(1)         # All main lines
        face_PQS.set_opacity(0.2)    # Plane PQS
        face_QRS.set_opacity(0.2)    # Plane QRS
        self.play(Create(dots[:4]), Create(labels[:4]), Create(lines))
        self.play(Create(face_PQS), Create(face_QRS))
        self.play(Indicate(dots[3], color="#FFFF00"))  # Highlight point R
        self.play(Indicate(face_PQS, color="#0000FF"))  # Highlight plane PQS
        self.wait(0.5)
        
        # Sentence 2: "This distance is a perpendicular line from R to the plane. We can find it by first calculating the altitude from R to the line QS in triangle QRS. Let's call this altitude RT."
        dots[4].set_opacity(1)  # Point T
        labels[4].set_opacity(1)  # T label
        construction_lines[0].set_opacity(1)  # RT line
        self.play(Create(dots[4]), Create(labels[4]), Create(construction_lines[0]))
        self.wait(0.5)
        
        # Sentence 3: "Using the values we know, RT is 13 times the sine of 60.7 degrees, which is about 11.34 cm. The shortest distance, let's call it 'h', is then RT times the sine of the 80-degree fold angle."
        construction_lines[1].set_opacity(1)  # h line
        measurement_labels[0].set_opacity(1)  # h = 11.17 cm
        measurement_labels[2].set_opacity(1)  # 80°
        dihedral_angle.set_opacity(1)
        self.play(Create(construction_lines[1]), FadeIn(measurement_labels[0]))
        self.play(Create(dihedral_angle), FadeIn(measurement_labels[2]))
        self.wait(0.5)
        
        # Sentence 4: "This gives us a final distance of approximately 11.17 centimeters."
        self.play(Indicate(construction_lines[1], color="#FF0000"))
        self.play(Indicate(measurement_labels[0], color="#FF0000"))
        self.wait(0.5)
        
        # Sentence 5: "For the final part, we must check if the distance from P to any point X on the plane QRS is always greater than 8 cm. This means we need to find the shortest possible distance from P to that plane."
        self.play(Indicate(dots[0], color="#FFFFFF"))  # Highlight point P
        self.play(Indicate(face_QRS, color="#00FF00"))  # Highlight plane QRS
        self.wait(0.5)
        
        # Sentence 6: "Similar to the last step, this distance 'd' depends on the altitude from P to the line QS in triangle PQS. Let's call this altitude PU. We can find PU using the area of triangle PQS."
        dots[5].set_opacity(1)  # Point U
        labels[5].set_opacity(1)  # U label
        construction_lines[2].set_opacity(1)  # PU line
        self.play(Create(dots[5]), Create(labels[5]), Create(construction_lines[2]))
        self.wait(0.5)
        
        # Sentence 7: "Solving for PU gives us about 8.19 cm. The shortest distance 'd' is then PU times the sine of the 80-degree fold angle."
        construction_lines[3].set_opacity(1)  # d line
        self.play(Create(construction_lines[3]))
        self.wait(0.5)
        
        # Sentence 8: "This calculation gives a shortest distance of approximately 8.07 cm. Since the shortest distance is 8.07 cm, which is greater than 8 cm, any other distance from P to the plane will also be greater. Therefore, the claim is correct."
        measurement_labels[1].set_opacity(1)  # d = 8.07 cm
        self.play(FadeIn(measurement_labels[1]))
        self.play(Indicate(construction_lines[3], color="#FF00FF"))
        self.play(Indicate(measurement_labels[1], color="#FF00FF"))
        self.wait(0.5)
        
        # Final summary highlighting
        self.play(Indicate(construction_lines[1], color="#FF0000"), Indicate(construction_lines[3], color="#FF00FF"))
        self.wait(1)
        
        # STEP 5: MANDATORY - Final rotation AFTER auto-scaling and AFTER all animations
        self.play(Rotate(complete_figure, angle=2*PI, axis=UP), run_time=8)
        self.wait(1)