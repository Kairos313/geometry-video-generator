from manim import *
import numpy as np
import math
import json

scene_plan = {
  "scene_id": "part_a_understand_goal",
  "sentence_timestamps": [
    {
      "text": "For part A, our first step is to understand what we need to prove.",
      "start": 0.0,
      "end": 3.24
    },
    {
      "text": "We need to show that triangle A B C is congruent to triangle B A D.",
      "start": 3.25,
      "end": 7.19
    },
    {
      "text": "Goal: Prove triangle A B C is congruent to triangle B A D.",
      "start": 7.2,
      "end": 10.86
    },
    {
      "text": "Our objective is to demonstrate the congruence of the two triangles.",
      "start": 10.87,
      "end": 14.76
    }
  ],
  "initial_mobjects": [],
  "mobjects": [
    {
      "name": "Title",
      "mobject_type": "Tex",
      "properties": {
        "text": "Part A: Prove Congruence",
        "position": "UP*3.5"
      }
    },
    {
      "name": "ProblemDiagram",
      "mobject_type": "VGroup",
      "properties": {
        "description": "Base diagram of the geometric problem.",
        "position": "LEFT*3"
      },
      "mobjects": [
        {
          "name": "Points",
          "mobject_type": "VGroup",
          "properties": {},
          "mobjects": [
            {
              "name": "A",
              "mobject_type": "Dot",
              "properties": {
                "point": "[-2, -1.5, 0]"
              }
            },
            {
              "name": "B",
              "mobject_type": "Dot",
              "properties": {
                "point": "[2, -1.5, 0]"
              }
            },
            {
              "name": "C",
              "mobject_type": "Dot",
              "properties": {
                "point": "[1.5, 1.5, 0]"
              }
            },
            {
              "name": "D",
              "mobject_type": "Dot",
              "properties": {
                "point": "[-1.5, 1.5, 0]"
              }
            },
            {
              "name": "E",
              "mobject_type": "Dot",
              "properties": {
                "description": "Intersection of AC and BD"
              }
            }
          ]
        },
        {
          "name": "Lines",
          "mobject_type": "VGroup",
          "properties": {},
          "mobjects": [
            {
              "name": "AB",
              "mobject_type": "Line",
              "properties": {
                "start": "A.get_center()",
                "end": "B.get_center()"
              }
            },
            {
              "name": "AC",
              "mobject_type": "Line",
              "properties": {
                "start": "A.get_center()",
                "end": "C.get_center()"
              }
            },
            {
              "name": "AD",
              "mobject_type": "Line",
              "properties": {
                "start": "A.get_center()",
                "end": "D.get_center()"
              }
            },
            {
              "name": "BC",
              "mobject_type": "Line",
              "properties": {
                "start": "B.get_center()",
                "end": "C.get_center()"
              }
            },
            {
              "name": "BD",
              "mobject_type": "Line",
              "properties": {
                "start": "B.get_center()",
                "end": "D.get_center()"
              }
            }
          ]
        },
        {
          "name": "Labels",
          "mobject_type": "VGroup",
          "properties": {},
          "mobjects": [
            {
              "name": "LabelA",
              "mobject_type": "Tex",
              "properties": {
                "text": "A",
                "position": "A.get_center() + DOWN*0.5"
              }
            },
            {
              "name": "LabelB",
              "mobject_type": "Tex",
              "properties": {
                "text": "B",
                "position": "B.get_center() + DOWN*0.5"
              }
            },
            {
              "name": "LabelC",
              "mobject_type": "Tex",
              "properties": {
                "text": "C",
                "position": "C.get_center() + UP*0.5"
              }
            },
            {
              "name": "LabelD",
              "mobject_type": "Tex",
              "properties": {
                "text": "D",
                "position": "D.get_center() + UP*0.5"
              }
            },
            {
              "name": "LabelE",
              "mobject_type": "Tex",
              "properties": {
                "text": "E",
                "position": "E.get_center() + RIGHT*0.5"
              }
            }
          ]
        }
      ]
    },
    {
      "name": "GoalText",
      "mobject_type": "MathTex",
      "properties": {
        "text": "\\text{Goal: Prove } \\triangle ABC \\cong \\triangle BAD",
        "position": "RIGHT*3"
      }
    },
    {
      "name": "TriangleHighlights",
      "mobject_type": "VGroup",
      "properties": {},
      "mobjects": [
        {
          "name": "HighlightABC",
          "mobject_type": "Polygon",
          "properties": {
            "vertices": [
              "A.get_center()",
              "B.get_center()",
              "C.get_center()"
            ],
            "color": "#3B82F6",
            "fill_opacity": 0.3
          }
        },
        {
          "name": "HighlightBAD",
          "mobject_type": "Polygon",
          "properties": {
            "vertices": [
              "B.get_center()",
              "A.get_center()",
              "D.get_center()"
            ],
            "color": "#F59E0B",
            "fill_opacity": 0.3
          }
        }
      ]
    }
  ],
  "animation_flow": [
    {
      "description": "Introduce Part A and the problem diagram.",
      "animations": [
        {
          "manim_function": "Write",
          "target_mobjects": [
            "Title"
          ]
        },
        {
          "manim_function": "Create",
          "target_mobjects": [
            "ProblemDiagram"
          ]
        }
      ]
    },
    {
      "description": "State the goal and visually identify the two triangles in question.",
      "animations": [
        {
          "manim_function": "Write",
          "target_mobjects": [
            "GoalText"
          ]
        },
        {
          "manim_function": "FadeIn",
          "target_mobjects": [
            "TriangleHighlights"
          ],
          "params": {
            "lag_ratio": 0.5
          }
        }
      ]
    },
    {
      "description": "Clear highlights for the next step.",
      "animations": [
        {
          "manim_function": "FadeOut",
          "target_mobjects": [
            "TriangleHighlights"
          ]
        }
      ]
    }
  ]
}
scene_script = {
  "scene_id": "part_a_understand_goal",
  "duration_seconds": 10,
  "audio_file_path": "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Scene/part_a_understand_goal_scene.mp3"
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
          "ShowCreation",
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
        "method": "ShowCreation",
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

class PartAUnderstandGoal(Scene):
    def construct(self):
        # --- 1. Parse Injected JSON ---
        plan = scene_plan
        script = scene_script
        style_data = style_config
        style = style_data.get("colors", {})
        
        self.camera.background_color = "#0C0C0C"

        # --- 2. Audio Setup (Conditional) ---
        audio_path = script.get("audio_file_path")
        if audio_path:
            self.add_sound(audio_path)
        
        # --- 3. Mobject Instantiation ---
        mobjects = {}
        
        # Create Title
        mobjects['Title'] = Tex("Part A: Prove Congruence", color=WHITE, font_size=40).to_edge(UP, buff=0.5)
        
        # Create Points first
        point_A = np.array([-2, -1.5, 0])
        point_B = np.array([2, -1.5, 0])
        point_C = np.array([1.5, 1.5, 0])
        point_D = np.array([-1.5, 1.5, 0])
        
        # Calculate intersection point E of lines AC and BD
        # Line AC: parametric form A + t(C - A)
        # Line BD: parametric form B + s(D - B)
        # Solving for intersection
        AC_dir = point_C - point_A
        BD_dir = point_D - point_B
        AB_vec = point_B - point_A
        
        # Solve: A + t(C-A) = B + s(D-B)
        # t(C-A) - s(D-B) = B - A
        det = AC_dir[0] * (-BD_dir[1]) - AC_dir[1] * (-BD_dir[0])
        t = (AB_vec[0] * (-BD_dir[1]) - AB_vec[1] * (-BD_dir[0])) / det
        point_E = point_A + t * AC_dir
        
        # Create dots
        dot_A = Dot(point_A, color=WHITE)
        dot_B = Dot(point_B, color=WHITE)
        dot_C = Dot(point_C, color=WHITE)
        dot_D = Dot(point_D, color=WHITE)
        dot_E = Dot(point_E, color=WHITE)
        
        # Create lines
        line_AB = Line(point_A, point_B, color=WHITE, stroke_width=2)
        line_AC = Line(point_A, point_C, color=WHITE, stroke_width=2)
        line_AD = Line(point_A, point_D, color=WHITE, stroke_width=2)
        line_BC = Line(point_B, point_C, color=WHITE, stroke_width=2)
        line_BD = Line(point_B, point_D, color=WHITE, stroke_width=2)
        
        # Create labels
        label_A = Tex("A", color=WHITE).next_to(dot_A, DOWN, buff=0.3)
        label_B = Tex("B", color=WHITE).next_to(dot_B, DOWN, buff=0.3)
        label_C = Tex("C", color=WHITE).next_to(dot_C, UP, buff=0.3)
        label_D = Tex("D", color=WHITE).next_to(dot_D, UP, buff=0.3)
        label_E = Tex("E", color=WHITE).next_to(dot_E, RIGHT, buff=0.3)
        
        # Group the diagram components
        points_group = VGroup(dot_A, dot_B, dot_C, dot_D, dot_E)
        lines_group = VGroup(line_AB, line_AC, line_AD, line_BC, line_BD)
        labels_group = VGroup(label_A, label_B, label_C, label_D, label_E)
        
        mobjects['ProblemDiagram'] = VGroup(points_group, lines_group, labels_group).shift(LEFT*3)
        
        # Create Goal Text
        mobjects['GoalText'] = MathTex(
            "\\text{Goal: Prove } \\triangle ABC \\cong \\triangle BAD",
            color=WHITE,
            font_size=32
        ).shift(RIGHT*3)
        
        # Create Triangle Highlights
        highlight_ABC = Polygon(
            point_A, point_B, point_C,
            color=style.get("primary", {}).get("blue", "#3B82F6"),
            fill_opacity=0.3,
            stroke_width=0
        ).shift(LEFT*3)
        
        highlight_BAD = Polygon(
            point_B, point_A, point_D,
            color=style.get("accent", {}).get("gold", "#F59E0B"),
            fill_opacity=0.3,
            stroke_width=0
        ).shift(LEFT*3)
        
        mobjects['TriangleHighlights'] = VGroup(highlight_ABC, highlight_BAD)

        # --- 4. Initial Scene Setup ---
        # No initial mobjects according to the plan
        
        # --- 5. Time Tracking & Animation ---
        current_time = 0.0
        
        # First sentence: 0.0 - 3.24 seconds
        # "For part A, our first step is to understand what we need to prove."
        self.play(
            Write(mobjects['Title']),
            Create(mobjects['ProblemDiagram']),
            run_time=2.5,
            rate_func=smooth
        )
        current_time += 2.5
        
        # Wait for remaining time of first sentence
        wait_time = 3.24 - current_time
        if wait_time > 0:
            self.wait(wait_time)
        current_time = 3.24
        
        # Second sentence: 3.25 - 7.19 seconds
        # "We need to show that triangle A B C is congruent to triangle B A D."
        self.play(
            Write(mobjects['GoalText']),
            FadeIn(mobjects['TriangleHighlights'], lag_ratio=0.5),
            run_time=2.5,
            rate_func=smooth
        )
        current_time += 2.5
        
        # Wait for remaining time of second sentence
        wait_time = 7.19 - current_time
        if wait_time > 0:
            self.wait(wait_time)
        current_time = 7.19
        
        # Third sentence: 7.2 - 10.86 seconds (but we only have 10 seconds total)
        # Clear highlights and prepare for next scene
        remaining_animation_time = min(1.5, script["duration_seconds"] - current_time - 0.5)
        
        self.play(
            FadeOut(mobjects['TriangleHighlights']),
            run_time=remaining_animation_time,
            rate_func=smooth
        )
        current_time += remaining_animation_time
        
        # --- 6. Final Padding ---
        remaining_time = script["duration_seconds"] - current_time
        if remaining_time > 0.01:
            self.wait(remaining_time)
