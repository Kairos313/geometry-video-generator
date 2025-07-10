from manim import *
import numpy as np

class PartBConfirmRightAngleBce(Scene):
    def construct(self):
        # 1. Scene Setup & Audio
        self.camera.background_color = "#1E293B"
        self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Scene/part_b_confirm_right_angle_bce_scene.mp3")

        #################################################################
        # PART 1: INSTANT RECONSTRUCTION of PartBCalculateCe's final state
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
        final_ce_result = VGroup(
            Text("Result:", font_size=26, color="#FFD700", weight=BOLD),
            MathTex(r"CE = 9 \text{ cm}", font_size=28, color="#FFD700")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -1.5, 0])
        
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

        # Add all reconstructed mobjects instantly
        self.add(
            tri_ABC, tri_BAD, pentagon_ABCED, tri_ADE, tri_AEB, line_AC, line_BD,
            dot_A, dot_B, dot_C, dot_D, dot_E,
            label_A, label_B, label_C, label_D, label_E,
            angle_ACB, angle_ADB, angle_ADE, angle_CAB, angle_DBA,
            final_ce_result,
            AD_length_label, DE_length_label, AE_length_label, BE_length_label,
            BD_length_label, AC_length_label, EC_length_label
        )

        #################################################################
        # PART 2: NEW ANIMATIONS for the current scene
        #################################################################
        current_time = 0

        # Sentence 1: 0.0s - 1.91s
        s1_start = 0.0
        s1_end = 1.91
        wait_duration = s1_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Introduce triangle BCE focus
        tri_BCE = Polygon(B, C, E, color="#58C4DD", fill_opacity=0.5, stroke_width=5)
        
        self.play(
            FadeOut(final_ce_result),
            Create(tri_BCE),
            Indicate(dot_B, color="#58C4DD", scale_factor=1.3),
            Indicate(dot_C, color="#58C4DD", scale_factor=1.3),
            Indicate(dot_E, color="#58C4DD", scale_factor=1.3),
            run_time=(s1_end - s1_start)
        )
        current_time = s1_end

        # Sentence 2: 1.92s - 9.68s
        s2_start = 1.92
        s2_end = 9.68
        wait_duration = s2_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Show side lengths of triangle BCE
        bce_intro = VGroup(
            Text("Triangle BCE side lengths:", font_size=24, color="#58C4DD", weight=BOLD),
            MathTex(r"BC = 12 \text{ cm}", font_size=22, color="#87C2A5"),
            MathTex(r"CE = 9 \text{ cm}", font_size=22, color="#87C2A5"),
            MathTex(r"BE = 15 \text{ cm}", font_size=22, color="#87C2A5")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 2.0, 0])
        
        # Add BC length label
        BC_length_label = MathTex("12 \text{ cm}", font_size=24, color="#58C4DD").next_to(
            (B + C) / 2, DOWN, buff=0.2
        )
        
        self.play(
            Write(bce_intro),
            Write(BC_length_label),
            Flash(BC_length_label, color="#58C4DD"),
            Flash(EC_length_label, color="#58C4DD"),
            Flash(BE_length_label, color="#58C4DD"),
            run_time=(s2_end - s2_start)
        )
        current_time = s2_end

        # Sentence 3: 9.69s - 15.12s
        s3_start = 9.69
        s3_end = 15.12
        wait_duration = s3_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Identify as 3-4-5 multiple
        triangle_type = VGroup(
            Text("This is a 9-12-15 triangle", font_size=24, color="#E2D28B"),
            Text("(3 × 3-4-5 right triangle)", font_size=22, color="#E2D28B")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 0.5, 0])
        
        self.play(
            Write(triangle_type),
            Indicate(tri_BCE, color="#E2D28B", scale_factor=1.05),
            run_time=(s3_end - s3_start)
        )
        current_time = s3_end

        # Sentence 4: 15.13s - 20.33s
        s4_start = 15.13
        s4_end = 20.33
        wait_duration = s4_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Introduce Pythagorean theorem verification
        pythag_intro = VGroup(
            Text("Verify using Pythagorean theorem:", font_size=24, color="#FFD700", weight=BOLD),
            Text("Converse: If a² + b² = c², then ∠C = 90°", font_size=20, color="#FFD700")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -0.5, 0])
        
        self.play(
            Write(pythag_intro),
            run_time=(s4_end - s4_start)
        )
        current_time = s4_end

        # Sentence 5: 20.34s - 23.71s
        s5_start = 20.34
        s5_end = 23.71
        wait_duration = s5_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Show the equation to check
        pythag_equation = MathTex(r"CE^2 + BC^2 = BE^2 \text{ ?}", font_size=26, color="#FFD700").move_to([4.0, -1.5, 0])
        
        self.play(
            Write(pythag_equation),
            run_time=(s5_end - s5_start)
        )
        current_time = s5_end

        # Sentence 6: 23.72s - 30.3s
        s6_start = 23.72
        s6_end = 30.3
        wait_duration = s6_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Calculate left side
        left_calculation = VGroup(
            MathTex(r"9^2 + 12^2", font_size=24, color="#87C2A5"),
            MathTex(r"= 81 + 144", font_size=24, color="#87C2A5"),
            MathTex(r"= 225", font_size=24, color="#87C2A5")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -2.5, 0])
        
        self.play(
            Write(left_calculation[0]),
            run_time=1.5
        )
        self.play(
            Write(left_calculation[1]),
            run_time=2.0
        )
        self.play(
            Write(left_calculation[2]),
            run_time=(s6_end - s6_start - 3.5)
        )
        current_time = s6_end

        # Sentence 7: 30.31s - 34.07s
        s7_start = 30.31
        s7_end = 34.07
        wait_duration = s7_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Calculate right side
        right_calculation = MathTex(r"BE^2 = 15^2 = 225", font_size=24, color="#87C2A5").move_to([4.0, -3.5, 0])
        
        self.play(
            Write(right_calculation),
            run_time=(s7_end - s7_start)
        )
        current_time = s7_end

        # Sentence 8: 34.08s - 40.06s
        s8_start = 34.08
        s8_end = 40.06
        wait_duration = s8_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Show conclusion
        conclusion = VGroup(
            MathTex(r"CE^2 + BC^2 = BE^2", font_size=26, color="#FFD700"),
            MathTex(r"\therefore \angle BCE = 90°", font_size=26, color="#FFD700")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 1.5, 0])
        
        # Add right angle marker at C for triangle BCE
        angle_BCE = RightAngle(Line(C, B), Line(C, E), length=0.3, color="#58C4DD")
        
        self.play(
            FadeOut(bce_intro),
            FadeOut(triangle_type),
            FadeOut(pythag_intro),
            FadeOut(pythag_equation),
            FadeOut(left_calculation),
            FadeOut(right_calculation),
            Write(conclusion),
            Create(angle_BCE),
            run_time=(s8_end - s8_start)
        )
        current_time = s8_end

        # Sentence 9: 40.07s - 43.31s
        s9_start = 40.07
        s9_end = 43.31
        wait_duration = s9_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Final confirmation
        final_result = VGroup(
            Text("Triangle BCE is right-angled at C", font_size=24, color="#58C4DD", weight=BOLD),
            MathTex(r"\angle BCE = 90°", font_size=26, color="#58C4DD")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 0.0, 0])
        
        self.play(
            Write(final_result),
            Flash(angle_BCE, color="#58C4DD"),
            Indicate(tri_BCE, color="#58C4DD", scale_factor=1.1),
            Flash(dot_C, color="#58C4DD"),
            run_time=(s9_end - s9_start)
        )
        current_time = s9_end
        
        self.wait(2)