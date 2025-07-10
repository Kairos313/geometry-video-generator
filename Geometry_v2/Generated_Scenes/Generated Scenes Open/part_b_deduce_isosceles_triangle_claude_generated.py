from manim import *
import numpy as np

class PartBDeduceIsoscelesTriangle(Scene):
    def construct(self):
        # 1. Scene Setup & Audio
        self.camera.background_color = "#1E293B"
        self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Scene/part_b_deduce_isosceles_triangle_scene.mp3")

        #################################################################
        # PART 1: INSTANT RECONSTRUCTION of PartBCalculateAe's final state
        #################################################################
        # Replicating the exact coordinate calculation logic from the previous scene
        
        # Base points to ground the diagram on the left side of the screen
        A = np.array([-5.5, -2, 0])
        B = np.array([-1.5, -2, 0])
        
        # Calculate D such that ∠ADB = 90°
        # Midpoint of AB
        AB_midpoint = (A + B) / 2
        AB_length = np.linalg.norm(B - A)
        # D is at distance AB_length/2 from midpoint, perpendicular to AB
        D = AB_midpoint + np.array([0, AB_length/2, 0])
        
        # Calculate C such that ∠ACB = 90° and BC = AD
        AD_length = np.linalg.norm(D - A)
        # C must be positioned such that BC = AD_length and ∠ACB = 90°
        # Place C below AB line for visual distinction
        C = AB_midpoint + np.array([0, -AD_length/2, 0])
        
        # Calculate intersection point E of AC and BD
        AC_vec = C - A
        BD_vec = D - B
        AB_vec = B - A
        
        # Solving the system of equations for intersection
        denominator = AC_vec[0] * BD_vec[1] - AC_vec[1] * BD_vec[0]
        if abs(denominator) > 1e-10:
            t = (AB_vec[0] * BD_vec[1] - AB_vec[1] * BD_vec[0]) / denominator
            E = A + t * AC_vec
        else:
            E = np.array([-3.5, -1, 0])  # Fallback position

        # Recreate all mobjects that were on screen at the end of previous scene
        tri_ABC = Polygon(A, B, C, color="#58C4DD", fill_opacity=0.3, stroke_width=3)
        tri_BAD = Polygon(B, A, D, color="#F07E48", fill_opacity=0.3, stroke_width=3)
        pentagon_ABCED = Polygon(A, B, C, E, D, color="#E2D28B", fill_opacity=0.2, stroke_width=4)
        tri_ADE = Polygon(A, D, E, color="#FFD700", fill_opacity=0.4, stroke_width=4)
        
        line_AC = Line(A, C, color="#87C2A5", stroke_width=2)
        line_BD = Line(B, D, color="#87C2A5", stroke_width=2)
        
        dot_A = Dot(A, color="#FFFFFF", radius=0.08)
        dot_B = Dot(B, color="#FFFFFF", radius=0.08)
        dot_C = Dot(C, color="#FFFFFF", radius=0.08)
        dot_D = Dot(D, color="#FFFFFF", radius=0.08)
        dot_E = Dot(E, color="#FFD700", radius=0.1)
        
        label_A = MathTex("A", color="#FFFFFF", font_size=32).next_to(A, DOWN + LEFT, buff=0.2)
        label_B = MathTex("B", color="#FFFFFF", font_size=32).next_to(B, DOWN + RIGHT, buff=0.2)
        label_C = MathTex("C", color="#FFFFFF", font_size=32).next_to(C, DOWN, buff=0.2)
        label_D = MathTex("D", color="#FFFFFF", font_size=32).next_to(D, UP, buff=0.2)
        label_E = MathTex("E", color="#FFD700", font_size=32).next_to(E, UP + RIGHT, buff=0.2)
        
        angle_ACB = RightAngle(Line(C, A), Line(C, B), length=0.3, color="#87C2A5")
        angle_ADB = RightAngle(Line(D, A), Line(D, B), length=0.3, color="#87C2A5")
        angle_ADE = RightAngle(Line(D, A), Line(D, E), length=0.3, color="#FFD700")
        
        # Previous scene's final text elements
        pythagorean_theorem = VGroup(
            Text("Pythagorean Theorem:", font_size=26, color="#FFD700", weight=BOLD),
            MathTex(r"AE^2 = AD^2 + DE^2", font_size=28, color="#58C4DD")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.0, -0.5, 0])
        
        substitution = MathTex(r"AE^2 = 12^2 + 9^2", font_size=28, color="#E2D28B").next_to(
            pythagorean_theorem, DOWN, buff=0.4
        )
        
        calculation1 = MathTex(r"AE^2 = 144 + 81", font_size=28, color="#E2D28B").next_to(
            substitution, DOWN, buff=0.3
        )
        
        calculation2 = MathTex(r"AE^2 = 225", font_size=28, color="#E2D28B").next_to(
            calculation1, DOWN, buff=0.3
        )
        
        final_calculation = MathTex(r"AE = \sqrt{225} = 15 \text{ cm}", font_size=28, color="#FFD700").next_to(
            calculation2, DOWN, buff=0.3
        )
        
        conclusion = VGroup(
            Text("Result:", font_size=28, color="#FFD700", weight=BOLD),
            MathTex(r"AE = 15 \text{ cm}", font_size=32, color="#FFD700")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -3.5, 0])
        
        # Add length labels from previous scene
        AD_length_label = MathTex("12 \text{ cm}", font_size=24, color="#E2D28B").next_to(
            (A + D) / 2, LEFT, buff=0.2
        )
        DE_length_label = MathTex("9 \text{ cm}", font_size=24, color="#E2D28B").next_to(
            (D + E) / 2, UP, buff=0.2
        )
        AE_length_label = MathTex("15 \text{ cm}", font_size=24, color="#FFD700").next_to(
            (A + E) / 2, DOWN + LEFT, buff=0.2
        )

        # Add all reconstructed mobjects instantly
        self.add(
            tri_ABC, tri_BAD, pentagon_ABCED, tri_ADE, line_AC, line_BD,
            dot_A, dot_B, dot_C, dot_D, dot_E,
            label_A, label_B, label_C, label_D, label_E,
            angle_ACB, angle_ADB, angle_ADE,
            pythagorean_theorem, substitution, calculation1, calculation2,
            final_calculation, conclusion, AD_length_label, DE_length_label, AE_length_label
        )

        #################################################################
        # PART 2: NEW ANIMATIONS for the current scene
        #################################################################
        current_time = 0

        # Sentence 1: 0.0s - 2.82s
        s1_start = 0.0
        s1_end = 2.82
        wait_duration = s1_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Fade out previous calculation text and introduce congruence
        self.play(
            FadeOut(pythagorean_theorem),
            FadeOut(substitution),
            FadeOut(calculation1),
            FadeOut(calculation2),
            FadeOut(final_calculation),
            FadeOut(conclusion),
            run_time=(s1_end - s1_start)
        )
        current_time = s1_end

        # Sentence 2: 2.83s - 8.58s
        s2_start = 2.83
        s2_end = 8.58
        wait_duration = s2_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Highlight the congruent triangles and introduce CPCTC
        congruence_text = VGroup(
            Text("From Part A:", font_size=28, color="#FFD700", weight=BOLD),
            MathTex(r"\triangle ABC \cong \triangle BAD", font_size=26, color="#58C4DD"),
            Text("By CPCTC:", font_size=24, color="#87C2A5"),
            Text("Corresponding angles are equal", font_size=22, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 2.0, 0])
        
        self.play(
            Write(congruence_text),
            Indicate(tri_ABC, color="#58C4DD", scale_factor=1.05),
            Indicate(tri_BAD, color="#F07E48", scale_factor=1.05),
            run_time=(s2_end - s2_start)
        )
        current_time = s2_end

        # Sentence 3: 8.59s - 11.7s
        s3_start = 8.59
        s3_end = 11.7
        wait_duration = s3_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Show the specific angle equality
        angle_equality = MathTex(r"\angle CAB = \angle DBA", font_size=28, color="#E2D28B").move_to([4.0, 0.5, 0])
        
        # Create angle arcs to highlight the angles
        angle_CAB = Arc(radius=0.5, start_angle=np.arctan2((C-A)[1], (C-A)[0]), 
                       angle=np.arctan2((B-A)[1], (B-A)[0]) - np.arctan2((C-A)[1], (C-A)[0]),
                       color="#E2D28B", stroke_width=4).move_arc_center_to(A)
        angle_DBA = Arc(radius=0.5, start_angle=np.arctan2((D-B)[1], (D-B)[0]), 
                       angle=np.arctan2((A-B)[1], (A-B)[0]) - np.arctan2((D-B)[1], (D-B)[0]),
                       color="#E2D28B", stroke_width=4).move_arc_center_to(B)
        
        self.play(
            Write(angle_equality),
            Create(angle_CAB),
            Create(angle_DBA),
            run_time=(s3_end - s3_start)
        )
        current_time = s3_end

        # Sentence 4: 11.71s - 19.13s
        s4_start = 11.71
        s4_end = 19.13
        wait_duration = s4_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Highlight triangle AEB and explain angle relationships
        tri_AEB = Polygon(A, E, B, color="#87C2A5", fill_opacity=0.3, stroke_width=4)
        
        triangle_aeb_text = VGroup(
            Text("In triangle AEB:", font_size=26, color="#87C2A5", weight=BOLD),
            MathTex(r"\angle EAB = \angle CAB", font_size=24, color="#E2D28B"),
            MathTex(r"\angle EBA = \angle DBA", font_size=24, color="#E2D28B")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -0.5, 0])
        
        self.play(
            Create(tri_AEB),
            Write(triangle_aeb_text),
            run_time=(s4_end - s4_start)
        )
        current_time = s4_end

        # Sentence 5: 19.14s - 24.57s
        s5_start = 19.14
        s5_end = 24.57
        wait_duration = s5_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Show that triangle AEB is isosceles
        isosceles_conclusion = VGroup(
            MathTex(r"\angle EAB = \angle EBA", font_size=26, color="#FFD700"),
            Text("Therefore:", font_size=24, color="#87C2A5"),
            Text("Triangle AEB is isosceles", font_size=24, color="#FFD700", weight=BOLD)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -2.5, 0])
        
        self.play(
            Write(isosceles_conclusion),
            Indicate(tri_AEB, color="#87C2A5", scale_factor=1.1),
            run_time=(s5_end - s5_start)
        )
        current_time = s5_end

        # Sentence 6: 24.58s - 30.93s
        s6_start = 24.58
        s6_end = 30.93
        wait_duration = s6_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Clear some text and restate the key relationship
        self.play(
            FadeOut(congruence_text),
            FadeOut(triangle_aeb_text),
            run_time=1.0
        )
        
        key_relationship = VGroup(
            Text("Key Relationship:", font_size=28, color="#FFD700", weight=BOLD),
            MathTex(r"\triangle ABC \cong \triangle BAD", font_size=26, color="#58C4DD"),
            MathTex(r"\Rightarrow \angle CAB = \angle DBA", font_size=26, color="#E2D28B")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 2.0, 0])
        
        self.play(
            Write(key_relationship),
            run_time=(s6_end - s6_start - 1.0)
        )
        current_time = s6_end

        # Sentence 7: 30.94s - 34.96s
        s7_start = 30.94
        s7_end = 34.96
        wait_duration = s7_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Emphasize the angle equality in triangle AEB
        triangle_aeb_angles = MathTex(r"\angle EAB = \angle EBA", font_size=28, color="#FFD700").move_to([4.0, 0.8, 0])
        
        self.play(
            Write(triangle_aeb_angles),
            Flash(angle_CAB, color="#E2D28B"),
            Flash(angle_DBA, color="#E2D28B"),
            run_time=(s7_end - s7_start)
        )
        current_time = s7_end

        # Sentence 8: 34.97s - 40.17s
        s8_start = 34.97
        s8_end = 40.17
        wait_duration = s8_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Final conclusion about isosceles triangle
        final_isosceles = VGroup(
            Text("Therefore:", font_size=26, color="#87C2A5"),
            Text("Triangle AEB is isosceles", font_size=26, color="#FFD700", weight=BOLD),
            MathTex(r"AE = BE", font_size=28, color="#FFD700")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -1.0, 0])
        
        self.play(
            FadeOut(isosceles_conclusion),
            Write(final_isosceles),
            run_time=(s8_end - s8_start)
        )
        current_time = s8_end

        # Sentence 9: 40.18s - 45.14s
        s9_start = 40.18
        s9_end = 45.14
        wait_duration = s9_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Show that BE = 15 cm
        be_calculation = VGroup(
            MathTex(r"AE = 15 \text{ cm}", font_size=26, color="#FFD700"),
            MathTex(r"\Rightarrow BE = 15 \text{ cm}", font_size=26, color="#FFD700")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -2.8, 0])
        
        # Add BE length label to the diagram
        BE_length_label = MathTex("15 \text{ cm}", font_size=24, color="#FFD700").next_to(
            (B + E) / 2, DOWN + RIGHT, buff=0.2
        )
        
        self.play(
            Write(be_calculation),
            Write(BE_length_label),
            Indicate(AE_length_label, color="#FFD700", scale_factor=1.2),
            run_time=(s9_end - s9_start)
        )
        current_time = s9_end
        
        self.wait(2)