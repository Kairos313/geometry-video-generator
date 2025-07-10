from manim import *

class PartAUnderstandGoal(Scene):
    def construct(self):
        # Set background color to match 3Blue1Brown style
        self.camera.background_color = "#1E293B"
        
        # ============== DIAGRAM CONSTRUCTION (LEFT SIDE) ==============
        # Define coordinates for the geometric diagram (all x-values negative)
        A = np.array([-5.0, -0.5, 0])
        B = np.array([-1.0, -0.5, 0])
        C = np.array([-3.0, 1.5, 0])
        D = np.array([-3.0, -2.5, 0])
        
        # Create triangles with distinct colors
        triangle_ABC = Polygon(A, B, C, 
                              color="#58C4DD", 
                              fill_opacity=0.4, 
                              stroke_width=4)
        triangle_BAD = Polygon(B, A, D, 
                              color="#F07E48", 
                              fill_opacity=0.4, 
                              stroke_width=4)
        
        # Create points and labels
        dot_A = Dot(A, color="#FFFFFF", radius=0.08)
        dot_B = Dot(B, color="#FFFFFF", radius=0.08)
        dot_C = Dot(C, color="#FFFFFF", radius=0.08)
        dot_D = Dot(D, color="#FFFFFF", radius=0.08)
        
        label_A = MathTex("A", color="#FFFFFF").next_to(A, DOWN, buff=0.15)
        label_B = MathTex("B", color="#FFFFFF").next_to(B, DOWN, buff=0.15)
        label_C = MathTex("C", color="#FFFFFF").next_to(C, UP, buff=0.15)
        label_D = MathTex("D", color="#FFFFFF").next_to(D, DOWN, buff=0.15)
        
        # Create shared side AB
        side_AB = Line(A, B, color="#E2D28B", stroke_width=6)
        
        # Group diagram elements
        diagram = VGroup(
            triangle_ABC, triangle_BAD, 
            dot_A, dot_B, dot_C, dot_D,
            label_A, label_B, label_C, label_D,
            side_AB
        ).scale(0.9).to_edge(LEFT, buff=1.0)
        
        # ============== TEXT CONTENT (RIGHT SIDE) ==============
        # Title (top-right position)
        title = Text("Part A: Understand the Goal", 
                    color="#E2D28B", 
                    font_size=36).move_to([3.5, 3.2, 0])
        
        # Create text blocks with precise positioning
        text0 = Text("For part A, our first step is to understand", 
                    t2c={"understand": "#87C2A5"}, 
                    font_size=28,
                    line_spacing=0.8).move_to([3.5, 2.2, 0])
        text0_sub = Text("what we need to prove.", 
                        font_size=28,
                        line_spacing=0.8).next_to(text0, DOWN, aligned_edge=LEFT)
        
        text1 = Text("We need to show that triangle ABC", 
                    t2c={"triangle ABC": "#58C4DD"}, 
                    font_size=28,
                    line_spacing=0.8).move_to([3.5, 0.4, 0])
        text1_sub = Text("is congruent to triangle BAD", 
                        t2c={"triangle BAD": "#F07E48"}, 
                        font_size=28,
                        line_spacing=0.8).next_to(text1, DOWN, aligned_edge=LEFT)
        
        # Goal statement with highlight
        goal_text = Text("Goal:", 
                        weight=BOLD, 
                        color="#FFD700", 
                        font_size=32).move_to([3.5, -1.4, 0])
        goal_content = MathTex(r"\triangle ABC \cong \triangle BAD", 
                            color="#FFFFFF", 
                            font_size=38).next_to(goal_text, DOWN, buff=0.3)
        
        # Apply color to triangle symbols to match diagram
        goal_content[0][:2].set_color("#58C4DD")  # ABC
        goal_content[0][3:5].set_color("#F07E48")  # BAD
        goal_content[0][2].set_color("#FFFFFF")    # Congruence symbol
        
        # Final objective statement
        text3 = Text("Our objective is to demonstrate", 
                    font_size=28,
                    line_spacing=0.8).move_to([3.5, -2.8, 0])
        text3_sub = Text("the congruence of the two triangles", 
                        t2c={"congruence": "#FFD700"}, 
                        font_size=28,
                        line_spacing=0.8).next_to(text3, DOWN, aligned_edge=LEFT)
        
        # Group all text elements
        text_group = VGroup(
            title,
            text0, text0_sub,
            text1, text1_sub,
            goal_text, goal_content,
            text3, text3_sub
        )
        
        # ============== ANIMATION SEQUENCE ==============
        # Audio timing data
        timings = [
            {"start": 0.0, "end": 3.24},      # Sentence 0
            {"start": 3.25, "end": 7.19},     # Sentence 1
            {"start": 7.2, "end": 10.86},     # Sentence 2
            {"start": 10.87, "end": 14.76}    # Sentence 3
        ]
        
        # Animate diagram creation
        self.play(
            LaggedStart(
                DrawBorderThenFill(triangle_ABC),
                DrawBorderThenFill(triangle_BAD),
                Create(side_AB),
                FadeIn(dot_A), FadeIn(dot_B), 
                FadeIn(dot_C), FadeIn(dot_D),
                Write(label_A), Write(label_B),
                Write(label_C), Write(label_D),
                lag_ratio=0.2
            ),
            run_time=3.0
        )
        
        # Sentence 0: "For part A, our first step..."
        self.play(
            Write(title),
            Write(text0),
            Write(text0_sub),
            run_time=timings[0]["end"] - timings[0]["start"]
        )
        
        # Sentence 1: "We need to show that triangle..."
        self.wait(timings[1]["start"] - timings[0]["end"])
        self.play(
            Write(text1),
            Write(text1_sub),
            run_time=timings[1]["end"] - timings[1]["start"]
        )
        
        # Highlight the relevant triangles during explanation
        self.play(
            Indicate(triangle_ABC, color="#58C4DD", scale_factor=1.1),
            Indicate(triangle_BAD, color="#F07E48", scale_factor=1.1),
            run_time=1.0
        )
        
        # Sentence 2: "Goal: Prove triangle ABC..."
        self.wait(timings[2]["start"] - timings[1]["end"])
        self.play(
            Write(goal_text),
            Write(goal_content),
            run_time=timings[2]["end"] - timings[2]["start"] - 0.5
        )
        
        # Highlight goal text
        self.play(
            Flash(goal_content, color="#FFD700", line_length=0.3, flash_radius=0.4),
            run_time=0.5
        )
        
        # Sentence 3: "Our objective is to demonstrate..."
        self.wait(timings[3]["start"] - timings[2]["end"])
        self.play(
            Write(text3),
            Write(text3_sub),
            run_time=timings[3]["end"] - timings[3]["start"]
        )
        
        # Final highlight of both triangles
        self.play(
            Circumscribe(VGroup(triangle_ABC, triangle_BAD), 
            color="#FFD700",
            run_time=1.5
            )
        )
        self.wait(2)