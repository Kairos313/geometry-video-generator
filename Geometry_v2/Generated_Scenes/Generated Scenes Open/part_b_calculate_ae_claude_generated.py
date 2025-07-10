from manim import *
import numpy as np

class PartBCalculateAe(Scene):
    def construct(self):
        # 1. Scene Setup & Audio
        self.camera.background_color = "#1E293B"
        self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Scene/part_b_calculate_ae_scene.mp3")

        #################################################################
        # PART 1: INSTANT RECONSTRUCTION of PartBUnderstandGoalAndGivens's final state
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
        
        # Previous scene's final text elements
        part_b_intro = VGroup(
            Text("Part B", font_size=36, color="#FFD700", weight=BOLD),
            Text("Find the area of pentagon ABCED", font_size=28, color="#58C4DD")
        ).arrange(DOWN, aligned_edge=CENTER, buff=0.3).move_to([4.0, 3.0, 0])
        
        goal_statement = VGroup(
            Text("Goal:", font_size=28, color="#FFD700", weight=BOLD),
            MathTex(r"\text{Find Area}(ABCED)", font_size=26, color="#58C4DD")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 0.0, 0])
        
        given_summary = VGroup(
            Text("Given:", font_size=28, color="#FFD700", weight=BOLD),
            MathTex(r"AD = 12 \text{ cm}", font_size=24, color="#E2D28B"),
            MathTex(r"DE = 9 \text{ cm}", font_size=24, color="#E2D28B")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -1.5, 0])
        
        objective_text = VGroup(
            Text("Objective:", font_size=28, color="#FFD700", weight=BOLD),
            Text("Calculate the area of the pentagon", font_size=24, color="#FFFFFF"),
            Text("using the given side lengths", font_size=24, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -3.0, 0])
        
        # Add length labels from previous scene
        AD_length_label = MathTex("12 \text{ cm}", font_size=24, color="#E2D28B").next_to(
            (A + D) / 2, LEFT, buff=0.2
        )
        DE_length_label = MathTex("9 \text{ cm}", font_size=24, color="#E2D28B").next_to(
            (D + E) / 2, UP, buff=0.2
        )

        # Add all reconstructed mobjects instantly
        self.add(
            tri_ABC, tri_BAD, pentagon_ABCED, line_AC, line_BD,
            dot_A, dot_B, dot_C, dot_D, dot_E,
            label_A, label_B, label_C, label_D, label_E,
            angle_ACB, angle_ADB, part_b_intro, goal_statement,
            given_summary, objective_text, AD_length_label, DE_length_label
        )

        #################################################################
        # PART 2: NEW ANIMATIONS for the current scene
        #################################################################
        current_time = 0

        # Sentence 1: 0.0s - 2.35s
        s1_start = 0.0
        s1_end = 2.35
        wait_duration = s1_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Focus on triangle ADE
        tri_ADE = Polygon(A, D, E, color="#FFD700", fill_opacity=0.4, stroke_width=4)
        
        self.play(
            FadeOut(part_b_intro),
            FadeOut(goal_statement),
            FadeOut(given_summary),
            FadeOut(objective_text),
            Create(tri_ADE),
            Indicate(tri_ADE, color="#FFD700", scale_factor=1.1),
            run_time=(s1_end - s1_start)
        )
        current_time = s1_end

        # Sentence 2: 2.36s - 8.63s
        s2_start = 2.36
        s2_end = 8.63
        wait_duration = s2_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Highlight angle ADE as 90 degrees
        angle_ADE = RightAngle(Line(D, A), Line(D, E), length=0.3, color="#FFD700")
        
        angle_explanation = VGroup(
            Text("From Part A:", font_size=28, color="#FFD700", weight=BOLD),
            MathTex(r"\angle ADB = 90°", font_size=26, color="#87C2A5"),
            MathTex(r"\therefore \angle ADE = 90°", font_size=26, color="#FFD700")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 2.5, 0])
        
        self.play(
            Create(angle_ADE),
            Write(angle_explanation),
            Flash(angle_ADB, color="#87C2A5"),
            run_time=(s2_end - s2_start)
        )
        current_time = s2_end

        # Sentence 3: 8.64s - 11.64s
        s3_start = 8.64
        s3_end = 11.64
        wait_duration = s3_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        right_triangle_text = VGroup(
            Text("Triangle ADE is", font_size=26, color="#FFFFFF"),
            Text("a right-angled triangle", font_size=26, color="#FFD700", weight=BOLD)
        ).arrange(DOWN, aligned_edge=CENTER, buff=0.2).move_to([4.0, 1.0, 0])
        
        self.play(
            Write(right_triangle_text),
            Indicate(tri_ADE, color="#FFD700", scale_factor=1.05),
            run_time=(s3_end - s3_start)
        )
        current_time = s3_end

        # Sentence 4: 11.65s - 19.54s
        s4_start = 11.65
        s4_end = 19.54
        wait_duration = s4_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        pythagorean_theorem = VGroup(
            Text("Pythagorean Theorem:", font_size=26, color="#FFD700", weight=BOLD),
            MathTex(r"AE^2 = AD^2 + DE^2", font_size=28, color="#58C4DD")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.0, -0.5, 0])
        
        # Highlight the hypotenuse AE
        line_AE = Line(A, E, color="#58C4DD", stroke_width=6)
        
        self.play(
            FadeOut(angle_explanation),
            FadeOut(right_triangle_text),
            Write(pythagorean_theorem),
            Create(line_AE),
            run_time=(s4_end - s4_start)
        )
        current_time = s4_end

        # Sentence 5: 19.55s - 22.37s
        s5_start = 19.55
        s5_end = 22.37
        wait_duration = s5_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        substitution = MathTex(r"AE^2 = 12^2 + 9^2", font_size=28, color="#E2D28B").next_to(
            pythagorean_theorem, DOWN, buff=0.4
        )
        
        self.play(
            Write(substitution),
            Flash(AD_length_label, color="#E2D28B"),
            Flash(DE_length_label, color="#E2D28B"),
            run_time=(s5_end - s5_start)
        )
        current_time = s5_end

        # Sentence 6: 22.38s - 25.49s
        s6_start = 22.38
        s6_end = 25.49
        wait_duration = s6_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        calculation1 = MathTex(r"AE^2 = 144 + 81", font_size=28, color="#E2D28B").next_to(
            substitution, DOWN, buff=0.3
        )
        
        self.play(
            Write(calculation1),
            run_time=(s6_end - s6_start)
        )
        current_time = s6_end

        # Sentence 7: 25.5s - 27.9s
        s7_start = 25.5
        s7_end = 27.9
        wait_duration = s7_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        calculation2 = MathTex(r"AE^2 = 225", font_size=28, color="#E2D28B").next_to(
            calculation1, DOWN, buff=0.3
        )
        
        self.play(
            Write(calculation2),
            run_time=(s7_end - s7_start)
        )
        current_time = s7_end

        # Sentence 8: 27.91s - 32.64s
        s8_start = 27.91
        s8_end = 32.64
        wait_duration = s8_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        final_calculation = MathTex(r"AE = \sqrt{225} = 15 \text{ cm}", font_size=28, color="#FFD700").next_to(
            calculation2, DOWN, buff=0.3
        )
        
        # Add AE length label to the diagram
        AE_length_label = MathTex("15 \text{ cm}", font_size=24, color="#FFD700").next_to(
            (A + E) / 2, DOWN + LEFT, buff=0.2
        )
        
        self.play(
            Write(final_calculation),
            Write(AE_length_label),
            FadeOut(line_AE),
            run_time=(s8_end - s8_start)
        )
        current_time = s8_end

        # Sentence 9: 32.65s - 35.24s
        s9_start = 32.65
        s9_end = 35.24
        wait_duration = s9_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        conclusion = VGroup(
            Text("Result:", font_size=28, color="#FFD700", weight=BOLD),
            MathTex(r"AE = 15 \text{ cm}", font_size=32, color="#FFD700")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -3.5, 0])
        
        self.play(
            Write(conclusion),
            Indicate(AE_length_label, color="#FFD700", scale_factor=1.2),
            run_time=(s9_end - s9_start)
        )
        current_time = s9_end
        
        self.wait(2)