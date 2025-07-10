import json
import os
import time
import logging
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from urllib.parse import urljoin, urlparse
import re
import google.generativeai as genai
import concurrent.futures
from typing import List, Dict, Optional, Any

# Import the prompt from orchestrator_prompts.py
from orchestrator_prompts import Animator_Phase_1_Blueprint_Manim_Docs_v2 as BLUEPRINT_PROMPT

# --- CONFIGURATION ---
INPUT_PATH = "Geometry_v2/deconstruct_parallel.json"
STYLE_PATH = "Geometry_v2/geo_v2_style.json"
IMAGE_PATH = "Geometry_v2/math_question.png"  # Set to None if not using image
BLUEPRINT_DIR = "Geometry_v2/Blueprint_Batch_Enhanced"
MODEL_NAME = "gemini-2.5-flash"

# --- SETUP LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# --- LOAD API KEY ---
load_dotenv(".env")
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise RuntimeError("GOOGLE_API_KEY not found in environment.")
genai.configure(api_key=google_api_key)

# --- ENHANCED MANIM SEARCH TOOLS ---

class ManimDocumentationSearcher:
    """Enhanced Manim documentation searcher with hybrid search capabilities"""
    
    def __init__(self):
        self.priority_sites = [
            "docs.manim.community",
            "github.com/ManimCommunity",
            "stackoverflow.com",
            "reddit.com/r/manim"
        ]
        
        self.search_mappings = {
            "geometry": "https://docs.manim.community/en/stable/reference/manim.mobject.geometry.html",
            "circle": "https://docs.manim.community/en/stable/reference/manim.mobject.geometry.arc.html",
            "line": "https://docs.manim.community/en/stable/reference/manim.mobject.geometry.line.html",
            "square": "https://docs.manim.community/en/stable/reference/manim.mobject.geometry.polygram.html",
            "triangle": "https://docs.manim.community/en/stable/reference/manim.mobject.geometry.polygram.html",
            "animation": "https://docs.manim.community/en/stable/reference_index/animations.html",
            "transform": "https://docs.manim.community/en/stable/reference/manim.animation.transform.html",
            "create": "https://docs.manim.community/en/stable/reference/manim.animation.creation.html",
            "fade": "https://docs.manim.community/en/stable/reference/manim.animation.fading.html",
            "text": "https://docs.manim.community/en/stable/reference/manim.mobject.text.html",
            "math": "https://docs.manim.community/en/stable/reference/manim.mobject.text.tex_mobject.html",
            "graph": "https://docs.manim.community/en/stable/reference/manim.mobject.graphing.html",
            "plot": "https://docs.manim.community/en/stable/reference/manim.mobject.graphing.html",
            "camera": "https://docs.manim.community/en/stable/reference_index/cameras.html",
            "scene": "https://docs.manim.community/en/stable/reference_index/scenes.html",
            "emphasize": "https://docs.manim.community/en/stable/reference/manim.animation.indication.html",
            "highlight": "https://docs.manim.community/en/stable/reference/manim.animation.indication.html",
            "brace": "https://docs.manim.community/en/stable/reference/manim.mobject.geometry.line.html",
            "arrow": "https://docs.manim.community/en/stable/reference/manim.mobject.geometry.line.html"
        }
    
    def search_web_for_manim(self, query: str, max_results: int = 3) -> str:
        """Uses DuckDuckGo to search for Manim-related content across the web."""
        try:
            logger.info(f"Web search for Manim: {query}")
            
            enhanced_query = f"{query} manim python animation"
            results = []
            
            with DDGS() as ddgs:
                search_results = list(ddgs.text(enhanced_query, max_results=max_results * 2))
                
                priority_results = []
                other_results = []
                
                for result in search_results:
                    url = result.get('href', '')
                    title = result.get('title', '')
                    snippet = result.get('body', '')
                    
                    is_priority = any(site in url.lower() for site in self.priority_sites)
                    
                    if any(term in url.lower() for term in ['manim', 'animation', 'python']):
                        formatted_result = {
                            'url': url,
                            'title': title,
                            'snippet': snippet,
                            'is_priority': is_priority
                        }
                        
                        if is_priority:
                            priority_results.append(formatted_result)
                        else:
                            other_results.append(formatted_result)
                
                final_results = priority_results + other_results
                final_results = final_results[:max_results]
                
                formatted_output = []
                for i, result in enumerate(final_results, 1):
                    priority_marker = "⭐ " if result['is_priority'] else ""
                    formatted_output.append(
                        f"{i}. {priority_marker}{result['title']}\n"
                        f"   URL: {result['url']}\n"
                        f"   Summary: {result['snippet'][:200]}...\n"
                    )
                
                return "\n".join(formatted_output) if formatted_output else "No relevant results found."
                
        except Exception as e:
            logger.error(f"Error in web search: {e}")
            return f"Error searching the web: {str(e)}"
    
    def browse_manim_docs(self, url: str) -> str:
        """Enhanced browsing for Manim documentation and web results."""
        try:
            logger.info(f"Browsing: {url}")
            
            parsed_url = urlparse(url)
            if not parsed_url.scheme:
                return "Error: Invalid URL format"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(["script", "style", "nav", "header", "footer", "aside", "advertisement"]):
                element.decompose()
            
            # Extract content based on site type
            content = None
            
            if 'docs.manim.community' in url:
                content = soup.select_one('main') or soup.select_one('.rst-content')
            elif 'github.com' in url:
                content = soup.select_one('.markdown-body') or soup.select_one('#readme')
            elif 'stackoverflow.com' in url:
                content = soup.select_one('.question') or soup.select_one('.answer')
            elif 'reddit.com' in url:
                content = soup.select_one('.Post') or soup.select_one('[data-testid="post-content"]')
            else:
                content_selectors = ['main', '.content', '.post-content', '.entry-content', 'article']
                for selector in content_selectors:
                    content = soup.select_one(selector)
                    if content:
                        break
            
            if not content:
                content = soup.find('body')
            
            if content:
                # Extract code blocks separately
                code_blocks = content.find_all(['pre', 'code'])
                code_snippets = []
                for i, block in enumerate(code_blocks):
                    if block.get_text().strip():
                        code_snippets.append(f"Code Example {i+1}:\n```\n{block.get_text().strip()}\n```")
                
                # Get regular text
                text = content.get_text(separator=' ', strip=True)
                text = re.sub(r'\s+', ' ', text)
                
                # Combine text and code
                result = text[:6000]
                if code_snippets:
                    result += "\n\n" + "\n\n".join(code_snippets[:3])
                
                return result[:8000]
            else:
                return "Error: Could not extract content from the webpage"
                
        except Exception as e:
            logger.error(f"Error browsing {url}: {e}")
            return f"Error fetching content: {str(e)}"
    
    def search_manim_targeted(self, query: str) -> str:
        """Targeted search combining curated docs with web search."""
        try:
            logger.info(f"Targeted Manim search: {query}")
            
            results = []
            
            # Check curated documentation first
            query_lower = query.lower()
            curated_urls = []
            
            for keyword, url in self.search_mappings.items():
                if keyword in query_lower:
                    curated_urls.append(url)
            
            if curated_urls:
                results.append("📚 Official Documentation:")
                for url in curated_urls[:2]:
                    results.append(f"   {url}")
                results.append("")
            
            # Web search for additional context
            web_results = self.search_web_for_manim(query, max_results=2)
            if web_results and "No relevant results found" not in web_results:
                results.append("🔍 Additional Web Results:")
                results.append(web_results)
            
            return "\n".join(results) if results else "No relevant information found."
            
        except Exception as e:
            logger.error(f"Error in targeted search: {e}")
            return f"Error in targeted search: {str(e)}"
    
    def get_manim_code_examples(self, concept: str) -> str:
        """Searches for specific code examples related to a concept."""
        try:
            logger.info(f"Getting code examples for: {concept}")
            
            search_query = f"{concept} manim python code example animation"
            
            with DDGS() as ddgs:
                results = list(ddgs.text(search_query, max_results=5))
                
                code_sources = []
                for result in results:
                    url = result.get('href', '')
                    title = result.get('title', '')
                    
                    if any(term in url.lower() for term in ['github', 'stackoverflow', 'gist', 'docs.manim']):
                        code_sources.append({
                            'url': url,
                            'title': title,
                            'snippet': result.get('body', '')
                        })
                
                if code_sources:
                    formatted_results = []
                    for i, source in enumerate(code_sources[:3], 1):
                        formatted_results.append(
                            f"Code Example Source {i}:\n"
                            f"Title: {source['title']}\n"
                            f"URL: {source['url']}\n"
                            f"Context: {source['snippet'][:150]}...\n"
                        )
                    
                    return "\n".join(formatted_results)
                else:
                    return "No specific code examples found."
                    
        except Exception as e:
            logger.error(f"Error getting code examples: {e}")
            return f"Error getting code examples: {str(e)}"

# --- ENHANCED BLUEPRINT GENERATOR ---

class EnhancedBlueprintGenerator:
    """Enhanced blueprint generator with integrated search capabilities"""
    
    def __init__(self):
        self.searcher = ManimDocumentationSearcher()
        self.model = genai.GenerativeModel(MODEL_NAME)
        self.scene_state = []  # Track mobjects across scenes
        
        # Use the imported prompt instead of hardcoded one
        self.blueprint_prompt = BLUEPRINT_PROMPT
    
    def analyze_scene_requirements(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze what the scene needs and search for appropriate Manim techniques."""
        scene_analysis = {
            'mobject_types': [],
            'animation_types': [],
            'layout_requirements': [],
            'search_queries': []
        }
        
        # Extract text content for analysis
        text_content = ""
        if 'sentences' in step:
            text_content = " ".join([s.get('text', '') for s in step['sentences']])
        
        # Identify mathematical content
        if any(term in text_content.lower() for term in ['equation', 'formula', 'calculate', 'solve']):
            scene_analysis['mobject_types'].append('MathTex')
            scene_analysis['animation_types'].append('TransformMatchingTex')
            scene_analysis['search_queries'].append('math equations manim')
        
        # Identify geometric content
        if any(term in text_content.lower() for term in ['triangle', 'circle', 'line', 'angle', 'parallel']):
            scene_analysis['mobject_types'].append('geometry')
            scene_analysis['layout_requirements'].append('diagram_split')
            scene_analysis['search_queries'].append('geometry shapes manim')
        
        # Identify emphasis needs
        if any(term in text_content.lower() for term in ['important', 'note', 'highlight', 'focus']):
            scene_analysis['animation_types'].append('emphasis')
            scene_analysis['search_queries'].append('emphasize highlight manim')
        
        # Identify transformation needs
        if any(term in text_content.lower() for term in ['transform', 'change', 'become', 'convert']):
            scene_analysis['animation_types'].append('transform')
            scene_analysis['search_queries'].append('transform animation manim')
        
        return scene_analysis
    
    def search_for_techniques(self, scene_analysis: Dict[str, Any]) -> str:
        """Search for appropriate Manim techniques based on scene analysis."""
        search_results = []
        
        for query in scene_analysis['search_queries']:
            result = self.searcher.search_manim_targeted(query)
            if result and "No relevant information found" not in result:
                search_results.append(f"=== {query.upper()} ===\n{result}\n")
        
        return "\n".join(search_results) if search_results else "No specific techniques found."
    
    def generate_blueprint(self, step: Dict[str, Any], scene_index: int, style_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate a high-quality blueprint for a single scene."""
        try:
            scene_id = step.get('scene_id', f'scene_{scene_index}')
            logger.info(f"Generating blueprint for scene {scene_index}: {scene_id}")
            
            # Analyze scene requirements
            scene_analysis = self.analyze_scene_requirements(step)
            
            # Search for appropriate techniques
            search_results = self.search_for_techniques(scene_analysis)
            
            # Prepare enhanced prompt
            enhanced_prompt = f"""{self.blueprint_prompt}

### **SCENE ANALYSIS:**
{json.dumps(scene_analysis, indent=2)}

### **MANIM TECHNIQUE SEARCH RESULTS:**
{search_results}

### **STYLE CONFIGURATION:**
```json
{json.dumps(style_config, indent=2)}
```

### **SOLUTION STEP TO ANIMATE:**
```json
{json.dumps(step, indent=2)}
```

### **CURRENT SCENE STATE:**
Previous scene mobjects: {json.dumps(self.scene_state)}

### **INSTRUCTIONS:**
1. Use the search results to choose the most appropriate Manim classes and functions
2. Create a technically sound and visually compelling animation blueprint
3. Ensure proper state management for scene transitions
4. Follow the enhanced visual design principles
5. Output ONLY the JSON blueprint object

Generate the blueprint now:
"""
            
            # Generate blueprint using Gemini
            response = self.model.generate_content(enhanced_prompt)
            response_text = response.text if hasattr(response, 'text') else str(response)
            
            # Extract JSON from response
            blueprint = self.extract_json_object(response_text)
            
            if blueprint:
                # Update scene state for next scene
                self.update_scene_state(blueprint)
                logger.info(f"Successfully generated blueprint for scene {scene_index}")
                return blueprint
            else:
                logger.error(f"Failed to extract blueprint JSON for scene {scene_index}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating blueprint for scene {scene_index}: {e}")
            return None
    
    def update_scene_state(self, blueprint: Dict[str, Any]):
        """Update the scene state based on the blueprint's final state."""
        # This is a simplified state tracker - in practice, you'd want to 
        # simulate the animation flow to determine final mobject states
        if 'mobjects' in blueprint:
            mobject_names = [mob.get('name') for mob in blueprint['mobjects'] if mob.get('name')]
            self.scene_state = mobject_names
    
    def extract_json_object(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract JSON object from response text."""
        text = text.strip()
        
        # Remove markdown code blocks
        if text.startswith('```json'):
            text = text[len('```json'):].strip()
        if text.startswith('```'):
            text = text[len('```'):].strip()
        if text.endswith('```'):
            text = text[:-3].strip()
        
        # Find JSON boundaries
        start = text.find('{')
        end = text.rfind('}')
        
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start:end+1])
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error: {e}")
        
        return None

# --- MAIN EXECUTION ---

def main():
    """Main execution function."""
    # Load input data
    try:
        with open(INPUT_PATH, "r", encoding="utf-8") as f:
            input_data = json.load(f)
        steps = input_data.get('solution_steps', [])
        if not steps:
            raise ValueError("No solution_steps found in input file.")
        
        with open(STYLE_PATH, "r", encoding="utf-8") as f:
            style_config = json.load(f)
        
        # Load image if provided
        image_obj = None
        if IMAGE_PATH and Path(IMAGE_PATH).exists():
            image_obj = Image.open(IMAGE_PATH)
        
    except Exception as e:
        logger.error(f"Error loading input files: {e}")
        return
    
    # Initialize generator
    generator = EnhancedBlueprintGenerator()
    
    # Create output directory
    output_dir = Path(BLUEPRINT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each scene
    for i, step in enumerate(steps):
        scene_id = step.get('scene_id', f'scene_{i}')
        output_path = output_dir / f"{i:02d}_{scene_id}.json"
        
        # Skip if already exists
        if output_path.exists():
            logger.info(f"Skipping scene {i} - already exists")
            continue
        
        # Generate blueprint
        blueprint = generator.generate_blueprint(step, i, style_config)
        
        if blueprint:
            # Save blueprint
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(blueprint, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved blueprint: {output_path}")
        else:
            logger.error(f"Failed to generate blueprint for scene {i}")
    
    print(f"\nBlueprint generation complete. Output directory: {output_dir}")

if __name__ == "__main__":
    main()