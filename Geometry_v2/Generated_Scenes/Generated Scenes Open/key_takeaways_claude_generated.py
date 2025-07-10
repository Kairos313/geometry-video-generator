from manim import *
import numpy as np

class KeyTakeaways(Scene):
    def construct(self):
        # 1. Scene Setup & Audio
        self.camera.background_color = "#1E293B"
        self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Scene/key_takeaways_scene.mp3")

        #################################################################
        # PART 1: INSTANT RECONSTRUCTION of PartBCalculateTotalArea's final state
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
        
        # Previous scene's final answer
        pentagon_intro = Text("Calculating Pentagon ABCED Area", font_size=28, color="#E2D28B", weight=BOLD).move_to([4.0, 3.0, 0])
        pentagon_formula = MathTex(
            r"\text{Area}(\text{pentagon } ABCED) = \text{Area}(\triangle ABD) + \text{Area}(\triangle BCE)",
            font_size=22, color="#E2D28B"
        ).move_to([4.0, 2.0, 0])
        pentagon_substitution = MathTex(
            r"\text{Area}(\text{pentagon } ABCED) = 144 + 54",
            font_size=24, color="#87C2A5"
        ).move_to([4.0, 1.0, 0])
        pentagon_result = MathTex(
            r"\text{Area}(\text{pentagon } ABCED) = 198 \text{ cm}^2",
            font_size=26, color="#FFD700", weight=BOLD
        ).move_to([4.0, 0.0, 0])
        final_answer = VGroup(
            Text("Final Answer:", font_size=24, color="#FFFFFF", weight=BOLD),
            MathTex(r"\text{Area of pentagon } ABCED = 198 \text{ cm}^2", font_size=26, color="#FFD700", weight=BOLD)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.0, -1.5, 0])

        # Add all reconstructed mobjects instantly
        self.add(
            tri_ABC, tri_BAD, pentagon_ABCED, tri_ADE, tri_AEB, tri_BCE, line_AC, line_BD,
            dot_A, dot_B, dot_C, dot_D, dot_E,
            label_A, label_B, label_C, label_D, label_E,
            angle_ACB, angle_ADB, angle_ADE, angle_BCE, angle_CAB, angle_DBA,
            pentagon_intro, pentagon_formula, pentagon_substitution, pentagon_result, final_answer
        )

        #################################################################
        # PART 2: NEW ANIMATIONS for the current scene
        #################################################################
        current_time = 0

        # Sentence 1: 0.0s - 1.8s
        s1_start = 0.0
        s1_end = 1.8
        wait_duration = s1_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Fade out previous content and introduce key takeaways
        key_takeaways_title = Text("Key Concepts from this Problem", font_size=32, color="#FFD700", weight=BOLD).move_to([4.0, 3.5, 0])
        
        self.play(
            FadeOut(pentagon_intro, pentagon_formula, pentagon_substitution, pentagon_result, final_answer),
            Write(key_takeaways_title),
            run_time=(s1_end - s1_start)
        )
        current_time = s1_end

        # Sentence 2: 1.81s - 16.44s
        s2_start = 1.81
        s2_end = 16.44
        wait_duration = s2_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # RHS Congruence Theorem
        rhs_concept = VGroup(
            Text("RHS Congruence Theorem:", font_size=24, color="#58C4DD", weight=BOLD),
            Text("For right-angled triangles, if hypotenuse", font_size=20, color="#FFFFFF"),
            Text("and one leg are equal, triangles are congruent", font_size=20, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 2.5, 0])
        
        self.play(
            Write(rhs_concept),
            Flash(tri_ABC, color="#58C4DD"),
            Flash(tri_BAD, color="#F07E48"),
            run_time=(s2_end - s2_start)
        )
        current_time = s2_end

        # Sentence 3: 16.45s - 27.21s
        s3_start = 16.45
        s3_end = 27.21
        wait_duration = s3_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # CPCTC
        cpctc_concept = VGroup(
            Text("CPCTC:", font_size=24, color="#87C2A5", weight=BOLD),
            Text("Corresponding Parts of Congruent", font_size=20, color="#FFFFFF"),
            Text("Triangles are Congruent", font_size=20, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 1.5, 0])
        
        self.play(
            Write(cpctc_concept),
            Indicate(angle_CAB, color="#E2D28B"),
            Indicate(angle_DBA, color="#E2D28B"),
            run_time=(s3_end - s3_start)
        )
        current_time = s3_end

        # Sentence 4: 27.22s - 43.42s
        s4_start = 27.22
        s4_end = 43.42
        wait_duration = s4_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Pythagorean Theorem
        pythagoras_concept = VGroup(
            Text("Pythagorean Theorem:", font_size=24, color="#F07E48", weight=BOLD),
            MathTex(r"a^2 + b^2 = c^2", font_size=22, color="#FFFFFF"),
            Text("For right triangles and finding side lengths", font_size=18, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, 0.5, 0])
        
        self.play(
            Write(pythagoras_concept),
            Flash(angle_ACB, color="#87C2A5"),
            Flash(angle_ADB, color="#87C2A5"),
            run_time=(s4_end - s4_start)
        )
        current_time = s4_end

        # Sentence 5: 43.43s - 55.55s
        s5_start = 43.43
        s5_end = 55.55
        wait_duration = s5_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Isosceles Triangle Properties
        isosceles_concept = VGroup(
            Text("Isosceles Triangle Properties:", font_size=24, color="#E2D28B", weight=BOLD),
            Text("Equal angles → Equal opposite sides", font_size=20, color="#FFFFFF"),
            Text("Used to find length BE", font_size=18, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -0.5, 0])
        
        self.play(
            Write(isosceles_concept),
            Indicate(Line(A, E), color="#FFD700"),
            Indicate(Line(B, E), color="#FFD700"),
            run_time=(s5_end - s5_start)
        )
        current_time = s5_end

        # Sentence 6: 55.56s - 65.83s
        s6_start = 55.56
        s6_end = 65.83
        wait_duration = s6_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        # Area of Right Triangle
        area_concept = VGroup(
            Text("Area of Right Triangle:", font_size=24, color="#FFD700", weight=BOLD),
            MathTex(r"\text{Area} = \frac{1}{2} \times \text{base} \times \text{height}", font_size=20, color="#FFFFFF"),
            Text("Using perpendicular sides", font_size=18, color="#FFFFFF")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -1.5, 0])
        
        self.play(
            Write(area_concept),
            Flash(tri_ADE, color="#FFD700"),
            Flash(tri_BCE, color="#58C4DD"),
            Flash(tri_BAD, color="#F07E48"),
            run_time=(s6_end - s6_start)
        )
        current_time = s6_end
        
        self.wait(2)