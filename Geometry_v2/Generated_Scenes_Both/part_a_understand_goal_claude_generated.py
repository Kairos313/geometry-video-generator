from manim import *
import numpy as np

def create_wrapped_text(text: str, max_width: float, font_size: int = 28, color: str = "#FFFFFF") -> VGroup:
    words = text.split(' ')
    lines_str = []
    
    while words:
        low, high = 0, len(words)
        best_split = 0
        while low <= high:
            mid = (low + high) // 2
            if mid == 0: 
                low = mid + 1
                continue
            line_to_test = " ".join(words[:mid])
            test_mobject = Text(line_to_test, font_size=font_size)
            if test_mobject.get_width() <= max_width:
                best_split = mid
                low = mid + 1
            else:
                high = mid - 1
        if best_split == 0 and words: 
            best_split = 1
        lines_str.append(" ".join(words[:best_split]))
        words = words[best_split:]
        
    line_mobjects = [Text(line, font_size=font_size, color=color) for line in lines_str]
    return VGroup(*line_mobjects).arrange(np.array([0, -1, 0]), aligned_edge=np.array([1, 0, 0]), buff=0.2)


class PartAUnderstandGoal(Scene):
    def construct(self):
        self.camera.background_color = "#1E293B"
        self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Scene/part_a_understand_goal_scene.mp3")
        
        MAX_TEXT_WIDTH = 3.0
        NARRATION_ANCHOR_POINT = np.array([6.9 - 0.5, 3.5, 0])

        # Define points based on the problem figure
        A = np.array([-6.0, -2.5, 0])
        B = np.array([-1.0, -2.5, 0])
        
        # Calculate positions for C and D to form the given configuration
        # C is positioned to create angle ACB = 90°
        C = np.array([-1.5, 1.5, 0])
        # D is positioned to create angle ADB = 90° and AD = BC
        D = np.array([-5.5, 1.0, 0])
        
        # Calculate intersection point E of AC and BD
        # Line AC: parametric form A + t*(C - A)
        # Line BD: parametric form B + s*(D - B)
        AC_direction = C - A
        BD_direction = D - B
        AB_vector = B - A
        
        # Solve for intersection: A + t*(C-A) = B + s*(D-B)
        # This gives us: t*(C-A) - s*(D-B) = B - A
        matrix = np.column_stack([AC_direction[:2], -BD_direction[:2]])
        rhs = AB_vector[:2]
        try:
            params = np.linalg.solve(matrix, rhs)
            t = params[0]
            E = A + t * AC_direction
        except:
            # Fallback if lines are parallel (shouldn't happen in this problem)
            E = np.array([-3.5, -0.5, 0])

        # Create geometric objects
        dot_A = Dot(A, color="#FFFFFF", radius=0.08).set_z_index(3)
        dot_B = Dot(B, color="#FFFFFF", radius=0.08).set_z_index(3)
        dot_C = Dot(C, color="#FFFFFF", radius=0.08).set_z_index(3)
        dot_D = Dot(D, color="#FFFFFF", radius=0.08).set_z_index(3)
        dot_E = Dot(E, color="#F07E48", radius=0.06).set_z_index(3)
        
        # Create lines
        line_AB = Line(A, B, color="#58C4DD", stroke_width=3)
        line_AC = Line(A, C, color="#58C4DD", stroke_width=3)
        line_BC = Line(B, C, color="#58C4DD", stroke_width=3)
        line_AD = Line(A, D, color="#58C4DD", stroke_width=3)
        line_BD = Line(B, D, color="#58C4DD", stroke_width=3)
        
        # Create triangles for highlighting
        triangle_ABC = Polygon(A, B, C, color="#87C2A5", fill_opacity=0.2, stroke_width=0)
        triangle_BAD = Polygon(B, A, D, color="#E2D28B", fill_opacity=0.2, stroke_width=0)
        
        # Create labels
        label_A = MathTex("A", color="#FFFFFF", font_size=32).next_to(dot_A, np.array([-0.3, -0.3, 0]))
        label_B = MathTex("B", color="#FFFFFF", font_size=32).next_to(dot_B, np.array([0.3, -0.3, 0]))
        label_C = MathTex("C", color="#FFFFFF", font_size=32).next_to(dot_C, np.array([0.3, 0.3, 0]))
        label_D = MathTex("D", color="#FFFFFF", font_size=32).next_to(dot_D, np.array([-0.3, 0.3, 0]))
        label_E = MathTex("E", color="#F07E48", font_size=28).next_to(dot_E, np.array([0.3, 0.2, 0]))
        
        # Create right angle markers
        right_angle_ACB = RightAngle(line_AC, line_BC, length=0.3, color="#FFD700", stroke_width=2)
        right_angle_ADB = RightAngle(line_AD, line_BD, length=0.3, color="#FFD700", stroke_width=2)
        
        # Group all diagram elements
        diagram_group = VGroup(
            line_AB, line_AC, line_BC, line_AD, line_BD,
            triangle_ABC, triangle_BAD,
            dot_A, dot_B, dot_C, dot_D, dot_E,
            label_A, label_B, label_C, label_D, label_E,
            right_angle_ACB, right_angle_ADB
        )
        
        # Master VGroup for narration text
        narration_vgroup = VGroup()
        
        current_time = 0
        
        # Sentence 1: "For part A, our first step is to understand what we need to prove."
        # (0.0 - 3.24) - Conversational, don't display text
        s1_start, s1_end = 0.0, 3.24
        
        # Start creating the basic diagram structure
        self.play(
            Create(line_AB),
            Create(line_AC),
            Create(line_BC),
            Create(line_AD),
            Create(line_BD),
            run_time=s1_end - s1_start
        )
        current_time = s1_end
        
        # Sentence 2: "We need to show that triangle A B C is congruent to triangle B A D."
        # (3.25 - 7.19) - Key statement, display as MathTex
        s2_start, s2_end = 3.25, 7.19
        
        goal_statement = MathTex(
            r"\triangle ABC \cong \triangle BAD",
            color="#FFD700",
            font_size=36
        )
        narration_vgroup.add(goal_statement)
        
        # Add points and labels, highlight the triangles
        self.play(
            Create(dot_A),
            Create(dot_B), 
            Create(dot_C),
            Create(dot_D),
            Create(dot_E),
            Create(label_A),
            Create(label_B),
            Create(label_C),
            Create(label_D),
            Create(label_E),
            FadeIn(triangle_ABC),
            FadeIn(triangle_BAD),
            narration_vgroup.animate.arrange(
                np.array([0, -1, 0]), aligned_edge=np.array([1, 0, 0]), buff=0.4
            ).move_to(
                NARRATION_ANCHOR_POINT, aligned_edge=np.array([1, 1, 0])
            ),
            run_time=s2_end - s2_start
        )
        current_time = s2_end
        
        # Sentence 3: "Goal: Prove triangle A B C is congruent to triangle B A D."
        # (7.2 - 10.86) - Formal goal statement
        s3_start, s3_end = 7.2, 10.86
        
        goal_formal = MathTex(
            r"\text{Goal: Prove } \triangle ABC \cong \triangle BAD",
            color="#FFFFFF",
            font_size=32
        )
        narration_vgroup.add(goal_formal)
        
        # Add right angle markers and emphasize the goal
        self.play(
            Create(right_angle_ACB),
            Create(right_angle_ADB),
            Indicate(triangle_ABC, color="#87C2A5"),
            Indicate(triangle_BAD, color="#E2D28B"),
            narration_vgroup.animate.arrange(
                np.array([0, -1, 0]), aligned_edge=np.array([1, 0, 0]), buff=0.4
            ).move_to(
                NARRATION_ANCHOR_POINT, aligned_edge=np.array([1, 1, 0])
            ),
            run_time=s3_end - s3_start
        )
        current_time = s3_end
        
        # Sentence 4: "Our objective is to demonstrate the congruence of the two triangles."
        # (10.87 - 14.76) - Conversational summary, just highlight existing elements
        s4_start, s4_end = 10.87, 14.76
        
        self.play(
            Flash(goal_statement, color="#FFD700"),
            triangle_ABC.animate.set_fill_opacity(0.3),
            triangle_BAD.animate.set_fill_opacity(0.3),
            run_time=s4_end - s4_start
        )
        current_time = s4_end
        
        self.wait(1)