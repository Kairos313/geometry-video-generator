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
        # PRINCIPLE: Establish a Base.
        A = np.array([-5.5, -2.5, 0])
        B = np.array([-1.5, -2.5, 0])
        
        # PRINCIPLE: Right Angles. Given ∠ACB = ∠ADB = 90°
        # For construction, place C and D such that they form right angles
        # and satisfy AD = BC constraint
        
        # Place C above and to the right to form right angle at C
        C = np.array([-1.5, 0.5, 0])
        
        # Place D above and to the left to form right angle at D
        # Ensuring AD = BC constraint is satisfied
        BC_length = np.linalg.norm(C - B)
        # D should be positioned so AD has the same length as BC
        D_direction = np.array([0, 1, 0])  # Direction from A upward
        D = A + BC_length * D_direction
        D = np.array([-5.5, 0.5, 0])  # Adjust for proper positioning
        
        # PRINCIPLE: Intersections. E is the intersection of AC and BD.
        AC_vec = C - A
        BD_vec = D - B
        matrix = np.array([[AC_vec[0], -BD_vec[0]], [AC_vec[1], -BD_vec[1]]])
        b_vector = B - A
        try:
            params = np.linalg.solve(matrix, b_vector[:2])
            t = params[0]
            E = A + t * AC_vec
        except np.linalg.LinAlgError:
            E = np.array([-3.5, -1, 0])  # Fallback position

        #################################################################
        # 3. Mobject Definition (Strict Positioning)
        #################################################################
        # Create the triangles
        tri_ABC = Polygon(A, B, C, color="#58C4DD", fill_opacity=0.3, stroke_width=3)
        tri_BAD = Polygon(B, A, D, color="#F07E48", fill_opacity=0.3, stroke_width=3)
        
        # Create lines AC and BD
        line_AC = Line(A, C, color="#87C2A5", stroke_width=2)
        line_BD = Line(B, D, color="#87C2A5", stroke_width=2)
        
        # Labels positioned using manual vector addition
        label_A = MathTex("A", color="#FFFFFF", font_size=36).move_to(A + np.array([-0.3, -0.4, 0]))
        label_B = MathTex("B", color="#FFFFFF", font_size=36).move_to(B + np.array([0.3, -0.4, 0]))
        label_C = MathTex("C", color="#FFFFFF", font_size=36).move_to(C + np.array([0.3, 0.3, 0]))
        label_D = MathTex("D", color="#FFFFFF", font_size=36).move_to(D + np.array([-0.3, 0.3, 0]))
        label_E = MathTex("E", color="#FFD700", font_size=32).move_to(E + np.array([0.3, 0.3, 0]))
        
        labels = VGroup(label_A, label_B, label_C, label_D, label_E)
        
        # Create dots for vertices
        dot_A = Dot(A, color="#FFFFFF", radius=0.08)
        dot_B = Dot(B, color="#FFFFFF", radius=0.08)
        dot_C = Dot(C, color="#FFFFFF", radius=0.08)
        dot_D = Dot(D, color="#FFFFFF", radius=0.08)
        dot_E = Dot(E, color="#FFD700", radius=0.08)
        
        dots = VGroup(dot_A, dot_B, dot_C, dot_D, dot_E)
        
        # Right angle markers
        angle_C = RightAngle(Line(C, A), Line(C, B), length=0.3, color="#87C2A5")
        angle_D = RightAngle(Line(D, B), Line(D, A), length=0.3, color="#87C2A5")
        
        # Group the main diagram
        diagram = VGroup(tri_ABC, tri_BAD, line_AC, line_BD, dots, labels, angle_C, angle_D)
        
        # Text mobjects for narration - positioned in right half of screen
        narration1 = VGroup(
            Text("For part A, our first step is to", font_size=28, color="#FFFFFF"),
            Text("understand what we need to prove.", font_size=28, color="#FFFFFF")
        ).arrange(np.array([0, -0.6, 0]), aligned_edge=np.array([-1, 0, 0])).move_to(np.array([3.5, 2.5, 0]))
        
        narration2 = VGroup(
            Text("We need to show that triangle ABC", font_size=28, color="#FFFFFF"),
            Text("is congruent to triangle BAD.", font_size=28, color="#FFFFFF")
        ).arrange(np.array([0, -0.6, 0]), aligned_edge=np.array([-1, 0, 0])).move_to(np.array([3.5, 1.0, 0]))
        
        goal_statement = VGroup(
            Text("Goal:", font_size=32, color="#FFD700"),
            MathTex(r"\triangle ABC \cong \triangle BAD", font_size=36, color="#58C4DD")
        ).arrange(np.array([0, -0.8, 0]), aligned_edge=np.array([-1, 0, 0])).move_to(np.array([3.5, -0.5, 0]))
        
        narration4 = VGroup(
            Text("Our objective is to demonstrate", font_size=28, color="#FFFFFF"),
            Text("the congruence of the two triangles.", font_size=28, color="#FFFFFF")
        ).arrange(np.array([0, -0.6, 0]), aligned_edge=np.array([-1, 0, 0])).move_to(np.array([3.5, -2.5, 0]))

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
            Create(diagram),
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
            Indicate(tri_ABC, color="#58C4DD"),
            Indicate(tri_BAD, color="#F07E48"),
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
            Write(goal_statement),
            Flash(goal_statement, color="#FFD700"),
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
            Write(narration4),
            Indicate(tri_ABC, color="#58C4DD"),
            Indicate(tri_BAD, color="#F07E48"),
            run_time=(s4_end - s4_start)
        )
        current_time = s4_end
        
        self.wait(2)