from manim import *
import numpy as np

class PartAApplyRhs(Scene):
    def construct(self):
        # 1. Scene Setup & Audio
        self.camera.background_color = "#1E293B"
        self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Scene/part_a_apply_rhs_scene.mp3")

        #################################################################
        # PART 1: INSTANT RECONSTRUCTION of PartAIdentifyGivens's final state
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
            Text("Goal:", font_size=28, color="#FFD700", weight=BOLD),
            MathTex(r"\triangle ABC \cong \triangle BAD", font_size=32, color="#58C4DD")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.0, -0.5, 0])
        
        given1_text = VGroup(
            Text("Given 1:", font_size=28, color="#FFD700", weight=BOLD),
            MathTex(r"\angle ACB = \angle ADB = 90°", font_size=28, color="#87C2A5")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 1.0, 0])
        
        explanation_text = VGroup(
            Text("Triangle ABC is right-angled at C", font_size=24, color="#58C4DD"),
            Text("Triangle BAD is right-angled at D", font_size=24, color="#F07E48")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -0.2, 0])
        
        given2_text = VGroup(
            Text("Given 2:", font_size=28, color="#FFD700", weight=BOLD),
            MathTex(r"AD = BC", font_size=28, color="#E2D28B")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -1.8, 0])
        
        common_side_text = VGroup(
            Text("Additionally:", font_size=28, color="#FFD700", weight=BOLD),
            MathTex(r"AB \text{ is common to both triangles}", font_size=24, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -3.2, 0])
        
        summary_text = VGroup(
            Text("Summary:", font_size=28, color="#FFD700", weight=BOLD),
            Text("• Two right angles", font_size=24, color="#87C2A5"),
            Text("• One pair of equal sides", font_size=24, color="#E2D28B"),
            Text("• Common hypotenuse", font_size=24, color="#FFD700")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([1.5, 2.0, 0])

        # Add all reconstructed mobjects instantly
        self.add(
            tri_ABC, tri_BAD, line_AC, line_BD,
            dot_A, dot_B, dot_C, dot_D, dot_E,
            label_A, label_B, label_C, label_D, label_E,
            angle_ACB, angle_ADB, goal_text, given1_text,
            explanation_text, given2_text, common_side_text, summary_text
        )

        #################################################################
        # PART 2: NEW ANIMATIONS for the current scene
        #################################################################
        current_time = 0

        # Sentence 1: 0.0s - 2.22s
        s1_start = 0.0
        s1_end = 2.22
        wait_duration = s1_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Fade out previous text and introduce RHS criterion
        intro_text = VGroup(
            Text("Applying RHS Congruence Criterion", font_size=28, color="#FFD700", weight=BOLD)
        ).move_to([4.0, 3.0, 0])
        
        self.play(
            FadeOut(summary_text),
            FadeOut(explanation_text),
            Write(intro_text),
            run_time=(s1_end - s1_start)
        )
        current_time = s1_end

        # Sentence 2: 2.23s - 11.61s
        s2_start = 2.23
        s2_end = 11.61
        wait_duration = s2_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        rhs_explanation = VGroup(
            Text("RHS Congruence Theorem:", font_size=26, color="#FFFFFF"),
            Text("If a right angle, hypotenuse, and", font_size=24, color="#FFFFFF"),
            Text("corresponding side are equal in both", font_size=24, color="#FFFFFF"),
            Text("triangles, then they are congruent.", font_size=24, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 1.5, 0])
        
        self.play(
            FadeOut(given1_text),
            FadeOut(given2_text),
            FadeOut(common_side_text),
            Write(rhs_explanation),
            run_time=(s2_end - s2_start)
        )
        current_time = s2_end

        # Sentence 3: 11.62s - 23.87s
        s3_start = 11.62
        s3_end = 23.87
        wait_duration = s3_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        condition1 = VGroup(
            Text("1. Right Angles:", font_size=26, color="#FFD700", weight=BOLD),
            MathTex(r"\angle ACB = \angle ADB = 90°", font_size=24, color="#87C2A5")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 0.5, 0])
        
        self.play(
            FadeOut(rhs_explanation),
            Write(condition1),
            Indicate(angle_ACB, color="#87C2A5", scale_factor=1.5),
            Indicate(angle_ADB, color="#87C2A5", scale_factor=1.5),
            run_time=(s3_end - s3_start)
        )
        current_time = s3_end

        # Sentence 4: 23.88s - 27.48s
        s4_start = 23.88
        s4_end = 27.48
        wait_duration = s4_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        condition2 = VGroup(
            Text("2. Common Hypotenuse:", font_size=26, color="#FFD700", weight=BOLD),
            MathTex(r"AB = BA", font_size=24, color="#FFD700")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -0.5, 0])
        
        # Highlight the common hypotenuse AB
        line_AB_highlight = Line(A, B, color="#FFD700", stroke_width=6)
        
        self.play(
            Write(condition2),
            Create(line_AB_highlight),
            run_time=(s4_end - s4_start)
        )
        current_time = s4_end

        # Sentence 5: 27.49s - 30.65s
        s5_start = 27.49
        s5_end = 30.65
        wait_duration = s5_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        condition3 = VGroup(
            Text("3. Corresponding Sides:", font_size=26, color="#FFD700", weight=BOLD),
            MathTex(r"BC = AD", font_size=24, color="#E2D28B")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -1.5, 0])
        
        # Highlight the equal sides BC and AD
        line_BC_highlight = Line(B, C, color="#E2D28B", stroke_width=5)
        line_AD_highlight = Line(A, D, color="#E2D28B", stroke_width=5)
        
        self.play(
            FadeOut(line_AB_highlight),
            Write(condition3),
            Create(line_BC_highlight),
            Create(line_AD_highlight),
            run_time=(s5_end - s5_start)
        )
        current_time = s5_end

        # Sentence 6: 30.66s - 36.59s
        s6_start = 30.66
        s6_end = 36.59
        wait_duration = s6_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        conclusion = VGroup(
            Text("Therefore, by RHS:", font_size=28, color="#FFD700", weight=BOLD),
            MathTex(r"\triangle ABC \cong \triangle BAD", font_size=32, color="#58C4DD")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.0, -2.8, 0])
        
        self.play(
            FadeOut(line_BC_highlight),
            FadeOut(line_AD_highlight),
            Write(conclusion),
            Flash(tri_ABC, color="#58C4DD"),
            Flash(tri_BAD, color="#F07E48"),
            run_time=(s6_end - s6_start)
        )
        current_time = s6_end

        # Sentence 7: 36.6s - 43.73s
        s7_start = 36.6
        s7_end = 43.73
        wait_duration = s7_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        final_statement = VGroup(
            Text("Proof Complete!", font_size=32, color="#FFD700", weight=BOLD),
            Text("Triangle ABC ≅ Triangle BAD", font_size=28, color="#58C4DD"),
            Text("by RHS Congruence Criterion", font_size=24, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=CENTER, buff=0.3).move_to([4.0, 2.5, 0])
        
        self.play(
            FadeOut(intro_text),
            FadeOut(condition1),
            FadeOut(condition2),
            FadeOut(condition3),
            Write(final_statement),
            Indicate(tri_ABC, color="#58C4DD", scale_factor=1.2),
            Indicate(tri_BAD, color="#F07E48", scale_factor=1.2),
            run_time=(s7_end - s7_start)
        )
        current_time = s7_end
        
        self.wait(2)