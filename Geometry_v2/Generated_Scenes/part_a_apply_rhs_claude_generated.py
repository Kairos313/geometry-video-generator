from manim import *

LIGHT_BLUE = "#ADD8E6"

class PartAApplyRhs(Scene):
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
        
        # Recreate previous scene's text elements
        new_title = Text("Given Information", color=YELLOW, font_size=36)
        new_title.to_edge(UP).shift(RIGHT * 2)
        
        intro_text = Text("Let's identify the given information\nthat will help us prove congruence:", 
                         color=WHITE, font_size=24, line_spacing=1.2)
        intro_text.to_edge(RIGHT, buff=1).shift(UP * 1.5)
        
        given1_text = VGroup(
            Text("Given 1:", color=GOLD, font_size=28),
            MathTex(r"\angle ACB = \angle ADB = 90°", color=WHITE, font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        given1_text.to_edge(RIGHT, buff=1).shift(UP * 0.5)
        
        explanation_text = Text("Both triangles are right-angled\nat C and D respectively", 
                               color=LIGHT_BLUE, font_size=22, line_spacing=1.2)
        explanation_text.to_edge(RIGHT, buff=1).shift(UP * 0.0)
        
        given2_text = VGroup(
            Text("Given 2:", color=GOLD, font_size=28),
            MathTex(r"AD = BC", color=WHITE, font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        given2_text.to_edge(RIGHT, buff=1).shift(DOWN * 0.8)
        
        common_side_text = VGroup(
            Text("Common Side:", color=GOLD, font_size=28),
            MathTex(r"AB \text{ is shared}", color=WHITE, font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        common_side_text.to_edge(RIGHT, buff=1).shift(DOWN * 1.8)
        
        summary_text = Text("Summary: Two right angles,\nequal sides, common hypotenuse", 
                           color=YELLOW, font_size=22, line_spacing=1.2)
        summary_text.to_edge(RIGHT, buff=1).shift(DOWN * 2.8)
        
        # Add all reconstructed elements instantly
        self.add(
            line_AB, line_AC, line_AD, line_BC, line_BD,
            dot_A, dot_B, dot_C, dot_D, dot_E,
            label_A, label_B, label_C, label_D, label_E,
            angle_ACB, angle_ADB,
            triangle_ABC, triangle_BAD,
            new_title, intro_text, given1_text, explanation_text,
            given2_text, common_side_text, summary_text
        )
        
        #################################################################
        # PART 2: NEW ANIMATIONS for current scene
        #################################################################
        
        current_time = 0.0
        
        # Fade out previous text elements
        self.play(
            FadeOut(new_title),
            FadeOut(intro_text),
            FadeOut(given1_text),
            FadeOut(explanation_text),
            FadeOut(given2_text),
            FadeOut(common_side_text),
            FadeOut(summary_text),
            run_time=1.0
        )
        current_time += 1.0
        
        # Sentence 1: "Now, let's apply a congruence criterion."
        sentence1_start = 0.0
        sentence1_end = 2.22
        wait_time = sentence1_start - (current_time - 1.0)
        if wait_time > 0:
            self.wait(wait_time)
        
        rhs_title = Text("Applying RHS Congruence Criterion", color=YELLOW, font_size=36)
        rhs_title.to_edge(UP).shift(RIGHT * 2)
        
        intro_rhs_text = Text("Let's apply the RHS congruence theorem\nto prove triangle congruence:", 
                             color=WHITE, font_size=24, line_spacing=1.2)
        intro_rhs_text.to_edge(RIGHT, buff=1).shift(UP * 1.5)
        
        self.play(
            Write(rhs_title),
            Write(intro_rhs_text),
            run_time=1.5
        )
        self.wait(sentence1_end - sentence1_start - 1.5)
        current_time = sentence1_end
        
        # Sentence 2: "Since we have a right angle, a hypotenuse, and a corresponding side..."
        sentence2_start = 2.23
        sentence2_end = 11.61
        wait_time = sentence2_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        rhs_explanation = Text("RHS Theorem: If a right angle, hypotenuse,\nand one side are equal in two triangles,\nthen the triangles are congruent.", 
                              color=LIGHT_BLUE, font_size=22, line_spacing=1.2)
        rhs_explanation.to_edge(RIGHT, buff=1).shift(UP * 0.5)
        
        self.play(
            Write(rhs_explanation),
            run_time=2.5
        )
        self.wait(sentence2_end - sentence2_start - 2.5)
        current_time = sentence2_end
        
        # Sentence 3: "In triangle ABC and triangle BAD: 1. Angle ACB equals angle ADB..."
        sentence3_start = 11.62
        sentence3_end = 23.87
        wait_time = sentence3_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        condition1_text = VGroup(
            Text("Condition 1 (Right Angle):", color=GOLD, font_size=26),
            MathTex(r"\angle ACB = \angle ADB = 90°", color=WHITE, font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        condition1_text.to_edge(RIGHT, buff=1).shift(DOWN * 0.2)
        
        self.play(
            Write(condition1_text),
            Indicate(angle_ACB, color=ORANGE, scale_factor=1.4),
            Indicate(angle_ADB, color=ORANGE, scale_factor=1.4),
            run_time=3.0
        )
        self.wait(sentence3_end - sentence3_start - 3.0)
        current_time = sentence3_end
        
        # Sentence 4: "2. Side AB equals side BA (Common hypotenuse)."
        sentence4_start = 23.88
        sentence4_end = 27.48
        wait_time = sentence4_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        condition2_text = VGroup(
            Text("Condition 2 (Hypotenuse):", color=GOLD, font_size=26),
            MathTex(r"AB = BA \text{ (common)}", color=WHITE, font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        condition2_text.to_edge(RIGHT, buff=1).shift(DOWN * 1.0)
        
        self.play(
            Write(condition2_text),
            Indicate(line_AB, color=WHITE, scale_factor=1.3),
            run_time=2.0
        )
        self.wait(sentence4_end - sentence4_start - 2.0)
        current_time = sentence4_end
        
        # Sentence 5: "3. Side BC equals side AD (Given side)."
        sentence5_start = 27.49
        sentence5_end = 30.65
        wait_time = sentence5_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        condition3_text = VGroup(
            Text("Condition 3 (Side):", color=GOLD, font_size=26),
            MathTex(r"BC = AD \text{ (given)}", color=WHITE, font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        condition3_text.to_edge(RIGHT, buff=1).shift(DOWN * 1.8)
        
        self.play(
            Write(condition3_text),
            Indicate(line_BC, color=GREEN, scale_factor=1.3),
            Indicate(line_AD, color=GREEN, scale_factor=1.3),
            run_time=2.0
        )
        self.wait(sentence5_end - sentence5_start - 2.0)
        current_time = sentence5_end
        
        # Sentence 6: "Therefore, by RHS congruence theorem, triangle ABC is congruent to triangle BAD."
        sentence6_start = 30.66
        sentence6_end = 36.59
        wait_time = sentence6_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        conclusion_text = VGroup(
            Text("Therefore, by RHS:", color=GOLD, font_size=28),
            MathTex(r"\triangle ABC \cong \triangle BAD", color=YELLOW, font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        conclusion_text.to_edge(RIGHT, buff=1).shift(DOWN * 2.8)
        
        self.play(
            Write(conclusion_text),
            Flash(triangle_ABC, color=BLUE, flash_radius=0.6),
            Flash(triangle_BAD, color=RED, flash_radius=0.6),
            run_time=2.5
        )
        self.wait(sentence6_end - sentence6_start - 2.5)
        current_time = sentence6_end
        
        # Sentence 7: "We have successfully proven that triangle ABC is congruent to triangle BAD..."
        sentence7_start = 36.6
        sentence7_end = 43.73
        wait_time = sentence7_start - current_time
        if wait_time > 0:
            self.wait(wait_time)
        
        success_text = Text("✓ Proof Complete!", color=GREEN, font_size=32, weight=BOLD)
        success_text.to_edge(RIGHT, buff=1).shift(DOWN * 3.5)
        
        self.play(
            Write(success_text),
            Flash(conclusion_text[1], color=YELLOW, flash_radius=0.5),
            run_time=2.0
        )
        self.wait(sentence7_end - sentence7_start - 2.0)
        
        self.wait(1)