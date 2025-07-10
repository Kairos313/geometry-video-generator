from manim import *

class PartAUnderstandGoal(Scene):
    def construct(self):
        # 1. Scene Setup
        self.camera.background_color = "#1E293B"

        # 2. Diagram Coordinates & Mobject Definition
        # Coordinates are calculated to ensure geometric properties are met:
        # - Angle ACB = Angle ADB = 90 degrees (C and D are on a circle with diameter AB)
        # - AD = BC (C and D are symmetric across the perpendicular bisector of AB)
        A = [-5.5, -2, 0]
        B = [-0.5, -2, 0]
        C = [-1.5, 0.5, 0]
        D = [-4.5, 0.5, 0]
        # Intersection E is not needed for this scene's goal but is defined for completeness
        # Line AC: y - A[1] = m_AC * (x - A[0])
        # Line BD: y - B[1] = m_BD * (x - B[0])
        # Solving the system of equations gives E.
        E = [-3.0, -0.5, 0]

        # Define colors from the palette
        c_blue = "#58C4DD"
        c_green = "#87C2A5"
        c_orange = "#F07E48"
        c_yellow = "#E2D28B"
        c_gold = "#FFD700"
        c_white = "#FFFFFF"

        # Define mobjects for the diagram
        tri_ABC = Polygon(A, B, C, color=c_orange, fill_opacity=0, stroke_width=3.5)
        tri_BAD = Polygon(B, A, D, color=c_blue, fill_opacity=0, stroke_width=3.5)
        
        line_AC = Line(A, C, color=c_white)
        line_BD = Line(B, D, color=c_white)
        line_AB = Line(A, B, color=c_white)

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
        
        # Given side equality ticks
        tick_AD = MathTex(r"\prime", color=c_green).scale(1.8).move_to(Line(A, D).get_center()).rotate(Line(A, D).get_angle() + PI/2)
        tick_BC = MathTex(r"\prime", color=c_green).scale(1.8).move_to(Line(B, C).get_center()).rotate(Line(B, C).get_angle() + PI/2)
        
        diagram = VGroup(line_AB, line_AC, line_BD, tri_ABC, tri_BAD, labels, dots, angle_C, angle_D, tick_AD, tick_BC)

        # 3. Explanatory Text Definition (TEXT ON RIGHT)
        # Position reference
        text_anchor = [4.5, 2.0, 0]

        intro_text = Text(
            "Our first step is to understand\nwhat we need to prove.",
            font_size=32,
            color=c_white,
            line_spacing=1.2
        ).move_to(text_anchor)

        goal_title = Text("Goal: Part (a)", color=c_yellow, weight=BOLD).scale(0.8)
        goal_title.move_to([text_anchor[0], text_anchor[1] + 1.2, 0])

        goal_statement = MathTex(
            r"\text{Prove: }", r"\triangle ABC", r"\cong", r"\triangle BAD"
        ).scale(1.1)
        goal_statement.next_to(goal_title, DOWN, buff=0.5)
        goal_statement[1].set_color(c_orange)
        goal_statement[3].set_color(c_blue)
        
        # 4. Synchronized Narration & Animation
        # Sentence timings from JSON
        s1 = {"start": 0.0, "end": 3.24}
        s2 = {"start": 3.25, "end": 7.19}
        s3 = {"start": 7.2, "end": 10.86}
        s4 = {"start": 10.87, "end": 14.76}

        # Initial state: Diagram is visible
        self.add(diagram)
        
        # Sentence 1: "For part A, our first step is to understand what we need to prove."
        self.play(Write(intro_text), run_time=(s1['end'] - s1['start']))
        self.wait(s2['start'] - s1['end'])

        # Sentence 2: "We need to show that triangle A B C is congruent to triangle B A D."
        s2_duration = s2['end'] - s2['start']
        self.play(FadeOut(intro_text, shift=UP), run_time=0.75)
        self.play(
            AnimationGroup(
                Write(goal_statement),
                Indicate(tri_ABC, color=c_orange, scale_factor=1.1),
                Indicate(tri_BAD, color=c_blue, scale_factor=1.1),
                lag_ratio=0.5
            ),
            run_time=(s2_duration - 0.75)
        )
        self.wait(s3['start'] - s2['end'])
        
        # Sentence 3: "Goal: Prove triangle A B C is congruent to triangle B A D."
        s3_duration = s3['end'] - s3['start']
        self.play(Write(goal_title), run_time=1.5)
        self.play(Circumscribe(goal_statement, color=c_gold, fade_out=True), run_time=(s3_duration - 1.5))
        self.wait(s4['start'] - s3['end'])
        
        # Sentence 4: "Our objective is to demonstrate the congruence of the two triangles."
        s4_duration = s4['end'] - s4['start']
        self.play(
            tri_ABC.animate.set_fill(c_orange, opacity=0.6),
            tri_BAD.animate.set_fill(c_blue, opacity=0.6),
            run_time=1.5
        )
        self.play(
            tri_ABC.animate.set_fill(opacity=0),
            tri_BAD.animate.set_fill(opacity=0),
            run_time=1.5
        )
        self.wait(s4_duration - 3.0)

        # Final pause
        self.wait(2)