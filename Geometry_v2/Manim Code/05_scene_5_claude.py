from manim import *
import numpy as np
import math
import json

scene_plan = {
  "blueprint": [
    {
      "scene_id": "part_b_deduce_isosceles_triangle",
      "sentence_timestamps": [
        {
          "text": "Now, let's use the congruence we proved in part A.",
          "start": 0.0,
          "end": 2.82
        },
        {
          "text": "Since triangle A B C is congruent to triangle B A D, their corresponding angles are equal.",
          "start": 2.83,
          "end": 8.58
        },
        {
          "text": "This means angle C A B equals angle D B A.",
          "start": 8.59,
          "end": 11.7
        },
        {
          "text": "In triangle A E B, angle E A B is the same as angle C A B, and angle E B A is the same as angle D B A.",
          "start": 11.71,
          "end": 19.13
        },
        {
          "text": "Since angle E A B equals angle E B A, triangle A E B is an isosceles triangle.",
          "start": 19.14,
          "end": 24.57
        },
        {
          "text": "From triangle A B C congruent to triangle B A D, we have Angle C A B equals Angle D B A.",
          "start": 24.58,
          "end": 30.93
        },
        {
          "text": "In triangle A E B, Angle E A B equals Angle E B A.",
          "start": 30.94,
          "end": 34.96
        },
        {
          "text": "Therefore, triangle A E B is an isosceles triangle with side A E equal to side B E.",
          "start": 34.97,
          "end": 40.17
        },
        {
          "text": "We deduced that A E equals B E, so B E is also fifteen centimeters.",
          "start": 40.18,
          "end": 45.14
        }
      ],
      "initial_mobjects": [
        "Title",
        "DiagramGroup",
        "CongruenceStatement_PartA"
      ],
      "mobjects": [
        {
          "name": "Title",
          "mobject_type": "Text",
          "properties": {
            "text": "Geometric Proof: Part B",
            "font_size": 64,
            "position": "UP*3.5",
            "color": "#FFFFFF"
          }
        },
        {
          "name": "Dot_A",
          "mobject_type": "Dot",
          "properties": {
            "position": "LEFT*3.5 + DOWN*1.5",
            "color": "#FFFFFF"
          }
        },
        {
          "name": "Label_A",
          "mobject_type": "Tex",
          "properties": {
            "text": "A",
            "font_size": 32,
            "position": "Dot_A.get_left() + LEFT*0.3 + DOWN*0.2",
            "color": "#FFFFFF"
          }
        },
        {
          "name": "Dot_B",
          "mobject_type": "Dot",
          "properties": {
            "position": "RIGHT*3.5 + DOWN*1.5",
            "color": "#FFFFFF"
          }
        },
        {
          "name": "Label_B",
          "mobject_type": "Tex",
          "properties": {
            "text": "B",
            "font_size": 32,
            "position": "Dot_B.get_right() + RIGHT*0.3 + DOWN*0.2",
            "color": "#FFFFFF"
          }
        },
        {
          "name": "Dot_C",
          "mobject_type": "Dot",
          "properties": {
            "position": "RIGHT*1.5 + UP*2.5",
            "color": "#FFFFFF"
          }
        },
        {
          "name": "Label_C",
          "mobject_type": "Tex",
          "properties": {
            "text": "C",
            "font_size": 32,
            "position": "Dot_C.get_right() + RIGHT*0.3 + UP*0.2",
            "color": "#FFFFFF"
          }
        },
        {
          "name": "Dot_D",
          "mobject_type": "Dot",
          "properties": {
            "position": "LEFT*1.5 + UP*2.5",
            "color": "#FFFFFF"
          }
        },
        {
          "name": "Label_D",
          "mobject_type": "Tex",
          "properties": {
            "text": "D",
            "font_size": 32,
            "position": "Dot_D.get_left() + LEFT*0.3 + UP*0.2",
            "color": "#FFFFFF"
          }
        },
        {
          "name": "Dot_E",
          "mobject_type": "Dot",
          "properties": {
            "position": "ORIGIN",
            "color": "#FFFFFF"
          }
        },
        {
          "name": "Label_E",
          "mobject_type": "Tex",
          "properties": {
            "text": "E",
            "font_size": 32,
            "position": "Dot_E.get_right() + RIGHT*0.3 + UP*0.3",
            "color": "#FFFFFF"
          }
        },
        {
          "name": "Line_AB",
          "mobject_type": "Line",
          "properties": {
            "start_point": "Dot_A.get_center()",
            "end_point": "Dot_B.get_center()",
            "color": "#FFFFFF"
          }
        },
        {
          "name": "Line_BC",
          "mobject_type": "Line",
          "properties": {
            "start_point": "Dot_B.get_center()",
            "end_point": "Dot_C.get_center()",
            "color": "#FFFFFF"
          }
        },
        {
          "name": "Line_CD",
          "mobject_type": "Line",
          "properties": {
            "start_point": "Dot_C.get_center()",
            "end_point": "Dot_D.get_center()",
            "color": "#FFFFFF"
          }
        },
        {
          "name": "Line_DA",
          "mobject_type": "Line",
          "properties": {
            "start_point": "Dot_D.get_center()",
            "end_point": "Dot_A.get_center()",
            "color": "#FFFFFF"
          }
        },
        {
          "name": "Line_AC",
          "mobject_type": "Line",
          "properties": {
            "start_point": "Dot_A.get_center()",
            "end_point": "Dot_C.get_center()",
            "color": "#FFFFFF"
          }
        },
        {
          "name": "Line_BD",
          "mobject_type": "Line",
          "properties": {
            "start_point": "Dot_B.get_center()",
            "end_point": "Dot_D.get_center()",
            "color": "#FFFFFF"
          }
        },
        {
          "name": "RightAngle_C",
          "mobject_type": "RightAngle",
          "properties": {
            "point": "Dot_C.get_center()",
            "v1": "Dot_B.get_center() - Dot_C.get_center()",
            "v2": "Dot_A.get_center() - Dot_C.get_center()",
            "length": 0.4,
            "color": "#FDE047",
            "stroke_width": 2
          }
        },
        {
          "name": "RightAngle_D",
          "mobject_type": "RightAngle",
          "properties": {
            "point": "Dot_D.get_center()",
            "v1": "Dot_A.get_center() - Dot_D.get_center()",
            "v2": "Dot_B.get_center() - Dot_D.get_center()",
            "length": 0.4,
            "color": "#FDE047",
            "stroke_width": 2
          }
        },
        {
          "name": "AD_length_label",
          "mobject_type": "MathTex",
          "properties": {
            "text": "12",
            "font_size": 28,
            "position": "Line_DA.get_center() + LEFT*0.3 + UP*0.3",
            "color": "#22C55E"
          }
        },
        {
          "name": "DE_length_label",
          "mobject_type": "MathTex",
          "properties": {
            "text": "9",
            "font_size": 28,
            "position": "VGroup(Dot_D, Dot_E).get_center() + UP*0.3 + LEFT*0.3",
            "color": "#22C55E"
          }
        },
        {
          "name": "AE_length_label",
          "mobject_type": "MathTex",
          "properties": {
            "text": "15",
            "font_size": 28,
            "position": "VGroup(Dot_A, Dot_E).get_center() + UP*0.3 + RIGHT*0.3",
            "color": "#22C55E"
          }
        },
        {
          "name": "AD_tick_mark",
          "mobject_type": "Line",
          "properties": {
            "start_point": "Line_DA.get_center() + Line_DA.copy().rotate(PI/2).get_unit_vector()*0.15",
            "end_point": "Line_DA.get_center() - Line_DA.copy().rotate(PI/2).get_unit_vector()*0.15",
            "stroke_width": 2,
            "color": "#3B82F6"
          }
        },
        {
          "name": "BC_tick_mark",
          "mobject_type": "Line",
          "properties": {
            "start_point": "Line_BC.get_center() + Line_BC.copy().rotate(PI/2).get_unit_vector()*0.15",
            "end_point": "Line_BC.get_center() - Line_BC.copy().rotate(PI/2).get_unit_vector()*0.15",
            "stroke_width": 2,
            "color": "#3B82F6"
          }
        },
        {
          "name": "DiagramGroup",
          "mobject_type": "VGroup",
          "properties": {
            "mobjects": [
              "Dot_A",
              "Label_A",
              "Dot_B",
              "Label_B",
              "Dot_C",
              "Label_C",
              "Dot_D",
              "Label_D",
              "Dot_E",
              "Label_E",
              "Line_AB",
              "Line_BC",
              "Line_CD",
              "Line_DA",
              "Line_AC",
              "Line_BD",
              "RightAngle_C",
              "RightAngle_D",
              "AD_length_label",
              "DE_length_label",
              "AE_length_label",
              "AD_tick_mark",
              "BC_tick_mark"
            ],
            "position": "ORIGIN"
          }
        },
        {
          "name": "CongruenceStatement_PartA",
          "mobject_type": "MathTex",
          "properties": {
            "text": "\\triangle ABC \\cong \\triangle BAD",
            "font_size": 48,
            "position": "UP*2.5 + LEFT*3",
            "color": "#22C55E"
          }
        },
        {
          "name": "Text_AnglesEqualReason",
          "mobject_type": "Text",
          "properties": {
            "text": "\\triangle ABC \\cong \\triangle BAD,",
            "font_size": 36,
            "position": "UP*2.5 + LEFT*3",
            "color": "#FFFFFF"
          }
        },
        {
          "name": "Text_CorrespondingAngles",
          "mobject_type": "Text",
          "properties": {
            "text": "their corresponding angles are equal.",
            "font_size": 36,
            "position": "Text_AnglesEqualReason.get_bottom() + DOWN*0.4",
            "color": "#FFFFFF"
          }
        },
        {
          "name": "Angle_CAB_arc",
          "mobject_type": "Angle",
          "properties": {
            "vertex": "Dot_A.get_center()",
            "p1": "Dot_C.get_center()",
            "p2": "Dot_B.get_center()",
            "radius": 0.7,
            "color": "#FDE047",
            "stroke_width": 4
          }
        },
        {
          "name": "Angle_DBA_arc",
          "mobject_type": "Angle",
          "properties": {
            "vertex": "Dot_B.get_center()",
            "p1": "Dot_D.get_center()",
            "p2": "Dot_A.get_center()",
            "radius": 0.7,
            "color": "#FDE047",
            "stroke_width": 4
          }
        },
        {
          "name": "AngleEquality_Equation",
          "mobject_type": "MathTex",
          "properties": {
            "text": "\\angle CAB = \\angle DBA",
            "font_size": 48,
            "position": "UP*1.5 + RIGHT*0.5",
            "color": "#F59E0B"
          }
        },
        {
          "name": "Triangle_AEB_Highlight",
          "mobject_type": "Polygon",
          "properties": {
            "vertices": [
              "Dot_A.get_center()",
              "Dot_E.get_center()",
              "Dot_B.get_center()"
            ],
            "fill_color": "#3B82F6",
            "fill_opacity": 0.3,
            "stroke_width": 0
          }
        },
        {
          "name": "Text_InTriangleAEB",
          "mobject_type": "Text",
          "properties": {
            "text": "In $\\triangle AEB$:",
            "font_size": 36,
            "position": "UP*2.5 + LEFT*3",
            "color": "#FFFFFF"
          }
        },
        {
          "name": "Angle_EAB_arc",
          "mobject_type": "Angle",
          "properties": {
            "vertex": "Dot_A.get_center()",
            "p1": "Dot_E.get_center()",
            "p2": "Dot_B.get_center()",
            "radius": 0.5,
            "color": "#FB923C",
            "stroke_width": 4
          }
        },
        {
          "name": "Angle_EBA_arc",
          "mobject_type": "Angle",
          "properties": {
            "vertex": "Dot_B.get_center()",
            "p1": "Dot_E.get_center()",
            "p2": "Dot_A.get_center()",
            "radius": 0.5,
            "color": "#FB923C",
            "stroke_width": 4
          }
        },
        {
          "name": "Angle_EAB_eq_CAB",
          "mobject_type": "MathTex",
          "properties": {
            "text": "\\angle EAB = \\angle CAB",
            "font_size": 32,
            "position": "Text_InTriangleAEB.get_bottom() + DOWN*0.5 + LEFT*0.5",
            "color": "#FFFFFF"
          }
        },
        {
          "name": "Angle_EBA_eq_DBA",
          "mobject_type": "MathTex",
          "properties": {
            "text": "\\angle EBA = \\angle DBA",
            "font_size": 32,
            "position": "Angle_EAB_eq_CAB.get_bottom() + DOWN*0.3 + LEFT*0.5",
            "color": "#FFFFFF"
          }
        },
        {
          "name": "IsoscelesConclusion_MathTex",
          "mobject_type": "MathTex",
          "properties": {
            "text": "\\implies \\angle EAB = \\angle EBA",
            "font_size": 48,
            "position": "UP*1.5 + RIGHT*0.5",
            "color": "#22C55E"
          }
        },
        {
          "name": "TriangleAEB_IsoscelesText",
          "mobject_type": "Text",
          "properties": {
            "text": "\\triangle AEB is isosceles.",
            "font_size": 36,
            "position": "IsoscelesConclusion_MathTex.get_bottom() + DOWN*0.5",
            "color": "#22C55E"
          }
        },
        {
          "name": "SideAE_tick_mark",
          "mobject_type": "Line",
          "properties": {
            "start_point": "VGroup(Dot_A, Dot_E).get_center() + VGroup(Dot_A, Dot_E).get_vector().rotate(PI/2).normalize()*0.15",
            "end_point": "VGroup(Dot_A, Dot_E).get_center() - VGroup(Dot_A, Dot_E).get_vector().rotate(PI/2).normalize()*0.15",
            "stroke_width": 2,
            "color": "#22C55E"
          }
        },
        {
          "name": "SideBE_tick_mark",
          "mobject_type": "Line",
          "properties": {
            "start_point": "VGroup(Dot_B, Dot_E).get_center() + VGroup(Dot_B, Dot_E).get_vector().rotate(-PI/2).normalize()*0.15",
            "end_point": "VGroup(Dot_B, Dot_E).get_center() - VGroup(Dot_B, Dot_E).get_vector().rotate(-PI/2).normalize()*0.15",
            "stroke_width": 2,
            "color": "#22C55E"
          }
        },
        {
          "name": "SideAE_eq_BE_statement",
          "mobject_type": "MathTex",
          "properties": {
            "text": "$AE = BE$",
            "font_size": 48,
            "position": "TriangleAEB_IsoscelesText.get_bottom() + DOWN*0.5",
            "color": "#3B82F6"
          }
        },
        {
          "name": "BE_length_value",
          "mobject_type": "MathTex",
          "properties": {
            "text": "$BE = 15 \\text{ cm}$",
            "font_size": 48,
            "position": "SideAE_eq_BE_statement.get_bottom() + DOWN*0.5",
            "color": "#F59E0B"
          }
        },
        {
          "name": "BE_length_label_final",
          "mobject_type": "MathTex",
          "properties": {
            "text": "15",
            "font_size": 28,
            "position": "VGroup(Dot_B, Dot_E).get_center() + UP*0.3 + LEFT*0.3",
            "color": "#22C55E"
          }
        }
      ],
      "animation_flow": [
        {
          "description": "Start by reminding the congruence from Part A and highlighting it, then introduce the reason.",
          "animations": [
            {
              "manim_function": "Indicate",
              "target_mobjects": [
                "CongruenceStatement_PartA"
              ],
              "run_time": 1.0,
              "color": "#FDE047"
            },
            {
              "manim_function": "FadeIn",
              "target_mobjects": [
                "Text_AnglesEqualReason"
              ],
              "run_time": 1.0
            },
            {
              "manim_function": "FadeIn",
              "target_mobjects": [
                "Text_CorrespondingAngles"
              ],
              "run_time": 1.0
            }
          ],
          "timing": "slow",
          "sync_point": "0.0"
        },
        {
          "description": "Highlight the corresponding angles CAB and DBA in the diagram.",
          "animations": [
            {
              "manim_function": "Create",
              "target_mobjects": [
                "Angle_CAB_arc"
              ],
              "run_time": 1.0
            },
            {
              "manim_function": "Create",
              "target_mobjects": [
                "Angle_DBA_arc"
              ],
              "run_time": 1.0
            }
          ],
          "timing": "normal",
          "sync_point": "2.83"
        },
        {
          "description": "Show the equality of angles CAB and DBA as an equation, moving previous text out.",
          "animations": [
            {
              "manim_function": "FadeOut",
              "target_mobjects": [
                "Text_CorrespondingAngles"
              ],
              "run_time": 0.5
            },
            {
              "manim_function": "FadeOut",
              "target_mobjects": [
                "Text_AnglesEqualReason"
              ],
              "run_time": 0.5
            },
            {
              "manim_function": "Write",
              "target_mobjects": [
                "AngleEquality_Equation"
              ],
              "run_time": 1.5
            }
          ],
          "timing": "slow",
          "sync_point": "8.59"
        },
        {
          "description": "Shift focus to triangle AEB by highlighting it and setting up for angle correspondence.",
          "animations": [
            {
              "manim_function": "FadeOut",
              "target_mobjects": [
                "Angle_CAB_arc",
                "Angle_DBA_arc"
              ],
              "run_time": 0.5
            },
            {
              "manim_function": "FadeIn",
              "target_mobjects": [
                "Triangle_AEB_Highlight"
              ],
              "run_time": 1.0
            },
            {
              "manim_function": "FadeOut",
              "target_mobjects": [
                "CongruenceStatement_PartA"
              ],
              "run_time": 0.5
            },
            {
              "manim_function": "Transform",
              "target_mobjects": [
                "AngleEquality_Equation"
              ],
              "new_position": "UP*1.5 + RIGHT*3",
              "run_time": 0.8
            },
            {
              "manim_function": "FadeIn",
              "target_mobjects": [
                "Text_InTriangleAEB"
              ],
              "run_time": 1.0
            }
          ],
          "timing": "slow",
          "sync_point": "11.71"
        },
        {
          "description": "Highlight angles EAB and EBA within triangle AEB and state their correspondence to CAB and DBA.",
          "animations": [
            {
              "manim_function": "Create",
              "target_mobjects": [
                "Angle_EAB_arc"
              ],
              "run_time": 1.0
            },
            {
              "manim_function": "Create",
              "target_mobjects": [
                "Angle_EBA_arc"
              ],
              "run_time": 1.0
            },
            {
              "manim_function": "Write",
              "target_mobjects": [
                "Angle_EAB_eq_CAB",
                "Angle_EBA_eq_DBA"
              ],
              "run_time": 1.5,
              "lag_ratio": 0.5
            }
          ],
          "timing": "slow",
          "sync_point": "14.0"
        },
        {
          "description": "Conclude that angles EAB and EBA are equal, making triangle AEB an isosceles triangle.",
          "animations": [
            {
              "manim_function": "FadeOut",
              "target_mobjects": [
                "Angle_EAB_eq_CAB",
                "Angle_EBA_eq_DBA",
                "Text_InTriangleAEB"
              ],
              "run_time": 0.5
            },
            {
              "manim_function": "Transform",
              "target_mobjects": [
                "AngleEquality_Equation"
              ],
              "new_mobject_name": "IsoscelesConclusion_MathTex",
              "run_time": 1.5
            },
            {
              "manim_function": "Write",
              "target_mobjects": [
                "TriangleAEB_IsoscelesText"
              ],
              "run_time": 1.5
            },
            {
              "manim_function": "Circumscribe",
              "target_mobjects": [
                "Triangle_AEB_Highlight"
              ],
              "color": "#22C55E",
              "buff": 0.5,
              "run_time": 1.0
            }
          ],
          "timing": "slow",
          "sync_point": "19.14"
        },
        {
          "description": "Show that AE equals BE due to the isosceles property and add tick marks.",
          "animations": [
            {
              "manim_function": "FadeIn",
              "target_mobjects": [
                "SideAE_eq_BE_statement"
              ],
              "run_time": 1.0
            },
            {
              "manim_function": "Create",
              "target_mobjects": [
                "SideAE_tick_mark",
                "SideBE_tick_mark"
              ],
              "run_time": 1.0
            },
            {
              "manim_function": "Indicate",
              "target_mobjects": [
                "Line_AC",
                "Line_BD"
              ],
              "color": "#3B82F6",
              "run_time": 1.0,
              "rate_func": "there_and_back"
            }
          ],
          "timing": "normal",
          "sync_point": "34.97"
        },
        {
          "description": "State the final length of BE based on AE's given length.",
          "animations": [
            {
              "manim_function": "Flash",
              "target_mobjects": [
                "AE_length_label"
              ],
              "color": "#FDE047",
              "run_time": 1.0
            },
            {
              "manim_function": "FadeIn",
              "target_mobjects": [
                "BE_length_value"
              ],
              "run_time": 1.0
            },
            {
              "manim_function": "Transform",
              "target_mobjects": [
                "BE_length_value"
              ],
              "new_mobject_name": "BE_length_label_final",
              "target_position": "BE_length_label_final.get_position()",
              "run_time": 1.5
            }
          ],
          "timing": "slow",
          "sync_point": "40.18"
        }
      ]
    }
  ]
}
scene_script = {
  "scene_id": "scene",
  "duration_seconds": 10,
  "audio_file_path": "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Scene/part_b_deduce_isosceles_triangle_scene.mp3"
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

class PartBDeduceIsoscelesTriangle(Scene):
    def construct(self):
        # --- 1. Style Setup ---
        style = style_config.get("config", {})
        self.camera.background_color = style.get("BACKGROUND_COLOR", "#0C0C0C")

        # --- 2. Audio Setup (Conditional) ---
        audio_path = scene_script.get("audio_file_path")
        if audio_path:
            self.add_sound(audio_path)
        
        # --- 3. Mobject Instantiation ---
        mobjects = {}
        
        # Helper function to safely evaluate positions
        def safe_eval_position(pos_str):
            try:
                # Handle common Manim position constants
                pos_str = pos_str.replace("UP", "np.array([0, 1, 0])")
                pos_str = pos_str.replace("DOWN", "np.array([0, -1, 0])")
                pos_str = pos_str.replace("LEFT", "np.array([-1, 0, 0])")
                pos_str = pos_str.replace("RIGHT", "np.array([1, 0, 0])")
                pos_str = pos_str.replace("ORIGIN", "np.array([0, 0, 0])")
                return eval(pos_str)
            except:
                return np.array([0, 0, 0])
        
        # Title
        mobjects['Title'] = Text(
            "Geometric Proof: Part B",
            font_size=64,
            color=WHITE
        ).move_to(UP*3.5)
        
        # Points
        mobjects['Dot_A'] = Dot(color=WHITE).move_to(LEFT*3.5 + DOWN*1.5)
        mobjects['Dot_B'] = Dot(color=WHITE).move_to(RIGHT*3.5 + DOWN*1.5)
        mobjects['Dot_C'] = Dot(color=WHITE).move_to(RIGHT*1.5 + UP*2.5)
        mobjects['Dot_D'] = Dot(color=WHITE).move_to(LEFT*1.5 + UP*2.5)
        mobjects['Dot_E'] = Dot(color=WHITE).move_to(ORIGIN)
        
        # Labels
        mobjects['Label_A'] = Tex("A", font_size=32, color=WHITE).next_to(mobjects['Dot_A'], LEFT+DOWN, buff=0.1)
        mobjects['Label_B'] = Tex("B", font_size=32, color=WHITE).next_to(mobjects['Dot_B'], RIGHT+DOWN, buff=0.1)
        mobjects['Label_C'] = Tex("C", font_size=32, color=WHITE).next_to(mobjects['Dot_C'], RIGHT+UP, buff=0.1)
        mobjects['Label_D'] = Tex("D", font_size=32, color=WHITE).next_to(mobjects['Dot_D'], LEFT+UP, buff=0.1)
        mobjects['Label_E'] = Tex("E", font_size=32, color=WHITE).next_to(mobjects['Dot_E'], RIGHT+UP, buff=0.1)
        
        # Lines
        mobjects['Line_AB'] = Line(mobjects['Dot_A'].get_center(), mobjects['Dot_B'].get_center(), color=WHITE)
        mobjects['Line_BC'] = Line(mobjects['Dot_B'].get_center(), mobjects['Dot_C'].get_center(), color=WHITE)
        mobjects['Line_CD'] = Line(mobjects['Dot_C'].get_center(), mobjects['Dot_D'].get_center(), color=WHITE)
        mobjects['Line_DA'] = Line(mobjects['Dot_D'].get_center(), mobjects['Dot_A'].get_center(), color=WHITE)
        mobjects['Line_AC'] = Line(mobjects['Dot_A'].get_center(), mobjects['Dot_C'].get_center(), color=WHITE)
        mobjects['Line_BD'] = Line(mobjects['Dot_B'].get_center(), mobjects['Dot_D'].get_center(), color=WHITE)
        
        # Right angles
        mobjects['RightAngle_C'] = RightAngle(
            Line(mobjects['Dot_C'].get_center(), mobjects['Dot_B'].get_center()),
            Line(mobjects['Dot_C'].get_center(), mobjects['Dot_A'].get_center()),
            length=0.4,
            color="#FDE047"
        )
        mobjects['RightAngle_D'] = RightAngle(
            Line(mobjects['Dot_D'].get_center(), mobjects['Dot_A'].get_center()),
            Line(mobjects['Dot_D'].get_center(), mobjects['Dot_B'].get_center()),
            length=0.4,
            color="#FDE047"
        )
        
        # Length labels
        mobjects['AD_length_label'] = MathTex("12", font_size=28, color="#22C55E").next_to(mobjects['Line_DA'], LEFT+UP, buff=0.1)
        mobjects['DE_length_label'] = MathTex("9", font_size=28, color="#22C55E").next_to(
            Line(mobjects['Dot_D'].get_center(), mobjects['Dot_E'].get_center()).get_center(), LEFT+UP, buff=0.1
        )
        mobjects['AE_length_label'] = MathTex("15", font_size=28, color="#22C55E").next_to(
            Line(mobjects['Dot_A'].get_center(), mobjects['Dot_E'].get_center()).get_center(), RIGHT+UP, buff=0.1
        )
        
        # Tick marks
        ad_perpendicular = (mobjects['Line_DA'].get_unit_vector() @ np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]))[:2]
        ad_perpendicular_3d = np.append(ad_perpendicular, 0)
        mobjects['AD_tick_mark'] = Line(
            mobjects['Line_DA'].get_center() + ad_perpendicular_3d * 0.15,
            mobjects['Line_DA'].get_center() - ad_perpendicular_3d * 0.15,
            stroke_width=2,
            color="#3B82F6"
        )
        
        bc_perpendicular = (mobjects['Line_BC'].get_unit_vector() @ np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]))[:2]
        bc_perpendicular_3d = np.append(bc_perpendicular, 0)
        mobjects['BC_tick_mark'] = Line(
            mobjects['Line_BC'].get_center() + bc_perpendicular_3d * 0.15,
            mobjects['Line_BC'].get_center() - bc_perpendicular_3d * 0.15,
            stroke_width=2,
            color="#3B82F6"
        )
        
        # Diagram group
        mobjects['DiagramGroup'] = VGroup(
            mobjects['Dot_A'], mobjects['Label_A'],
            mobjects['Dot_B'], mobjects['Label_B'],
            mobjects['Dot_C'], mobjects['Label_C'],
            mobjects['Dot_D'], mobjects['Label_D'],
            mobjects['Dot_E'], mobjects['Label_E'],
            mobjects['Line_AB'], mobjects['Line_BC'], mobjects['Line_CD'], mobjects['Line_DA'],
            mobjects['Line_AC'], mobjects['Line_BD'],
            mobjects['RightAngle_C'], mobjects['RightAngle_D'],
            mobjects['AD_length_label'], mobjects['DE_length_label'], mobjects['AE_length_label'],
            mobjects['AD_tick_mark'], mobjects['BC_tick_mark']
        )
        
        # Congruence statement
        mobjects['CongruenceStatement_PartA'] = MathTex(
            "\\triangle ABC \\cong \\triangle BAD",
            font_size=48,
            color="#22C55E"
        ).move_to(UP*2.5 + LEFT*3)
        
        # Text elements
        mobjects['Text_AnglesEqualReason'] = Text(
            "Since △ABC ≅ △BAD,",
            font_size=36,
            color=WHITE
        ).move_to(UP*2.5 + LEFT*3)
        
        mobjects['Text_CorrespondingAngles'] = Text(
            "their corresponding angles are equal.",
            font_size=36,
            color=WHITE
        ).next_to(mobjects['Text_AnglesEqualReason'], DOWN, buff=0.4)
        
        # Angle arcs
        mobjects['Angle_CAB_arc'] = Angle(
            mobjects['Line_AC'], mobjects['Line_AB'],
            radius=0.7,
            color="#FDE047",
            stroke_width=4
        )
        
        mobjects['Angle_DBA_arc'] = Angle(
            mobjects['Line_BD'], mobjects['Line_AB'],
            radius=0.7,
            color="#FDE047",
            stroke_width=4
        )
        
        # Angle equality equation
        mobjects['AngleEquality_Equation'] = MathTex(
            "\\angle CAB = \\angle DBA",
            font_size=48,
            color="#F59E0B"
        ).move_to(UP*1.5 + RIGHT*0.5)
        
        # Triangle AEB highlight
        mobjects['Triangle_AEB_Highlight'] = Polygon(
            mobjects['Dot_A'].get_center(),
            mobjects['Dot_E'].get_center(),
            mobjects['Dot_B'].get_center(),
            fill_color="#3B82F6",
            fill_opacity=0.3,
            stroke_width=0
        )
        
        # Triangle AEB text
        mobjects['Text_InTriangleAEB'] = Text(
            "In △AEB:",
            font_size=36,
            color=WHITE
        ).move_to(UP*2.5 + LEFT*3)
        
        # More angle arcs
        mobjects['Angle_EAB_arc'] = Angle(
            Line(mobjects['Dot_A'].get_center(), mobjects['Dot_E'].get_center()),
            Line(mobjects['Dot_A'].get_center(), mobjects['Dot_B'].get_center()),
            radius=0.5,
            color="#FB923C",
            stroke_width=4
        )
        
        mobjects['Angle_EBA_arc'] = Angle(
            Line(mobjects['Dot_B'].get_center(), mobjects['Dot_E'].get_center()),
            Line(mobjects['Dot_B'].get_center(), mobjects['Dot_A'].get_center()),
            radius=0.5,
            color="#FB923C",
            stroke_width=4
        )
        
        # Angle equations
        mobjects['Angle_EAB_eq_CAB'] = MathTex(
            "\\angle EAB = \\angle CAB",
            font_size=32,
            color=WHITE
        ).next_to(mobjects['Text_InTriangleAEB'], DOWN, buff=0.5)
        
        mobjects['Angle_EBA_eq_DBA'] = MathTex(
            "\\angle EBA = \\angle DBA",
            font_size=32,
            color=WHITE
        ).next_to(mobjects['Angle_EAB_eq_CAB'], DOWN, buff=0.3)
        
        # Isosceles conclusion
        mobjects['IsoscelesConclusion_MathTex'] = MathTex(
            "\\implies \\angle EAB = \\angle EBA",
            font_size=48,
            color="#22C55E"
        ).move_to(UP*1.5 + RIGHT*0.5)
        
        mobjects['TriangleAEB_IsoscelesText'] = Text(
            "Therefore, △AEB is isosceles.",
            font_size=36,
            color="#22C55E"
        ).next_to(mobjects['IsoscelesConclusion_MathTex'], DOWN, buff=0.5)
        
        # Side tick marks for isosceles triangle
        ae_center = Line(mobjects['Dot_A'].get_center(), mobjects['Dot_E'].get_center()).get_center()
        ae_perpendicular = (Line(mobjects['Dot_A'].get_center(), mobjects['Dot_E'].get_center()).get_unit_vector() @ 
                           np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]))[:2]
        ae_perpendicular_3d = np.append(ae_perpendicular, 0)
        mobjects['SideAE_tick_mark'] = Line(
            ae_center + ae_perpendicular_3d * 0.15,
            ae_center - ae_perpendicular_3d * 0.15,
            stroke_width=2,
            color="#22C55E"
        )
        
        be_center = Line(mobjects['Dot_B'].get_center(), mobjects['Dot_E'].get_center()).get_center()
        be_perpendicular = (Line(mobjects['Dot_B'].get_center(), mobjects['Dot_E'].get_center()).get_unit_vector() @ 
                           np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]]))[:2]
        be_perpendicular_3d = np.append(be_perpendicular, 0)
        mobjects['SideBE_tick_mark'] = Line(
            be_center + be_perpendicular_3d * 0.15,
            be_center - be_perpendicular_3d * 0.15,
            stroke_width=2,
            color="#22C55E"
        )
        
        # Final statements
        mobjects['SideAE_eq_BE_statement'] = MathTex(
            "AE = BE",
            font_size=48,
            color="#3B82F6"
        ).next_to(mobjects['TriangleAEB_IsoscelesText'], DOWN, buff=0.5)
        
        mobjects['BE_length_value'] = MathTex(
            "BE = 15 \\text{ cm}",
            font_size=48,
            color="#F59E0B"
        ).next_to(mobjects['SideAE_eq_BE_statement'], DOWN, buff=0.5)
        
        mobjects['BE_length_label_final'] = MathTex(
            "15",
            font_size=28,
            color="#22C55E"
        ).next_to(be_center, LEFT+UP, buff=0.1)
        
        # --- 4. Initial Scene Setup ---
        plan = scene_plan["blueprint"][0]
        for mobject_name in plan['initial_mobjects']:
            self.add(mobjects[mobject_name])
        
        # --- 5. Time Tracking & Animation Flow ---
        current_time = 0.0
        for anim_group in plan.get('animation_flow', []):
            sync_point = float(anim_group.get('sync_point', 0.0))
            wait_time = sync_point - current_time
            if wait_time > 0:
                self.wait(wait_time)
            animations = []
            for anim in anim_group.get('animations', []):
                manim_func = anim.get('manim_function')
                targets = anim.get('target_mobjects', [])
                run_time = anim.get('run_time', 1.0)
                for target in targets:
                    if target in mobjects:
                        if manim_func == 'Write':
                            animations.append(Write(mobjects[target], run_time=run_time))
                        elif manim_func == 'Create':
                            animations.append(Create(mobjects[target], run_time=run_time))
                        elif manim_func == 'FadeIn':
                            animations.append(FadeIn(mobjects[target], run_time=run_time))
                        elif manim_func == 'FadeOut':
                            animations.append(FadeOut(mobjects[target], run_time=run_time))
                        elif manim_func == 'Indicate':
                            color = anim.get('color', YELLOW)
                            animations.append(Indicate(mobjects[target], color=color, run_time=run_time))
                        elif manim_func == 'Transform':
                            new_mob_name = anim.get('new_mobject_name')
                            
                            # Handle transformation to a new mobject (the source of the error)
                            if new_mob_name and new_mob_name in mobjects:
                                # Use ReplacementTransform for robustness with different mobject structures
                                animations.append(ReplacementTransform(mobjects[target], mobjects[new_mob_name], run_time=run_time))
                            
                            # Handle transformations like moving to a new position
                            elif 'new_position' in anim:
                                new_pos_str = anim.get('new_position')
                                new_pos = safe_eval_position(new_pos_str)
                                animations.append(mobjects[target].animate(run_time=run_time).move_to(new_pos))
                            
                            # You could add other transform types here (e.g., scaling, rotating)
                            
                        # This handles the Circumscribe animation from your JSON
                        elif manim_func == 'Circumscribe':
                            color = anim.get('color', YELLOW)
                            if hasattr(mobjects[target], '__class__') and issubclass(mobjects[target].__class__, Mobject):
                                animations.append(Circumscribe(mobjects[target], color=color, run_time=run_time))
                            else:
                                print(f"[Warning] Circumscribe target '{target}' is not a valid Mobject: {type(mobjects[target])}")
                        
                        # This handles the Flash animation
                        elif manim_func == 'Flash':
                            color = anim.get('color', YELLOW)
                            if hasattr(mobjects[target], '__class__') and issubclass(mobjects[target].__class__, Mobject):
                                animations.append(Flash(mobjects[target], color=color, run_time=run_time))
                            else:
                                print(f"[Warning] Flash target '{target}' is not a valid Mobject: {type(mobjects[target])}")
            if animations:
                self.play(*animations)
            current_time = sync_point + max([anim.get('run_time', 1.0) for anim in anim_group.get('animations', [])] or [1.0])
            
        # --- 6. Final Padding ---
        remaining_time = scene_script.get("duration_seconds", 45.14) - current_time
        if remaining_time > 0.01:
            self.wait(remaining_time)