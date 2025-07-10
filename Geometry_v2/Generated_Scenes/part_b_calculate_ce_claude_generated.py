from manim import *

class PartBCalculateCe(Scene):
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
        
        # Angle arcs from previous scene
        angle_CAB = Arc(radius=0.4, start_angle=0, angle=PI/4, color=YELLOW, stroke_width=3)
        angle_CAB.move_arc_center_to(A)
        
        angle_DBA = Arc(radius=0.4, start_angle=PI*3/4, angle=PI/4, color=YELLOW, stroke_width=3)
        angle_DBA.move_arc_center_to(B)
        
        # Previous scene's final text elements
        part_b_title = Text("Part B: Pentagon Area", color=YELLOW, font_size=36, weight=BOLD)
        part_b_title.to_edge(UP).shift(RIGHT * 2)
        
        intro_text = Text("Finding BD and AC lengths:", color=GOLD, font_size=28, weight=BOLD)
        intro_text.to_edge(RIGHT, buff=1).shift(UP * 1.5)
        
        bd_composition_text = Text("BD is composed of BE and DE", color=LIGHT_BLUE, font_size=26)
        bd_composition_text.to_edge(RIGHT, buff=1).shift(UP * 0.8)
        
        congruence_reminder_text = Text("From congruence: AC = BD", color=ORANGE, font_size=26, weight=BOLD)
        congruence_reminder_text.to_edge(RIGHT, buff=1).shift(UP * 0.3)
        
        bd_equation_text = MathTex(r"BD = BE + DE", color=YELLOW, font_size=28)
        bd_equation_text.to_edge(RIGHT, buff=1).shift(DOWN * 0.2)
        
        bd_substitution_text = MathTex(r"BD = 15 + 9", color=LIGHT_GREEN, font_size=28)
        bd_substitution_text.to_edge(RIGHT, buff=1).shift(DOWN * 0.8)
        
        bd_result_text = MathTex(r"BD = 24 \text{ cm}", color=GREEN, font_size=30, weight=BOLD)
        bd_result_text.to_edge(RIGHT, buff=1).shift(DOWN * 1.4)
        
        ac_equals_bd_text = MathTex(r"AC = BD = 24 \text{ cm}", color=BLUE, font_size=30, weight=BOLD)
        ac_equals_bd_text.to_edge(RIGHT, buff=1).shift(DOWN * 2.0)
        
        final_summary_text = Text("Final Results:", color=GOLD, font_size=28, weight=BOLD)
        final_summary_text.to_edge(RIGHT, buff=1).shift(DOWN * 2.8)
        
        bd_final_text = Text("BD = 24 cm", color=GREEN, font_size=26)
        bd_final_text.to_edge(RIGHT, buff=1).shift(DOWN * 3.3)
        
        ac_final_text = Text("AC = 24 cm", color=BLUE, font_size=26)
        ac_final_text.to_edge(RIGHT, buff=1).shift(DOWN * 3.8)
        
        # Add all reconstructed elements instantly
        self.add(
            line_AB, line_AC, line_AD, line_BC, line_BD, line_AE, line_BE, line_CE,
            dot_A, dot_B, dot_C, dot_D, dot_E,
            label_A, label_B, label_C, label_D, label_E,
            angle_ACB, angle_ADB, angle_ADE,
            triangle_ABC, triangle_BAD, triangle_ADE, triangle_AEB,
            pentagon_ABCED,
            ad_length_label, de_length_label, ae_length_label, be_length_label,
            bd_length_label, ac_length_label,
            angle_CAB, angle_DBA,
            part_b_title, intro_text, bd_composition_text, congruence_reminder_text,
            bd_equation_text, bd_substitution_text, bd_result_text,
            ac_equals_bd_text, final_summary_text, bd_final_text, ac_final_text
        )
        
        #################################################################
        # PART 2: NEW ANIMATIONS for current scene
        #################################################################
        
        current_time = 0.0
        
        # Fade out previous text elements
        self.play(
            FadeOut(intro_text),
            FadeOut(bd_composition_text),
            FadeOut(congruence_reminder_text),
            FadeOut(bd_equation_text),
            FadeOut(bd_substitution_text),
            FadeOut(bd_result_text),
            FadeOut(ac_equals_bd_text),
            FadeOut(final_summary_text),
            FadeOut(bd_final_text),
            FadeOut(ac_final_text),
            run_time=1.0
        )
        current_time += 1.0
        
        # Sentence 1: "With A C known, we can now find the length of C E."
        sentence1_start = 0.0
        sentence1_end = 3.0
        wait_time = sentence1_start - (current_time - 1.0)
        if wait_time > 0:
            self.wait(wait_time)
        
        ce_intro_text = Text("Finding CE length:", color=GOLD, font_size=28, weight=BOLD)
        ce_intro_text.to_edge(RIGHT, buff=1).shift(UP * 1.5)
        
        self.play(
            Write(ce_intro_text),
            Indicate(line_CE, color=ORANGE, scale_factor=1.2),
            Indicate(ac_length_label, color=BLUE, scale_factor=1.3),
            run_time=2.0
        )
        self.wait(sentence1_end - sentence1_start - 2.0)
        current_time = sentence1_end
        
        # Sentence 2: "A C equals A E plus E C."
        sentence2_start = 3.01
        sentence2_end = 5.13
        wait_time = sentence2_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        ac_composition_text = Text("AC is composed of AE and EC", color=LIGHT_BLUE, font_size=26)
        ac_composition_text.to_edge(RIGHT, buff=1).shift(UP * 0.8)
        
        ac_equation_text = MathTex(r"AC = AE + EC", color=YELLOW, font_size=28)
        ac_equation_text.to_edge(RIGHT, buff=1).shift(UP * 0.3)
        
        self.play(
            Write(ac_composition_text),
            Write(ac_equation_text),
            Indicate(line_AE, color=CYAN, scale_factor=1.2),
            Indicate(line_CE, color=ORANGE, scale_factor=1.2),
            run_time=1.5
        )
        self.wait(sentence2_end - sentence2_start - 1.5)
        current_time = sentence2_end
        
        # Sentence 3: "Twenty-four equals fifteen plus E C."
        sentence3_start = 5.14
        sentence3_end = 7.54
        wait_time = sentence3_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        ac_substitution_text = MathTex(r"24 = 15 + EC", color=LIGHT_GREEN, font_size=28)
        ac_substitution_text.to_edge(RIGHT, buff=1).shift(DOWN * 0.2)
        
        self.play(
            Write(ac_substitution_text),
            Indicate(ac_length_label, color=BLUE, scale_factor=1.3),
            Indicate(ae_length_label, color=GREEN, scale_factor=1.3),
            run_time=1.8
        )
        self.wait(sentence3_end - sentence3_start - 1.8)
        current_time = sentence3_end
        
        # Sentence 4: "E C equals twenty-four minus fifteen."
        sentence4_start = 7.55
        sentence4_end = 9.88
        wait_time = sentence4_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        ec_calculation_text = MathTex(r"EC = 24 - 15", color=ORANGE, font_size=28)
        ec_calculation_text.to_edge(RIGHT, buff=1).shift(DOWN * 0.8)
        
        self.play(
            Write(ec_calculation_text),
            run_time=1.5
        )
        self.wait(sentence4_end - sentence4_start - 1.5)
        current_time = sentence4_end
        
        # Sentence 5: "E C equals nine centimeters."
        sentence5_start = 9.89
        sentence5_end = 11.74
        wait_time = sentence5_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        ec_result_text = MathTex(r"EC = 9 \text{ cm}", color=ORANGE, font_size=30, weight=BOLD)
        ec_result_text.to_edge(RIGHT, buff=1).shift(DOWN * 1.4)
        
        # Add CE length label to the diagram
        ce_length_label = MathTex("9", color=ORANGE, font_size=24).next_to(
            line_CE.get_center(), UP, buff=0.2
        )
        
        self.play(
            Write(ec_result_text),
            Write(ce_length_label),
            Flash(line_CE, color=ORANGE, flash_radius=0.8),
            run_time=1.3
        )
        self.wait(sentence5_end - sentence5_start - 1.3)
        current_time = sentence5_end
        
        # Sentence 6: "We found C E equals nine centimeters."
        sentence6_start = 11.75
        sentence6_end = 14.26
        wait_time = sentence6_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        ce_summary_text = Text("Result: CE = 9 cm", color=ORANGE, font_size=28, weight=BOLD)
        ce_summary_text.to_edge(RIGHT, buff=1).shift(DOWN * 2.0)
        
        verification_text = Text("Verification: AC = AE + EC", color=LIGHT_BLUE, font_size=24)
        verification_text.to_edge(RIGHT, buff=1).shift(DOWN * 2.6)
        
        verification_calc_text = MathTex(r"24 = 15 + 9 \checkmark", color=GREEN, font_size=26)
        verification_calc_text.to_edge(RIGHT, buff=1).shift(DOWN * 3.1)
        
        self.play(
            Write(ce_summary_text),
            Write(verification_text),
            Write(verification_calc_text),
            Indicate(ce_length_label, color=ORANGE, scale_factor=1.3),
            run_time=2.0
        )
        self.wait(sentence6_end - sentence6_start - 2.0)
        
        self.wait(1)