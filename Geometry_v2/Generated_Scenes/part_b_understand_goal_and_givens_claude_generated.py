from manim import *

class PartBUnderstandGoalAndGivens(Scene):
    def construct(self):
        # 1. Scene Setup
        self.camera.background_color = "#0C0C0C"
        
        #################################################################
        # PART 1: INSTANT RECONSTRUCTION of previous scene's final state
        #################################################################
        
        # Recreate exact coordinates from previous scene
        A = [-6.0, -2.0, 0]
        B = [0.0, -2.0, 0]
        C = [-1.5, 1.5, 0]
        D = [-4.5, 1.5, 0]
        E = [-3.0, 0.0, 0]
        
        # Recreate all diagram elements exactly as they were
        dot_A = Dot(A, color=WHITE)
        dot_B = Dot(B, color=WHITE)
        dot_C = Dot(C, color=WHITE)
        dot_D = Dot(D, color=WHITE)
        dot_E = Dot(E, color=YELLOW)
        
        label_A = MathTex("A", color=WHITE).next_to(A, DOWN, buff=0.2)
        label_B = MathTex("B", color=WHITE).next_to(B, DOWN, buff=0.2)
        label_C = MathTex("C", color=WHITE).next_to(C, UP, buff=0.2)
        label_D = MathTex("D", color=WHITE).next_to(D, UP, buff=0.2)
        label_E = MathTex("E", color=YELLOW).next_to(E, RIGHT, buff=0.2)
        
        line_AB = Line(A, B, color=WHITE, stroke_width=3)
        line_AC = Line(A, C, color=BLUE, stroke_width=3)
        line_AD = Line(A, D, color=GREEN, stroke_width=3)
        line_BC = Line(B, C, color=GREEN, stroke_width=3)
        line_BD = Line(B, D, color=BLUE, stroke_width=3)
        
        triangle_ABC = Polygon(A, B, C, color=BLUE, fill_opacity=0.2, stroke_width=2)
        triangle_BAD = Polygon(B, A, D, color=RED, fill_opacity=0.2, stroke_width=2)
        
        angle_ACB = RightAngle(Line(C, A), Line(C, B), length=0.3, color=ORANGE)
        angle_ADB = RightAngle(Line(D, A), Line(D, B), length=0.3, color=ORANGE)
        
        # Recreate previous scene's final text elements
        rhs_title = Text("Applying RHS Congruence Criterion", color=YELLOW, font_size=36)
        rhs_title.to_edge(UP).shift(RIGHT * 2)
        
        intro_rhs_text = Text("Let's apply the RHS congruence theorem\nto prove triangle congruence:", 
                             color=WHITE, font_size=24, line_spacing=1.2)
        intro_rhs_text.to_edge(RIGHT, buff=1).shift(UP * 1.5)
        
        rhs_explanation = Text("RHS Theorem: If a right angle, hypotenuse,\nand one side are equal in two triangles,\nthen the triangles are congruent.", 
                              color=LIGHT_BLUE, font_size=22, line_spacing=1.2)
        rhs_explanation.to_edge(RIGHT, buff=1).shift(UP * 0.5)
        
        condition1_text = VGroup(
            Text("Condition 1 (Right Angle):", color=GOLD, font_size=26),
            MathTex(r"\angle ACB = \angle ADB = 90°", color=WHITE, font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        condition1_text.to_edge(RIGHT, buff=1).shift(DOWN * 0.2)
        
        condition2_text = VGroup(
            Text("Condition 2 (Hypotenuse):", color=GOLD, font_size=26),
            MathTex(r"AB = BA \text{ (common)}", color=WHITE, font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        condition2_text.to_edge(RIGHT, buff=1).shift(DOWN * 1.0)
        
        condition3_text = VGroup(
            Text("Condition 3 (Side):", color=GOLD, font_size=26),
            MathTex(r"BC = AD \text{ (given)}", color=WHITE, font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        condition3_text.to_edge(RIGHT, buff=1).shift(DOWN * 1.8)
        
        conclusion_text = VGroup(
            Text("Therefore, by RHS:", color=GOLD, font_size=28),
            MathTex(r"\triangle ABC \cong \triangle BAD", color=YELLOW, font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        conclusion_text.to_edge(RIGHT, buff=1).shift(DOWN * 2.8)
        
        success_text = Text("✓ Proof Complete!", color=GREEN, font_size=32, weight=BOLD)
        success_text.to_edge(RIGHT, buff=1).shift(DOWN * 3.5)
        
        # Add all reconstructed elements instantly
        self.add(
            line_AB, line_AC, line_AD, line_BC, line_BD,
            dot_A, dot_B, dot_C, dot_D, dot_E,
            label_A, label_B, label_C, label_D, label_E,
            angle_ACB, angle_ADB,
            triangle_ABC, triangle_BAD,
            rhs_title, intro_rhs_text, rhs_explanation,
            condition1_text, condition2_text, condition3_text,
            conclusion_text, success_text
        )
        
        #################################################################
        # PART 2: NEW ANIMATIONS for current scene
        #################################################################
        
        current_time = 0.0
        
        # Fade out all previous text elements
        self.play(
            FadeOut(rhs_title),
            FadeOut(intro_rhs_text),
            FadeOut(rhs_explanation),
            FadeOut(condition1_text),
            FadeOut(condition2_text),
            FadeOut(condition3_text),
            FadeOut(conclusion_text),
            FadeOut(success_text),
            run_time=1.0
        )
        current_time += 1.0
        
        # Sentence 1: "Moving on to part B, we need to find the area of the pentagon A B C E D."
        sentence1_start = 0.0
        sentence1_end = 4.6
        wait_time = sentence1_start - (current_time - 1.0)
        if wait_time > 0:
            self.wait(wait_time)
        
        part_b_title = Text("Part B: Pentagon Area", color=YELLOW, font_size=36, weight=BOLD)
        part_b_title.to_edge(UP).shift(RIGHT * 2)
        
        intro_text = Text("We need to find the area of\npentagon ABCED", 
                         color=WHITE, font_size=28, line_spacing=1.2)
        intro_text.to_edge(RIGHT, buff=1).shift(UP * 1.5)
        
        # Highlight the pentagon by creating its outline
        pentagon_ABCED = Polygon(A, B, C, E, D, color=PURPLE, fill_opacity=0.1, stroke_width=4)
        
        self.play(
            Write(part_b_title),
            Write(intro_text),
            Create(pentagon_ABCED),
            run_time=2.0
        )
        self.wait(sentence1_end - sentence1_start - 2.0)
        current_time = sentence1_end
        
        # Sentence 2: "We are given specific lengths: A D equals twelve centimeters and D E equals nine centimeters."
        sentence2_start = 4.61
        sentence2_end = 11.32
        wait_time = sentence2_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        given_lengths_text = Text("Given specific lengths:", color=LIGHT_BLUE, font_size=26)
        given_lengths_text.to_edge(RIGHT, buff=1).shift(UP * 0.5)
        
        # Create length labels for AD and DE
        ad_length_label = MathTex("12", color=YELLOW, font_size=24).next_to(
            Line(A, D).get_center(), LEFT, buff=0.3
        )
        de_length_label = MathTex("9", color=YELLOW, font_size=24).next_to(
            Line(D, E).get_center(), UP, buff=0.3
        )
        
        self.play(
            Write(given_lengths_text),
            Write(ad_length_label),
            Write(de_length_label),
            Indicate(line_AD, color=YELLOW, scale_factor=1.3),
            run_time=2.5
        )
        self.wait(sentence2_end - sentence2_start - 2.5)
        current_time = sentence2_end
        
        # Sentence 3: "Goal: Find Area(A B C E D)."
        sentence3_start = 11.33
        sentence3_end = 13.32
        wait_time = sentence3_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        goal_text = VGroup(
            Text("Goal:", color=GOLD, font_size=28, weight=BOLD),
            MathTex(r"\text{Area}(ABCED)", color=YELLOW, font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        goal_text.to_edge(RIGHT, buff=1).shift(DOWN * 0.2)
        
        self.play(
            Write(goal_text),
            Flash(pentagon_ABCED, color=PURPLE, flash_radius=0.8),
            run_time=1.5
        )
        self.wait(sentence3_end - sentence3_start - 1.5)
        current_time = sentence3_end
        
        # Sentence 4: "Given: A D equals twelve centimeters, D E equals nine centimeters."
        sentence4_start = 13.33
        sentence4_end = 17.82
        wait_time = sentence4_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        given_text = VGroup(
            Text("Given:", color=GOLD, font_size=28, weight=BOLD),
            MathTex(r"AD = 12 \text{ cm}", color=WHITE, font_size=26),
            MathTex(r"DE = 9 \text{ cm}", color=WHITE, font_size=26)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        given_text.to_edge(RIGHT, buff=1).shift(DOWN * 1.2)
        
        self.play(
            Write(given_text),
            Indicate(ad_length_label, color=YELLOW, scale_factor=1.4),
            Indicate(de_length_label, color=YELLOW, scale_factor=1.4),
            run_time=2.0
        )
        self.wait(sentence4_end - sentence4_start - 2.0)
        current_time = sentence4_end
        
        # Sentence 5: "The objective is to calculate the area of the pentagon, given two side lengths."
        sentence5_start = 17.83
        sentence5_end = 22.14
        wait_time = sentence5_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        objective_text = Text("Objective: Calculate pentagon area\nusing the given side lengths", 
                             color=LIGHT_GREEN, font_size=24, line_spacing=1.2)
        objective_text.to_edge(RIGHT, buff=1).shift(DOWN * 2.5)
        
        self.play(
            Write(objective_text),
            Indicate(pentagon_ABCED, color=PURPLE, scale_factor=1.1),
            run_time=2.0
        )
        self.wait(sentence5_end - sentence5_start - 2.0)
        
        self.wait(1)