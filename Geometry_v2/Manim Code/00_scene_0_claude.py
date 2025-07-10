from manim import *
import numpy as np
import math
import json

scene_plan = {
  "blueprint": [
    {
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
          "name": "SceneTitle",
          "mobject_type": "Text",
          "properties": {
            "text": "Part A: Understanding the Goal",
            "font_size": 48,
            "color": "#FFFFFF",
            "position": "UP * 3.2"
          }
        },
        {
          "name": "GeometryDiagram",
          "mobject_type": "VGroup",
          "properties": {
            "description": "Main quadrilateral ABCD with diagonals creating triangles ABC and BAD",
            "position": "LEFT * 3.5",
            "scale": 1.5
          }
        },
        {
          "name": "TriangleABC",
          "mobject_type": "Polygon",
          "properties": {
            "vertices": "[[0, 0, 0], [2, 0, 0], [1, 1.5, 0]]",
            "color": "#3B82F6",
            "fill_opacity": 0.2,
            "stroke_width": 3
          }
        },
        {
          "name": "TriangleBAD",
          "mobject_type": "Polygon",
          "properties": {
            "vertices": "[[2, 0, 0], [0, 0, 0], [0.5, -1.5, 0]]",
            "color": "#22C55E",
            "fill_opacity": 0.2,
            "stroke_width": 3
          }
        },
        {
          "name": "PointA",
          "mobject_type": "Dot",
          "properties": {
            "point": "[0, 0, 0]",
            "color": "#FFFFFF",
            "radius": 0.08
          }
        },
        {
          "name": "PointB",
          "mobject_type": "Dot",
          "properties": {
            "point": "[2, 0, 0]",
            "color": "#FFFFFF",
            "radius": 0.08
          }
        },
        {
          "name": "PointC",
          "mobject_type": "Dot",
          "properties": {
            "point": "[1, 1.5, 0]",
            "color": "#FFFFFF",
            "radius": 0.08
          }
        },
        {
          "name": "PointD",
          "mobject_type": "Dot",
          "properties": {
            "point": "[0.5, -1.5, 0]",
            "color": "#FFFFFF",
            "radius": 0.08
          }
        },
        {
          "name": "LabelA",
          "mobject_type": "Text",
          "properties": {
            "text": "A",
            "font_size": 32,
            "color": "#FFFFFF",
            "position": "PointA.get_center() + LEFT * 0.3 + UP * 0.2"
          }
        },
        {
          "name": "LabelB",
          "mobject_type": "Text",
          "properties": {
            "text": "B",
            "font_size": 32,
            "color": "#FFFFFF",
            "position": "PointB.get_center() + RIGHT * 0.3 + UP * 0.2"
          }
        },
        {
          "name": "LabelC",
          "mobject_type": "Text",
          "properties": {
            "text": "C",
            "font_size": 32,
            "color": "#FFFFFF",
            "position": "PointC.get_center() + UP * 0.3"
          }
        },
        {
          "name": "LabelD",
          "mobject_type": "Text",
          "properties": {
            "text": "D",
            "font_size": 32,
            "color": "#FFFFFF",
            "position": "PointD.get_center() + DOWN * 0.3"
          }
        },
        {
          "name": "GoalStatement",
          "mobject_type": "Tex",
          "properties": {
            "text": "Goal: Prove $\\triangle ABC \\cong \\triangle BAD$",
            "font_size": 40,
            "color": "#FDE047",
            "position": "RIGHT * 3 + UP * 1.5"
          }
        },
        {
          "name": "GoalBox",
          "mobject_type": "SurroundingRectangle",
          "properties": {
            "mobject": "GoalStatement",
            "color": "#F59E0B",
            "stroke_width": 2,
            "buff": 0.2
          }
        },
        {
          "name": "CongruenceSymbol",
          "mobject_type": "MathTex",
          "properties": {
            "text": "\\cong",
            "font_size": 60,
            "color": "#FB923C",
            "position": "RIGHT * 3 + DOWN * 0.5"
          }
        },
        {
          "name": "Triangle1Label",
          "mobject_type": "Text",
          "properties": {
            "text": "Triangle 1",
            "font_size": 28,
            "color": "#3B82F6",
            "position": "RIGHT * 2 + DOWN * 1.5"
          }
        },
        {
          "name": "Triangle2Label",
          "mobject_type": "Text",
          "properties": {
            "text": "Triangle 2",
            "font_size": 28,
            "color": "#22C55E",
            "position": "RIGHT * 4 + DOWN * 1.5"
          }
        },
        {
          "name": "ObjectiveText",
          "mobject_type": "Text",
          "properties": {
            "text": "Objective: Demonstrate congruence",
            "font_size": 32,
            "color": "#FFFFFF",
            "position": "RIGHT * 3 + DOWN * 2.5"
          }
        }
      ],
      "animation_flow": [
        {
          "description": "Introduce the scene with title",
          "animations": [
            {
              "manim_function": "Write",
              "target_mobjects": [
                "SceneTitle"
              ],
              "run_time": 1.0
            }
          ]
        },
        {
          "description": "Create the geometric diagram with points and labels",
          "animations": [
            {
              "manim_function": "Create",
              "target_mobjects": [
                "PointA",
                "PointB",
                "PointC",
                "PointD"
              ],
              "run_time": 1.0
            },
            {
              "manim_function": "Write",
              "target_mobjects": [
                "LabelA",
                "LabelB",
                "LabelC",
                "LabelD"
              ],
              "run_time": 0.8
            }
          ]
        },
        {
          "description": "Highlight triangle ABC",
          "animations": [
            {
              "manim_function": "Create",
              "target_mobjects": [
                "TriangleABC"
              ],
              "run_time": 1.2
            },
            {
              "manim_function": "Write",
              "target_mobjects": [
                "Triangle1Label"
              ],
              "run_time": 0.6
            }
          ]
        },
        {
          "description": "Highlight triangle BAD",
          "animations": [
            {
              "manim_function": "Create",
              "target_mobjects": [
                "TriangleBAD"
              ],
              "run_time": 1.2
            },
            {
              "manim_function": "Write",
              "target_mobjects": [
                "Triangle2Label"
              ],
              "run_time": 0.6
            }
          ]
        },
        {
          "description": "Present the goal statement with emphasis",
          "animations": [
            {
              "manim_function": "Write",
              "target_mobjects": [
                "GoalStatement"
              ],
              "run_time": 1.5
            },
            {
              "manim_function": "Create",
              "target_mobjects": [
                "GoalBox"
              ],
              "run_time": 0.8
            }
          ]
        },
        {
          "description": "Show congruence symbol and emphasize the objective",
          "animations": [
            {
              "manim_function": "Write",
              "target_mobjects": [
                "CongruenceSymbol"
              ],
              "run_time": 1.0
            },
            {
              "manim_function": "Indicate",
              "target_mobjects": [
                "CongruenceSymbol"
              ],
              "run_time": 0.5
            }
          ]
        },
        {
          "description": "Final emphasis on the objective",
          "animations": [
            {
              "manim_function": "Write",
              "target_mobjects": [
                "ObjectiveText"
              ],
              "run_time": 1.5
            },
            {
              "manim_function": "Wiggle",
              "target_mobjects": [
                "TriangleABC",
                "TriangleBAD"
              ],
              "run_time": 1.0
            }
          ]
        }
      ]
    }
  ]
}
scene_script = {
  "scene_id": "scene",
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
        # --- 1. Use Injected Python Dicts Directly ---
        style = style_config.get("colors", {})
        
        self.camera.background_color = "#0C0C0C"

        # --- 2. Audio Setup (Conditional) ---
        audio_path = scene_script.get("audio_file_path")
        if audio_path:
            self.add_sound(audio_path)
        
        # --- 3. Mobject Instantiation ---
        mobjects = {}
        
        # Create title
        mobjects['SceneTitle'] = Text(
            "Part A: Understanding the Goal",
            font_size=48,
            color=style.get("neutral", {}).get("white", "#FFFFFF")
        ).to_edge(UP)
        
        # Create geometric points
        mobjects['PointA'] = Dot(np.array([0, 0, 0]), color="#FFFFFF", radius=0.08)
        mobjects['PointB'] = Dot(np.array([2, 0, 0]), color="#FFFFFF", radius=0.08)
        mobjects['PointC'] = Dot(np.array([1, 1.5, 0]), color="#FFFFFF", radius=0.08)
        mobjects['PointD'] = Dot(np.array([0.5, -1.5, 0]), color="#FFFFFF", radius=0.08)
        
        # Create triangles
        mobjects['TriangleABC'] = Polygon(
            np.array([0, 0, 0]), np.array([2, 0, 0]), np.array([1, 1.5, 0]),
            color=style.get("primary", {}).get("blue", "#3B82F6"),
            fill_opacity=0.2,
            stroke_width=3
        )
        
        mobjects['TriangleBAD'] = Polygon(
            np.array([2, 0, 0]), np.array([0, 0, 0]), np.array([0.5, -1.5, 0]),
            color=style.get("accent", {}).get("green", "#22C55E"),
            fill_opacity=0.2,
            stroke_width=3
        )
        
        # Create labels
        mobjects['LabelA'] = Text("A", font_size=32, color="#FFFFFF").next_to(mobjects['PointA'], LEFT + UP, buff=0.1)
        mobjects['LabelB'] = Text("B", font_size=32, color="#FFFFFF").next_to(mobjects['PointB'], RIGHT + UP, buff=0.1)
        mobjects['LabelC'] = Text("C", font_size=32, color="#FFFFFF").next_to(mobjects['PointC'], UP, buff=0.1)
        mobjects['LabelD'] = Text("D", font_size=32, color="#FFFFFF").next_to(mobjects['PointD'], DOWN, buff=0.1)
        
        # Create geometry diagram group
        geometry_group = VGroup(
            mobjects['PointA'], mobjects['PointB'], mobjects['PointC'], mobjects['PointD'],
            mobjects['TriangleABC'], mobjects['TriangleBAD'],
            mobjects['LabelA'], mobjects['LabelB'], mobjects['LabelC'], mobjects['LabelD']
        )
        geometry_group.scale(1.5).shift(LEFT * 3.5)
        
        # Create goal statement
        mobjects['GoalStatement'] = Tex(
            "Goal: Prove $\\triangle ABC \\cong \\triangle BAD$",
            font_size=40,
            color=style.get("accent", {}).get("yellow", "#FDE047")
        ).shift(RIGHT * 3 + UP * 1.5)
        
        # SurroundingRectangle will be created after GoalStatement is written
        
        # Create congruence symbol
        mobjects['CongruenceSymbol'] = MathTex(
            "\\cong",
            font_size=60,
            color=style.get("accent", {}).get("orange", "#FB923C")
        ).shift(RIGHT * 3 + DOWN * 0.5)
        
        # Create triangle labels
        mobjects['Triangle1Label'] = Text(
            "Triangle 1",
            font_size=28,
            color=style.get("primary", {}).get("blue", "#3B82F6")
        ).shift(RIGHT * 2 + DOWN * 1.5)
        
        mobjects['Triangle2Label'] = Text(
            "Triangle 2",
            font_size=28,
            color=style.get("accent", {}).get("green", "#22C55E")
        ).shift(RIGHT * 4 + DOWN * 1.5)
        
        # Create objective text
        mobjects['ObjectiveText'] = Text(
            "Objective: Demonstrate congruence",
            font_size=32,
            color="#FFFFFF"
        ).shift(RIGHT * 3 + DOWN * 2.5)

        # --- 4. Initial Scene Setup ---
        # No initial mobjects specified

        # --- 5. Time Tracking & Animation Flow ---
        current_time = 0.0
        
        # Animation Group 1: Introduce title (0.0 - 3.24)
        sentence_end_time = 3.24
        self.play(
            Write(mobjects['SceneTitle']),
            run_time=1.0,
            rate_func=smooth
        )
        current_time += 1.0
        
        wait_duration = sentence_end_time - current_time
        if wait_duration > 0:
            self.wait(wait_duration)
        current_time = sentence_end_time
        
        # Animation Group 2: Create geometric diagram (3.25 - 7.19)
        sentence_end_time = 7.19
        self.play(
            Create(mobjects['PointA']),
            Create(mobjects['PointB']),
            Create(mobjects['PointC']),
            Create(mobjects['PointD']),
            run_time=1.0,
            rate_func=smooth
        )
        current_time += 1.0
        
        self.play(
            Write(mobjects['LabelA']),
            Write(mobjects['LabelB']),
            Write(mobjects['LabelC']),
            Write(mobjects['LabelD']),
            run_time=0.8,
            rate_func=smooth
        )
        current_time += 0.8
        
        # Create triangles
        self.play(
            Create(mobjects['TriangleABC']),
            run_time=1.2,
            rate_func=smooth
        )
        current_time += 1.2
        
        self.play(
            Create(mobjects['TriangleBAD']),
            run_time=1.2,
            rate_func=smooth
        )
        current_time += 1.2
        
        wait_duration = sentence_end_time - current_time
        if wait_duration > 0:
            self.wait(wait_duration)
        current_time = sentence_end_time
        
        # Animation Group 3: Present goal statement (7.2 - 10.86)
        sentence_end_time = 10.86
        self.play(
            Write(mobjects['GoalStatement']),
            run_time=1.5,
            rate_func=smooth
        )
        current_time += 1.5
        
        # Now create and animate the SurroundingRectangle (GoalBox) after GoalStatement is on the scene
        from manim import Mobject
        if isinstance(mobjects['GoalStatement'], Mobject):
            mobjects['GoalBox'] = SurroundingRectangle(
                mobjects['GoalStatement'],
                color=style.get("accent", {}).get("gold", "#F59E0B"),
                stroke_width=2,
                buff=0.2
            )
            self.play(
                Create(mobjects['GoalBox']),
                run_time=0.8,
                rate_func=smooth
            )
            current_time += 0.8
        else:
            print("Warning: GoalStatement is not a valid Mobject for SurroundingRectangle.")
        
        # Show congruence symbol
        self.play(
            Write(mobjects['CongruenceSymbol']),
            run_time=1.0,
            rate_func=smooth
        )
        current_time += 1.0
        
        self.play(
            Indicate(mobjects['CongruenceSymbol']),
            run_time=0.5,
            rate_func=smooth
        )
        current_time += 0.5
        
        wait_duration = sentence_end_time - current_time
        if wait_duration > 0:
            self.wait(wait_duration)
        current_time = sentence_end_time
        
        # Final animation: Emphasize objective (remaining time)
        remaining_time = scene_script["duration_seconds"] - current_time
        if remaining_time > 0:
            animation_time = min(1.5, remaining_time * 0.7)
            self.play(
                Write(mobjects['ObjectiveText']),
                run_time=animation_time,
                rate_func=smooth
            )
            current_time += animation_time
            
            # Final wiggle if there's time
            final_remaining = scene_script["duration_seconds"] - current_time
            if final_remaining > 0.5:
                wiggle_time = min(1.0, final_remaining * 0.8)
                self.play(
                    Wiggle(mobjects['TriangleABC']),
                    Wiggle(mobjects['TriangleBAD']),
                    run_time=wiggle_time,
                    rate_func=smooth
                )
                current_time += wiggle_time
        
        # --- 6. Final Padding ---
        final_wait = scene_script["duration_seconds"] - current_time
        if final_wait > 0.01:
            self.wait(final_wait)
