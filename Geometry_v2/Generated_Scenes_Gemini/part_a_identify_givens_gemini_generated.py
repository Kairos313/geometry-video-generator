# Final Manim code for the scene.
from manim import *

class PartAIdentifyGivens(Scene):
    def construct(self):
        # 1. Scene Setup
        self.camera.background_color = "#1E293B"

        # JSON Timings from current_step_json
        s = [
            {"start": 0.0, "end": 5.62},
            {"start": 5.63, "end": 11.25},
            {"start": 11.26, "end": 18.13},
            {"start": 18.14, "end": 20.49},
            {"start": 20.50, "end": 24.81},
            {"start": 24.82, "end": 29.60}
        ]

        #################################################################
        # PART 1: INSTANT RECONSTRUCTION of the previous scene's final state
        #################################################################

        # Coordinates
        A = [-5.5, -2, 0]
        B = [-0.5, -2, 0]
        C = [-1.5, 0.5, 0]
        D = [-4.5, 0.5, 0]
        E = [-3.0, -0.5, 0]

        # Colors
        c_blue = "#58C4DD"
        c_green = "#87C2A5"
        c_orange = "#F07E48"
        c_yellow = "#E2D28B"
        c_gold = "#FFD700"
        c_white = "#FFFFFF"

        # Diagram Mobjects
        # Polygons for colored strokes and fill animations
        tri_ABC = Polygon(A, B, C, color=c_orange, fill_opacity=0, stroke_width=3.5)
        tri_BAD = Polygon(B, A, D, color=c_blue, fill_opacity=0, stroke_width=3.5)
        
        # Underlying white lines for the complete figure
        line_AC = Line(A, C, color=c_white)
        line_BD = Line(B, D, color=c_white)
        line_AB = Line(A, B, color=c_white)

        # Labels, dots, and annotations
        labels = VGroup(
            MathTex("A", color=c_white).next_to(A, DOWN, buff=0.2),
            MathTex("B", color=c_white).next_to(B, DOWN, buff=0.2),
            MathTex("C", color=c_white).next_to(C, UP, buff=0.2),
            MathTex("D", color=c_white).next_to(D, UP, buff=0.2),
            MathTex("E", color=c_yellow).scale(0.8).next_to(E, DOWN, buff=0.1)
        )
        dots = VGroup(Dot(A), Dot(B), Dot(C), Dot(D), Dot(E, color=c_yellow))
        angle_C = RightAngle(Line(C, B), Line(C, A), length=0.4, color=c_green, stroke_width=3)
        angle_D = RightAngle(Line(D, A), Line(D, B), length=0.4, color=c_green, stroke_width=3)
        tick_AD = MathTex(r"\prime", color=c_green).scale(1.8).move_to(Line(A, D).get_center()).rotate(Line(A, D).get_angle() + PI/2)
        tick_BC = MathTex(r"\prime", color=c_green).scale(1.8).move_to(Line(B, C).get_center()).rotate(Line(B, C).get_angle() + PI/2)
        
        # Group all diagram components to match previous scene's structure
        diagram = VGroup(line_AB, line_AC, line_BD, tri_ABC, tri_BAD, labels, dots, angle_C, angle_D, tick_AD, tick_BC)

        # Previous scene's text mobjects, positioned absolutely
        text_anchor = [4.5, 2.0, 0]
        goal_title = Text("Goal: Part (a)", color=c_yellow, weight=BOLD).scale(0.8)
        goal_title.move_to([text_anchor[0], text_anchor[1] + 1.2, 0])
        goal_statement = MathTex(r"\text{Prove: }", r"\triangle ABC", r"\cong", r"\triangle BAD").scale(1.1)
        goal_statement.next_to(goal_title, DOWN, buff=0.5)
        goal_statement[1].set_color(c_orange)
        goal_statement[3].set_color(c_blue)
        
        previous_text_group = VGroup(goal_title, goal_statement)

        # Add all reconstructed mobjects to the scene instantly
        self.add(diagram, previous_text_group)
        
        #################################################################
        # PART 2: NEW ANIMATIONS for the current scene
        #################################################################

        current_time = 0.0

        # S1 (0.0 - 5.62): Transition from "Goal" to "Givens"
        wait_time = s[0]['start'] - current_time
        if wait_time > 0: self.wait(wait_time)
        
        new_title = Text("Givens:", color=c_yellow, weight=BOLD).scale(0.8).move_to(goal_title.get_center())
        
        self.play(
            FadeOut(previous_text_group, shift=UP),
            FadeIn(new_title, shift=UP),
            run_time=1.5
        )
        self.wait(s[0]['end'] - (s[0]['start'] + 1.5))
        current_time = s[0]['end']

        # Define text for the list of givens
        given1_text = MathTex(r"\text{1. } \angle ACB = \angle ADB = 90^\circ", color=c_white).scale(0.8)
        given2_text = MathTex(r"\text{2. } AD = BC", color=c_white).scale(0.8)
        given3_text = MathTex(r"\text{3. } AB \text{ is common}", color=c_white).scale(0.8)

        givens_vgroup = VGroup(given1_text, given2_text, given3_text).arrange(
            DOWN, buff=0.4, aligned_edge=LEFT
        ).next_to(new_title, DOWN, buff=0.5)

        # S2 (5.63 - 11.25): Write first given (angles)
        wait_time = s[1]['start'] - current_time
        if wait_time > 0: self.wait(wait_time)
        
        self.play(
            Write(given1_text),
            Indicate(VGroup(angle_C, angle_D), color=c_green, scale_factor=1.5),
            run_time=2.0
        )
        self.wait(s[1]['end'] - (s[1]['start'] + 2.0))
        current_time = s[1]['end']

        # S3 (11.26 - 18.13): Explain right-angled triangles
        wait_time = s[2]['start'] - current_time
        if wait_time > 0: self.wait(wait_time)
        
        anim_start_time = s[2]['start']
        self.wait(1.5) # Wait for "triangle ABC" in narration
        self.play(Flash(tri_ABC, color=c_orange, flash_radius=1.5, line_length=0.5), run_time=1.5)
        self.wait(1.5) # Wait for "triangle BAD" in narration
        self.play(Flash(tri_BAD, color=c_blue, flash_radius=1.5, line_length=0.5), run_time=1.5)
        
        total_anim_duration = 1.5 + 1.5 + 1.5 + 1.5
        self.wait(s[2]['end'] - (anim_start_time + total_anim_duration))
        current_time = s[2]['end']

        # S4 (18.14 - 20.49): Write second given (sides)
        wait_time = s[3]['start'] - current_time
        if wait_time > 0: self.wait(wait_time)

        side_AD_line = Line(A, D)
        side_BC_line = Line(B, C)
        
        self.play(
            Write(given2_text),
            Indicate(VGroup(side_AD_line, tick_AD), color=c_gold),
            Indicate(VGroup(side_BC_line, tick_BC), color=c_gold),
            run_time=2.0
        )
        self.wait(s[3]['end'] - (s[3]['start'] + 2.0))
        current_time = s[3]['end']

        # S5 (20.50 - 24.81): Write third given (common side)
        wait_time = s[4]['start'] - current_time
        if wait_time > 0: self.wait(wait_time)

        self.play(
            Write(given3_text),
            run_time=1.5
        )
        self.play(
            Indicate(line_AB, color=c_gold, scale_factor=1.1),
            run_time=1.5
        )
        self.wait(s[4]['end'] - (s[4]['start'] + 1.5 + 1.5))
        current_time = s[4]['end']

        # S6 (24.82 - 29.60): Summary of givens
        wait_time = s[5]['start'] - current_time
        if wait_time > 0: self.wait(wait_time)
        
        self.play(Indicate(VGroup(angle_C, angle_D), color=c_green, scale_factor=1.5), run_time=1.5) # "two right angles"
        self.wait(0.2)
        self.play(Indicate(VGroup(side_AD_line, tick_AD, side_BC_line, tick_BC), color=c_green), run_time=1.5) # "one pair of equal sides"
        self.wait(0.2)
        self.play(Indicate(line_AB, color=c_gold), run_time=1.3) # "and a common hypotenuse"
        
        total_s6_anim_time = 1.5 + 0.2 + 1.5 + 0.2 + 1.3
        self.wait(s[5]['end'] - (s[5]['start'] + total_s6_anim_time))

        # Final pause
        self.wait(2)