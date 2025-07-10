from manim import *

class PartBCalculateBdAndAc(Scene):
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
        
        # Angle arcs from previous scene
        angle_CAB = Arc(radius=0.4, start_angle=0, angle=PI/4, color=YELLOW, stroke_width=3)
        angle_CAB.move_arc_center_to(A)
        
        angle_DBA = Arc(radius=0.4, start_angle=PI*3/4, angle=PI/4, color=YELLOW, stroke_width=3)
        angle_DBA.move_arc_center_to(B)
        
        # Previous scene's final text elements
        part_b_title = Text("Part B: Pentagon Area", color=YELLOW, font_size=36, weight=BOLD)
        part_b_title.to_edge(UP).shift(RIGHT * 2)
        
        congruence_text = Text("Using congruence from Part A:", color=GOLD, font_size=28, weight=BOLD)
        congruence_text.to_edge(RIGHT, buff=1).shift(UP * 1.5)
        
        congruent_text = MathTex(r"\triangle ABC \cong \triangle BAD", color=LIGHT_BLUE, font_size=28)
        congruent_text.to_edge(RIGHT, buff=1).shift(UP * 0.8)
        
        corresponding_angles_text = Text("Corresponding angles are equal", color=LIGHT_BLUE, font_size=24)
        corresponding_angles_text.to_edge(RIGHT, buff=1).shift(UP * 0.3)
        
        angle_equality_text = MathTex(r"\angle CAB = \angle DBA", color=YELLOW, font_size=28)
        angle_equality_text.to_edge(RIGHT, buff=1).shift(DOWN * 0.2)
        
        triangle_aeb_text = Text("In triangle AEB:", color=PINK, font_size=26, weight=BOLD)
        triangle_aeb_text.to_edge(RIGHT, buff=1).shift(DOWN * 0.8)
        
        angle_explanation_text = Text("∠EAB = ∠CAB\n∠EBA = ∠DBA", 
                                    color=PINK, font_size=24, line_spacing=1.2)
        angle_explanation_text.to_edge(RIGHT, buff=1).shift(DOWN * 1.4)
        
        isosceles_conclusion_text = Text("∠EAB = ∠EBA", color=ORANGE, font_size=26, weight=BOLD)
        isosceles_conclusion_text.to_edge(RIGHT, buff=1).shift(DOWN * 2.2)
        
        isosceles_text = Text("Therefore: △AEB is isosceles", color=ORANGE, font_size=26, weight=BOLD)
        isosceles_text.to_edge(RIGHT, buff=1).shift(DOWN * 2.8)
        
        summary_text1 = Text("Summary:", color=GOLD, font_size=28, weight=BOLD)
        summary_text1.to_edge(RIGHT, buff=1).shift(DOWN * 3.4)
        
        summary_equation1 = MathTex(r"\triangle ABC \cong \triangle BAD \Rightarrow \angle CAB = \angle DBA", 
                                   color=WHITE, font_size=24)
        summary_equation1.to_edge(RIGHT, buff=1).shift(DOWN * 3.9)
        
        summary_equation2 = MathTex(r"\text{In } \triangle AEB: \angle EAB = \angle EBA", 
                                   color=PINK, font_size=24)
        summary_equation2.to_edge(RIGHT, buff=1).shift(DOWN * 4.4)
        
        final_conclusion_text = MathTex(r"\triangle AEB \text{ is isosceles} \Rightarrow AE = BE", 
                                       color=GREEN, font_size=26)
        final_conclusion_text.to_edge(RIGHT, buff=1).shift(DOWN * 4.9)
        
        final_result_text = Text("Result: BE = 15 cm", color=GREEN, font_size=28, weight=BOLD)
        final_result_text.to_edge(RIGHT, buff=1).shift(DOWN * 5.4)
        
        # Add all reconstructed elements instantly
        self.add(
            line_AB, line_AC, line_AD, line_BC, line_BD, line_AE, line_BE,
            dot_A, dot_B, dot_C, dot_D, dot_E,
            label_A, label_B, label_C, label_D, label_E,
            angle_ACB, angle_ADB, angle_ADE,
            triangle_ABC, triangle_BAD, triangle_ADE, triangle_AEB,
            pentagon_ABCED,
            ad_length_label, de_length_label, ae_length_label, be_length_label,
            angle_CAB, angle_DBA,
            part_b_title, congruence_text, congruent_text, corresponding_angles_text,
            angle_equality_text, triangle_aeb_text, angle_explanation_text,
            isosceles_conclusion_text, isosceles_text, summary_text1,
            summary_equation1, summary_equation2, final_conclusion_text, final_result_text
        )
        
        #################################################################
        # PART 2: NEW ANIMATIONS for current scene
        #################################################################
        
        current_time = 0.0
        
        # Fade out previous text elements
        self.play(
            FadeOut(congruence_text),
            FadeOut(congruent_text),
            FadeOut(corresponding_angles_text),
            FadeOut(angle_equality_text),
            FadeOut(triangle_aeb_text),
            FadeOut(angle_explanation_text),
            FadeOut(isosceles_conclusion_text),
            FadeOut(isosceles_text),
            FadeOut(summary_text1),
            FadeOut(summary_equation1),
            FadeOut(summary_equation2),
            FadeOut(final_conclusion_text),
            FadeOut(final_result_text),
            run_time=1.0
        )
        current_time += 1.0
        
        # Sentence 1: "We now have enough information to find the length of B D and A C."
        sentence1_start = 0.0
        sentence1_end = 3.66
        wait_time = sentence1_start - (current_time - 1.0)
        if wait_time > 0:
            self.wait(wait_time)
        
        intro_text = Text("Finding BD and AC lengths:", color=GOLD, font_size=28, weight=BOLD)
        intro_text.to_edge(RIGHT, buff=1).shift(UP * 1.5)
        
        self.play(
            Write(intro_text),
            Indicate(line_BD, color=BLUE, scale_factor=1.2),
            Indicate(line_AC, color=BLUE, scale_factor=1.2),
            run_time=2.0
        )
        self.wait(sentence1_end - sentence1_start - 2.0)
        current_time = sentence1_end
        
        # Sentence 2: "We know B D is composed of B E and D E."
        sentence2_start = 3.67
        sentence2_end = 6.18
        wait_time = sentence2_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        bd_composition_text = Text("BD is composed of BE and DE", color=LIGHT_BLUE, font_size=26)
        bd_composition_text.to_edge(RIGHT, buff=1).shift(UP * 0.8)
        
        self.play(
            Write(bd_composition_text),
            Indicate(line_BE, color=PINK, scale_factor=1.2),
            Indicate(Line(D, E), color=YELLOW, scale_factor=1.2),
            run_time=1.5
        )
        self.wait(sentence2_end - sentence2_start - 1.5)
        current_time = sentence2_end
        
        # Sentence 3: "Also, from the congruence in part A, we know that A C equals B D."
        sentence3_start = 6.19
        sentence3_end = 10.37
        wait_time = sentence3_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        congruence_reminder_text = Text("From congruence: AC = BD", color=ORANGE, font_size=26, weight=BOLD)
        congruence_reminder_text.to_edge(RIGHT, buff=1).shift(UP * 0.3)
        
        self.play(
            Write(congruence_reminder_text),
            Flash(triangle_ABC, color=BLUE, flash_radius=0.8),
            Flash(triangle_BAD, color=RED, flash_radius=0.8),
            run_time=2.5
        )
        self.wait(sentence3_end - sentence3_start - 2.5)
        current_time = sentence3_end
        
        # Sentence 4: "B D equals B E plus D E."
        sentence4_start = 10.38
        sentence4_end = 12.47
        wait_time = sentence4_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        bd_equation_text = MathTex(r"BD = BE + DE", color=YELLOW, font_size=28)
        bd_equation_text.to_edge(RIGHT, buff=1).shift(DOWN * 0.2)
        
        self.play(
            Write(bd_equation_text),
            run_time=1.2
        )
        self.wait(sentence4_end - sentence4_start - 1.2)
        current_time = sentence4_end
        
        # Sentence 5: "B D equals fifteen centimeters plus nine centimeters."
        sentence5_start = 12.48
        sentence5_end = 15.67
        wait_time = sentence5_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        bd_substitution_text = MathTex(r"BD = 15 + 9", color=LIGHT_GREEN, font_size=28)
        bd_substitution_text.to_edge(RIGHT, buff=1).shift(DOWN * 0.8)
        
        self.play(
            Write(bd_substitution_text),
            Indicate(be_length_label, color=GREEN, scale_factor=1.3),
            Indicate(de_length_label, color=YELLOW, scale_factor=1.3),
            run_time=2.0
        )
        self.wait(sentence5_end - sentence5_start - 2.0)
        current_time = sentence5_end
        
        # Sentence 6: "B D equals twenty-four centimeters."
        sentence6_start = 15.68
        sentence6_end = 17.95
        wait_time = sentence6_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        bd_result_text = MathTex(r"BD = 24 \text{ cm}", color=GREEN, font_size=30, weight=BOLD)
        bd_result_text.to_edge(RIGHT, buff=1).shift(DOWN * 1.4)
        
        # Add BD length label to the diagram
        bd_length_label = MathTex("24", color=GREEN, font_size=24).next_to(
            line_BD.get_center(), UP, buff=0.2
        )
        
        self.play(
            Write(bd_result_text),
            Write(bd_length_label),
            Flash(line_BD, color=GREEN, flash_radius=0.8),
            run_time=1.5
        )
        self.wait(sentence6_end - sentence6_start - 1.5)
        current_time = sentence6_end
        
        # Sentence 7: "Since A C equals B D, then A C also equals twenty-four centimeters."
        sentence7_start = 17.96
        sentence7_end = 22.56
        wait_time = sentence7_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        ac_equals_bd_text = MathTex(r"AC = BD = 24 \text{ cm}", color=BLUE, font_size=30, weight=BOLD)
        ac_equals_bd_text.to_edge(RIGHT, buff=1).shift(DOWN * 2.0)
        
        # Add AC length label to the diagram
        ac_length_label = MathTex("24", color=BLUE, font_size=24).next_to(
            line_AC.get_center(), LEFT, buff=0.2
        )
        
        self.play(
            Write(ac_equals_bd_text),
            Write(ac_length_label),
            Flash(line_AC, color=BLUE, flash_radius=0.8),
            run_time=2.5
        )
        self.wait(sentence7_end - sentence7_start - 2.5)
        current_time = sentence7_end
        
        # Sentence 8: "B D equals twenty-four centimeters, and A C also equals twenty-four centimeters."
        sentence8_start = 22.57
        sentence8_end = 27.25
        wait_time = sentence8_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        final_summary_text = Text("Final Results:", color=GOLD, font_size=28, weight=BOLD)
        final_summary_text.to_edge(RIGHT, buff=1).shift(DOWN * 2.8)
        
        bd_final_text = Text("BD = 24 cm", color=GREEN, font_size=26)
        bd_final_text.to_edge(RIGHT, buff=1).shift(DOWN * 3.3)
        
        ac_final_text = Text("AC = 24 cm", color=BLUE, font_size=26)
        ac_final_text.to_edge(RIGHT, buff=1).shift(DOWN * 3.8)
        
        self.play(
            Write(final_summary_text),
            Write(bd_final_text),
            Write(ac_final_text),
            Indicate(bd_length_label, color=GREEN, scale_factor=1.3),
            Indicate(ac_length_label, color=BLUE, scale_factor=1.3),
            run_time=2.5
        )
        self.wait(sentence8_end - sentence8_start - 2.5)
        
        self.wait(1)