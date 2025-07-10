from manim import *
import numpy as np

class PartBCalculateIndividualAreas(Scene):
    def construct(self):
        # 1. Scene Setup & Audio
        self.camera.background_color = "#1E293B"
        self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Scene/part_b_calculate_individual_areas_scene.mp3")

        #################################################################
        # PART 1: INSTANT RECONSTRUCTION of PartBConfirmRightAngleBce's final state
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
        tri_BCE = Polygon(B, C, E, color="#58C4DD", fill_opacity=0.5, stroke_width=5)
        
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
        angle_BCE = RightAngle(Line(C, B), Line(C, E), length=0.3, color="#58C4DD")
        
        # Create angle arcs from previous scene
        angle_CAB = Arc(radius=0.5, start_angle=np.arctan2((C-A)[1], (C-A)[0]), 
                       angle=np.arctan2((B-A)[1], (B-A)[0]) - np.arctan2((C-A)[1], (C-A)[0]),
                       color="#E2D28B", stroke_width=4).move_arc_center_to(A)
        angle_DBA = Arc(radius=0.5, start_angle=np.arctan2((D-B)[1], (D-B)[0]), 
                       angle=np.arctan2((A-B)[1], (A-B)[0]) - np.arctan2((D-B)[1], (D-B)[0]),
                       color="#E2D28B", stroke_width=4).move_arc_center_to(B)
        
        # Previous scene's final text elements
        conclusion = VGroup(
            MathTex(r"CE^2 + BC^2 = BE^2", font_size=26, color="#FFD700"),
            MathTex(r"\therefore \angle BCE = 90°", font_size=26, color="#FFD700")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 1.5, 0])
        
        final_result = VGroup(
            Text("Triangle BCE is right-angled at C", font_size=24, color="#58C4DD", weight=BOLD),
            MathTex(r"\angle BCE = 90°", font_size=26, color="#58C4DD")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 0.0, 0])
        
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
        EC_length_label = MathTex("9 \text{ cm}", font_size=24, color="#FFD700").next_to(
            (E + C) / 2, DOWN + RIGHT, buff=0.2
        )
        BC_length_label = MathTex("12 \text{ cm}", font_size=24, color="#58C4DD").next_to(
            (B + C) / 2, DOWN, buff=0.2
        )

        # Add all reconstructed mobjects instantly
        self.add(
            tri_ABC, tri_BAD, pentagon_ABCED, tri_ADE, tri_AEB, tri_BCE, line_AC, line_BD,
            dot_A, dot_B, dot_C, dot_D, dot_E,
            label_A, label_B, label_C, label_D, label_E,
            angle_ACB, angle_ADB, angle_ADE, angle_BCE, angle_CAB, angle_DBA,
            conclusion, final_result,
            AD_length_label, DE_length_label, AE_length_label, BE_length_label,
            BD_length_label, AC_length_label, EC_length_label, BC_length_label
        )

        #################################################################
        # PART 2: NEW ANIMATIONS for the current scene
        #################################################################
        current_time = 0

        # Sentence 1: 0.0s - 4.0s
        s1_start = 0.0
        s1_end = 4.0
        wait_duration = s1_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Introduce area calculations
        intro_text = Text("Calculating Individual Triangle Areas", font_size=28, color="#FFD700", weight=BOLD).move_to([4.0, 3.0, 0])
        
        self.play(
            FadeOut(conclusion),
            FadeOut(final_result),
            Write(intro_text),
            run_time=(s1_end - s1_start)
        )
        current_time = s1_end

        # Sentence 2: 4.01s - 11.12s
        s2_start = 4.01
        s2_end = 11.12
        wait_duration = s2_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Focus on triangle ADE
        self.play(
            Indicate(tri_ADE, color="#FFD700", scale_factor=1.1),
            Flash(angle_ADE, color="#FFD700"),
            run_time=2.0
        )
        
        ade_intro = VGroup(
            Text("Triangle ADE (right-angled at D):", font_size=24, color="#FFD700", weight=BOLD),
            Text("Area = ½ × base × height", font_size=22, color="#FFD700")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 2.0, 0])
        
        self.play(
            Write(ade_intro),
            run_time=(s2_end - s2_start - 2.0)
        )
        current_time = s2_end

        # Sentence 3: 11.13s - 15.02s
        s3_start = 11.13
        s3_end = 15.02
        wait_duration = s3_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Show ADE area formula
        ade_formula = MathTex(r"\text{Area}(\triangle ADE) = \frac{1}{2} \times AD \times DE", 
                             font_size=24, color="#FFD700").move_to([4.0, 1.0, 0])
        
        self.play(
            Write(ade_formula),
            Flash(AD_length_label, color="#FFD700"),
            Flash(DE_length_label, color="#FFD700"),
            run_time=(s3_end - s3_start)
        )
        current_time = s3_end

        # Sentence 4: 15.03s - 21.43s
        s4_start = 15.03
        s4_end = 21.43
        wait_duration = s4_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Calculate ADE area
        ade_calculation = VGroup(
            MathTex(r"\text{Area}(\triangle ADE) = \frac{1}{2} \times 12 \times 9", font_size=22, color="#87C2A5"),
            MathTex(r"= 54 \text{ cm}^2", font_size=24, color="#87C2A5", weight=BOLD)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 0.0, 0])
        
        self.play(
            Write(ade_calculation),
            run_time=(s4_end - s4_start)
        )
        current_time = s4_end

        # Sentence 5: 21.44s - 28.49s
        s5_start = 21.44
        s5_end = 28.49
        wait_duration = s5_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Focus on triangle BCE
        self.play(
            Indicate(tri_BCE, color="#58C4DD", scale_factor=1.1),
            Flash(angle_BCE, color="#58C4DD"),
            run_time=2.0
        )
        
        bce_intro = VGroup(
            Text("Triangle BCE (right-angled at C):", font_size=24, color="#58C4DD", weight=BOLD),
            Text("Area = ½ × base × height", font_size=22, color="#58C4DD")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -1.0, 0])
        
        self.play(
            Write(bce_intro),
            run_time=(s5_end - s5_start - 2.0)
        )
        current_time = s5_end

        # Sentence 6: 28.5s - 32.68s
        s6_start = 28.5
        s6_end = 32.68
        wait_duration = s6_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Show BCE area formula
        bce_formula = MathTex(r"\text{Area}(\triangle BCE) = \frac{1}{2} \times BC \times CE", 
                             font_size=24, color="#58C4DD").move_to([4.0, -2.0, 0])
        
        self.play(
            Write(bce_formula),
            Flash(BC_length_label, color="#58C4DD"),
            Flash(EC_length_label, color="#58C4DD"),
            run_time=(s6_end - s6_start)
        )
        current_time = s6_end

        # Sentence 7: 32.69s - 38.8s
        s7_start = 32.69
        s7_end = 38.8
        wait_duration = s7_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Calculate BCE area
        bce_calculation = VGroup(
            MathTex(r"\text{Area}(\triangle BCE) = \frac{1}{2} \times 12 \times 9", font_size=22, color="#87C2A5"),
            MathTex(r"= 54 \text{ cm}^2", font_size=24, color="#87C2A5", weight=BOLD)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -3.0, 0])
        
        self.play(
            Write(bce_calculation),
            run_time=(s7_end - s7_start)
        )
        current_time = s7_end

        # Sentence 8: 38.81s - 42.6s
        s8_start = 38.81
        s8_end = 42.6
        wait_duration = s8_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Clear previous calculations and focus on triangle ABD
        self.play(
            FadeOut(ade_intro),
            FadeOut(ade_formula),
            FadeOut(ade_calculation),
            FadeOut(bce_intro),
            FadeOut(bce_formula),
            FadeOut(bce_calculation),
            Indicate(tri_BAD, color="#F07E48", scale_factor=1.1),
            Flash(angle_ADB, color="#F07E48"),
            run_time=(s8_end - s8_start)
        )
        current_time = s8_end

        # Sentence 9: 42.61s - 46.63s
        s9_start = 42.61
        s9_end = 46.63
        wait_duration = s9_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Show ABD area formula
        abd_formula = MathTex(r"\text{Area}(\triangle ABD) = \frac{1}{2} \times AD \times BD", 
                             font_size=24, color="#F07E48").move_to([4.0, 1.5, 0])
        
        self.play(
            Write(abd_formula),
            Flash(AD_length_label, color="#F07E48"),
            Flash(BD_length_label, color="#F07E48"),
            run_time=(s9_end - s9_start)
        )
        current_time = s9_end

        # Sentence 10: 46.64s - 56.44s
        s10_start = 46.64
        s10_end = 56.44
        wait_duration = s10_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Calculate ABD area step by step
        abd_calculation = VGroup(
            MathTex(r"\text{Area}(\triangle ABD) = \frac{1}{2} \times 12 \times 24", font_size=22, color="#87C2A5"),
            MathTex(r"= 6 \times 24", font_size=22, color="#87C2A5"),
            MathTex(r"= 144 \text{ cm}^2", font_size=24, color="#87C2A5", weight=BOLD)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 0.0, 0])
        
        self.play(
            Write(abd_calculation[0]),
            run_time=3.0
        )
        self.play(
            Write(abd_calculation[1]),
            run_time=3.0
        )
        self.play(
            Write(abd_calculation[2]),
            run_time=(s10_end - s10_start - 6.0)
        )
        current_time = s10_end

        # Sentences 11-13: 56.45s - 67.63s (Summary)
        s11_start = 56.45
        s11_end = 67.63
        wait_duration = s11_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Clear previous calculations and show final summary
        self.play(
            FadeOut(intro_text),
            FadeOut(abd_formula),
            FadeOut(abd_calculation),
            run_time=1.0
        )
        
        # Final summary of all areas
        final_summary = VGroup(
            Text("Triangle Areas Summary:", font_size=26, color="#FFD700", weight=BOLD),
            MathTex(r"\text{Area}(\triangle ADE) = 54 \text{ cm}^2", font_size=24, color="#FFD700"),
            MathTex(r"\text{Area}(\triangle BCE) = 54 \text{ cm}^2", font_size=24, color="#58C4DD"),
            MathTex(r"\text{Area}(\triangle ABD) = 144 \text{ cm}^2", font_size=24, color="#F07E48")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.0, 1.0, 0])
        
        # Animate each line of the summary
        self.play(Write(final_summary[0]), run_time=1.5)
        self.play(
            Write(final_summary[1]),
            Flash(tri_ADE, color="#FFD700"),
            run_time=1.5
        )
        self.play(
            Write(final_summary[2]),
            Flash(tri_BCE, color="#58C4DD"),
            run_time=1.5
        )
        self.play(
            Write(final_summary[3]),
            Flash(tri_BAD, color="#F07E48"),
            run_time=(s11_end - s11_start - 4.5)
        )
        current_time = s11_end
        
        self.wait(2)