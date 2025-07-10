from manim import *
import numpy as np

class PartBUnderstandGoalAndGivens(Scene):
    def construct(self):
        # 1. Scene Setup & Audio
        self.camera.background_color = "#1E293B"
        self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Scene/part_b_understand_goal_and_givens_scene.mp3")

        #################################################################
        # PART 1: INSTANT RECONSTRUCTION of PartAApplyRhs's final state
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
        goal_text = VGroup(
            MathTex(r"\triangle ABC \cong \triangle BAD", font_size=32, color="#58C4DD")
        ).move_to([4.0, -0.5, 0])
        
        final_statement = VGroup(
            Text("Proof Complete!", font_size=32, color="#FFD700", weight=BOLD),
            Text("Triangle ABC ≅ Triangle BAD", font_size=28, color="#58C4DD"),
            Text("by RHS Congruence Criterion", font_size=24, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=CENTER, buff=0.3).move_to([4.0, 2.5, 0])
        
        conclusion = VGroup(
            Text("Therefore, by RHS:", font_size=28, color="#FFD700", weight=BOLD),
            MathTex(r"\triangle ABC \cong \triangle BAD", font_size=32, color="#58C4DD")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.0, -2.8, 0])

        # Add all reconstructed mobjects instantly
        self.add(
            tri_ABC, tri_BAD, line_AC, line_BD,
            dot_A, dot_B, dot_C, dot_D, dot_E,
            label_A, label_B, label_C, label_D, label_E,
            angle_ACB, angle_ADB, goal_text, final_statement, conclusion
        )

        #################################################################
        # PART 2: NEW ANIMATIONS for the current scene
        #################################################################
        current_time = 0

        # Sentence 1: 0.0s - 4.6s
        s1_start = 0.0
        s1_end = 4.6
        wait_duration = s1_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Fade out previous text and introduce Part B
        part_b_intro = VGroup(
            Text("Part B", font_size=36, color="#FFD700", weight=BOLD),
            Text("Find the area of pentagon ABCED", font_size=28, color="#58C4DD")
        ).arrange(DOWN, aligned_edge=CENTER, buff=0.3).move_to([4.0, 3.0, 0])
        
        # Highlight the pentagon ABCED
        pentagon_ABCED = Polygon(A, B, C, E, D, color="#E2D28B", fill_opacity=0.2, stroke_width=4)
        
        self.play(
            FadeOut(final_statement),
            FadeOut(conclusion),
            FadeOut(goal_text),
            Write(part_b_intro),
            Create(pentagon_ABCED),
            run_time=(s1_end - s1_start)
        )
        current_time = s1_end

        # Sentence 2: 4.61s - 11.32s
        s2_start = 4.61
        s2_end = 11.32
        wait_duration = s2_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        given_lengths = VGroup(
            Text("Given Lengths:", font_size=28, color="#FFD700", weight=BOLD),
            MathTex(r"AD = 12 \text{ cm}", font_size=26, color="#E2D28B"),
            MathTex(r"DE = 9 \text{ cm}", font_size=26, color="#E2D28B")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.0, 1.5, 0])
        
        # Highlight AD and DE segments
        line_AD_highlight = Line(A, D, color="#E2D28B", stroke_width=6)
        line_DE_highlight = Line(D, E, color="#E2D28B", stroke_width=6)
        
        # Add length labels
        AD_length_label = MathTex("12 \text{ cm}", font_size=24, color="#E2D28B").next_to(
            (A + D) / 2, LEFT, buff=0.2
        )
        DE_length_label = MathTex("9 \text{ cm}", font_size=24, color="#E2D28B").next_to(
            (D + E) / 2, UP, buff=0.2
        )
        
        self.play(
            Write(given_lengths),
            Create(line_AD_highlight),
            Create(line_DE_highlight),
            Write(AD_length_label),
            Write(DE_length_label),
            run_time=(s2_end - s2_start)
        )
        current_time = s2_end

        # Sentence 3: 11.33s - 13.32s
        s3_start = 11.33
        s3_end = 13.32
        wait_duration = s3_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        goal_statement = VGroup(
            Text("Goal:", font_size=28, color="#FFD700", weight=BOLD),
            MathTex(r"\text{Find Area}(ABCED)", font_size=26, color="#58C4DD")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 0.0, 0])
        
        self.play(
            FadeOut(line_AD_highlight),
            FadeOut(line_DE_highlight),
            Write(goal_statement),
            Indicate(pentagon_ABCED, color="#58C4DD", scale_factor=1.1),
            run_time=(s3_end - s3_start)
        )
        current_time = s3_end

        # Sentence 4: 13.33s - 17.82s
        s4_start = 13.33
        s4_end = 17.82
        wait_duration = s4_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        given_summary = VGroup(
            Text("Given:", font_size=28, color="#FFD700", weight=BOLD),
            MathTex(r"AD = 12 \text{ cm}", font_size=24, color="#E2D28B"),
            MathTex(r"DE = 9 \text{ cm}", font_size=24, color="#E2D28B")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -1.5, 0])
        
        self.play(
            FadeOut(given_lengths),
            Write(given_summary),
            Flash(AD_length_label, color="#E2D28B"),
            Flash(DE_length_label, color="#E2D28B"),
            run_time=(s4_end - s4_start)
        )
        current_time = s4_end

        # Sentence 5: 17.83s - 22.14s
        s5_start = 17.83
        s5_end = 22.14
        wait_duration = s5_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        objective_text = VGroup(
            Text("Objective:", font_size=28, color="#FFD700", weight=BOLD),
            Text("Calculate the area of the pentagon", font_size=24, color="#FFFFFF"),
            Text("using the given side lengths", font_size=24, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -3.0, 0])
        
        self.play(
            Write(objective_text),
            Indicate(pentagon_ABCED, color="#E2D28B", scale_factor=1.05),
            run_time=(s5_end - s5_start)
        )
        current_time = s5_end
        
        self.wait(2)