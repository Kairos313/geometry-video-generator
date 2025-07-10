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
      "name": "TitleCard",
      "mobject_type": "Tex",
      "properties": {
        "text": "Part A: Stating the Goal",
        "font_size": 40,
        "position": "UP*3.5"
      }
    },
    {
      "name": "ProblemDiagram",
      "mobject_type": "VGroup",
      "properties": {
        "description": "The main geometric diagram showing points A, B, C, D, and E, with right angle markers.",
        "position": "LEFT*3.5"
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
            }
          ]
        },
        {
          "name": "Lines",
          "mobject_type": "VGroup",
          "properties": {},
          "mobjects": [
            {
              "name": "Line_AB",
              "mobject_type": "Line",
              "properties": {
                "start": "A.get_center()",
                "end": "B.get_center()"
              }
            },
            {
              "name": "Line_AC",
              "mobject_type": "Line",
              "properties": {
                "start": "A.get_center()",
                "end": "C.get_center()"
              }
            },
            {
              "name": "Line_AD",
              "mobject_type": "Line",
              "properties": {
                "start": "A.get_center()",
                "end": "D.get_center()"
              }
            },
            {
              "name": "Line_BC",
              "mobject_type": "Line",
              "properties": {
                "start": "B.get_center()",
                "end": "C.get_center()"
              }
            },
            {
              "name": "Line_BD",
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
              "name": "Label_A",
              "mobject_type": "MathTex",
              "properties": {
                "text": "A",
                "next_to": "A",
                "direction": "DL"
              }
            },
            {
              "name": "Label_B",
              "mobject_type": "MathTex",
              "properties": {
                "text": "B",
                "next_to": "B",
                "direction": "DR"
              }
            },
            {
              "name": "Label_C",
              "mobject_type": "MathTex",
              "properties": {
                "text": "C",
                "next_to": "C",
                "direction": "UR"
              }
            },
            {
              "name": "Label_D",
              "mobject_type": "MathTex",
              "properties": {
                "text": "D",
                "next_to": "D",
                "direction": "UL"
              }
            }
          ]
        },
        {
          "name": "AngleMarkers",
          "mobject_type": "VGroup",
          "properties": {},
          "mobjects": [
            {
              "name": "Angle_ACB",
              "mobject_type": "RightAngle",
              "properties": {
                "line1": "Line(C.get_center(), A.get_center())",
                "line2": "Line(C.get_center(), B.get_center())",
                "length": 0.3
              }
            },
            {
              "name": "Angle_ADB",
              "mobject_type": "RightAngle",
              "properties": {
                "line1": "Line(D.get_center(), A.get_center())",
                "line2": "Line(D.get_center(), B.get_center())",
                "length": 0.3
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
        "font_size": 42,
        "position": "RIGHT*2.5 + UP*0.5"
      }
    },
    {
      "name": "TriangleHighlights",
      "mobject_type": "VGroup",
      "properties": {},
      "mobjects": [
        {
          "name": "TriangleABC_Highlight",
          "mobject_type": "Polygon",
          "properties": {
            "vertices": "[A.get_center(), B.get_center(), C.get_center()]",
            "fill_color": "#00BFFF",
            "fill_opacity": 0.5,
            "stroke_width": 0
          }
        },
        {
          "name": "TriangleBAD_Highlight",
          "mobject_type": "Polygon",
          "properties": {
            "vertices": "[B.get_center(), A.get_center(), D.get_center()]",
            "fill_color": "#FFD700",
            "fill_opacity": 0.5,
            "stroke_width": 0
          }
        }
      ]
    }
  ],
  "animation_flow": [
    {
      "description": "Introduce the title and the problem diagram.",
      "animation_time_start": 0.0,
      "animation_time_end": 3.24,
      "animations": [
        {
          "manim_function": "Write",
          "target_mobjects": [
            "TitleCard"
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
      "description": "State the congruence goal and highlight the two relevant triangles.",
      "animation_time_start": 3.25,
      "animation_time_end": 10.86,
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
            "run_time": 2
          }
        }
      ]
    },
    {
      "description": "Emphasize the final objective.",
      "animation_time_start": 10.87,
      "animation_time_end": 14.76,
      "animations": [
        {
          "manim_function": "Indicate",
          "target_mobjects": [
            "GoalText"
          ]
        },
        {
          "manim_function": "Indicate",
          "target_mobjects": [
            "TriangleHighlights"
          ],
          "params": {
            "scale_factor": 1.05
          }
        }
      ]
    }
  ],
  "generated_at": 1751511938.976547,
  "step_index": 0,
  "original_step_id": "part_a_understand_goal",
  "audio_file_scene": "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Scene/part_a_understand_goal_scene.mp3",
  "duration_scene_seconds": 14.76
}
scene_script = {
  "scene_id": "part_a_understand_goal",
  "duration_seconds": 14.76,
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
        style = style_data.get("config", {})

        # --- Set Background Color ---
        background_color = style.get("theme", {}).get("background_color", "#0C0C0C")
        self.camera.background_color = background_color

        # --- 2. Audio Setup (Conditional) ---
        audio_path = script.get("audio_file_path")
        if audio_path:
            self.add_sound(audio_path)

        # --- 3. Mobject Instantiation ---
        mobjects = {}

        # --- Helper function for nested color lookup ---
        def get_color(path, default):
            keys = path.split('.')
            val = style.get("colors", {})
            for key in keys:
                val = val.get(key, {})
            return val if isinstance(val, str) else default

        # Instantiate TitleCard
        mobjects['TitleCard'] = Tex(
            "Part A: Stating the Goal",
            font_size=plan['mobjects'][0]['properties']['font_size']
        ).move_to(UP * 3.5)

        # Instantiate ProblemDiagram components
        # Points
        mobjects['A'] = Dot(point=np.array([-2, -1.5, 0]))
        mobjects['B'] = Dot(point=np.array([2, -1.5, 0]))
        mobjects['C'] = Dot(point=np.array([1.5, 1.5, 0]))
        mobjects['D'] = Dot(point=np.array([-1.5, 1.5, 0]))
        mobjects['Points'] = VGroup(mobjects['A'], mobjects['B'], mobjects['C'], mobjects['D'])

        # Lines
        mobjects['Line_AB'] = Line(mobjects['A'].get_center(), mobjects['B'].get_center())
        mobjects['Line_AC'] = Line(mobjects['A'].get_center(), mobjects['C'].get_center())
        mobjects['Line_AD'] = Line(mobjects['A'].get_center(), mobjects['D'].get_center())
        mobjects['Line_BC'] = Line(mobjects['B'].get_center(), mobjects['C'].get_center())
        mobjects['Line_BD'] = Line(mobjects['B'].get_center(), mobjects['D'].get_center())
        mobjects['Lines'] = VGroup(mobjects['Line_AB'], mobjects['Line_AC'], mobjects['Line_AD'], mobjects['Line_BC'], mobjects['Line_BD'])

        # Labels
        mobjects['Label_A'] = MathTex("A").next_to(mobjects['A'], DL)
        mobjects['Label_B'] = MathTex("B").next_to(mobjects['B'], DR)
        mobjects['Label_C'] = MathTex("C").next_to(mobjects['C'], UR)
        mobjects['Label_D'] = MathTex("D").next_to(mobjects['D'], UL)
        mobjects['Labels'] = VGroup(mobjects['Label_A'], mobjects['Label_B'], mobjects['Label_C'], mobjects['Label_D'])

        # Angle Markers
        mobjects['Angle_ACB'] = RightAngle(Line(mobjects['C'].get_center(), mobjects['A'].get_center()), Line(mobjects['C'].get_center(), mobjects['B'].get_center()), length=0.3)
        mobjects['Angle_ADB'] = RightAngle(Line(mobjects['D'].get_center(), mobjects['A'].get_center()), Line(mobjects['D'].get_center(), mobjects['B'].get_center()), length=0.3)
        mobjects['AngleMarkers'] = VGroup(mobjects['Angle_ACB'], mobjects['Angle_ADB'])

        # Assemble ProblemDiagram
        mobjects['ProblemDiagram'] = VGroup(
            mobjects['Points'], mobjects['Lines'], mobjects['Labels'], mobjects['AngleMarkers']
        ).move_to(LEFT * 3.5)
        
        # Instantiate GoalText
        mobjects['GoalText'] = MathTex(
            r"\text{Goal: Prove } \triangle ABC \cong \triangle BAD",
            font_size=plan['mobjects'][2]['properties']['font_size']
        ).move_to(RIGHT * 2.5 + UP * 0.5)

        # Instantiate TriangleHighlights (after ProblemDiagram is positioned)
        mobjects['TriangleABC_Highlight'] = Polygon(
            mobjects['A'].get_center(), mobjects['B'].get_center(), mobjects['C'].get_center(),
            fill_color="#00BFFF", fill_opacity=0.5, stroke_width=0
        )
        mobjects['TriangleBAD_Highlight'] = Polygon(
            mobjects['B'].get_center(), mobjects['A'].get_center(), mobjects['D'].get_center(),
            fill_color="#FFD700", fill_opacity=0.5, stroke_width=0
        )
        mobjects['TriangleHighlights'] = VGroup(mobjects['TriangleABC_Highlight'], mobjects['TriangleBAD_Highlight'])


        # --- 4. Initial Scene Setup ---
        # No initial mobjects specified in the plan. The scene starts empty.

        # --- 5. Time Tracking & Animation Flow ---
        current_time = 0.0

        # Animation Group 1: Introduce title and diagram
        anim_group_1 = plan['animation_flow'][0]
        start_time = anim_group_1['animation_time_start']
        end_time = anim_group_1['animation_time_end']
        
        wait_duration = start_time - current_time
        if wait_duration > 0:
            self.wait(wait_duration)

        run_time = 2.0
        self.play(
            Write(mobjects['TitleCard']),
            Create(mobjects['ProblemDiagram']),
            run_time=run_time,
            rate_func=smooth
        )
        
        wait_duration = end_time - start_time - run_time
        if wait_duration > 0:
            self.wait(wait_duration)
        current_time = end_time

        # Animation Group 2: State goal and highlight triangles
        anim_group_2 = plan['animation_flow'][1]
        start_time = anim_group_2['animation_time_start']
        end_time = anim_group_2['animation_time_end']

        wait_duration = start_time - current_time
        if wait_duration > 0:
            self.wait(wait_duration)

        run_time_write = 2.5
        self.play(Write(mobjects['GoalText']), run_time=run_time_write, rate_func=smooth)
        
        self.wait(1.0) # Pause for emphasis

        run_time_fade = 2.0
        self.play(FadeIn(mobjects['TriangleHighlights']), run_time=run_time_fade, rate_func=smooth)
        
        total_anim_time = run_time_write + 1.0 + run_time_fade
        wait_duration = (end_time - start_time) - total_anim_time
        if wait_duration > 0:
            self.wait(wait_duration)
        current_time = end_time

        # Animation Group 3: Emphasize the objective
        anim_group_3 = plan['animation_flow'][2]
        start_time = anim_group_3['animation_time_start']
        end_time = anim_group_3['animation_time_end']

        wait_duration = start_time - current_time
        if wait_duration > 0:
            self.wait(wait_duration)
        
        run_time = 1.5
        self.play(
            Indicate(mobjects['GoalText']),
            Indicate(mobjects['TriangleHighlights'], scale_factor=1.05),
            run_time=run_time,
            rate_func=smooth
        )
        
        wait_duration = end_time - start_time - run_time
        if wait_duration > 0:
            self.wait(wait_duration)
        current_time = end_time

        # --- 6. Final Padding ---
        remaining_time = script["duration_seconds"] - current_time
        if remaining_time > 0.01:
            self.wait(remaining_time)
