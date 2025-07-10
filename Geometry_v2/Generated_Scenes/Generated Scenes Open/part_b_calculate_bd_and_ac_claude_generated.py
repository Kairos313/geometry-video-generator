from manim import *
import numpy as np

class PartBCalculateBdAndAc(Scene):
    def construct(self):
        # 1. Scene Setup & Audio
        self.camera.background_color = "#1E293B"
        self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Scene/part_b_calculate_bd_and_ac_scene.mp3")

        #################################################################
        # PART 1: INSTANT RECONSTRUCTION of PartBDeduceIsoscelesTriangle's final state
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
        tri_AEB = Polygon(A, E, B, color="#87C2A5", fill_opacity=0.3, stroke_width=4)
        
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
        
        # Create angle arcs from previous scene
        angle_CAB = Arc(radius=0.5, start_angle=np.arctan2((C-A)[1], (C-A)[0]), 
                       angle=np.arctan2((B-A)[1], (B-A)[0]) - np.arctan2((C-A)[1], (C-A)[0]),
                       color="#E2D28B", stroke_width=4).move_arc_center_to(A)
        angle_DBA = Arc(radius=0.5, start_angle=np.arctan2((D-B)[1], (D-B)[0]), 
                       angle=np.arctan2((A-B)[1], (A-B)[0]) - np.arctan2((D-B)[1], (D-B)[0]),
                       color="#E2D28B", stroke_width=4).move_arc_center_to(B)
        
        # Previous scene's final text elements
        key_relationship = VGroup(
            Text("Key Relationship:", font_size=28, color="#FFD700", weight=BOLD),
            MathTex(r"\triangle ABC \cong \triangle BAD", font_size=26, color="#58C4DD"),
            MathTex(r"\Rightarrow \angle CAB = \angle DBA", font_size=26, color="#E2D28B")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 2.0, 0])
        
        angle_equality = MathTex(r"\angle CAB = \angle DBA", font_size=28, color="#E2D28B").move_to([4.0, 0.5, 0])
        triangle_aeb_angles = MathTex(r"\angle EAB = \angle EBA", font_size=28, color="#FFD700").move_to([4.0, 0.8, 0])
        
        final_isosceles = VGroup(
            Text("Therefore:", font_size=26, color="#87C2A5"),
            Text("Triangle AEB is isosceles", font_size=26, color="#FFD700", weight=BOLD),
            MathTex(r"AE = BE", font_size=28, color="#FFD700")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -1.0, 0])
        
        be_calculation = VGroup(
            MathTex(r"AE = 15 \text{ cm}", font_size=26, color="#FFD700"),
            MathTex(r"\Rightarrow BE = 15 \text{ cm}", font_size=26, color="#FFD700")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -2.8, 0])
        
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
        BE_length_label = MathTex("15 \text{ cm}", font_size=24, color="#FFD700").next_to(
            (B + E) / 2, DOWN + RIGHT, buff=0.2
        )

        # Add all reconstructed mobjects instantly
        self.add(
            tri_ABC, tri_BAD, pentagon_ABCED, tri_ADE, tri_AEB, line_AC, line_BD,
            dot_A, dot_B, dot_C, dot_D, dot_E,
            label_A, label_B, label_C, label_D, label_E,
            angle_ACB, angle_ADB, angle_ADE, angle_CAB, angle_DBA,
            key_relationship, angle_equality, triangle_aeb_angles, final_isosceles, be_calculation,
            AD_length_label, DE_length_label, AE_length_label, BE_length_label
        )

        #################################################################
        # PART 2: NEW ANIMATIONS for the current scene
        #################################################################
        current_time = 0

        # Sentence 1: 0.0s - 3.66s
        s1_start = 0.0
        s1_end = 3.66
        wait_duration = s1_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Fade out previous text and introduce new calculation
        self.play(
            FadeOut(key_relationship),
            FadeOut(angle_equality),
            FadeOut(triangle_aeb_angles),
            FadeOut(final_isosceles),
            FadeOut(be_calculation),
            run_time=(s1_end - s1_start)
        )
        current_time = s1_end

        # Sentence 2: 3.67s - 6.18s
        s2_start = 3.67
        s2_end = 6.18
        wait_duration = s2_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Highlight BD and its components
        bd_composition = VGroup(
            Text("BD is composed of:", font_size=26, color="#FFD700", weight=BOLD),
            MathTex(r"BD = BE + DE", font_size=28, color="#87C2A5")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 2.5, 0])
        
        self.play(
            Write(bd_composition),
            Indicate(line_BD, color="#87C2A5", scale_factor=1.1),
            run_time=(s2_end - s2_start)
        )
        current_time = s2_end

        # Sentence 3: 6.19s - 10.37s
        s3_start = 6.19
        s3_end = 10.37
        wait_duration = s3_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Show congruence relationship
        congruence_reminder = VGroup(
            Text("From Part A congruence:", font_size=24, color="#58C4DD"),
            MathTex(r"AC = BD", font_size=28, color="#E2D28B")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 1.5, 0])
        
        self.play(
            Write(congruence_reminder),
            Indicate(line_AC, color="#58C4DD", scale_factor=1.1),
            run_time=(s3_end - s3_start)
        )
        current_time = s3_end

        # Sentence 4: 10.38s - 12.47s
        s4_start = 10.38
        s4_end = 12.47
        wait_duration = s4_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Show BD calculation setup
        bd_calculation_setup = MathTex(r"BD = BE + DE", font_size=28, color="#87C2A5").move_to([4.0, 0.5, 0])
        
        self.play(
            Write(bd_calculation_setup),
            run_time=(s4_end - s4_start)
        )
        current_time = s4_end

        # Sentence 5: 12.48s - 15.67s
        s5_start = 12.48
        s5_end = 15.67
        wait_duration = s5_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Substitute values
        bd_substitution = MathTex(r"BD = 15 + 9", font_size=28, color="#E2D28B").move_to([4.0, 0.0, 0])
        
        self.play(
            Write(bd_substitution),
            Flash(BE_length_label, color="#FFD700"),
            Flash(DE_length_label, color="#E2D28B"),
            run_time=(s5_end - s5_start)
        )
        current_time = s5_end

        # Sentence 6: 15.68s - 17.95s
        s6_start = 15.68
        s6_end = 17.95
        wait_duration = s6_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Show BD result
        bd_result = MathTex(r"BD = 24 \text{ cm}", font_size=28, color="#FFD700").move_to([4.0, -0.5, 0])
        
        # Add BD length label to diagram
        BD_length_label = MathTex("24 \text{ cm}", font_size=24, color="#FFD700").next_to(
            (B + D) / 2, RIGHT, buff=0.2
        )
        
        self.play(
            Write(bd_result),
            Write(BD_length_label),
            run_time=(s6_end - s6_start)
        )
        current_time = s6_end

        # Sentence 7: 17.96s - 22.56s
        s7_start = 17.96
        s7_end = 22.56
        wait_duration = s7_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Show AC equals BD
        ac_equals_bd = MathTex(r"AC = BD = 24 \text{ cm}", font_size=28, color="#FFD700").move_to([4.0, -1.0, 0])
        
        # Add AC length label to diagram
        AC_length_label = MathTex("24 \text{ cm}", font_size=24, color="#FFD700").next_to(
            (A + C) / 2, LEFT, buff=0.2
        )
        
        self.play(
            Write(ac_equals_bd),
            Write(AC_length_label),
            run_time=(s7_end - s7_start)
        )
        current_time = s7_end

        # Sentence 8: 22.57s - 27.25s
        s8_start = 22.57
        s8_end = 27.25
        wait_duration = s8_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Final summary
        final_summary = VGroup(
            Text("Final Results:", font_size=26, color="#FFD700", weight=BOLD),
            MathTex(r"BD = 24 \text{ cm}", font_size=26, color="#87C2A5"),
            MathTex(r"AC = 24 \text{ cm}", font_size=26, color="#58C4DD")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -2.0, 0])
        
        self.play(
            FadeOut(bd_composition),
            FadeOut(congruence_reminder),
            FadeOut(bd_calculation_setup),
            FadeOut(bd_substitution),
            FadeOut(bd_result),
            FadeOut(ac_equals_bd),
            Write(final_summary),
            Indicate(BD_length_label, color="#FFD700", scale_factor=1.2),
            Indicate(AC_length_label, color="#FFD700", scale_factor=1.2),
            run_time=(s8_end - s8_start)
        )
        current_time = s8_end
        
        self.wait(2)