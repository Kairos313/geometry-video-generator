from manim import *

class PartBDeduceIsoscelesTriangle(Scene):
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
        line_AE = Line(A, E, color=CYAN, stroke_width=3)
        
        triangle_ABC = Polygon(A, B, C, color=BLUE, fill_opacity=0.2, stroke_width=2)
        triangle_BAD = Polygon(B, A, D, color=RED, fill_opacity=0.2, stroke_width=2)
        triangle_ADE = Polygon(A, D, E, color=CYAN, fill_opacity=0.3, stroke_width=3)
        
        angle_ACB = RightAngle(Line(C, A), Line(C, B), length=0.3, color=ORANGE)
        angle_ADB = RightAngle(Line(D, A), Line(D, B), length=0.3, color=ORANGE)
        angle_ADE = RightAngle(Line(D, A), Line(D, E), length=0.3, color=CYAN)
        
        # Pentagon from previous scene
        pentagon_ABCED = Polygon(A, B, C, E, D, color=PURPLE, fill_opacity=0.1, stroke_width=4)
        
        # Length labels from previous scene
        ad_length_label = MathTex("12", color=YELLOW, font_size=24).next_to(
            Line(A, D).get_center(), LEFT, buff=0.3
        )
        de_length_label = MathTex("9", color=YELLOW, font_size=24).next_to(
            Line(D, E).get_center(), UP, buff=0.3
        )
        ae_length_label = MathTex("15", color=GREEN, font_size=24).next_to(
            line_AE.get_center(), DOWN, buff=0.2
        )
        
        # Previous scene's final text elements
        part_b_title = Text("Part B: Pentagon Area", color=YELLOW, font_size=36, weight=BOLD)
        part_b_title.to_edge(UP).shift(RIGHT * 2)
        
        focus_text = Text("Focus on triangle ADE", color=CYAN, font_size=28, weight=BOLD)
        focus_text.to_edge(RIGHT, buff=1).shift(UP * 1.5)
        
        angle_explanation = Text("From Part A: ∠ADB = 90°\nTherefore: ∠ADE = 90°", 
                               color=LIGHT_BLUE, font_size=24, line_spacing=1.2)
        angle_explanation.to_edge(RIGHT, buff=1).shift(UP * 0.5)
        
        right_triangle_text = Text("Triangle ADE is a right-angled triangle", 
                                 color=CYAN, font_size=26, weight=BOLD)
        right_triangle_text.to_edge(RIGHT, buff=1).shift(DOWN * 0.2)
        
        pythagorean_text = VGroup(
            Text("Pythagorean Theorem:", color=GOLD, font_size=26, weight=BOLD),
            MathTex(r"AE^2 = AD^2 + DE^2", color=WHITE, font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        pythagorean_text.to_edge(RIGHT, buff=1).shift(DOWN * 1.0)
        
        substitution_text = MathTex(r"AE^2 = 12^2 + 9^2", color=YELLOW, font_size=28)
        substitution_text.to_edge(RIGHT, buff=1).shift(DOWN * 1.8)
        
        calculation1_text = MathTex(r"AE^2 = 144 + 81", color=LIGHT_GREEN, font_size=28)
        calculation1_text.to_edge(RIGHT, buff=1).shift(DOWN * 2.4)
        
        calculation2_text = MathTex(r"AE^2 = 225", color=LIGHT_GREEN, font_size=28)
        calculation2_text.to_edge(RIGHT, buff=1).shift(DOWN * 3.0)
        
        final_calculation_text = MathTex(r"AE = \sqrt{225} = 15 \text{ cm}", color=GREEN, font_size=30)
        final_calculation_text.to_edge(RIGHT, buff=1).shift(DOWN * 3.6)
        
        result_text = Text("Result: AE = 15 cm", color=GREEN, font_size=32, weight=BOLD)
        result_text.to_edge(RIGHT, buff=1).shift(DOWN * 4.2)
        
        # Add all reconstructed elements instantly
        self.add(
            line_AB, line_AC, line_AD, line_BC, line_BD, line_AE,
            dot_A, dot_B, dot_C, dot_D, dot_E,
            label_A, label_B, label_C, label_D, label_E,
            angle_ACB, angle_ADB, angle_ADE,
            triangle_ABC, triangle_BAD, triangle_ADE,
            pentagon_ABCED,
            ad_length_label, de_length_label, ae_length_label,
            part_b_title, focus_text, angle_explanation, right_triangle_text,
            pythagorean_text, substitution_text, calculation1_text,
            calculation2_text, final_calculation_text, result_text
        )
        
        #################################################################
        # PART 2: NEW ANIMATIONS for current scene
        #################################################################
        
        current_time = 0.0
        
        # Fade out previous text elements
        self.play(
            FadeOut(focus_text),
            FadeOut(angle_explanation),
            FadeOut(right_triangle_text),
            FadeOut(pythagorean_text),
            FadeOut(substitution_text),
            FadeOut(calculation1_text),
            FadeOut(calculation2_text),
            FadeOut(final_calculation_text),
            FadeOut(result_text),
            run_time=1.0
        )
        current_time += 1.0
        
        # Sentence 1: "Now, let's use the congruence we proved in part A."
        sentence1_start = 0.0
        sentence1_end = 2.82
        wait_time = sentence1_start - (current_time - 1.0)
        if wait_time > 0:
            self.wait(wait_time)
        
        congruence_text = Text("Using congruence from Part A:", color=GOLD, font_size=28, weight=BOLD)
        congruence_text.to_edge(RIGHT, buff=1).shift(UP * 1.5)
        
        self.play(
            Write(congruence_text),
            Indicate(triangle_ABC, color=BLUE, scale_factor=1.1),
            Indicate(triangle_BAD, color=RED, scale_factor=1.1),
            run_time=1.5
        )
        self.wait(sentence1_end - sentence1_start - 1.5)
        current_time = sentence1_end
        
        # Sentence 2: "Since triangle A B C is congruent to triangle B A D, their corresponding angles are equal."
        sentence2_start = 2.83
        sentence2_end = 8.58
        wait_time = sentence2_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        congruent_text = MathTex(r"\triangle ABC \cong \triangle BAD", color=LIGHT_BLUE, font_size=28)
        congruent_text.to_edge(RIGHT, buff=1).shift(UP * 0.8)
        
        corresponding_angles_text = Text("Corresponding angles are equal", color=LIGHT_BLUE, font_size=24)
        corresponding_angles_text.to_edge(RIGHT, buff=1).shift(UP * 0.3)
        
        self.play(
            Write(congruent_text),
            Write(corresponding_angles_text),
            run_time=2.5
        )
        self.wait(sentence2_end - sentence2_start - 2.5)
        current_time = sentence2_end
        
        # Sentence 3: "This means angle C A B equals angle D B A."
        sentence3_start = 8.59
        sentence3_end = 11.7
        wait_time = sentence3_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        angle_equality_text = MathTex(r"\angle CAB = \angle DBA", color=YELLOW, font_size=28)
        angle_equality_text.to_edge(RIGHT, buff=1).shift(DOWN * 0.2)
        
        # Create angle arcs to highlight the angles
        angle_CAB = Arc(radius=0.4, start_angle=0, angle=PI/4, color=YELLOW, stroke_width=3)
        angle_CAB.move_arc_center_to(A)
        
        angle_DBA = Arc(radius=0.4, start_angle=PI*3/4, angle=PI/4, color=YELLOW, stroke_width=3)
        angle_DBA.move_arc_center_to(B)
        
        self.play(
            Write(angle_equality_text),
            Create(angle_CAB),
            Create(angle_DBA),
            run_time=1.8
        )
        self.wait(sentence3_end - sentence3_start - 1.8)
        current_time = sentence3_end
        
        # Sentence 4: "In triangle A E B, angle E A B is the same as angle C A B, and angle E B A is the same as angle D B A."
        sentence4_start = 11.71
        sentence4_end = 19.13
        wait_time = sentence4_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        # Create triangle AEB
        line_BE = Line(B, E, color=PINK, stroke_width=3)
        triangle_AEB = Polygon(A, E, B, color=PINK, fill_opacity=0.2, stroke_width=3)
        
        triangle_aeb_text = Text("In triangle AEB:", color=PINK, font_size=26, weight=BOLD)
        triangle_aeb_text.to_edge(RIGHT, buff=1).shift(DOWN * 0.8)
        
        angle_explanation_text = Text("∠EAB = ∠CAB\n∠EBA = ∠DBA", 
                                    color=PINK, font_size=24, line_spacing=1.2)
        angle_explanation_text.to_edge(RIGHT, buff=1).shift(DOWN * 1.4)
        
        self.play(
            Create(triangle_AEB),
            Create(line_BE),
            Write(triangle_aeb_text),
            Write(angle_explanation_text),
            run_time=3.0
        )
        self.wait(sentence4_end - sentence4_start - 3.0)
        current_time = sentence4_end
        
        # Sentence 5: "Since angle E A B equals angle E B A, triangle A E B is an isosceles triangle."
        sentence5_start = 19.14
        sentence5_end = 24.57
        wait_time = sentence5_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        isosceles_conclusion_text = Text("∠EAB = ∠EBA", color=ORANGE, font_size=26, weight=BOLD)
        isosceles_conclusion_text.to_edge(RIGHT, buff=1).shift(DOWN * 2.2)
        
        isosceles_text = Text("Therefore: △AEB is isosceles", color=ORANGE, font_size=26, weight=BOLD)
        isosceles_text.to_edge(RIGHT, buff=1).shift(DOWN * 2.8)
        
        self.play(
            Write(isosceles_conclusion_text),
            Write(isosceles_text),
            Flash(triangle_AEB, color=PINK, flash_radius=0.8),
            run_time=2.5
        )
        self.wait(sentence5_end - sentence5_start - 2.5)
        current_time = sentence5_end
        
        # Sentence 6: "From triangle A B C congruent to triangle B A D, we have Angle C A B equals Angle D B A."
        sentence6_start = 24.58
        sentence6_end = 30.93
        wait_time = sentence6_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        summary_text1 = Text("Summary:", color=GOLD, font_size=28, weight=BOLD)
        summary_text1.to_edge(RIGHT, buff=1).shift(DOWN * 3.4)
        
        summary_equation1 = MathTex(r"\triangle ABC \cong \triangle BAD \Rightarrow \angle CAB = \angle DBA", 
                                   color=WHITE, font_size=24)
        summary_equation1.to_edge(RIGHT, buff=1).shift(DOWN * 3.9)
        
        self.play(
            Write(summary_text1),
            Write(summary_equation1),
            Indicate(angle_CAB, color=YELLOW, scale_factor=1.3),
            Indicate(angle_DBA, color=YELLOW, scale_factor=1.3),
            run_time=2.8
        )
        self.wait(sentence6_end - sentence6_start - 2.8)
        current_time = sentence6_end
        
        # Sentence 7: "In triangle A E B, Angle E A B equals Angle E B A."
        sentence7_start = 30.94
        sentence7_end = 34.96
        wait_time = sentence7_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        summary_equation2 = MathTex(r"\text{In } \triangle AEB: \angle EAB = \angle EBA", 
                                   color=PINK, font_size=24)
        summary_equation2.to_edge(RIGHT, buff=1).shift(DOWN * 4.4)
        
        self.play(
            Write(summary_equation2),
            Indicate(triangle_AEB, color=PINK, scale_factor=1.1),
            run_time=2.0
        )
        self.wait(sentence7_end - sentence7_start - 2.0)
        current_time = sentence7_end
        
        # Sentence 8: "Therefore, triangle A E B is an isosceles triangle with side A E equal to side B E."
        sentence8_start = 34.97
        sentence8_end = 40.17
        wait_time = sentence8_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        final_conclusion_text = MathTex(r"\triangle AEB \text{ is isosceles} \Rightarrow AE = BE", 
                                       color=GREEN, font_size=26)
        final_conclusion_text.to_edge(RIGHT, buff=1).shift(DOWN * 4.9)
        
        self.play(
            Write(final_conclusion_text),
            Indicate(line_AE, color=GREEN, scale_factor=1.2),
            Indicate(line_BE, color=GREEN, scale_factor=1.2),
            run_time=2.5
        )
        self.wait(sentence8_end - sentence8_start - 2.5)
        current_time = sentence8_end
        
        # Sentence 9: "We deduced that A E equals B E, so B E is also fifteen centimeters."
        sentence9_start = 40.18
        sentence9_end = 45.14
        wait_time = sentence9_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        # Add BE length label
        be_length_label = MathTex("15", color=GREEN, font_size=24).next_to(
            line_BE.get_center(), RIGHT, buff=0.2
        )
        
        final_result_text = Text("Result: BE = 15 cm", color=GREEN, font_size=28, weight=BOLD)
        final_result_text.to_edge(RIGHT, buff=1).shift(DOWN * 5.4)
        
        self.play(
            Write(be_length_label),
            Write(final_result_text),
            Flash(line_BE, color=GREEN, flash_radius=0.6),
            run_time=2.5
        )
        self.wait(sentence9_end - sentence9_start - 2.5)
        
        self.wait(1)