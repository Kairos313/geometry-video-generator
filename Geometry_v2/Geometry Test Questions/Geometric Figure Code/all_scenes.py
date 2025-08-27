#!/usr/bin/env python3
"""Generated Manim Code"""



import sys
import os
from manim import *
import json
import re
import numpy as np

# CRITICAL: Add grandparent directory to path to import helpers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from functions import *
from geometric_figure_output import *

# Enhanced Style Configuration
ENHANCED_STYLE_CONFIG = {
    "background_color": "#0C0C0C",
    "colors": {
        "primary_blue": "#3B82F6",
        "accent_yellow": "#FDE047",
        "accent_orange": "#FB923C",
        "accent_green": "#22C55E",
        "text_white": "#FFFFFF",
        "highlight": "#FDE047"
    }
}

class PartAFindAngleXWY(Scene):
    def construct(self):
        # 1. Setup scene background
        self.camera.background_color = ENHANCED_STYLE_CONFIG["background_color"]
        
        # 2. Load JSON data for this specific scene
        deconstruct_data = {
            "solution_steps": [
                {
                    "step_id": "part_a_find_angle_XWY",
                    "sentences": [
                        {
                            "text": "First, let's solve part (a). We need to find the angle X W Y in the triangle W X Y.",
                            "audio_file_individual": "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Audio/part_a_find_angle_XWY_0.mp3",
                            "duration_seconds": 6.11,
                            "start_time_seconds": 0.0,
                            "end_time_seconds": 6.11
                        },
                        {
                            "text": "We're given side W X is 6, side X Y is 5, and angle W Y X is 70 degrees. The Sine Rule is the perfect tool here.",
                            "audio_file_individual": "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Audio/part_a_find_angle_XWY_1.mp3",
                            "duration_seconds": 8.54,
                            "start_time_seconds": 6.12,
                            "end_time_seconds": 14.66
                        },
                        {
                            "text": "This rule connects sides to the sines of their opposite angles.",
                            "audio_file_individual": "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Audio/part_a_find_angle_XWY_2.mp3",
                            "duration_seconds": 3.58,
                            "start_time_seconds": 14.67,
                            "end_time_seconds": 18.25
                        },
                        {
                            "text": "The side opposite angle W Y X is W X, and the side opposite angle X W Y is X Y.",
                            "audio_file_individual": "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Audio/part_a_find_angle_XWY_3.mp3",
                            "duration_seconds": 6.03,
                            "start_time_seconds": 18.26,
                            "end_time_seconds": 24.29
                        },
                        {
                            "text": "So, we set up the ratio: 5 divided by the sine of angle X W Y equals 6 divided by the sine of 70 degrees.",
                            "audio_file_individual": "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Audio/part_a_find_angle_XWY_4.mp3",
                            "duration_seconds": 7.37,
                            "start_time_seconds": 24.3,
                            "end_time_seconds": 31.67
                        },
                        {
                            "text": "Rearranging the formula, the sine of angle X W Y is 5 times the sine of 70 degrees, all divided by 6.",
                            "audio_file_individual": "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Audio/part_a_find_angle_XWY_5.mp3",
                            "duration_seconds": 7.24,
                            "start_time_seconds": 31.68,
                            "end_time_seconds": 38.92
                        },
                        {
                            "text": "This gives us approximately 0 point 7 8 3.",
                            "audio_file_individual": "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Audio/part_a_find_angle_XWY_6.mp3",
                            "duration_seconds": 2.95,
                            "start_time_seconds": 38.93,
                            "end_time_seconds": 41.88
                        },
                        {
                            "text": "Taking the inverse sine, we find angle X W Y is about 51 point 5 degrees.",
                            "audio_file_individual": "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Audio/part_a_find_angle_XWY_7.mp3",
                            "duration_seconds": 5.2,
                            "start_time_seconds": 41.89,
                            "end_time_seconds": 47.09
                        }
                    ],
                    "audio_file_scene": "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Scene/part_a_find_angle_XWY_scene.mp3",
                    "duration_scene_seconds": 47.09
                }
            ]
        }
        
        scene_data = deconstruct_data['solution_steps'][0]
        
        # 3. Add complete audio file for entire scene
        try:
            audio_file = scene_data['audio_file_scene']
            if os.path.exists(audio_file):
                self.add_sound(audio_file)
        except Exception as e:
            print(f"Warning: Could not add audio file: {e}")
        
        # 4. Create and position base diagram
        base_figure = create_base_diagram_2d_main_a()
        auto_scale_to_left_screen(base_figure, is_3d=False)
        self.add(base_figure)
        
        # 5. Extract scaled coordinates for dynamic element positioning
        scaled_coords = {}
        dots_group = base_figure[0][2]  # geometry_group -> dots
        scaled_coords['Y'] = dots_group[0].get_center()
        scaled_coords['W'] = dots_group[1].get_center()
        scaled_coords['X'] = dots_group[2].get_center()
        
        # 6. Process each sentence with PRECISE TIMING
        sentences = scene_data['sentences']
        current_time = 0.0
        
        # Wait for first sentence to begin
        if sentences[0]['start_time_seconds'] > 0.01:
            self.wait(sentences[0]['start_time_seconds'])
            current_time = sentences[0]['start_time_seconds']
        
        for i, sentence in enumerate(sentences):
            start_time = sentence['start_time_seconds']
            end_time = sentence['end_time_seconds']
            voiceover_text = sentence['text']
            
            # PRECISE TIMING: Wait until this sentence starts
            wait_time = start_time - current_time
            if wait_time > 0.01:
                self.wait(wait_time)
            
            # Convert to Khan Academy style text and create animations
            khan_academy_text = self._convert_to_khan_academy_style(voiceover_text, i)
            animations = self._create_visual_highlights_and_constructions(voiceover_text, scaled_coords, i)
            
            # Display text if generated
            if khan_academy_text:
                if isinstance(khan_academy_text, list):
                    for text_item in khan_academy_text:
                        if isinstance(text_item, str) and ('\\' in text_item or text_item.startswith('$')):
                            add_explanation_text(self, MathTex(text_item))
                        else:
                            add_explanation_text(self, text_item)
                else:
                    if isinstance(khan_academy_text, str) and ('\\' in khan_academy_text or khan_academy_text.startswith('$')):
                        add_explanation_text(self, MathTex(khan_academy_text))
                    else:
                        add_explanation_text(self, khan_academy_text)
            
            # Play animations if any were generated
            if animations:
                animation_duration = min((end_time - start_time) * 0.7, 2.0)
                self.play(*animations, run_time=animation_duration)
            
            # Update current time to end of sentence
            current_time = end_time
        
        # 7. PRECISE SCENE DURATION: Ensure it matches voiceover length exactly
        total_voiceover_duration = scene_data['duration_scene_seconds']
        remaining_time = total_voiceover_duration - current_time
        if remaining_time > 0.01:
            self.wait(remaining_time)

    def _convert_to_khan_academy_style(self, verbose_text, sentence_index):
        """Convert verbose explanations to concise Khan Academy-style mathematical text"""
        text_lower = verbose_text.lower()
        
        if sentence_index == 0:  # Introduction
            return "\\text{Find: }\\angle XWY"
        
        elif sentence_index == 1:  # Given information
            return [
                "Given:",
                "WX = 6\\text{ cm}",
                "XY = 5\\text{ cm}",
                "\\angle WYX = 70^{\\circ}"
            ]
        
        elif sentence_index == 2:  # Sine Rule introduction
            return [
                "Using Law of Sines:",
                "\\frac{a}{\\sin A} = \\frac{b}{\\sin B}"
            ]
        
        elif sentence_index == 3:  # Opposite sides
            return "\\frac{XY}{\\sin(\\angle XWY)} = \\frac{WX}{\\sin(\\angle WYX)}"
        
        elif sentence_index == 4:  # Setup equation
            return "\\frac{5}{\\sin(\\angle XWY)} = \\frac{6}{\\sin(70^{\\circ})}"
        
        elif sentence_index == 5:  # Rearrange
            return "\\sin(\\angle XWY) = \\frac{5 \\sin(70^{\\circ})}{6}"
        
        elif sentence_index == 6:  # Numerical result
            return "\\sin(\\angle XWY) \\approx 0.783"
        
        elif sentence_index == 7:  # Final answer
            return "\\angle XWY \\approx 51.5^{\\circ}"
        
        return None

    def _create_visual_highlights_and_constructions(self, voiceover_text, scaled_coords, sentence_index):
        """Create visual highlighting animations based on voiceover content"""
        animations = []
        text_lower = voiceover_text.lower()
        
        if sentence_index == 0:  # Highlight triangle
            triangle = Polygon(scaled_coords['W'], scaled_coords['X'], scaled_coords['Y'], 
                             color=ENHANCED_STYLE_CONFIG["colors"]["highlight"], fill_opacity=0.2)
            animations.append(Indicate(triangle, color=ENHANCED_STYLE_CONFIG["colors"]["highlight"]))
        
        elif sentence_index == 1:  # Highlight given elements
            # Highlight given angle
            angle_arc = create_2d_angle_arc(scaled_coords['Y'], scaled_coords['W'], scaled_coords['X'], 
                                          color=ENHANCED_STYLE_CONFIG["colors"]["highlight"])
            animations.append(Create(angle_arc))
            
            # Highlight given sides
            line_WX = Line(scaled_coords['W'], scaled_coords['X'], color=ENHANCED_STYLE_CONFIG["colors"]["accent_green"])
            line_XY = Line(scaled_coords['X'], scaled_coords['Y'], color=ENHANCED_STYLE_CONFIG["colors"]["accent_green"])
            animations.extend([Indicate(line_WX), Indicate(line_XY)])
        
        elif sentence_index == 7:  # Highlight the answer angle
            answer_angle = create_2d_angle_arc(scaled_coords['W'], scaled_coords['X'], scaled_coords['Y'], 
                                             color=ENHANCED_STYLE_CONFIG["colors"]["accent_orange"])
            animations.append(Create(answer_angle))
        
        return animations


class PartBIdentifyDihedralAngle(ThreeDScene):
    def construct(self):
        # Setup scene background
        self.camera.background_color = ENHANCED_STYLE_CONFIG["background_color"]
        
        # Load scene data
        scene_data = {
            "step_id": "part_b_identify_dihedral_angle",
            "sentences": [
                {
                    "text": "Now for part (b). We need to find the angle between the base triangle W X Y and the face triangle X Y Z. This is called a dihedral angle.",
                    "duration_seconds": 10.11,
                    "start_time_seconds": 0.0,
                    "end_time_seconds": 10.11
                },
                {
                    "text": "To find it, we'll create a special right-angled triangle.",
                    "duration_seconds": 3.06,
                    "start_time_seconds": 10.12,
                    "end_time_seconds": 13.18
                },
                {
                    "text": "Let O be the point on the base directly under the peak Z, and let M be the midpoint of the line X Y.",
                    "duration_seconds": 5.8,
                    "start_time_seconds": 13.19,
                    "end_time_seconds": 18.99
                },
                {
                    "text": "The angle we need to find is Z M O.",
                    "duration_seconds": 2.33,
                    "start_time_seconds": 19.0,
                    "end_time_seconds": 21.33
                },
                {
                    "text": "In the right-angled triangle Z O M, the tangent of angle Z M O is the length of side Z O divided by the length of side O M.",
                    "duration_seconds": 8.31,
                    "start_time_seconds": 21.34,
                    "end_time_seconds": 29.65
                }
            ],
            "audio_file_scene": "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Scene/part_b_identify_dihedral_angle_scene.mp3",
            "duration_scene_seconds": 29.64
        }
        
        # Add audio
        try:
            audio_file = scene_data['audio_file_scene']
            if os.path.exists(audio_file):
                self.add_sound(audio_file)
        except Exception as e:
            print(f"Warning: Could not add audio file: {e}")
        
        # Create and position base 3D diagram
        base_figure = create_base_diagram_3d_main_b()
        auto_scale_to_left_screen(base_figure, is_3d=True)
        self.add(base_figure)
        
        # MANDATORY: Initial 3D rotation
        self.play(Rotate(base_figure, angle=2*PI, axis=UP), run_time=3)
        
        # Extract scaled coordinates
        dots_group = base_figure[0][2]  # geometry_group -> dots
        scaled_coords = {
            'Y': dots_group[0].get_center(),
            'W': dots_group[1].get_center(),
            'X': dots_group[2].get_center(),
            'Z': dots_group[3].get_center()
        }
        
        # Calculate additional points from coordinates.txt
        coord_C = np.array([2.721, 1.670, 0.000])  # Point O (circumcenter)
        coord_M = (scaled_coords['X'] + scaled_coords['Y']) / 2  # Midpoint of XY
        
        # Process sentences with timing
        sentences = scene_data['sentences']
        current_time = 3.0  # Account for initial rotation
        
        for i, sentence in enumerate(sentences):
            start_time = sentence['start_time_seconds'] + 3.0  # Offset for rotation
            end_time = sentence['end_time_seconds'] + 3.0
            
            wait_time = start_time - current_time
            if wait_time > 0.01:
                self.wait(wait_time)
            
            # Generate text and animations
            khan_text = self._convert_to_khan_academy_style_3d(sentence['text'], i)
            animations = self._create_3d_visual_elements(sentence['text'], scaled_coords, coord_C, coord_M, i)
            
            if khan_text:
                if isinstance(khan_text, list):
                    for text_item in khan_text:
                        if isinstance(text_item, str) and ('\\' in text_item):
                            add_explanation_text(self, MathTex(text_item))
                        else:
                            add_explanation_text(self, text_item)
                else:
                    if isinstance(khan_text, str) and ('\\' in khan_text):
                        add_explanation_text(self, MathTex(khan_text))
                    else:
                        add_explanation_text(self, khan_text)
            
            if animations:
                animation_duration = min((end_time - start_time) * 0.7, 2.0)
                self.play(*animations, run_time=animation_duration)
            
            current_time = end_time
        
        # Ensure scene duration matches
        total_duration = scene_data['duration_scene_seconds'] + 3.0
        remaining_time = total_duration - current_time
        if remaining_time > 0.01:
            self.wait(remaining_time)

    def _convert_to_khan_academy_style_3d(self, verbose_text, sentence_index):
        """Convert 3D geometry explanations to Khan Academy style"""
        if sentence_index == 0:
            return "\\text{Find dihedral angle between planes WXY and XYZ}"
        elif sentence_index == 1:
            return "\\text{Method: Create right triangle ZOM}"
        elif sentence_index == 2:
            return [
                "\\text{Let } O = \\text{circumcenter of } \\triangle WXY",
                "\\text{Let } M = \\text{midpoint of } XY"
            ]
        elif sentence_index == 3:
            return "\\text{Dihedral angle} = \\angle ZMO"
        elif sentence_index == 4:
            return "\\tan(\\angle ZMO) = \\frac{ZO}{OM}"
        return None

    def _create_3d_visual_elements(self, voiceover_text, scaled_coords, coord_C, coord_M, sentence_index):
        """Create 3D visual elements and highlights"""
        animations = []
        
        if sentence_index == 0:  # Highlight both triangular faces
            base_triangle = Polygon(scaled_coords['W'], scaled_coords['X'], scaled_coords['Y'],
                                  color=ENHANCED_STYLE_CONFIG["colors"]["primary_blue"], fill_opacity=0.3)
            face_triangle = Polygon(scaled_coords['X'], scaled_coords['Y'], scaled_coords['Z'],
                                  color=ENHANCED_STYLE_CONFIG["colors"]["accent_green"], fill_opacity=0.3)
            animations.extend([Indicate(base_triangle), Indicate(face_triangle)])
        
        elif sentence_index == 2:  # Construct points O and M
            point_O = Dot3D(coord_C, radius=0.1, color=ENHANCED_STYLE_CONFIG["colors"]["highlight"])
            point_M = Dot3D(coord_M, radius=0.1, color=ENHANCED_STYLE_CONFIG["colors"]["highlight"])
            animations.extend([Create(point_O), Create(point_M)])
        
        elif sentence_index == 3:  # Highlight the angle ZMO
            if 'Z' in scaled_coords:
                angle_arc = create_3d_angle_arc_with_connections(
                    center=coord_M,
                    point1=scaled_coords['Z'],
                    point2=coord_C,
                    radius=0.5,
                    color=ENHANCED_STYLE_CONFIG["colors"]["accent_orange"]
                )
                animations.append(Create(angle_arc))
        
        return animations


class PartBCalculateLengthsZOAndOM(ThreeDScene):
    def construct(self):
        self.camera.background_color = ENHANCED_STYLE_CONFIG["background_color"]
        
        # Scene data with timing
        scene_data = {
            "duration_scene_seconds": 48.7,
            "audio_file_scene": "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Scene/part_b_calculate_lengths_ZO_and_OM_scene.mp3"
        }
        
        # Add audio
        try:
            if os.path.exists(scene_data['audio_file_scene']):
                self.add_sound(scene_data['audio_file_scene'])
        except Exception as e:
            print(f"Warning: Could not add audio file: {e}")
        
        # Recreate the 3D figure from previous scene
        base_figure = create_base_diagram_3d_main_b()
        auto_scale_to_left_screen(base_figure, is_3d=True)
        self.add(base_figure)
        
        # Add the constructed points from previous scene
        dots_group = base_figure[0][2]
        scaled_coords = {
            'Y': dots_group[0].get_center(),
            'W': dots_group[1].get_center(),
            'X': dots_group[2].get_center(),
            'Z': dots_group[3].get_center()
        }
        
        coord_C = np.array([2.721, 1.670, 0.000])  # Point O
        coord_M = (scaled_coords['X'] + scaled_coords['Y']) / 2  # Midpoint M
        
        point_O = Dot3D(coord_C, radius=0.1, color=ENHANCED_STYLE_CONFIG["colors"]["highlight"])
        point_M = Dot3D(coord_M, radius=0.1, color=ENHANCED_STYLE_CONFIG["colors"]["highlight"])
        self.add(point_O, point_M)
        
        # Show calculations step by step
        self.wait(2.33)  # "So we need to find the lengths of Z O and O M."
        add_explanation_text(self, "\\text{Calculate: } ZO \\text{ and } OM")
        
        self.wait(10.11)  # Circumradius calculation
        add_explanation_text(self, "\\text{Circumradius: } R = \\frac{6}{2\\sin(70^{\\circ})}")
        add_explanation_text(self, MathTex("R \\approx 3.193\\text{ cm}"))
        
        self.wait(10.03)  # OM calculation
        add_explanation_text(self, "OM = \\sqrt{R^2 - (\\frac{XY}{2})^2}")
        add_explanation_text(self, MathTex("OM \\approx 1.986\\text{ cm}"))
        
        self.wait(8.18)  # ZO setup
        add_explanation_text(self, "\\text{Given: } \\angle ZWO = 30^{\\circ}")
        
        self.wait(8.8)  # ZO calculation
        add_explanation_text(self, "ZO = R \\tan(30^{\\circ})")
        add_explanation_text(self, MathTex("ZO \\approx 1.843\\text{ cm}"))
        
        # Wait for remaining time
        remaining_time = scene_data['duration_scene_seconds'] - 48.7
        if remaining_time > 0.01:
            self.wait(remaining_time)


class PartBCalculateFinalAngleAndConclude(ThreeDScene):
    def construct(self):
        self.camera.background_color = ENHANCED_STYLE_CONFIG["background_color"]
        
        scene_data = {
            "duration_scene_seconds": 23.51,
            "audio_file_scene": "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Scene/part_b_calculate_final_angle_and_conclude_scene.mp3"
        }
        
        # Add audio
        try:
            if os.path.exists(scene_data['audio_file_scene']):
                self.add_sound(scene_data['audio_file_scene'])
        except Exception as e:
            print(f"Warning: Could not add audio file: {e}")
        
        # Recreate scene state
        base_figure = create_base_diagram_3d_main_b()
        auto_scale_to_left_screen(base_figure, is_3d=True)
        self.add(base_figure)
        
        # Show final calculation
        self.wait(10.58)  # Final calculation setup
        add_explanation_text(self, MathTex("\\tan(\\angle ZMO) = \\frac{ZO}{OM}"))
        add_explanation_text(self, MathTex("\\tan(\\angle ZMO) = \\frac{1.843}{1.986}"))
        
        self.wait(2.12)  # Numerical result
        add_explanation_text(self, MathTex("\\tan(\\angle ZMO) \\approx 0.928"))
        
        self.wait(4.44)  # Final angle
        add_explanation_text(self, MathTex("\\angle ZMO \\approx 42.9^{\\circ}"))
        
        self.wait(6.35)  # Conclusion
        add_explanation_text(self, "\\text{Since } 42.9^{\\circ} < 45^{\\circ}")
        add_explanation_text(self, "\\text{Answer: NO}")
        
        # Wait for remaining time
        remaining_time = scene_data['duration_scene_seconds'] - 23.51
        if remaining_time > 0.01:
            self.wait(remaining_time)


class KeyTakeaways(Scene):
    def construct(self):
        self.camera.background_color = ENHANCED_STYLE_CONFIG["background_color"]
        
        scene_data = {
            "duration_scene_seconds": 13.5,
            "audio_file_scene": "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Geometry Test Questions/Scene/key_takeaways_scene.mp3"
        }
        
        # Add audio
        try:
            if os.path.exists(scene_data['audio_file_scene']):
                self.add_sound(scene_data['audio_file_scene'])
        except Exception as e:
            print(f"Warning: Could not add audio file: {e}")
        
        # Show key takeaways
        self.wait(2.95)  # Sine Rule
        add_explanation_text(self, "\\textbf{Key Methods:}")
        add_explanation_text(self, "\\text{1. Law of Sines for triangles}")
        
        self.wait(4.54)  # Circumcenter
        add_explanation_text(self, "\\text{2. Circumcenter properties}")
        
        self.wait(5.98)  # 3D to 2D
        add_explanation_text(self, "\\text{3. 3D } \\rightarrow \\text{ 2D decomposition}")
        
        # Wait for remaining time
        remaining_time = scene_data['duration_scene_seconds'] - 13.5
        if remaining_time > 0.01:
            self.wait(remaining_time)


# Test scenes for individual rendering
class TestPartA(Scene):
    def construct(self):
        self.camera.background_color = "#0C0C0C"
        figure = create_base_diagram_2d_main_a()
        auto_scale_to_left_screen(figure, is_3d=False)
        self.play(Create(figure), run_time=2)
        self.wait(2)


class TestPartB(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#0C0C0C"
        figure = create_base_diagram_3d_main_b()
        auto_scale_to_left_screen(figure, is_3d=True)
        self.play(Create(figure), run_time=3)
        self.play(Rotate(figure, angle=2*PI, axis=UP), run_time=8)
        self.wait(1)
