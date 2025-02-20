"""Module for managing LLM prompts and templates."""

from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
import yaml
import os

class PromptTemplate:
    def __init__(self, name: str, template: str, required_context: List[str], description: str = ""):
        self.name = name
        self.template = template
        self.required_context = required_context
        self.description = description
        
    def format(self, **kwargs) -> str:
        """Format the template with the given context."""
        # Validate required context
        missing = [key for key in self.required_context if key not in kwargs]
        if missing:
            raise ValueError(f"Missing required context variables: {', '.join(missing)}")
        return self.template.format(**kwargs)
    
    @classmethod
    def from_yaml(cls, yaml_path: Path) -> 'PromptTemplate':
        """Load a prompt template from a YAML file."""
        with open(yaml_path) as f:
            data = yaml.safe_load(f)
            
        return cls(
            name=data['name'],
            template=data['template'],
            required_context=data['required_context'],
            description=data.get('description', '')
        )

class PromptManager:
    def __init__(self):
        self.templates: Dict[str, PromptTemplate] = {}
        self._load_templates()
    
    def _load_templates(self):
        """Load all templates from the templates directory."""
        # Get the templates directory relative to this file
        base_dir = Path(__file__).parent
        templates_dir = base_dir / 'templates'
        
        # Load default templates first
        default_dir = templates_dir / 'default'
        if default_dir.exists():
            self._load_directory(default_dir)
        
        # Load custom templates (overriding defaults if same name)
        custom_dir = templates_dir / 'custom'
        if custom_dir.exists():
            self._load_directory(custom_dir)
        
        # Load project-specific templates if in a project
        cwd = Path.cwd()
        project_templates = cwd / 'prompt_templates'
        if project_templates.exists():
            self._load_directory(project_templates)
    
    def _load_directory(self, directory: Path):
        """Load all YAML templates from a directory."""
        if not directory.exists():
            return
            
        for file in directory.glob('*.yaml'):
            try:
                template = PromptTemplate.from_yaml(file)
                self.templates[template.name] = template
            except Exception as e:
                print(f"Error loading template {file}: {e}")
    
    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """Get a prompt template by name."""
        return self.templates.get(name)
    
    def list_templates(self) -> List[Dict[str, str]]:
        """List all available templates."""
        return [
            {
                'name': template.name,
                'description': template.description,
                'required_context': template.required_context
            }
            for template in self.templates.values()
        ]

def save_prompt_history(memory_bank, command_name: str, prompt: str, response: str):
    """Save prompt and response to memory bank."""
    context = memory_bank.load_context_memory()
    if "commandHistory" not in context:
        context["commandHistory"] = []
    
    context["commandHistory"].append({
        "command": command_name,
        "prompt": prompt,
        "response": response,
        "timestamp": datetime.now().isoformat()
    })
    
    memory_bank.save_context_memory(context)

# Initialize the global prompt manager
_prompt_manager = PromptManager()

def print_prompt_info(prompt_name: str, prompt: str):
    """Print prompt information in a formatted way."""
    print("\n" + "="*80)
    print(f"Using prompt template: {prompt_name}")
    print("="*80)
    print(prompt)
    print("="*80 + "\n")

def get_prompt_for_command(command_name: str) -> str:
    """Get prompt for a specific command.
    
    Args:
        command_name: Name of the command
        
    Returns:
        Formatted prompt string
    """
    manager = PromptManager()
    template = manager.get_template(command_name)
    if template:
        # Display prompt to user
        print_prompt_info(command_name, template.template)
        return template.template
    return None

def list_available_templates() -> List[Dict[str, str]]:
    """List all available prompt templates."""
    return _prompt_manager.list_templates()
