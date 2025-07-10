from manim import *

class PartBConfirmRightAngleBce(Scene):
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
        line_BE = Line(B, E, color=PINK, stroke_width=3)
        line_CE = Line(C, E, color=ORANGE, stroke_width=3)
        
        triangle_ABC = Polygon(A, B, C, color=BLUE, fill_opacity=0.2, stroke_width=2)
        triangle_BAD = Polygon(B, A, D, color=RED, fill_opacity=0.2, stroke_width=2)
        triangle_ADE = Polygon(A, D, E, color=CYAN, fill_opacity=0.3, stroke_width=3)
        triangle_AEB = Polygon(A, E, B, color=PINK, fill_opacity=0.2, stroke_width=3)
        
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
        be_length_label = MathTex("15", color=GREEN, font_size=24).next_to(
            line_BE.get_center(), RIGHT, buff=0.2
        )
        bd_length_label = MathTex("24", color=GREEN, font_size=24).next_to(
            line_BD.get_center(), UP, buff=0.2
        )
        ac_length_label = MathTex("24", color=BLUE, font_size=24).next_to(
            line_AC.get_center(), LEFT, buff=0.2
        )
        ce_length_label = MathTex("9", color=ORANGE, font_size=24).next_to(
            line_CE.get_center(), UP, buff=0.2
        )
        
        # Angle arcs from previous scene
        angle_CAB = Arc(radius=0.4, start_angle=0, angle=PI/4, color=YELLOW, stroke_width=3)
        angle_CAB.move_arc_center_to(A)
        
        angle_DBA = Arc(radius=0.4, start_angle=PI*3/4, angle=PI/4, color=YELLOW, stroke_width=3)
        angle_DBA.move_arc_center_to(B)
        
        # Previous scene's final text elements
        part_b_title = Text("Part B: Pentagon Area", color=YELLOW, font_size=36, weight=BOLD)
        part_b_title.to_edge(UP).shift(RIGHT * 2)
        
        ce_intro_text = Text("Finding CE length:", color=GOLD, font_size=28, weight=BOLD)
        ce_intro_text.to_edge(RIGHT, buff=1).shift(UP * 1.5)
        
        ac_composition_text = Text("AC is composed of AE and EC", color=LIGHT_BLUE, font_size=26)
        ac_composition_text.to_edge(RIGHT, buff=1).shift(UP * 0.8)
        
        ac_equation_text = MathTex(r"AC = AE + EC", color=YELLOW, font_size=28)
        ac_equation_text.to_edge(RIGHT, buff=1).shift(UP * 0.3)
        
        ac_substitution_text = MathTex(r"24 = 15 + EC", color=LIGHT_GREEN, font_size=28)
        ac_substitution_text.to_edge(RIGHT, buff=1).shift(DOWN * 0.2)
        
        ec_calculation_text = MathTex(r"EC = 24 - 15", color=ORANGE, font_size=28)
        ec_calculation_text.to_edge(RIGHT, buff=1).shift(DOWN * 0.8)
        
        ec_result_text = MathTex(r"EC = 9 \text{ cm}", color=ORANGE, font_size=30, weight=BOLD)
        ec_result_text.to_edge(RIGHT, buff=1).shift(DOWN * 1.4)
        
        ce_summary_text = Text("Result: CE = 9 cm", color=ORANGE, font_size=28, weight=BOLD)
        ce_summary_text.to_edge(RIGHT, buff=1).shift(DOWN * 2.0)
        
        verification_text = Text("Verification: AC = AE + EC", color=LIGHT_BLUE, font_size=24)
        verification_text.to_edge(RIGHT, buff=1).shift(DOWN * 2.6)
        
        verification_calc_text = MathTex(r"24 = 15 + 9 \checkmark", color=GREEN, font_size=26)
        verification_calc_text.to_edge(RIGHT, buff=1).shift(DOWN * 3.1)
        
        # Add all reconstructed elements instantly
        self.add(
            line_AB, line_AC, line_AD, line_BC, line_BD, line_AE, line_BE, line_CE,
            dot_A, dot_B, dot_C, dot_D, dot_E,
            label_A, label_B, label_C, label_D, label_E,
            angle_ACB, angle_ADB, angle_ADE,
            triangle_ABC, triangle_BAD, triangle_ADE, triangle_AEB,
            pentagon_ABCED,
            ad_length_label, de_length_label, ae_length_label, be_length_label,
            bd_length_label, ac_length_label, ce_length_label,
            angle_CAB, angle_DBA,
            part_b_title, ce_intro_text, ac_composition_text, ac_equation_text,
            ac_substitution_text, ec_calculation_text, ec_result_text,
            ce_summary_text, verification_text, verification_calc_text
        )
        
        #################################################################
        # PART 2: NEW ANIMATIONS for current scene
        #################################################################
        
        current_time = 0.0
        
        # Fade out previous text elements
        self.play(
            FadeOut(ce_intro_text),
            FadeOut(ac_composition_text),
            FadeOut(ac_equation_text),
            FadeOut(ac_substitution_text),
            FadeOut(ec_calculation_text),
            FadeOut(ec_result_text),
            FadeOut(ce_summary_text),
            FadeOut(verification_text),
            FadeOut(verification_calc_text),
            run_time=1.0
        )
        current_time += 1.0
        
        # Sentence 1: "Let's check triangle B C E."
        sentence1_start = 0.0
        sentence1_end = 1.91
        wait_time = sentence1_start - (current_time - 1.0)
        if wait_time > 0:
            self.wait(wait_time)
        
        triangle_bce_intro_text = Text("Checking Triangle BCE:", color=GOLD, font_size=28, weight=BOLD)
        triangle_bce_intro_text.to_edge(RIGHT, buff=1).shift(UP * 1.5)
        
        # Create triangle BCE for highlighting
        triangle_BCE = Polygon(B, C, E, color=PURPLE, fill_opacity=0.3, stroke_width=4)
        
        self.play(
            Write(triangle_bce_intro_text),
            Create(triangle_BCE),
            run_time=1.5
        )
        self.wait(sentence1_end - sentence1_start - 1.5)
        current_time = sentence1_end
        
        # Sentence 2: "We have its side lengths: B C is twelve centimeters (given), C E is nine centimeters, and B E is fifteen centimeters."
        sentence2_start = 1.92
        sentence2_end = 9.68
        wait_time = sentence2_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        side_lengths_text = Text("Side lengths of triangle BCE:", color=LIGHT_BLUE, font_size=26)
        side_lengths_text.to_edge(RIGHT, buff=1).shift(UP * 0.8)
        
        bc_length_text = Text("BC = 12 cm (given)", color=GREEN, font_size=24)
        bc_length_text.to_edge(RIGHT, buff=1).shift(UP * 0.3)
        
        ce_length_text = Text("CE = 9 cm (calculated)", color=ORANGE, font_size=24)
        ce_length_text.to_edge(RIGHT, buff=1).shift(DOWN * 0.1)
        
        be_length_text = Text("BE = 15 cm (calculated)", color=PINK, font_size=24)
        be_length_text.to_edge(RIGHT, buff=1).shift(DOWN * 0.5)
        
        # Add BC length label to diagram
        bc_length_label = MathTex("12", color=GREEN, font_size=24).next_to(
            line_BC.get_center(), LEFT, buff=0.2
        )
        
        self.play(
            Write(side_lengths_text),
            Write(bc_length_text),
            Write(ce_length_text),
            Write(be_length_text),
            Write(bc_length_label),
            Indicate(line_BC, color=GREEN, scale_factor=1.2),
            Indicate(line_CE, color=ORANGE, scale_factor=1.2),
            Indicate(line_BE, color=PINK, scale_factor=1.2),
            run_time=3.0
        )
        self.wait(sentence2_end - sentence2_start - 3.0)
        current_time = sentence2_end
        
        # Sentence 3: "This is a nine-twelve-fifteen triangle, which is a multiple of a three-four-five right triangle."
        sentence3_start = 9.69
        sentence3_end = 15.12
        wait_time = sentence3_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        triangle_type_text = Text("9-12-15 triangle:", color=YELLOW, font_size=26, weight=BOLD)
        triangle_type_text.to_edge(RIGHT, buff=1).shift(DOWN * 1.0)
        
        multiple_text = Text("Multiple of 3-4-5 right triangle", color=LIGHT_GREEN, font_size=24)
        multiple_text.to_edge(RIGHT, buff=1).shift(DOWN * 1.4)
        
        ratio_text = MathTex(r"9:12:15 = 3 \times (3:4:5)", color=CYAN, font_size=24)
        ratio_text.to_edge(RIGHT, buff=1).shift(DOWN * 1.8)
        
        self.play(
            Write(triangle_type_text),
            Write(multiple_text),
            Write(ratio_text),
            run_time=2.5
        )
        self.wait(sentence3_end - sentence3_start - 2.5)
        current_time = sentence3_end
        
        # Sentence 4: "Let's verify if it's a right-angled triangle using the converse of the Pythagorean theorem."
        sentence4_start = 15.13
        sentence4_end = 20.33
        wait_time = sentence4_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        verification_header_text = Text("Pythagorean Theorem Verification:", color=GOLD, font_size=26, weight=BOLD)
        verification_header_text.to_edge(RIGHT, buff=1).shift(DOWN * 2.3)
        
        self.play(
            Write(verification_header_text),
            run_time=2.0
        )
        self.wait(sentence4_end - sentence4_start - 2.0)
        current_time = sentence4_end
        
        # Sentence 5: "Is C E squared plus B C squared equal to B E squared?"
        sentence5_start = 20.34
        sentence5_end = 23.71
        wait_time = sentence5_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        pythagorean_question_text = MathTex(r"CE^2 + BC^2 = BE^2 \text{ ?}", color=YELLOW, font_size=28)
        pythagorean_question_text.to_edge(RIGHT, buff=1).shift(DOWN * 2.8)
        
        self.play(
            Write(pythagorean_question_text),
            run_time=1.5
        )
        self.wait(sentence5_end - sentence5_start - 1.5)
        current_time = sentence5_end
        
        # Sentence 6: "Nine squared plus twelve squared equals eighty-one plus one hundred forty-four equals two hundred twenty-five."
        sentence6_start = 23.72
        sentence6_end = 30.3
        wait_time = sentence6_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        left_side_calc_text = MathTex(r"9^2 + 12^2 = 81 + 144 = 225", color=LIGHT_GREEN, font_size=26)
        left_side_calc_text.to_edge(RIGHT, buff=1).shift(DOWN * 3.3)
        
        self.play(
            Write(left_side_calc_text),
            run_time=3.0
        )
        self.wait(sentence6_end - sentence6_start - 3.0)
        current_time = sentence6_end
        
        # Sentence 7: "B E squared equals fifteen squared equals two hundred twenty-five."
        sentence7_start = 30.31
        sentence7_end = 34.07
        wait_time = sentence7_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        right_side_calc_text = MathTex(r"BE^2 = 15^2 = 225", color=PINK, font_size=26)
        right_side_calc_text.to_edge(RIGHT, buff=1).shift(DOWN * 3.8)
        
        self.play(
            Write(right_side_calc_text),
            run_time=1.8
        )
        self.wait(sentence7_end - sentence7_start - 1.8)
        current_time = sentence7_end
        
        # Sentence 8: "Since C E squared plus B C squared equals B E squared, angle B C E is ninety degrees."
        sentence8_start = 34.08
        sentence8_end = 40.06
        wait_time = sentence8_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        conclusion_text = MathTex(r"225 = 225 \checkmark", color=GREEN, font_size=28, weight=BOLD)
        conclusion_text.to_edge(RIGHT, buff=1).shift(DOWN * 4.3)
        
        angle_bce_text = Text("∠BCE = 90°", color=ORANGE, font_size=26, weight=BOLD)
        angle_bce_text.to_edge(RIGHT, buff=1).shift(DOWN * 4.8)
        
        # Add right angle marker at C for triangle BCE
        angle_BCE = RightAngle(Line(C, B), Line(C, E), length=0.3, color=PURPLE)
        
        self.play(
            Write(conclusion_text),
            Write(angle_bce_text),
            Create(angle_BCE),
            Flash(angle_BCE, color=PURPLE, flash_radius=0.5),
            run_time=2.5
        )
        self.wait(sentence8_end - sentence8_start - 2.5)
        current_time = sentence8_end
        
        # Sentence 9: "Triangle B C E is a right-angled triangle at C."
        sentence9_start = 40.07
        sentence9_end = 43.31
        wait_time = sentence9_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        final_conclusion_text = Text("Triangle BCE is right-angled at C", color=PURPLE, font_size=26, weight=BOLD)
        final_conclusion_text.to_edge(RIGHT, buff=1).shift(DOWN * 5.3)
        
        self.play(
            Write(final_conclusion_text),
            Indicate(triangle_BCE, color=PURPLE, scale_factor=1.1),
            Indicate(angle_BCE, color=PURPLE, scale_factor=1.3),
            run_time=2.0
        )
        self.wait(sentence9_end - sentence9_start - 2.0)
        
        self.wait(1)