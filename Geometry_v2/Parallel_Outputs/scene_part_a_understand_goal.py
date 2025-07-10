import json
from manim import *
import numpy as np
from Geometry_v2.geometric_figure_output import *

# Load the JSON data
with open("Geometry_v2/deconstruct_parallel.json", "r") as f:
    deconstruct_parallel_data = json.load(f)

with open("Geometry_v2/geo_v2_style.json", "r") as f:
    style_data = json.load(f)

# --- TARGET SCENE CONFIGURATION (SET BY USER) ---
TARGET_STEP_ID = "part_a_understand_goal"
# ------------------------------------------------

class PartAUnderstandGoal(Scene):
    def construct(self):
        # Extract style information
        background_color = style_data["theme"]["background_color"]
        text_color = style_data["objects"]["text"]["default_color"]
        highlight_color_yellow = style_data["colors"]["accent"]["yellow"]
        highlight_color_green = style_data["colors"]["accent"]["green"]
        highlight_color_orange = style_data["colors"]["accent"]["orange"]
        blue_triangle_color = style_data["colors"]["primary"]["blue"]
        contrasting_triangle_color = style_data["colors"]["accent"]["orange"]
        
        # Find the target step data
        step_data = None
        for step in deconstruct_parallel_data["solution_steps"]:
            if step["step_id"] == TARGET_STEP_ID:
                step_data = step
                break
        
        if step_data is None:
            raise ValueError(f"Step ID {TARGET_STEP_ID} not found in deconstruct_parallel.json")

        # --- PART 1: Scene Initialization & Base Diagram Setup ---
        self.camera.background_color = background_color
        # // DOCS: manim.scene.scene.Scene.add_sound
        self.add_sound(step_data["audio_file_scene"])

        # --- RE-IMPLEMENT GEOMETRIC CALCULATIONS FROM geometric_figure_output.py ---
        scale_factor = 0.25
        ad_len = 12 * scale_factor
        de_len = 9 * scale_factor
        bc_len = 12 * scale_factor
        ae_len = 15 * scale_factor
        be_len = 15 * scale_factor
        bd_len = 24 * scale_factor
        ac_len = 24 * scale_factor
        ce_len = 9 * scale_factor
        
        # Establish base coordinates
        # // NUMPY-DOCS: numpy.array
        coord_A = np.array([-4.0, -1.5, 0])
        coord_B = np.array([4.0, -1.5, 0])
        
        # Calculate D position using circle intersections
        # // NUMPY-DOCS: numpy.linalg.norm
        ab_len = np.linalg.norm(coord_B - coord_A)
        mid_AB = (coord_A + coord_B) / 2
        radius_ab_circle = ab_len / 2
        
        d = np.linalg.norm(mid_AB - coord_A)
        a = (ad_len**2 - radius_ab_circle**2 + d**2) / (2 * d)
        # // NUMPY-DOCS: numpy.sqrt
        h = np.sqrt(ad_len**2 - a**2)
        p2 = coord_A + a * (mid_AB - coord_A) / d
        
        coord_D = np.array([p2[0] - h*(mid_AB[1]-coord_A[1])/d, p2[1] + h*(mid_AB[0]-coord_A[0])/d, 0])
        
        # Calculate C position
        a_c = (bc_len**2 - radius_ab_circle**2 + d**2) / (2 * d)
        h_c = np.sqrt(bc_len**2 - a_c**2)
        p2_c = coord_B + a_c * (mid_AB - coord_B) / d
        
        coord_C = np.array([p2_c[0] + h_c*(mid_AB[1]-coord_B[1])/d, p2_c[1] - h_c*(mid_AB[0]-coord_B[0])/d, 0])
        
        # Find E as intersection of AC and BD
        # // DOCS: manim.utils.geometry.line_intersection
        coord_E = line_intersection((coord_A, coord_C), (coord_B, coord_D))
        
        # Apply scale factor
        coord_A = coord_A * scale_factor
        coord_B = coord_B * scale_factor
        coord_C = coord_C * scale_factor
        coord_D = coord_D * scale_factor
        coord_E = coord_E * scale_factor
        
        # --- END OF GEOMETRIC CALCULATIONS ---

        # Create individual mobjects for the base diagram
        # // DOCS: manim.mobject.geometry.line.Line
        line_AB = Line(start=coord_A, end=coord_B, color="#FFFFFF", stroke_width=2)
        line_BC = Line(start=coord_B, end=coord_C, color="#FFFFFF", stroke_width=2)
        line_CD = Line(start=coord_C, end=coord_D, color="#FFFFFF", stroke_width=2)
        line_DA = Line(start=coord_D, end=coord_A, color="#FFFFFF", stroke_width=2)
        line_AC = Line(start=coord_A, end=coord_C, color="#FFFFFF", stroke_width=2)
        line_BD = Line(start=coord_B, end=coord_D, color="#FFFFFF", stroke_width=2)

        # // DOCS: manim.mobject.text.tex_mobject.MathTex
        # // DOCS: manim.mobject.mobject.Mobject.move_to
        # // NUMPY-DOCS: numpy.array
        label_A = MathTex("A", color="#FFFFFF", font_size=32).move_to(coord_A + np.array([-0.3, -0.3, 0]))
        label_B = MathTex("B", color="#FFFFFF", font_size=32).move_to(coord_B + np.array([0.3, -0.3, 0]))
        label_C = MathTex("C", color="#FFFFFF", font_size=32).move_to(coord_C + np.array([0.3, 0.3, 0]))
        label_D = MathTex("D", color="#FFFFFF", font_size=32).move_to(coord_D + np.array([-0.3, 0.3, 0]))
        label_E = MathTex("E", color="#FFFFFF", font_size=32).move_to(coord_E + np.array([0.0, 0.3, 0]))

        label_AD = MathTex("12", color="#22C55E", font_size=24).move_to((coord_A + coord_D) / 2 + np.array([-0.4, 0.0, 0]))
        label_DE = MathTex("9", color="#22C55E", font_size=24).move_to((coord_D + coord_E) / 2 + np.array([0.0, 0.4, 0]))
        label_AE = MathTex("15", color="#22C55E", font_size=24).move_to((coord_A + coord_E) / 2 + np.array([-0.3, 0.0, 0]))
        
        # Right angle at C (angle ACB)
        # // DOCS: manim.mobject.geometry.angle.RightAngle
        right_angle_C = RightAngle(line1=line_AC, line2=line_BC, length=0.3, color=highlight_color_yellow)
        
        # Right angle at D (angle ADB)
        right_angle_D = RightAngle(line1=line_DA, line2=line_BD, length=0.3, color=highlight_color_yellow)
        
        # // DOCS: manim.mobject.geometry.arc.Dot
        dot_A = Dot(point=coord_A, radius=0.08, color="#FFFFFF")
        dot_B = Dot(point=coord_B, radius=0.08, color="#FFFFFF")
        dot_C = Dot(point=coord_C, radius=0.08, color="#FFFFFF")
        dot_D = Dot(point=coord_D, radius=0.08, color="#FFFFFF")
        dot_E = Dot(point=coord_E, radius=0.08, color="#FFFFFF")
        
        # // DOCS: manim.mobject.container.VGroup
        base_diagram_elements = VGroup(
            line_AB, line_BC, line_CD, line_DA, line_AC, line_BD,
            dot_A, dot_B, dot_C, dot_D, dot_E,
            label_A, label_B, label_C, label_D, label_E,
            label_AD, label_DE, label_AE,
            right_angle_C, right_angle_D
        )

        # Adjust position of the diagram to the left side
        # // DOCS: manim.mobject.mobject.Mobject.get_right
        current_right_x_coord = base_diagram_elements.get_right()[0]
        # // DOCS: manim.mobject.mobject.Mobject.get_center
        current_center_y_coord = base_diagram_elements.get_center()[1]

        target_right_x = -0.1
        shift_x = target_right_x - current_right_x_coord
        shift_y = -current_center_y_coord

        # // DOCS: manim.mobject.mobject.Mobject.shift
        # // NUMPY-DOCS: numpy.array
        base_diagram_elements.shift(np.array([shift_x, shift_y, 0]))
        
        # // DOCS: manim.scene.scene.Scene.add
        self.add(base_diagram_elements)

        current_time = 0.0
        all_scene_mobjects = VGroup(base_diagram_elements)

        # --- PART 2: Animated Content (Synchronized with Audio) ---
        last_text_mobj = None

        for i, sentence in enumerate(step_data["sentences"]):
            start_time = sentence["start_time_seconds"]
            end_time = sentence["end_time_seconds"]
            sentence_text_str = sentence["text"]

            # Wait for the start of the sentence
            wait_duration = start_time - current_time
            if wait_duration >= 0.01:
                # // DOCS: manim.scene.scene.Scene.wait
                self.wait(duration=wait_duration)
            current_time = start_time

            # Prepare text mobject with pedagogical rephrasing and math symbols
            mobj_to_play = VGroup()

            # // DOCS: manim.mobject.text.text_mobject.Text
            # // DOCS: manim.mobject.text.tex_mobject.MathTex
            # // DOCS: manim.mobject.mobject.Mobject.to_corner
            # // DOCS: manim.mobject.mobject.Mobject.align_to
            # // DOCS: manim.camera.camera.Camera.frame_width
            # // DOCS: manim.mobject.mobject.Mobject.next_to
            # // NUMPY-DOCS: numpy.array

            if i == 0: # "For part A, our first step is to understand what we need to prove."
                text_content = Text(
                    "Part A: Understanding Our Goal",
                    font_size=style_data["fonts"]["text"]["size"]["large"],
                    color=highlight_color_yellow
                )
                text_content.to_corner(corner=np.array([1, 1, 0])).align_to(mobject_or_point=np.array([-self.camera.frame_width / 2 + 0.1, 0, 0]), direction=np.array([1, 0, 0]))
                text_content.shift(np.array([0, -0.5, 0]))

            elif i == 1: # "We need to show that triangle A B C is congruent to triangle B A D."
                text_content = MathTex(
                    r"\text{Prove: } \triangle ABC \cong \triangle BAD",
                    font_size=style_data["fonts"]["math"]["size"]["medium"],
                    color=text_color
                ).next_to(mobject_or_point=last_text_mobj, direction=np.array([0, -1, 0]), buff=style_data["layout"]["spacing"]["medium"], aligned_edge=np.array([-1, 0, 0]))
                
                # Highlight the triangles
                # // DOCS: manim.mobject.geometry.polygram.Polygon
                # // DOCS: manim.animation.fading.FadeIn
                triangle_ABC_fill = Polygon(coord_A, coord_B, coord_C, fill_color=blue_triangle_color, fill_opacity=0.3, stroke_width=0)
                triangle_BAD_fill = Polygon(coord_B, coord_A, coord_D, fill_color=contrasting_triangle_color, fill_opacity=0.3, stroke_width=0)
                
                self.play(FadeIn(triangle_ABC_fill), FadeIn(triangle_BAD_fill))
                all_scene_mobjects.add(triangle_ABC_fill, triangle_BAD_fill)

            elif i == 2: # "Goal: Prove triangle A B C is congruent to triangle B A D."
                text_content = Text(
                    "Goal: Establish Triangle Congruence",
                    font_size=style_data["fonts"]["text"]["size"]["medium"],
                    color=highlight_color_green
                ).next_to(mobject_or_point=last_text_mobj, direction=np.array([0, -1, 0]), buff=style_data["layout"]["spacing"]["small"], aligned_edge=np.array([-1, 0, 0]))

            elif i == 3: # "Our objective is to demonstrate the congruence of the two triangles."
                text_content_line1 = Text(
                    "We must demonstrate that these",
                    font_size=style_data["fonts"]["text"]["size"]["medium"],
                    color=text_color
                ).next_to(mobject_or_point=last_text_mobj, direction=np.array([0, -1, 0]), buff=style_data["layout"]["spacing"]["small"], aligned_edge=np.array([-1, 0, 0]))
                
                text_content_line2 = Text(
                    "two triangles are congruent.",
                    font_size=style_data["fonts"]["text"]["size"]["medium"],
                    color=text_color
                ).next_to(mobject_or_point=text_content_line1, direction=np.array([0, -1, 0]), buff=style_data["layout"]["spacing"]["small"], aligned_edge=np.array([-1, 0, 0]))
                
                text_content = VGroup(text_content_line1, text_content_line2)

            # Add current sentence text to the group of mobjects to be played
            mobj_to_play.add(text_content)
            
            # Perform the animation
            # // DOCS: manim.scene.scene.Scene.play
            self.play(*[FadeIn(mob) for mob in mobj_to_play], run_time=(end_time - start_time))
            
            last_text_mobj = text_content
            all_scene_mobjects.add(text_content)
            current_time = end_time

        # --- PART 3: Scene Conclusion ---

        # Wait for any remaining audio after the last sentence
        remaining_audio_time = step_data["duration_scene_seconds"] - current_time
        if remaining_audio_time > 0.01:
            self.wait(duration=remaining_audio_time)

        # Fade out all mobjects at the end of the scene
        # // DOCS: manim.animation.fading.FadeOut
        self.play(*[FadeOut(mob) for mob in all_scene_mobjects], run_time=1.0)