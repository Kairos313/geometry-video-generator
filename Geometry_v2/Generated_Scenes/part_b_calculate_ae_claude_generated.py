from manim import *

class PartBCalculateAe(Scene):
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
        
        # Pentagon from previous scene
        pentagon_ABCED = Polygon(A, B, C, E, D, color=PURPLE, fill_opacity=0.1, stroke_width=4)
        
        # Length labels from previous scene
        ad_length_label = MathTex("12", color=YELLOW, font_size=24).next_to(
            Line(A, D).get_center(), LEFT, buff=0.3
        )
        de_length_label = MathTex("9", color=YELLOW, font_size=24).next_to(
            Line(D, E).get_center(), UP, buff=0.3
        )
        
        # Previous scene's final text elements
        part_b_title = Text("Part B: Pentagon Area", color=YELLOW, font_size=36, weight=BOLD)
        part_b_title.to_edge(UP).shift(RIGHT * 2)
        
        intro_text = Text("We need to find the area of\npentagon ABCED", 
                         color=WHITE, font_size=28, line_spacing=1.2)
        intro_text.to_edge(RIGHT, buff=1).shift(UP * 1.5)
        
        given_lengths_text = Text("Given specific lengths:", color=LIGHT_BLUE, font_size=26)
        given_lengths_text.to_edge(RIGHT, buff=1).shift(UP * 0.5)
        
        goal_text = VGroup(
            Text("Goal:", color=GOLD, font_size=28, weight=BOLD),
            MathTex(r"\text{Area}(ABCED)", color=YELLOW, font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        goal_text.to_edge(RIGHT, buff=1).shift(DOWN * 0.2)
        
        given_text = VGroup(
            Text("Given:", color=GOLD, font_size=28, weight=BOLD),
            MathTex(r"AD = 12 \text{ cm}", color=WHITE, font_size=26),
            MathTex(r"DE = 9 \text{ cm}", color=WHITE, font_size=26)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        given_text.to_edge(RIGHT, buff=1).shift(DOWN * 1.2)
        
        objective_text = Text("Objective: Calculate pentagon area\nusing the given side lengths", 
                             color=LIGHT_GREEN, font_size=24, line_spacing=1.2)
        objective_text.to_edge(RIGHT, buff=1).shift(DOWN * 2.5)
        
        # Add all reconstructed elements instantly
        self.add(
            line_AB, line_AC, line_AD, line_BC, line_BD,
            dot_A, dot_B, dot_C, dot_D, dot_E,
            label_A, label_B, label_C, label_D, label_E,
            angle_ACB, angle_ADB,
            triangle_ABC, triangle_BAD,
            pentagon_ABCED,
            ad_length_label, de_length_label,
            part_b_title, intro_text, given_lengths_text,
            goal_text, given_text, objective_text
        )
        
        #################################################################
        # PART 2: NEW ANIMATIONS for current scene
        #################################################################
        
        current_time = 0.0
        
        # Fade out previous text elements
        self.play(
            FadeOut(intro_text),
            FadeOut(given_lengths_text),
            FadeOut(goal_text),
            FadeOut(given_text),
            FadeOut(objective_text),
            run_time=1.0
        )
        current_time += 1.0
        
        # Sentence 1: "Let's first focus on triangle A D E."
        sentence1_start = 0.0
        sentence1_end = 2.35
        wait_time = sentence1_start - (current_time - 1.0)
        if wait_time > 0:
            self.wait(wait_time)
        
        # Create triangle ADE
        triangle_ADE = Polygon(A, D, E, color=CYAN, fill_opacity=0.3, stroke_width=3)
        line_AE = Line(A, E, color=CYAN, stroke_width=3)
        
        focus_text = Text("Focus on triangle ADE", color=CYAN, font_size=28, weight=BOLD)
        focus_text.to_edge(RIGHT, buff=1).shift(UP * 1.5)
        
        self.play(
            Create(triangle_ADE),
            Create(line_AE),
            Write(focus_text),
            run_time=1.5
        )
        self.wait(sentence1_end - sentence1_start - 1.5)
        current_time = sentence1_end
        
        # Sentence 2: "From part A, we know that angle A D B is ninety degrees, which means angle A D E is also ninety degrees."
        sentence2_start = 2.36
        sentence2_end = 8.63
        wait_time = sentence2_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        angle_explanation = Text("From Part A: ∠ADB = 90°\nTherefore: ∠ADE = 90°", 
                               color=LIGHT_BLUE, font_size=24, line_spacing=1.2)
        angle_explanation.to_edge(RIGHT, buff=1).shift(UP * 0.5)
        
        # Create right angle marker for ADE
        angle_ADE = RightAngle(Line(D, A), Line(D, E), length=0.3, color=CYAN)
        
        self.play(
            Write(angle_explanation),
            Create(angle_ADE),
            Indicate(angle_ADB, color=ORANGE, scale_factor=1.3),
            run_time=2.5
        )
        self.wait(sentence2_end - sentence2_start - 2.5)
        current_time = sentence2_end
        
        # Sentence 3: "So, triangle A D E is a right-angled triangle."
        sentence3_start = 8.64
        sentence3_end = 11.64
        wait_time = sentence3_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        right_triangle_text = Text("Triangle ADE is a right-angled triangle", 
                                 color=CYAN, font_size=26, weight=BOLD)
        right_triangle_text.to_edge(RIGHT, buff=1).shift(DOWN * 0.2)
        
        self.play(
            Write(right_triangle_text),
            Flash(triangle_ADE, color=CYAN, flash_radius=0.8),
            run_time=1.5
        )
        self.wait(sentence3_end - sentence3_start - 1.5)
        current_time = sentence3_end
        
        # Sentence 4: "In right-angled triangle A D E: By the Pythagorean theorem, A E squared equals A D squared plus D E squared."
        sentence4_start = 11.65
        sentence4_end = 19.54
        wait_time = sentence4_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        pythagorean_text = VGroup(
            Text("Pythagorean Theorem:", color=GOLD, font_size=26, weight=BOLD),
            MathTex(r"AE^2 = AD^2 + DE^2", color=WHITE, font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        pythagorean_text.to_edge(RIGHT, buff=1).shift(DOWN * 1.0)
        
        self.play(
            Write(pythagorean_text),
            Indicate(line_AE, color=CYAN, scale_factor=1.2),
            run_time=2.5
        )
        self.wait(sentence4_end - sentence4_start - 2.5)
        current_time = sentence4_end
        
        # Sentence 5: "A E squared equals twelve squared plus nine squared."
        sentence5_start = 19.55
        sentence5_end = 22.37
        wait_time = sentence5_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        substitution_text = MathTex(r"AE^2 = 12^2 + 9^2", color=YELLOW, font_size=28)
        substitution_text.to_edge(RIGHT, buff=1).shift(DOWN * 1.8)
        
        self.play(
            Write(substitution_text),
            Indicate(ad_length_label, color=YELLOW, scale_factor=1.4),
            Indicate(de_length_label, color=YELLOW, scale_factor=1.4),
            run_time=1.5
        )
        self.wait(sentence5_end - sentence5_start - 1.5)
        current_time = sentence5_end
        
        # Sentence 6: "A E squared equals one hundred forty-four plus eighty-one."
        sentence6_start = 22.38
        sentence6_end = 25.49
        wait_time = sentence6_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        calculation1_text = MathTex(r"AE^2 = 144 + 81", color=LIGHT_GREEN, font_size=28)
        calculation1_text.to_edge(RIGHT, buff=1).shift(DOWN * 2.4)
        
        self.play(
            Write(calculation1_text),
            run_time=1.5
        )
        self.wait(sentence6_end - sentence6_start - 1.5)
        current_time = sentence6_end
        
        # Sentence 7: "A E squared equals two hundred twenty-five."
        sentence7_start = 25.5
        sentence7_end = 27.9
        wait_time = sentence7_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        calculation2_text = MathTex(r"AE^2 = 225", color=LIGHT_GREEN, font_size=28)
        calculation2_text.to_edge(RIGHT, buff=1).shift(DOWN * 3.0)
        
        self.play(
            Write(calculation2_text),
            run_time=1.2
        )
        self.wait(sentence7_end - sentence7_start - 1.2)
        current_time = sentence7_end
        
        # Sentence 8: "A E equals the square root of two hundred twenty-five, which is fifteen centimeters."
        sentence8_start = 27.91
        sentence8_end = 32.64
        wait_time = sentence8_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        final_calculation_text = MathTex(r"AE = \sqrt{225} = 15 \text{ cm}", color=GREEN, font_size=30)
        final_calculation_text.to_edge(RIGHT, buff=1).shift(DOWN * 3.6)
        
        # Add AE length label to the diagram
        ae_length_label = MathTex("15", color=GREEN, font_size=24).next_to(
            line_AE.get_center(), DOWN, buff=0.2
        )
        
        self.play(
            Write(final_calculation_text),
            Write(ae_length_label),
            Flash(line_AE, color=GREEN, flash_radius=0.6),
            run_time=2.5
        )
        self.wait(sentence8_end - sentence8_start - 2.5)
        current_time = sentence8_end
        
        # Sentence 9: "We found A E equals fifteen centimeters."
        sentence9_start = 32.65
        sentence9_end = 35.24
        wait_time = sentence9_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        result_text = Text("Result: AE = 15 cm", color=GREEN, font_size=32, weight=BOLD)
        result_text.to_edge(RIGHT, buff=1).shift(DOWN * 4.2)
        
        self.play(
            Write(result_text),
            Indicate(ae_length_label, color=GREEN, scale_factor=1.5),
            run_time=1.5
        )
        self.wait(sentence9_end - sentence9_start - 1.5)
        
        self.wait(1)