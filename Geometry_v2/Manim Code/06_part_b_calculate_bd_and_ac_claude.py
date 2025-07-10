from manim import *
import numpy as np
import math
import json
import re

scene_plan = {
  "scene_id": "part_b_calculate_bd_and_ac",
  "sentence_timestamps": [
    {
      "text": "We now have enough information to find the length of B D and A C.",
      "start": 0.0,
      "end": 3.66
    },
    {
      "text": "We know B D is composed of B E and D E.",
      "start": 3.67,
      "end": 6.18
    },
    {
      "text": "Also, from the congruence in part A, we know that A C equals B D.",
      "start": 6.19,
      "end": 10.37
    },
    {
      "text": "B D equals B E plus D E.",
      "start": 10.38,
      "end": 12.47
    },
    {
      "text": "B D equals fifteen centimeters plus nine centimeters.",
      "start": 12.48,
      "end": 15.67
    },
    {
      "text": "B D equals twenty-four centimeters.",
      "start": 15.68,
      "end": 17.95
    },
    {
      "text": "Since A C equals B D, then A C also equals twenty-four centimeters.",
      "start": 17.96,
      "end": 22.56
    },
    {
      "text": "B D equals twenty-four centimeters, and A C also equals twenty-four centimeters.",
      "start": 22.57,
      "end": 27.25
    }
  ],
  "initial_mobjects": [
    {
      "name": "ProblemDiagram",
      "mobject_type": "VGroup",
      "properties": {
        "position": "LEFT*3"
      }
    },
    {
      "name": "DiagramLabels",
      "mobject_type": "VGroup",
      "properties": {}
    }
  ],
  "mobjects": [
    {
      "name": "CalcTitle",
      "mobject_type": "Tex",
      "properties": {
        "text": "Calculate Diagonal Lengths AC and BD",
        "position": "UP*3.5"
      }
    },
    {
      "name": "Calculations",
      "mobject_type": "VGroup",
      "properties": {
        "position": "RIGHT*3",
        "arrange_direction": "DOWN",
        "arrange_buff": 1
      },
      "mobjects": [
        {
          "name": "CalcBD",
          "mobject_type": "MathTex",
          "properties": {
            "text": "BD = BE + DE = 15 + 9 = 24 \\text{ cm}"
          }
        },
        {
          "name": "CalcAC",
          "mobject_type": "MathTex",
          "properties": {
            "text": "AC = BD = 24 \\text{ cm} \\text{ (from congruence)}"
          }
        }
      ]
    },
    {
      "name": "Braces",
      "mobject_type": "VGroup",
      "properties": {},
      "mobjects": [
        {
          "name": "BraceBD",
          "mobject_type": "Brace",
          "properties": {
            "mobject": "mobject_from_name('BD')",
            "direction": "RIGHT"
          }
        },
        {
          "name": "BraceAC",
          "mobject_type": "Brace",
          "properties": {
            "mobject": "mobject_from_name('AC')",
            "direction": "LEFT"
          }
        }
      ]
    },
    {
      "name": "BraceLabels",
      "mobject_type": "VGroup",
      "properties": {},
      "mobjects": [
        {
          "name": "LabelBraceBD",
          "mobject_type": "MathTex",
          "properties": {
            "text": "24",
            "position": "BraceBD.get_center() + RIGHT*0.5"
          }
        },
        {
          "name": "LabelBraceAC",
          "mobject_type": "MathTex",
          "properties": {
            "text": "24",
            "position": "BraceAC.get_center() + LEFT*0.5"
          }
        }
      ]
    }
  ],
  "animation_flow": [
    {
      "description": "Display the initial diagram and title.",
      "animations": [
        {
          "manim_function": "FadeIn",
          "target_mobjects": [
            "ProblemDiagram",
            "DiagramLabels"
          ]
        },
        {
          "manim_function": "Write",
          "target_mobjects": [
            "CalcTitle"
          ]
        }
      ]
    },
    {
      "description": "Show the calculation for BD and AC.",
      "animations": [
        {
          "manim_function": "Write",
          "target_mobjects": [
            "Calculations[0]"
          ]
        },
        {
          "manim_function": "Write",
          "target_mobjects": [
            "Calculations[1]"
          ],
          "params": {
            "run_time": 1.5
          }
        }
      ]
    },
    {
      "description": "Add braces and labels to the diagram to show the full lengths.",
      "animations": [
        {
          "manim_function": "Create",
          "target_mobjects": [
            "Braces"
          ]
        },
        {
          "manim_function": "Write",
          "target_mobjects": [
            "BraceLabels"
          ]
        }
      ]
    }
  ]
}
scene_script = {
  "scene_id": "part_b_calculate_bd_and_ac",
  "duration_seconds": 10,
  "audio_file_path": "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Scene/part_b_calculate_bd_and_ac_scene.mp3"
}
style_config = {
  "theme": {
    "name": "3Blue1Brown",
    "description": "Mathematical animation style inspired by 3Blue1Brown",
    "background_color": "#0C0C0C",
    "grid_color": "#1E1E1E",
    "show_grid": False
  },
  "colors": {
    "primary": {
      "blue": "#3B82F6",
      "light_blue": "#60A5FA",
      "dark_blue": "#1E40AF",
      "navy": "#1E3A8A"
    },
    "accent": {
      "yellow": "#FDE047",
      "gold": "#F59E0B",
      "orange": "#FB923C",
      "red": "#EF4444",
      "green": "#22C55E",
      "purple": "#A855F7",
      "pink": "#EC4899"
    },
    "neutral": {
      "white": "#FFFFFF",
      "light_gray": "#E5E7EB",
      "gray": "#9CA3AF",
      "dark_gray": "#4B5563",
      "black": "#000000"
    },
    "mathematical": {
      "vector": "#3B82F6",
      "matrix": "#22C55E",
      "function": "#F59E0B",
      "derivative": "#EF4444",
      "integral": "#A855F7",
      "complex": "#EC4899",
      "real": "#60A5FA",
      "imaginary": "#FB923C"
    },
    "semantic": {
      "correct": "#22C55E",
      "incorrect": "#EF4444",
      "neutral": "#9CA3AF",
      "highlight": "#FDE047",
      "emphasis": "#FB923C",
      "subtle": "#6B7280"
    }
  },
  "fonts": {
    "math": {
      "family": "CMU Serif",
      "fallback": [
        "Times New Roman",
        "serif"
      ],
      "size": {
        "small": 24,
        "medium": 32,
        "large": 48,
        "xlarge": 64
      }
    },
    "text": {
      "family": "Inter",
      "fallback": [
        "Arial",
        "Helvetica",
        "sans-serif"
      ],
      "size": {
        "small": 20,
        "medium": 28,
        "large": 36,
        "xlarge": 48
      }
    },
    "code": {
      "family": "JetBrains Mono",
      "fallback": [
        "Consolas",
        "Monaco",
        "monospace"
      ],
      "size": {
        "small": 18,
        "medium": 24,
        "large": 32
      }
    },
    "title": {
      "family": "Inter",
      "fallback": [
        "Arial",
        "Helvetica",
        "sans-serif"
      ],
      "weight": "bold",
      "size": {
        "medium": 40,
        "large": 56,
        "xlarge": 72
      }
    }
  },
  "animations": {
    "default_duration": 1.0,
    "default_run_time": 1.0,
    "timing": {
      "very_fast": 0.3,
      "fast": 0.5,
      "normal": 1.0,
      "slow": 1.5,
      "very_slow": 2.0
    },
    "easing": {
      "default": "smooth",
      "gentle": "ease_in_out_cubic",
      "sharp": "ease_in_out_expo",
      "bounce": "ease_out_bounce",
      "elastic": "ease_out_elastic"
    },
    "types": {
      "creation": {
        "preferred": "DrawBorderThenFill",
        "alternatives": [
          "Create",
          "Create",
          "Write"
        ],
        "duration": 1.0
      },
      "transformation": {
        "preferred": "Transform",
        "alternatives": [
          "ReplacementTransform",
          "TransformFromCopy"
        ],
        "duration": 1.0
      },
      "movement": {
        "preferred": "shift",
        "alternatives": [
          "move_to",
          "next_to"
        ],
        "duration": 0.5
      },
      "emphasis": {
        "preferred": "Indicate",
        "alternatives": [
          "Flash",
          "ShowIncreasingSubsets",
          "Circumscribe"
        ],
        "duration": 0.8
      },
      "reveal": {
        "preferred": "FadeIn",
        "alternatives": [
          "GrowFromCenter",
          "DrawBorderThenFill"
        ],
        "duration": 0.8
      },
      "hide": {
        "preferred": "FadeOut",
        "alternatives": [
          "ShrinkToCenter",
          "Unwrite"
        ],
        "duration": 0.5
      }
    },
    "mathematical": {
      "equation_reveal": {
        "method": "Write",
        "duration": 2.0,
        "stagger": 0.1
      },
      "function_plot": {
        "method": "Create",
        "duration": 2.0,
        "rate_func": "linear"
      },
      "vector_draw": {
        "method": "GrowArrow",
        "duration": 1.0
      },
      "transformation_matrix": {
        "method": "Transform",
        "duration": 1.5,
        "show_basis_vectors": True
      }
    }
  },
  "objects": {
    "axes": {
      "color": "#4B5563",
      "stroke_width": 2,
      "tick_color": "#6B7280",
      "label_color": "#E5E7EB",
      "number_scale_factor": 0.7,
      "include_tip": True,
      "tip_length": 0.2
    },
    "grid": {
      "color": "#1F2937",
      "stroke_width": 1,
      "opacity": 0.3
    },
    "vectors": {
      "color": "#3B82F6",
      "stroke_width": 4,
      "tip_length": 0.3,
      "max_tip_length_to_length_ratio": 0.25,
      "max_stroke_width_to_length_ratio": 8
    },
    "functions": {
      "color": "#F59E0B",
      "stroke_width": 3,
      "discontinuities_style": "dot"
    },
    "text": {
      "default_color": "#FFFFFF",
      "math_color": "#FFFFFF",
      "background_stroke_width": 0,
      "background_stroke_color": "#000000"
    },
    "shapes": {
      "fill_opacity": 0.3,
      "stroke_width": 2,
      "stroke_opacity": 1.0
    },
    "dots": {
      "radius": 0.08,
      "color": "#FFFFFF",
      "stroke_width": 0
    },
    "lines": {
      "stroke_width": 2,
      "color": "#FFFFFF"
    }
  },
  "layout": {
    "margins": {
      "top": 0.5,
      "bottom": 0.5,
      "left": 0.5,
      "right": 0.5
    },
    "spacing": {
      "small": 0.2,
      "medium": 0.5,
      "large": 1.0,
      "xlarge": 1.5
    },
    "positioning": {
      "title": "UP * 3",
      "subtitle": "UP * 2.2",
      "equation_main": "ORIGIN",
      "equation_steps": "DOWN * 0.8",
      "side_notes": "RIGHT * 4",
      "bottom_notes": "DOWN * 3"
    }
  },
  "mathematical_objects": {
    "matrices": {
      "bracket_color": "#FFFFFF",
      "element_color": "#FFFFFF",
      "bracket_h_buff": 0.1,
      "bracket_v_buff": 0.1,
      "element_alignment": "center"
    },
    "vectors": {
      "bracket_type": "square",
      "color": "#3B82F6",
      "component_colors": [
        "#3B82F6",
        "#22C55E",
        "#EF4444"
      ]
    },
    "equations": {
      "equals_color": "#FFFFFF",
      "operator_color": "#F59E0B",
      "variable_color": "#3B82F6",
      "constant_color": "#22C55E",
      "function_color": "#A855F7"
    },
    "graphs": {
      "axes_color": "#4B5563",
      "grid_color": "#1F2937",
      "function_colors": [
        "#3B82F6",
        "#22C55E",
        "#F59E0B",
        "#EF4444",
        "#A855F7"
      ],
      "point_color": "#FFFFFF",
      "tangent_color": "#FB923C",
      "area_fill_opacity": 0.3
    },
    "geometry": {
      "line_color": "#FFFFFF",
      "angle_color": "#FDE047",
      "right_angle_symbol": True,
      "point_labels": True,
      "measurement_color": "#22C55E"
    }
  },
  "scenes": {
    "intro": {
      "background_color": "#0C0C0C",
      "title_color": "#FFFFFF",
      "subtitle_color": "#9CA3AF",
      "accent_color": "#3B82F6"
    },
    "explanation": {
      "background_color": "#0C0C0C",
      "text_color": "#FFFFFF",
      "highlight_color": "#FDE047",
      "emphasis_color": "#FB923C"
    },
    "calculation": {
      "background_color": "#0C0C0C",
      "equation_color": "#FFFFFF",
      "step_highlight_color": "#22C55E",
      "error_color": "#EF4444"
    },
    "visualization": {
      "background_color": "#0C0C0C",
      "primary_object_color": "#3B82F6",
      "secondary_object_color": "#22C55E",
      "auxiliary_color": "#6B7280"
    }
  },
  "transitions": {
    "scene_to_scene": {
      "type": "FadeTransition",
      "duration": 0.5
    },
    "equation_steps": {
      "type": "TransformMatchingParts",
      "duration": 1.0,
      "stagger": 0.1
    },
    "concept_introduction": {
      "type": "GrowFromCenter",
      "duration": 1.0
    }
  },
  "audio": {
    "sync_equations_to_speech": True,
    "equation_reveal_timing": "word_by_word",
    "pause_durations": {
      "short": 0.5,
      "medium": 1.0,
      "long": 1.5
    }
  },
  "preferences": {
    "show_coordinate_system": False,
    "show_frame_border": False,
    "auto_scale_equations": True,
    "center_equations": True,
    "use_tex_templates": True,
    "tex_template": "amsmath",
    "render_quality": "high",
    "frame_rate": 60
  },
  "custom_styles": {
    "theorem_box": {
      "background_color": "#1E3A8A",
      "background_opacity": 0.2,
      "border_color": "#3B82F6",
      "border_width": 2,
      "text_color": "#FFFFFF",
      "padding": 0.3
    },
    "definition_box": {
      "background_color": "#166534",
      "background_opacity": 0.2,
      "border_color": "#22C55E",
      "border_width": 2,
      "text_color": "#FFFFFF",
      "padding": 0.3
    },
    "example_box": {
      "background_color": "#92400E",
      "background_opacity": 0.2,
      "border_color": "#F59E0B",
      "border_width": 2,
      "text_color": "#FFFFFF",
      "padding": 0.3
    },
    "highlight_bubble": {
      "color": "#FDE047",
      "opacity": 0.3,
      "stroke_width": 2,
      "stroke_color": "#F59E0B"
    },
    "thought_bubble": {
      "fill_color": "#374151",
      "fill_opacity": 0.8,
      "stroke_color": "#9CA3AF",
      "stroke_width": 1,
      "text_color": "#FFFFFF"
    }
  },
  "interactive_elements": {
    "slider": {
      "track_color": "#4B5563",
      "handle_color": "#3B82F6",
      "value_color": "#FFFFFF"
    },
    "button": {
      "fill_color": "#3B82F6",
      "stroke_color": "#1E40AF",
      "text_color": "#FFFFFF",
      "hover_color": "#60A5FA"
    },
    "checkbox": {
      "unchecked_color": "#4B5563",
      "checked_color": "#22C55E",
      "checkmark_color": "#FFFFFF"
    }
  },
  "accessibility": {
    "high_contrast_mode": False,
    "large_text_mode": False,
    "color_blind_friendly": True,
    "screen_reader_compatible": False
  },
  "version": "1.0",
  "created_by": "Manim Orchestrator",
  "description": "A comprehensive style configuration that emulates the distinctive visual style of 3Blue1Brown mathematical animations, featuring deep blue primary colors, careful typography choices, smooth animations, and mathematical object styling optimized for educational content."
}

class PartBCalculateBdAndAc(Scene):
    def construct(self):
        # Parse injected JSON variables
        plan = scene_plan
        script = scene_script
        style_data = style_config
        style = style_data
        
        # Set background color
        self.camera.background_color = style.get("theme", {}).get("background_color", "#0C0C0C")
        
        # Audio setup
        audio_path = script.get("audio_file_path")
        if audio_path:
            self.add_sound(audio_path)
        
        # Mobject instantiation
        mobjects = {}
        
        # Create problem diagram (simplified geometric diagram)
        diagram_elements = VGroup()
        
        # Create a quadrilateral ABCD with diagonals
        A = Dot(LEFT*2 + UP*1.5, color=style["colors"]["neutral"]["white"])
        B = Dot(RIGHT*0.5 + UP*1.5, color=style["colors"]["neutral"]["white"])
        C = Dot(RIGHT*0.5 + DOWN*1.5, color=style["colors"]["neutral"]["white"])
        D = Dot(LEFT*2 + DOWN*1.5, color=style["colors"]["neutral"]["white"])
        E = Dot(LEFT*0.75 + ORIGIN, color=style["colors"]["accent"]["yellow"])
        
        # Create the quadrilateral
        quad = Polygon(A.get_center(), B.get_center(), C.get_center(), D.get_center(), 
                      color=style["colors"]["primary"]["blue"], stroke_width=2, fill_opacity=0.1)
        
        # Create diagonals
        diagonal_AC = Line(A.get_center(), C.get_center(), color=style["colors"]["accent"]["red"], stroke_width=3)
        diagonal_BD = Line(B.get_center(), D.get_center(), color=style["colors"]["accent"]["green"], stroke_width=3)
        
        # Add points
        diagram_elements.add(quad, diagonal_AC, diagonal_BD, A, B, C, D, E)
        
        # Create labels
        label_A = Tex("A", color=style["colors"]["neutral"]["white"]).next_to(A, UP+LEFT, buff=0.1)
        label_B = Tex("B", color=style["colors"]["neutral"]["white"]).next_to(B, UP+RIGHT, buff=0.1)
        label_C = Tex("C", color=style["colors"]["neutral"]["white"]).next_to(C, DOWN+RIGHT, buff=0.1)
        label_D = Tex("D", color=style["colors"]["neutral"]["white"]).next_to(D, DOWN+LEFT, buff=0.1)
        label_E = Tex("E", color=style["colors"]["accent"]["yellow"]).next_to(E, RIGHT, buff=0.1)
        
        # Add segment labels
        label_BE = Tex("15", color=style["colors"]["accent"]["orange"]).next_to(
            Line(B.get_center(), E.get_center()).get_center(), UP, buff=0.1)
        label_DE = Tex("9", color=style["colors"]["accent"]["orange"]).next_to(
            Line(D.get_center(), E.get_center()).get_center(), DOWN, buff=0.1)
        
        labels = VGroup(label_A, label_B, label_C, label_D, label_E, label_BE, label_DE)
        
        mobjects["ProblemDiagram"] = diagram_elements.move_to(LEFT*3)
        mobjects["DiagramLabels"] = labels.move_to(LEFT*3)
        
        # Create title
        mobjects["CalcTitle"] = Tex("Calculate Diagonal Lengths AC and BD", 
                                   color=style["colors"]["neutral"]["white"]).to_edge(UP)
        
        # Create calculations
        calc_bd = MathTex("BD = BE + DE = 15 + 9 = 24 \\text{ cm}", 
                         color=style["colors"]["neutral"]["white"])
        calc_ac = MathTex("AC = BD = 24 \\text{ cm} \\text{ (from congruence)}", 
                         color=style["colors"]["neutral"]["white"])
        
        mobjects["Calculations"] = VGroup(calc_bd, calc_ac).arrange(DOWN, buff=0.8).move_to(RIGHT*3)
        
        # Create braces for the diagram
        brace_bd = Brace(diagonal_BD, RIGHT, color=style["colors"]["accent"]["green"])
        brace_ac = Brace(diagonal_AC, LEFT, color=style["colors"]["accent"]["red"])
        
        mobjects["Braces"] = VGroup(brace_bd, brace_ac)
        
        # Create brace labels
        label_brace_bd = MathTex("24", color=style["colors"]["accent"]["green"]).next_to(brace_bd, RIGHT)
        label_brace_ac = MathTex("24", color=style["colors"]["accent"]["red"]).next_to(brace_ac, LEFT)
        
        mobjects["BraceLabels"] = VGroup(label_brace_bd, label_brace_ac)
        
        # Initial scene setup
        for mobject_name in ["ProblemDiagram", "DiagramLabels"]:
            if mobject_name in mobjects:
                self.add(mobjects[mobject_name])
        
        # Time tracking and animation flow
        current_time = 0.0
        
        # Animation group 1: Display initial diagram and title (0.0 - 3.66)
        sentence_group_end_time = 3.66
        animation_run_time = 1.5
        
        self.play(
            Write(mobjects["CalcTitle"]),
            run_time=animation_run_time,
            rate_func=smooth
        )
        
        wait_duration = sentence_group_end_time - current_time - animation_run_time
        if wait_duration > 0:
            self.wait(wait_duration)
        current_time = sentence_group_end_time
        
        # Animation group 2: Show BD calculation (3.67 - 6.18)
        sentence_group_end_time = 6.18
        animation_run_time = 1.5
        
        # Highlight BE and DE segments
        highlight_be = Line(B.get_center(), E.get_center(), color=style["colors"]["accent"]["yellow"], stroke_width=6)
        highlight_de = Line(D.get_center(), E.get_center(), color=style["colors"]["accent"]["yellow"], stroke_width=6)
        
        self.play(
            Create(highlight_be),
            Create(highlight_de),
            run_time=animation_run_time,
            rate_func=smooth
        )
        
        wait_duration = sentence_group_end_time - current_time - animation_run_time
        if wait_duration > 0:
            self.wait(wait_duration)
        current_time = sentence_group_end_time
        
        # Animation group 3: Show AC = BD relationship (6.19 - 10.37)
        sentence_group_end_time = 10.0  # Adjusted to fit within scene duration
        animation_run_time = 2.0
        
        self.play(
            Write(mobjects["Calculations"][0]),
            run_time=animation_run_time,
            rate_func=smooth
        )
        
        wait_duration = sentence_group_end_time - current_time - animation_run_time
        if wait_duration > 0:
            self.wait(wait_duration)
        current_time = sentence_group_end_time
        
        # Final animation: Show AC calculation and add braces
        remaining_time = script["duration_seconds"] - current_time
        if remaining_time > 0.5:
            animation_run_time = min(remaining_time - 0.1, 2.0)
            
            self.play(
                Write(mobjects["Calculations"][1]),
                Create(mobjects["Braces"]),
                Write(mobjects["BraceLabels"]),
                run_time=animation_run_time,
                rate_func=smooth
            )
            
            current_time += animation_run_time
        
        # Final padding
        remaining_time = script["duration_seconds"] - current_time
        if remaining_time > 0.01:
            self.wait(remaining_time)

# Replace Create with Create for Manim v0.19.0 compatibility
with open(__file__, 'r', encoding='utf-8') as f:
    code = f.read()
code = re.sub('Create', 'Create', code)
with open(__file__, 'w', encoding='utf-8') as f:
    f.write(code)
