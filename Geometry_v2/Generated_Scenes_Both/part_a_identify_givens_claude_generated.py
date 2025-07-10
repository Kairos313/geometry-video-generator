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


class PartAIdentifyGivens(Scene):
    def construct(self):
        self.camera.background_color = "#1E293B"
        self.add_sound("/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Scene/part_a_identify_givens_scene.mp3")
        
        MAX_TEXT_WIDTH = 3.0
        NARRATION_ANCHOR_POINT = np.array([6.9 - 0.5, 3.5, 0])

        #################################################################
        # PART 1: INSTANT RECONSTRUCTION
        #################################################################
        
        # Replicate exact coordinate calculation logic from previous scene
        A = np.array([-6.0, -2.5, 0])
        B = np.array([-1.0, -2.5, 0])
        C = np.array([-1.5, 1.5, 0])
        D = np.array([-5.5, 1.0, 0])
        
        # Calculate intersection point E of AC and BD using same logic
        AC_direction = C - A
        BD_direction = D - B
        AB_vector = B - A
        
        matrix = np.column_stack([AC_direction[:2], -BD_direction[:2]])
        rhs = AB_vector[:2]
        try:
            params = np.linalg.solve(matrix, rhs)
            t = params[0]
            E = A + t * AC_direction
        except:
            E = np.array([-3.5, -0.5, 0])

        # Recreate all geometric objects with exact same properties
        dot_A = Dot(A, color="#FFFFFF", radius=0.08).set_z_index(3)
        dot_B = Dot(B, color="#FFFFFF", radius=0.08).set_z_index(3)
        dot_C = Dot(C, color="#FFFFFF", radius=0.08).set_z_index(3)
        dot_D = Dot(D, color="#FFFFFF", radius=0.08).set_z_index(3)
        dot_E = Dot(E, color="#F07E48", radius=0.06).set_z_index(3)
        
        line_AB = Line(A, B, color="#58C4DD", stroke_width=3)
        line_AC = Line(A, C, color="#58C4DD", stroke_width=3)
        line_BC = Line(B, C, color="#58C4DD", stroke_width=3)
        line_AD = Line(A, D, color="#58C4DD", stroke_width=3)
        line_BD = Line(B, D, color="#58C4DD", stroke_width=3)
        
        triangle_ABC = Polygon(A, B, C, color="#87C2A5", fill_opacity=0.3, stroke_width=0)
        triangle_BAD = Polygon(B, A, D, color="#E2D28B", fill_opacity=0.3, stroke_width=0)
        
        label_A = MathTex("A", color="#FFFFFF", font_size=32).next_to(dot_A, np.array([-0.3, -0.3, 0]))
        label_B = MathTex("B", color="#FFFFFF", font_size=32).next_to(dot_B, np.array([0.3, -0.3, 0]))
        label_C = MathTex("C", color="#FFFFFF", font_size=32).next_to(dot_C, np.array([0.3, 0.3, 0]))
        label_D = MathTex("D", color="#FFFFFF", font_size=32).next_to(dot_D, np.array([-0.3, 0.3, 0]))
        label_E = MathTex("E", color="#F07E48", font_size=28).next_to(dot_E, np.array([0.3, 0.2, 0]))
        
        right_angle_ACB = RightAngle(line_AC, line_BC, length=0.3, color="#FFD700", stroke_width=2)
        right_angle_ADB = RightAngle(line_AD, line_BD, length=0.3, color="#FFD700", stroke_width=2)
        
        # Recreate the previous scene's final narration state
        goal_statement = MathTex(r"\triangle ABC \cong \triangle BAD", color="#FFD700", font_size=36)
        goal_formal = MathTex(r"\text{Goal: Prove } \triangle ABC \cong \triangle BAD", color="#FFFFFF", font_size=32)
        old_narration_vgroup = VGroup(goal_statement, goal_formal).arrange(
            np.array([0, -1, 0]), aligned_edge=np.array([1, 0, 0]), buff=0.4
        ).move_to(NARRATION_ANCHOR_POINT, aligned_edge=np.array([1, 1, 0]))
        
        # Add all elements instantly to recreate previous scene's final state
        self.add(
            line_AB, line_AC, line_BC, line_AD, line_BD,
            triangle_ABC, triangle_BAD,
            dot_A, dot_B, dot_C, dot_D, dot_E,
            label_A, label_B, label_C, label_D, label_E,
            right_angle_ACB, right_angle_ADB,
            old_narration_vgroup
        )

        #################################################################
        # PART 2: NEW ANIMATIONS
        #################################################################
        
        # Master VGroup for new narration text (Rolling List pattern)
        givens_vgroup = VGroup()
        current_time = 0
        
        # Sentence 1: "Next, let's list the information given in the problem..."
        # (0.0 - 5.62) - Conversational, don't display text
        s1_start, s1_end = 0.0, 5.62
        
        # Fade out old narration and prepare for new content
        self.play(
            FadeOut(old_narration_vgroup),
            run_time=s1_end - s1_start
        )
        current_time = s1_end
        
        # Sentence 2: "We are given: 1. Angle ACB equals angle ADB, and both are ninety degrees."
        # (5.63 - 11.25) - Key given information, display as MathTex
        s2_start, s2_end = 5.63, 11.25
        
        given_1 = MathTex(
            r"\text{Given 1: } \angle ACB = \angle ADB = 90°",
            color="#E2D28B",
            font_size=32
        )
        givens_vgroup.add(given_1)
        
        wait_duration = s2_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        self.play(
            Indicate(right_angle_ACB, color="#FFD700"),
            Indicate(right_angle_ADB, color="#FFD700"),
            givens_vgroup.animate.arrange(
                np.array([0, -1, 0]), aligned_edge=np.array([1, 0, 0]), buff=0.4
            ).move_to(
                NARRATION_ANCHOR_POINT, aligned_edge=np.array([1, 1, 0])
            ),
            run_time=s2_end - s2_start
        )
        current_time = s2_end
        
        # Sentence 3: "This tells us that triangle ABC is a right-angled triangle at C..."
        # (11.26 - 18.13) - Describes animation, don't create text, just animate
        s3_start, s3_end = 11.26, 18.13
        
        wait_duration = s3_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        self.play(
            triangle_ABC.animate.set_fill_opacity(0.4),
            triangle_BAD.animate.set_fill_opacity(0.4),
            Flash(dot_C, color="#87C2A5"),
            Flash(dot_D, color="#E2D28B"),
            run_time=s3_end - s3_start
        )
        current_time = s3_end
        
        # Sentence 4: "2. Side AD equals side BC."
        # (18.14 - 20.49) - Key given information, display as MathTex
        s4_start, s4_end = 18.14, 20.49
        
        given_2 = MathTex(
            r"\text{Given 2: } AD = BC",
            color="#E2D28B",
            font_size=32
        )
        givens_vgroup.add(given_2)
        
        wait_duration = s4_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        self.play(
            line_AD.animate.set_color("#F07E48").set_stroke_width(5),
            line_BC.animate.set_color("#F07E48").set_stroke_width(5),
            givens_vgroup.animate.arrange(
                np.array([0, -1, 0]), aligned_edge=np.array([1, 0, 0]), buff=0.4
            ).move_to(
                NARRATION_ANCHOR_POINT, aligned_edge=np.array([1, 1, 0])
            ),
            run_time=s4_end - s4_start
        )
        current_time = s4_end
        
        # Sentence 5: "Additionally, we can observe that side AB is a common side..."
        # (20.5 - 24.81) - Describes animation, don't create text
        s5_start, s5_end = 20.5, 24.81
        
        wait_duration = s5_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        self.play(
            line_AB.animate.set_color("#FFD700").set_stroke_width(6),
            run_time=s5_end - s5_start
        )
        current_time = s5_end
        
        # Sentence 6: "We have two right angles, one pair of equal sides, and a common hypotenuse."
        # (24.82 - 29.6) - Summary statement, display as MathTex
        s6_start, s6_end = 24.82, 29.6
        
        summary = MathTex(
            r"\text{Summary: } 2 \text{ right angles, } AD = BC, \text{ common } AB",
            color="#FFFFFF",
            font_size=28
        )
        givens_vgroup.add(summary)
        
        wait_duration = s6_start - current_time
        if wait_duration >= 0.01:
            self.wait(wait_duration)
        
        self.play(
            Flash(right_angle_ACB, color="#FFD700"),
            Flash(right_angle_ADB, color="#FFD700"),
            givens_vgroup.animate.arrange(
                np.array([0, -1, 0]), aligned_edge=np.array([1, 0, 0]), buff=0.4
            ).move_to(
                NARRATION_ANCHOR_POINT, aligned_edge=np.array([1, 1, 0])
            ),
            run_time=s6_end - s6_start
        )
        current_time = s6_end
        
        self.wait(1)