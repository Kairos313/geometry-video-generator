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
        
        # Base points (from previous scene's logic)
        A = np.array([-5.5, -2.5, 0])
        B = np.array([-1.5, -2.5, 0])
        
        # Derived points maintaining right angles and AD = BC constraint
        C = np.array([-1.5, 0.5, 0])
        D = np.array([-5.5, 0.5, 0])
        
        # Intersection point E calculation (replicating previous logic)
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

        # Recreate all mobjects from previous scene's final state
        tri_ABC = Polygon(A, B, C, color="#58C4DD", fill_opacity=0.3, stroke_width=3)
        tri_BAD = Polygon(B, A, D, color="#F07E48", fill_opacity=0.3, stroke_width=3)
        
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
        
        # Previous scene's final text state
        goal_statement = VGroup(
            Text("Goal:", font_size=32, color="#FFD700"),
            MathTex(r"\triangle ABC \cong \triangle BAD", font_size=36, color="#58C4DD")
        ).arrange(DOWN, aligned_edge=LEFT).move_to([3.5, -0.5, 0])
        
        narration4 = VGroup(
            Text("Our objective is to demonstrate", font_size=28, color="#FFFFFF"),
            Text("the congruence of the two triangles.", font_size=28, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT).move_to([3.5, -2.5, 0])

        # Add all reconstructed mobjects instantly
        self.add(diagram, goal_statement, narration4)

        #################################################################
        # PART 2: NEW ANIMATIONS for the current scene
        #################################################################
        current_time = 0

        # Sentence 1: 0.0s - 5.62s
        s1_start = 0.0
        s1_end = 5.62
        
        # Fade out previous text and introduce new content
        intro_text = VGroup(
            Text("Next, let's list the information given", font_size=28, color="#FFFFFF"),
            Text("in the problem and from the diagram", font_size=28, color="#FFFFFF"),
            Text("that will help us prove congruence.", font_size=28, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT).move_to([3.5, 2.5, 0])
        
        self.play(
            FadeOut(goal_statement),
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
            Text("Given:", font_size=32, color="#FFD700"),
            MathTex(r"1. \angle ACB = \angle ADB = 90°", font_size=28, color="#E2D28B")
        ).arrange(DOWN, aligned_edge=LEFT).move_to([3.5, 1.0, 0])
        
        self.play(
            Write(given1_text),
            Indicate(angle_C, color="#87C2A5"),
            Indicate(angle_D, color="#87C2A5"),
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
            Text("This tells us that triangle ABC is", font_size=24, color="#FFFFFF"),
            Text("a right-angled triangle at C, and", font_size=24, color="#FFFFFF"),
            Text("triangle BAD is a right-angled", font_size=24, color="#FFFFFF"),
            Text("triangle at D.", font_size=24, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT).move_to([3.5, -0.5, 0])
        
        self.play(
            Write(explanation_text),
            Indicate(tri_ABC, color="#58C4DD"),
            Indicate(tri_BAD, color="#F07E48"),
            run_time=(s3_end - s3_start)
        )
        current_time = s3_end

        # Sentence 4: 18.14s - 20.49s
        s4_start = 18.14
        s4_end = 20.49
        wait_duration = s4_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        given2_text = MathTex(r"2. AD = BC", font_size=28, color="#E2D28B").next_to(given1_text, DOWN, buff=0.3, aligned_edge=LEFT)
        
        # Create lines to highlight AD and BC
        line_AD = Line(A, D, color="#FFD700", stroke_width=4)
        line_BC = Line(B, C, color="#FFD700", stroke_width=4)
        
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
            Text("Additionally, we can observe that", font_size=24, color="#FFFFFF"),
            Text("side AB is a common side to both", font_size=24, color="#FFFFFF"),
            Text("triangles.", font_size=24, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT).move_to([3.5, -2.5, 0])
        
        # Highlight the common side AB
        line_AB = Line(A, B, color="#FFD700", stroke_width=4)
        
        self.play(
            FadeOut(line_AD),
            FadeOut(line_BC),
            Write(common_side_text),
            Create(line_AB),
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
            Text("We have two right angles, one pair", font_size=24, color="#FFFFFF"),
            Text("of equal sides, and a common", font_size=24, color="#FFFFFF"),
            Text("hypotenuse.", font_size=24, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT).move_to([4.5, 0.5, 0])
        
        self.play(
            FadeOut(explanation_text),
            FadeOut(line_AB),
            Write(summary_text),
            Flash(angle_C, color="#87C2A5"),
            Flash(angle_D, color="#87C2A5"),
            run_time=(s6_end - s6_start)
        )
        current_time = s6_end
        
        self.wait(2)