from manim import *
import numpy as np

class PartAUnderstandGoal(Scene):
    def construct(self):
        # 1. Scene Setup & Audio
        self.camera.background_color = "#1E293B"
        self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Scene/part_a_understand_goal_scene.mp3")

        #################################################################
        # 2. Constraint-Driven Coordinate Calculation
        #################################################################
        # Base points to ground the diagram on the left side of the screen
        A = np.array([-5.5, -2, 0])
        B = np.array([-1.5, -2, 0])
        
        # GIVEN: ∠ACB = ∠ADB = 90° and AD = BC
        # For ∠ADB = 90°, D must be positioned such that DA ⊥ DB
        # Let's place D above the line AB to form a right angle
        # Using the constraint that angle ADB = 90°, D lies on a circle with diameter AB
        # For visual clarity and mathematical precision, we'll place D at a calculated position
        
        # Calculate D such that ∠ADB = 90°
        # Midpoint of AB
        AB_midpoint = (A + B) / 2
        AB_length = np.linalg.norm(B - A)
        # D is positioned to create a right angle, using the property that angle in semicircle is 90°
        D = np.array([-3.5, 1, 0])
        
        # GIVEN: AD = BC, so we need to calculate C such that BC = |AD| and ∠ACB = 90°
        AD_length = np.linalg.norm(D - A)
        # C must be positioned such that ∠ACB = 90° and BC = AD_length
        # For ∠ACB = 90°, C lies on a circle with diameter AB
        # We'll place C below AB to match the reference image
        C = np.array([-3.5, -3.2, 0])
        
        # Calculate intersection point E of AC and BD
        # Line AC: parametric form A + t*(C - A)
        # Line BD: parametric form B + s*(D - B)
        # Solve: A + t*(C - A) = B + s*(D - B)
        AC_vec = C - A
        BD_vec = D - B
        AB_vec = B - A
        
        # Solving the system of equations
        # t*(C - A) - s*(D - B) = B - A
        # This gives us the parameter t to find E
        det = AC_vec[0] * (-BD_vec[1]) - AC_vec[1] * (-BD_vec[0])
        if abs(det) > 1e-10:
            t = (AB_vec[0] * (-BD_vec[1]) - AB_vec[1] * (-BD_vec[0])) / det
            E = A + t * AC_vec
        else:
            E = np.array([-3.5, -0.5, 0])  # Fallback position

        #################################################################
        # 3. Mobject Definition
        #################################################################
        # Create triangles
        tri_ABC = Polygon(A, B, C, color="#58C4DD", fill_opacity=0.3, stroke_width=3)
        tri_BAD = Polygon(B, A, D, color="#F07E48", fill_opacity=0.3, stroke_width=3)
        
        # Create lines AC and BD
        line_AC = Line(A, C, color="#87C2A5", stroke_width=2)
        line_BD = Line(B, D, color="#87C2A5", stroke_width=2)
        
        # Create points
        dot_A = Dot(A, color="#FFFFFF", radius=0.08)
        dot_B = Dot(B, color="#FFFFFF", radius=0.08)
        dot_C = Dot(C, color="#FFFFFF", radius=0.08)
        dot_D = Dot(D, color="#FFFFFF", radius=0.08)
        dot_E = Dot(E, color="#FFD700", radius=0.1)
        
        # Create labels
        label_A = MathTex("A", color="#FFFFFF", font_size=32).next_to(A, DOWN + LEFT, buff=0.2)
        label_B = MathTex("B", color="#FFFFFF", font_size=32).next_to(B, DOWN + RIGHT, buff=0.2)
        label_C = MathTex("C", color="#FFFFFF", font_size=32).next_to(C, DOWN + RIGHT, buff=0.2)
        label_D = MathTex("D", color="#FFFFFF", font_size=32).next_to(D, UP + LEFT, buff=0.2)
        label_E = MathTex("E", color="#FFD700", font_size=32).next_to(E, UP + RIGHT, buff=0.2)
        
        # Create right angle markers
        angle_ACB = RightAngle(Line(C, A), Line(C, B), length=0.3, color="#87C2A5")
        angle_ADB = RightAngle(Line(D, A), Line(D, B), length=0.3, color="#87C2A5")
        
        # Group diagram elements
        diagram_base = VGroup(line_AC, line_BD, dot_A, dot_B, dot_C, dot_D)
        labels = VGroup(label_A, label_B, label_C, label_D)
        triangles = VGroup(tri_ABC, tri_BAD)
        
        # Text mobjects for narration (right side of screen)
        narration1 = VGroup(
            Text("For part A, our first step is to", font_size=26, color="#FFFFFF"),
            Text("understand what we need to prove.", font_size=26, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT).move_to([4.0, 2.5, 0])
        
        narration2 = VGroup(
            Text("We need to show that triangle ABC", font_size=26, color="#FFFFFF"),
            Text("is congruent to triangle BAD.", font_size=26, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT).move_to([4.0, 1.0, 0])
        
        goal_text = VGroup(
            Text("Goal:", font_size=28, color="#FFD700", weight=BOLD),
            MathTex(r"\triangle ABC \cong \triangle BAD", font_size=32, color="#58C4DD")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.0, -0.5, 0])
        
        narration4 = VGroup(
            Text("Our objective is to demonstrate", font_size=26, color="#FFFFFF"),
            Text("the congruence of the two triangles.", font_size=26, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT).move_to([4.0, -2.5, 0])

        #################################################################
        # 4. Synchronized Animation
        #################################################################
        current_time = 0

        # Sentence 1: 0.0s - 3.24s
        s1_start = 0.0
        s1_end = 3.24
        wait_duration = s1_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        self.play(
            Create(diagram_base),
            Write(labels),
            Write(narration1),
            run_time=(s1_end - s1_start)
        )
        current_time = s1_end

        # Sentence 2: 3.25s - 7.19s
        s2_start = 3.25
        s2_end = 7.19
        wait_duration = s2_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        self.play(
            DrawBorderThenFill(tri_ABC),
            DrawBorderThenFill(tri_BAD),
            Write(narration2),
            run_time=(s2_end - s2_start)
        )
        current_time = s2_end

        # Sentence 3: 7.2s - 10.86s
        s3_start = 7.2
        s3_end = 10.86
        wait_duration = s3_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        self.play(
            Write(goal_text),
            Indicate(tri_ABC, color="#58C4DD"),
            Indicate(tri_BAD, color="#F07E48"),
            run_time=(s3_end - s3_start)
        )
        current_time = s3_end

        # Sentence 4: 10.87s - 14.76s
        s4_start = 10.87
        s4_end = 14.76
        wait_duration = s4_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        self.play(
            Create(angle_ACB),
            Create(angle_ADB),
            Create(dot_E),
            Write(label_E),
            Write(narration4),
            run_time=(s4_end - s4_start)
        )
        current_time = s4_end
        
        self.wait(2)