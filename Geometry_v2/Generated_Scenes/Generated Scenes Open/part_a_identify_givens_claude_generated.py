from manim import *
import numpy as np

class PartAIdentifyGivens(Scene):
    def construct(self):
        # 1. Scene Setup & Audio
        self.camera.background_color = "#1E293B"
        self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Scene/part_a_identify_givens_scene.mp3")

        #################################################################
        # PART 1: INSTANT RECONSTRUCTION of PartAUnderstandGoal's final state
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
        
        narration4 = VGroup(
            Text("Our objective is to demonstrate", font_size=26, color="#FFFFFF"),
            Text("the congruence of the two triangles.", font_size=26, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT).move_to([4.0, -2.5, 0])

        # Add all reconstructed mobjects instantly
        self.add(
            tri_ABC, tri_BAD, line_AC, line_BD,
            dot_A, dot_B, dot_C, dot_D, dot_E,
            label_A, label_B, label_C, label_D, label_E,
            angle_ACB, angle_ADB, goal_text, narration4
        )

        #################################################################
        # PART 2: NEW ANIMATIONS for the current scene
        #################################################################
        current_time = 0

        # Sentence 1: 0.0s - 5.62s
        s1_start = 0.0
        s1_end = 5.62
        wait_duration = s1_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Fade out previous narration and introduce new content
        intro_text = VGroup(
            Text("Next, let's list the information given", font_size=26, color="#FFFFFF"),
            Text("in the problem and from the diagram", font_size=26, color="#FFFFFF"),
            Text("that will help us prove congruence.", font_size=26, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT).move_to([4.0, 2.5, 0])
        
        self.play(
            FadeOut(narration4),
            Write(intro_text),
            run_time=(s1_end - s1_start)
        )
        current_time = s1_end

        # Sentence 2: 5.63s - 11.25s
        s2_start = 5.63
        s2_end = 11.25
        wait_duration = s2_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        given1_text = VGroup(
            Text("Given 1:", font_size=28, color="#FFD700", weight=BOLD),
            MathTex(r"\angle ACB = \angle ADB = 90°", font_size=28, color="#87C2A5")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 1.0, 0])
        
        self.play(
            Write(given1_text),
            Indicate(angle_ACB, color="#87C2A5"),
            Indicate(angle_ADB, color="#87C2A5"),
            run_time=(s2_end - s2_start)
        )
        current_time = s2_end

        # Sentence 3: 11.26s - 18.13s
        s3_start = 11.26
        s3_end = 18.13
        wait_duration = s3_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        explanation_text = VGroup(
            Text("Triangle ABC is right-angled at C", font_size=24, color="#58C4DD"),
            Text("Triangle BAD is right-angled at D", font_size=24, color="#F07E48")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -0.2, 0])
        
        self.play(
            Write(explanation_text),
            Flash(tri_ABC, color="#58C4DD"),
            Flash(tri_BAD, color="#F07E48"),
            run_time=(s3_end - s3_start)
        )
        current_time = s3_end

        # Sentence 4: 18.14s - 20.49s
        s4_start = 18.14
        s4_end = 20.49
        wait_duration = s4_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        given2_text = VGroup(
            Text("Given 2:", font_size=28, color="#FFD700", weight=BOLD),
            MathTex(r"AD = BC", font_size=28, color="#E2D28B")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -1.8, 0])
        
        # Create temporary lines to highlight AD and BC
        line_AD = Line(A, D, color="#E2D28B", stroke_width=4)
        line_BC = Line(B, C, color="#E2D28B", stroke_width=4)
        
        self.play(
            Write(given2_text),
            Create(line_AD),
            Create(line_BC),
            run_time=(s4_end - s4_start)
        )
        current_time = s4_end

        # Sentence 5: 20.5s - 24.81s
        s5_start = 20.5
        s5_end = 24.81
        wait_duration = s5_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        common_side_text = VGroup(
            Text("Additionally:", font_size=28, color="#FFD700", weight=BOLD),
            MathTex(r"AB \text{ is common to both triangles}", font_size=24, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -3.2, 0])
        
        # Highlight the common side AB
        line_AB_highlight = Line(A, B, color="#FFD700", stroke_width=6)
        
        self.play(
            FadeOut(line_AD),
            FadeOut(line_BC),
            Write(common_side_text),
            Create(line_AB_highlight),
            run_time=(s5_end - s5_start)
        )
        current_time = s5_end

        # Sentence 6: 24.82s - 29.6s
        s6_start = 24.82
        s6_end = 29.6
        wait_duration = s6_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        summary_text = VGroup(
            Text("Summary:", font_size=28, color="#FFD700", weight=BOLD),
            Text("• Two right angles", font_size=24, color="#87C2A5"),
            Text("• One pair of equal sides", font_size=24, color="#E2D28B"),
            Text("• Common hypotenuse", font_size=24, color="#FFD700")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([1.5, 2.0, 0])
        
        self.play(
            FadeOut(line_AB_highlight),
            Write(summary_text),
            Flash(angle_ACB, color="#87C2A5"),
            Flash(angle_ADB, color="#87C2A5"),
            run_time=(s6_end - s6_start)
        )
        current_time = s6_end
        
        self.wait(2)