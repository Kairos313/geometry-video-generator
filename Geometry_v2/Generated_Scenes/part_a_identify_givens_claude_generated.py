from manim import *

class PartAIdentifyGivens(Scene):
    def construct(self):
        # 1. Setup & Audio
        self.camera.background_color = "#1E293B"
        self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Scene/part_a_identify_givens_scene.mp3")

        #################################################################
        # PART 2: INSTANT RECONSTRUCTION of the geometric diagram
        #################################################################
        # Define coordinates based on the problem figure
        A = [-6.0, -2.0, 0]
        B = [2.0, -2.0, 0]
        C = [1.0, 2.0, 0]
        D = [-3.0, 2.5, 0]
        E = [-1.5, 0.5, 0]  # Intersection point of AC and BD
        
        # Define coordinates for the geometric figure
        # Based on the problem image, we have points A, B, C, D, E
        A = np.array([-6.5, -2.0, 0])
        B = np.array([-1.5, -2.0, 0])
        C = np.array([-2.5, 1.5, 0])
        D = np.array([-5.5, 1.5, 0])
        
        # Calculate intersection point E of AC and BD
        # Line AC: from A to C
        # Line BD: from B to D
        # Using parametric equations to find intersection
        AC_direction = C - A
        BD_direction = D - B
        AB_vector = B - A
        
        # Solve for intersection using cross product method
        t = np.cross(AB_vector[:2], BD_direction[:2]) / np.cross(AC_direction[:2], BD_direction[:2])
        E = A + t * AC_direction
        
        # Create the geometric elements
        # Main quadrilateral outline
        quad_outline = Polygon(A, B, C, D, color="#FFFFFF", stroke_width=2, fill_opacity=0)
        
        # Triangles ABC and BAD
        triangle_ABC = Polygon(A, B, C, color="#58C4DD", fill_opacity=0.2, stroke_width=3)
        triangle_BAD = Polygon(B, A, D, color="#F07E48", fill_opacity=0.2, stroke_width=3)
        
        # Diagonal lines AC and BD
        line_AC = Line(A, C, color="#87C2A5", stroke_width=2)
        line_BD = Line(B, D, color="#87C2A5", stroke_width=2)
        
        # Points
        point_A = Dot(A, color="#FFFFFF", radius=0.08)
        point_B = Dot(B, color="#FFFFFF", radius=0.08)
        point_C = Dot(C, color="#FFFFFF", radius=0.08)
        point_D = Dot(D, color="#FFFFFF", radius=0.08)
        point_E = Dot(E, color="#E2D28B", radius=0.1)
        
        # Labels
        label_A = MathTex("A", color="#FFFFFF", font_size=36).next_to(A, DOWN + LEFT, buff=0.2)
        label_B = MathTex("B", color="#FFFFFF", font_size=36).next_to(B, DOWN + RIGHT, buff=0.2)
        label_C = MathTex("C", color="#FFFFFF", font_size=36).next_to(C, UP + RIGHT, buff=0.2)
        label_D = MathTex("D", color="#FFFFFF", font_size=36).next_to(D, UP + LEFT, buff=0.2)
        label_E = MathTex("E", color="#E2D28B", font_size=32).next_to(E, UP + RIGHT, buff=0.15)
        
        # Right angle markers
        angle_C = RightAngle(Line(C, A), Line(C, B), length=0.3, color="#87C2A5", stroke_width=2)
        angle_D = RightAngle(Line(D, B), Line(D, A), length=0.3, color="#87C2A5", stroke_width=2)
        
        # Group all diagram elements
        diagram = VGroup(
            quad_outline, triangle_ABC, triangle_BAD, line_AC, line_BD,
            point_A, point_B, point_C, point_D, point_E,
            label_A, label_B, label_C, label_D, label_E,
            angle_C, angle_D
        )
        
        # Add diagram to scene instantly (since this is the first scene)
        self.add(diagram)
        
        #################################################################
        # PART 2: NEW ANIMATIONS - Identify the given
        #################################################################
        
        # Track timing for synchronization
        current_time = 0.0
        
        # Sentence 1: Introduction
        sentence_1 = current_step_json["sentences"][0]
        wait_time = sentence_1["start_time_seconds"] - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        # Title for the analysis
        title = Text("Given Information", color="#E2D28B", font_size=40).move_to([4.0, 3.2, 0])
        intro_text = Text("Let's identify what we know:", color="#FFFFFF", font_size=28).move_to([4.0, 2.6, 0])
        
        self.play(
            Write(title),
            Write(intro_text),
            run_time=2.0
        )
        
        remaining_time = sentence_1["end_time_seconds"] - (sentence_1["start_time_seconds"] + 2.0)
        if remaining_time > 0:
            self.wait(remaining_time)
        current_time = sentence_1["end_time_seconds"]
        
        # Sentence 2: Right angles
        sentence_2 = current_step_json["sentences"][1]
        wait_time = sentence_2["start_time_seconds"] - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        given_1 = MathTex(r"\text{1. } \angle ACB = \angle ADB = 90°", color="#87C2A5", font_size=32).move_to([4.0, 1.8, 0])
        
        self.play(
            Write(given_1),
            Indicate(angle_C, color="#FFD700"),
            Indicate(angle_D, color="#FFD700"),
            run_time=2.5
        )
        
        remaining_time = sentence_2["end_time_seconds"] - (sentence_2["start_time_seconds"] + 2.5)
        if remaining_time > 0:
            self.wait(remaining_time)
        current_time = sentence_2["end_time_seconds"]
        
        # Sentence 3: Right triangles explanation
        sentence_3 = current_step_json["sentences"][2]
        wait_time = sentence_3["start_time_seconds"] - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        explanation_1 = Text("△ABC is right-angled at C", color="#58C4DD", font_size=24).move_to([4.0, 1.3, 0])
        explanation_2 = Text("△BAD is right-angled at D", color="#F07E48", font_size=24).move_to([4.0, 1.0, 0])
        
        self.play(
            Write(explanation_1),
            Indicate(triangle_ABC, color="#58C4DD"),
            run_time=1.5
        )
        self.play(
            Write(explanation_2),
            Indicate(triangle_BAD, color="#F07E48"),
            run_time=1.5
        )
        
        remaining_time = sentence_3["end_time_seconds"] - (sentence_3["start_time_seconds"] + 3.0)
        if remaining_time > 0:
            self.wait(remaining_time)
        current_time = sentence_3["end_time_seconds"]
        
        # Sentence 4: Equal sides
        sentence_4 = current_step_json["sentences"][3]
        wait_time = sentence_4["start_time_seconds"] - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        given_2 = MathTex(r"\text{2. } AD = BC", color="#87C2A5", font_size=32).move_to([4.0, 0.4, 0])
        
        # Highlight the equal sides
        side_AD = Line(A, D, color="#FFD700", stroke_width=6)
        side_BC = Line(B, C, color="#FFD700", stroke_width=6)
        
        self.play(
            Write(given_2),
            Create(side_AD),
            Create(side_BC),
            run_time=2.0
        )
        
        remaining_time = sentence_4["end_time_seconds"] - (sentence_4["start_time_seconds"] + 2.0)
        if remaining_time > 0:
            self.wait(remaining_time)
        current_time = sentence_4["end_time_seconds"]
        
        # Sentence 5: Common side
        sentence_5 = current_step_json["sentences"][4]
        wait_time = sentence_5["start_time_seconds"] - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        given_3 = MathTex(r"\text{3. } AB \text{ is common to both triangles}", color="#87C2A5", font_size=32).move_to([4.0, -0.2, 0])
        
        # Highlight the common side
        side_AB = Line(A, B, color="#FFD700", stroke_width=8)
        
        self.play(
            Write(given_3),
            Create(side_AB),
            run_time=2.0
        )
        
        remaining_time = sentence_5["end_time_seconds"] - (sentence_5["start_time_seconds"] + 2.0)
        if remaining_time > 0:
            self.wait(remaining_time)
        current_time = sentence_5["end_time_seconds"]
        
        # Sentence 6: Summary
        sentence_6 = current_step_json["sentences"][5]
        wait_time = sentence_6["start_time_seconds"] - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        summary = Text("Ready for RHS Congruence!", color="#FFD700", font_size=32).move_to([4.0, -1.0, 0])
        summary_details = VGroup(
            Text("• Two right angles ✓", color="#FFFFFF", font_size=24),
            Text("• Equal sides (AD = BC) ✓", color="#FFFFFF", font_size=24),
            Text("• Common hypotenuse (AB) ✓", color="#FFFFFF", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.0, -2.0, 0])
        
        self.play(
            Write(summary),
            Write(summary_details),
            run_time=2.5
        )
        
        remaining_time = sentence_6["end_time_seconds"] - (sentence_6["start_time_seconds"] + 2.5)
        if remaining_time > 0:
            self.wait(remaining_time)
        
        # Final pause
        self.wait(1.0)
        
        # Fade out the highlighted sides to clean up for next scene
        self.play(
            FadeOut(side_AD),
            FadeOut(side_BC),
            FadeOut(side_AB),
            run_time=1.0
        )