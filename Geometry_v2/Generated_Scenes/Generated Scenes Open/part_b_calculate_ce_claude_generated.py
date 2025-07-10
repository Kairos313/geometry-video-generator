from manim import *
import numpy as np

class PartBCalculateCe(Scene):
    def construct(self):
        # 1. Scene Setup & Audio
        self.camera.background_color = "#1E293B"
        self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Scene/part_b_calculate_ce_scene.mp3")

        #################################################################
        # PART 1: INSTANT RECONSTRUCTION of PartBCalculateBdAndAc's final state
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
        final_summary = VGroup(
            Text("Final Results:", font_size=26, color="#FFD700", weight=BOLD),
            MathTex(r"BD = 24 \text{ cm}", font_size=26, color="#87C2A5"),
            MathTex(r"AC = 24 \text{ cm}", font_size=26, color="#58C4DD")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -2.0, 0])
        
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
        BD_length_label = MathTex("24 \text{ cm}", font_size=24, color="#FFD700").next_to(
            (B + D) / 2, RIGHT, buff=0.2
        )
        AC_length_label = MathTex("24 \text{ cm}", font_size=24, color="#FFD700").next_to(
            (A + C) / 2, LEFT, buff=0.2
        )

        # Add all reconstructed mobjects instantly
        self.add(
            tri_ABC, tri_BAD, pentagon_ABCED, tri_ADE, tri_AEB, line_AC, line_BD,
            dot_A, dot_B, dot_C, dot_D, dot_E,
            label_A, label_B, label_C, label_D, label_E,
            angle_ACB, angle_ADB, angle_ADE, angle_CAB, angle_DBA,
            final_summary,
            AD_length_label, DE_length_label, AE_length_label, BE_length_label,
            BD_length_label, AC_length_label
        )

        #################################################################
        # PART 2: NEW ANIMATIONS for the current scene
        #################################################################
        current_time = 0

        # Sentence 1: 0.0s - 3.0s
        s1_start = 0.0
        s1_end = 3.0
        wait_duration = s1_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Fade out previous summary and introduce CE calculation
        ce_intro = VGroup(
            Text("Now finding CE:", font_size=26, color="#FFD700", weight=BOLD),
            Text("Using AC = AE + EC", font_size=24, color="#87C2A5")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 2.5, 0])
        
        self.play(
            FadeOut(final_summary),
            Write(ce_intro),
            Indicate(line_AC, color="#58C4DD", scale_factor=1.1),
            run_time=(s1_end - s1_start)
        )
        current_time = s1_end

        # Sentence 2: 3.01s - 5.13s
        s2_start = 3.01
        s2_end = 5.13
        wait_duration = s2_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Show AC composition equation
        ac_composition = MathTex(r"AC = AE + EC", font_size=28, color="#87C2A5").move_to([4.0, 1.5, 0])
        
        self.play(
            Write(ac_composition),
            Flash(AE_length_label, color="#FFD700"),
            run_time=(s2_end - s2_start)
        )
        current_time = s2_end

        # Sentence 3: 5.14s - 7.54s
        s3_start = 5.14
        s3_end = 7.54
        wait_duration = s3_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Substitute known values
        ac_substitution = MathTex(r"24 = 15 + EC", font_size=28, color="#E2D28B").move_to([4.0, 1.0, 0])
        
        self.play(
            Write(ac_substitution),
            Flash(AC_length_label, color="#FFD700"),
            Flash(AE_length_label, color="#FFD700"),
            run_time=(s3_end - s3_start)
        )
        current_time = s3_end

        # Sentence 4: 7.55s - 9.88s
        s4_start = 7.55
        s4_end = 9.88
        wait_duration = s4_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Show rearranged equation
        ec_equation = MathTex(r"EC = 24 - 15", font_size=28, color="#E2D28B").move_to([4.0, 0.5, 0])
        
        self.play(
            Write(ec_equation),
            run_time=(s4_end - s4_start)
        )
        current_time = s4_end

        # Sentence 5: 9.89s - 11.74s
        s5_start = 9.89
        s5_end = 11.74
        wait_duration = s5_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Show EC result
        ec_result = MathTex(r"EC = 9 \text{ cm}", font_size=28, color="#FFD700").move_to([4.0, 0.0, 0])
        
        # Add EC length label to diagram
        EC_length_label = MathTex("9 \text{ cm}", font_size=24, color="#FFD700").next_to(
            (E + C) / 2, DOWN + RIGHT, buff=0.2
        )
        
        self.play(
            Write(ec_result),
            Write(EC_length_label),
            run_time=(s5_end - s5_start)
        )
        current_time = s5_end

        # Sentence 6: 11.75s - 14.26s
        s6_start = 11.75
        s6_end = 14.26
        wait_duration = s6_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Final confirmation and highlight
        final_ce_result = VGroup(
            Text("Result:", font_size=26, color="#FFD700", weight=BOLD),
            MathTex(r"CE = 9 \text{ cm}", font_size=28, color="#FFD700")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -1.5, 0])
        
        self.play(
            FadeOut(ce_intro),
            FadeOut(ac_composition),
            FadeOut(ac_substitution),
            FadeOut(ec_equation),
            FadeOut(ec_result),
            Write(final_ce_result),
            Indicate(EC_length_label, color="#FFD700", scale_factor=1.3),
            Flash(dot_E, color="#FFD700"),
            Flash(dot_C, color="#FFD700"),
            run_time=(s6_end - s6_start)
        )
        current_time = s6_end
        
        self.wait(2)