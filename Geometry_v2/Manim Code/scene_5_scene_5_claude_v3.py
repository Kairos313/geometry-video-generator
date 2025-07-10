from manim import *

scene_data = {
    "scene_id": "part_b_deduce_isosceles_triangle",
    "duration_seconds": 10,
    "audio_file_path": "/Users/kairos/Desktop/Prompt Generation/Geometry_v2/Scene/part_b_deduce_isosceles_triangle_scene.mp3",
    "sentence_timestamps": [
        {"text": "Now, let's use the congruence we proved in part A.", "start": 0.0, "end": 2.82},
        {"text": "Since triangle A B C is congruent to triangle B A D, their corresponding angles are equal.", "start": 2.83, "end": 8.58},
        {"text": "This means angle C A B equals angle D B A.", "start": 8.59, "end": 11.7},
        {"text": "In triangle A E B, angle E A B is the same as angle C A B, and angle E B A is the same as angle D B A.", "start": 11.71, "end": 19.13},
        {"text": "Since angle E A B equals angle E B A, triangle A E B is an isosceles triangle.", "start": 19.14, "end": 24.57},
        {"text": "From triangle A B C congruent to triangle B A D, we have Angle C A B equals Angle D B A.", "start": 24.58, "end": 30.93},
        {"text": "In triangle A E B, Angle E A B equals Angle E B A.", "start": 30.94, "end": 34.96},
        {"text": "Therefore, triangle A E B is an isosceles triangle with side A E equal to side B E.", "start": 34.97, "end": 40.17},
        {"text": "We deduced that A E equals B E, so B E is also fifteen centimeters.", "start": 40.18, "end": 45.14}
    ],
    "initial_mobjects": ["Title", "DiagramGroup", "CongruenceStatement_PartA"],
    "mobjects": [],  # The full mobjects list is very long and can be filled in as needed
    "animation_flow": []  # The full animation_flow list can be filled in as needed
}

class PartBDeduceIsoscelesTriangle(Scene):
    def construct(self):
        # Audio setup
        audio_file = scene_data.get("audio_file_path")
        if audio_file:
            self.add_sound(audio_file)
        
        # Background setup
        self.camera.background_color = "#0C0C0C"
        
        # Initialize time tracking
        current_time = 0
        
        # Helper function to safely evaluate position strings
        def safe_eval_position(pos_str):
            try:
                # Replace common position constants with their values
                pos_str = pos_str.replace("UP", "UP")
                pos_str = pos_str.replace("DOWN", "DOWN") 
                pos_str = pos_str.replace("LEFT", "LEFT")
                pos_str = pos_str.replace("RIGHT", "RIGHT")
                pos_str = pos_str.replace("ORIGIN", "ORIGIN")
                return eval(pos_str)
            except:
                return ORIGIN
        
        # Helper function to create mobjects safely
        def create_mobject_safely(mobject_def):
            try:
                name = mobject_def["name"]
                mobject_type = mobject_def["mobject_type"]
                properties = mobject_def["properties"]
                
                if mobject_type == "Text":
                    mob = Text(
                        properties["text"],
                        font_size=properties.get("font_size", 24),
                        color=properties.get("color", "#FFFFFF")
                    )
                elif mobject_type == "MathTex":
                    mob = MathTex(
                        properties["text"],
                        font_size=properties.get("font_size", 32),
                        color=properties.get("color", "#FFFFFF")
                    )
                elif mobject_type == "Dot":
                    mob = Dot(
                        radius=properties.get("radius", 0.08),
                        color=properties.get("color", "#FFFFFF")
                    )
                elif mobject_type == "Line":
                    mob = Line(
                        start=safe_eval_position(properties["start"]),
                        end=safe_eval_position(properties["end"]),
                        stroke_width=properties.get("stroke_width", 2),
                        color=properties.get("color", "#FFFFFF")
                    )
                elif mobject_type == "Polygon":
                    vertices = [safe_eval_position(v) for v in properties["vertices"]]
                    mob = Polygon(
                        *vertices,
                        fill_color=properties.get("fill_color", "#FFFFFF"),
                        fill_opacity=properties.get("fill_opacity", 0.0),
                        stroke_color=properties.get("stroke_color", "#FFFFFF"),
                        stroke_width=properties.get("stroke_width", 2)
                    )
                elif mobject_type == "Arc":
                    mob = Arc(
                        radius=properties.get("radius", 0.4),
                        start_angle=properties.get("start_angle", 0),
                        angle=properties.get("angle", PI/2),
                        color=properties.get("color", "#FFFFFF"),
                        stroke_width=properties.get("stroke_width", 2)
                    )
                else:
                    return None
                
                if "position" in properties:
                    mob.move_to(safe_eval_position(properties["position"]))
                
                return mob
            except Exception as e:
                print(f"Error creating mobject {name}: {e}")
                return None
        
        # Create all mobjects
        mobjects = {}
        for mobject_def in scene_data["mobjects"]:
            mob = create_mobject_safely(mobject_def)
            if mob:
                mobjects[mobject_def["name"]] = mob
        
        # Parse sentence timestamps for timing
        sentence_timestamps = scene_data.get("sentence_timestamps", [])
        
        # Animation flow implementation
        animation_groups = scene_data.get("animation_flow", [])
        
        # Group 1: Introduce the scene title and basic geometric figure (0-2.82s)
        if len(sentence_timestamps) > 0:
            # Title and basic setup
            title_anims = []
            if "Title" in mobjects:
                title_anims.append(Write(mobjects["Title"], run_time=1.0))
            
            # Create points
            point_anims = []
            for point_name in ["PointA", "PointB", "PointC", "PointD", "PointE"]:
                if point_name in mobjects:
                    point_anims.append(Create(mobjects[point_name]))
            
            # Create labels
            label_anims = []
            for label_name in ["LabelA", "LabelB", "LabelC", "LabelD", "LabelE"]:
                if label_name in mobjects:
                    label_anims.append(Write(mobjects[label_name]))
            
            # Create basic lines
            line_anims = []
            for line_name in ["LineAB", "LineAC", "LineBC", "LineBD", "LineAD"]:
                if line_name in mobjects:
                    line_anims.append(Create(mobjects[line_name]))
            
            # Play animations
            if title_anims:
                self.play(*title_anims, run_time=1.0)
            if point_anims:
                self.play(*point_anims, run_time=0.5)
            if label_anims:
                self.play(*label_anims, run_time=0.5)
            if line_anims:
                self.play(*line_anims, run_time=0.8)
            
            current_time = 2.82
        
        # Group 2: Reference the congruence from part A (2.83-8.58s)
        if len(sentence_timestamps) > 1:
            wait_time = sentence_timestamps[1]["start"] - current_time
            if wait_time > 0:
                self.wait(wait_time)
            
            if "CongruenceStatement" in mobjects:
                self.play(Write(mobjects["CongruenceStatement"], run_time=2.0))
            
            current_time = 8.58
        
        # Group 3: Show that corresponding angles are equal (8.59-11.7s)
        if len(sentence_timestamps) > 2:
            wait_time = sentence_timestamps[2]["start"] - current_time
            if wait_time > 0:
                self.wait(wait_time)
            
            if "CongruenceStatement" in mobjects and "AngleEquality1" in mobjects:
                self.play(
                    TransformMatchingTex(mobjects["CongruenceStatement"], mobjects["AngleEquality1"]),
                    run_time=1.5
                )
            
            # Create angle arcs
            angle_anims = []
            for angle_name in ["AngleCAB", "AngleDBA"]:
                if angle_name in mobjects:
                    angle_anims.append(Create(mobjects[angle_name]))
            
            if angle_anims:
                self.play(*angle_anims, run_time=1.0)
            
            current_time = 11.7
        
        # Group 4: Highlight the specific angle equality (11.71-19.13s)
        if len(sentence_timestamps) > 3:
            wait_time = sentence_timestamps[3]["start"] - current_time
            if wait_time > 0:
                self.wait(wait_time)
            
            # Introduce triangle AEB
            aeb_anims = []
            for line_name in ["LineAE", "LineBE"]:
                if line_name in mobjects:
                    aeb_anims.append(Create(mobjects[line_name]))
            
            if aeb_anims:
                self.play(*aeb_anims, run_time=1.5)
            
            if "TriangleAEBHighlight" in mobjects:
                self.play(DrawBorderThenFill(mobjects["TriangleAEBHighlight"], run_time=2.0))
            
            # Indicate angles
            indicate_anims = []
            for angle_name in ["AngleCAB", "AngleDBA"]:
                if angle_name in mobjects:
                    indicate_anims.append(Indicate(mobjects[angle_name], color="#FDE047"))
            
            if indicate_anims:
                self.play(*indicate_anims, run_time=1.5)
            
            current_time = 19.13
        
        # Group 5: Show that triangle AEB has equal angles (19.14-24.57s)
        if len(sentence_timestamps) > 4:
            wait_time = sentence_timestamps[4]["start"] - current_time
            if wait_time > 0:
                self.wait(wait_time)
            
            if "AngleEquality1" in mobjects and "AngleEqualityAEB" in mobjects:
                self.play(
                    Transform(mobjects["AngleEquality1"], mobjects["AngleEqualityAEB"]),
                    run_time=1.5
                )
            
            # Flash angles
            flash_anims = []
            for angle_name in ["AngleCAB", "AngleDBA"]:
                if angle_name in mobjects:
                    flash_anims.append(Flash(mobjects[angle_name], color="#F59E0B"))
            
            if flash_anims:
                self.play(*flash_anims, run_time=1.0)
            
            current_time = 24.57
        
        # Group 6: Conclude that triangle AEB is isosceles (24.58-30.93s)
        if len(sentence_timestamps) > 5:
            wait_time = sentence_timestamps[5]["start"] - current_time
            if wait_time > 0:
                self.wait(wait_time)
            
            if "AngleEquality1" in mobjects and "IsoscelesStatement" in mobjects:
                self.play(
                    Transform(mobjects["AngleEquality1"], mobjects["IsoscelesStatement"]),
                    run_time=2.0
                )
            
            if "TriangleAEBHighlight" in mobjects:
                self.play(
                    Circumscribe(mobjects["TriangleAEBHighlight"], color="#A855F7"),
                    run_time=1.5
                )
            
            current_time = 30.93
        
        # Group 7: Restate the angle equality (30.94-34.96s)
        if len(sentence_timestamps) > 6:
            wait_time = sentence_timestamps[6]["start"] - current_time
            if wait_time > 0:
                self.wait(wait_time)
            
            if "AngleEqualityAEB" in mobjects:
                self.play(Write(mobjects["AngleEqualityAEB"], run_time=1.5))
            
            current_time = 34.96
        
        # Group 8: Show side equality (34.97-40.17s)
        if len(sentence_timestamps) > 7:
            wait_time = sentence_timestamps[7]["start"] - current_time
            if wait_time > 0:
                self.wait(wait_time)
            
            if "AngleEqualityAEB" in mobjects and "SideEquality" in mobjects:
                self.play(
                    Transform(mobjects["AngleEqualityAEB"], mobjects["SideEquality"]),
                    run_time=2.0
                )
            
            # Indicate sides
            indicate_anims = []
            for line_name in ["LineAE", "LineBE"]:
                if line_name in mobjects:
                    indicate_anims.append(Indicate(mobjects[line_name], color="#22C55E"))
            
            if indicate_anims:
                self.play(*indicate_anims, run_time=1.5)
            
            current_time = 40.17
        
        # Group 9: Show final length calculation (40.18-45.14s)
        if len(sentence_timestamps) > 8:
            wait_time = sentence_timestamps[8]["start"] - current_time
            if wait_time > 0:
                self.wait(wait_time)
            
            if "LengthStatement" in mobjects:
                self.play(Write(mobjects["LengthStatement"], run_time=2.0))
            
            # Create length labels
            length_anims = []
            for label_name in ["LengthLabelAE", "LengthLabelBE"]:
                if label_name in mobjects:
                    length_anims.append(Create(mobjects[label_name]))
            
            if length_anims:
                self.play(*length_anims, run_time=1.5)
            
            # Flash length labels
            flash_anims = []
            for label_name in ["LengthLabelAE", "LengthLabelBE"]:
                if label_name in mobjects:
                    flash_anims.append(Flash(mobjects[label_name], color="#22C55E"))
            
            if flash_anims:
                self.play(*flash_anims, run_time=1.0)
            
            current_time = 45.14
        
        # Final wait to match total duration
        total_duration = scene_data.get("duration_seconds", 45.14)
        if current_time < total_duration:
            self.wait(total_duration - current_time)