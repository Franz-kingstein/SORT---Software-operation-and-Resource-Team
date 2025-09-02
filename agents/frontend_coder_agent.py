#!/usr/bin/env python3
"""
Frontend Coder Agent (Coder2)
=============================

This agen        # Enhanced capabilities when AI is available
        if AI_INTEGRATION_AVAILABLE:
            print("🔧 Frontend Agent: Enhanced AI integration enabled")
            self.enhanced_mode = True
        else:
            print("💻 Frontend Agent: Running in standard mode")
            self.enhanced_mode = False
        
        # Initialize ai_tool later when needed (lazy initialization)
        self._ai_tool = Nonees frontend development tasks including:
- User interface design and implementation
- Client-side functionality
- Form creation and validation
- Responsive web design

Team Member: [ASSIGN TO FRONTEND DEVELOPER]
Status: TODO - Implementation needed

Usage:
    agent = FrontendCoderAgent()
    result = agent.execute_task(task_assignment)
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Import Qwen AI service
try:
    from .qwen_ai_service import get_qwen_service, AIResponse
    QWEN_AVAILABLE = True
except ImportError:
    try:
        from qwen_ai_service import get_qwen_service, AIResponse
        QWEN_AVAILABLE = True
    except ImportError:
        QWEN_AVAILABLE = False
        print("⚠️ Qwen AI not available for Frontend Agent")

# Enhanced AI integration (optional imports) - Temporarily disabled
# TODO: Fix langchain/crewai import hanging issue
AI_INTEGRATION_AVAILABLE = False
class BaseTool:
    pass
class CrewBaseTool:
    pass
print("💡 Running in basic mode. LangChain/CrewAI temporarily disabled.")

# Uncomment when import issues are resolved:
# try:
#     from langchain.tools import BaseTool
#     from langchain.schema import BaseMessage
#     from crewai.tools import BaseTool as CrewBaseTool
#     AI_INTEGRATION_AVAILABLE = True
# except ImportError:
#     # Fallback classes for when LangChain/CrewAI not available
#     class BaseTool:
#         pass
#     class CrewBaseTool:
#         pass
#     AI_INTEGRATION_AVAILABLE = False
#     print("💡 Running in basic mode. Install langchain and crewai for enhanced AI features.")


@dataclass
class ExecutionResult:
    """Result of task execution."""
    success: bool
    message: str
    files_created: List[str]
    output: Optional[str] = None
    error: Optional[str] = None


class FrontendCoderAgent:
    """
    Frontend development agent that implements client-side functionality.
    
    Specializes in:
    - HTML/CSS/JavaScript development
    - React/Vue.js components
    - Responsive design
    - Form handling and validation
    """
    
    def __init__(self):
        self.name = "Frontend Coder Agent"
        self.role = "Frontend Developer"
        self.specialties = ["frontend", "ui", "web", "client-side"]
        self.supported_frameworks = ["vanilla", "react", "vue", "bootstrap"]
        self.supported_styles = ["css", "scss", "tailwind"]
        
        # Initialize Qwen AI service
        if QWEN_AVAILABLE:
            self.qwen_service = get_qwen_service()
            self.enhanced_mode = True
            self.ai_enhanced = True
            print("🤖 Frontend Agent: Enhanced with Qwen AI")
        else:
            self.qwen_service = None
            self.enhanced_mode = False
            self.ai_enhanced = False
            print("💻 Frontend Agent: Running in standard mode")
        
        # Enhanced capabilities when AI is available
        if AI_INTEGRATION_AVAILABLE:
            print("🔧 Frontend Agent: Enhanced AI integration enabled")
            self.enhanced_mode = True
        else:
            print("� Frontend Agent: Running in standard mode")
            self.enhanced_mode = False
    
    def execute_task(self, task_assignment: Dict[str, str]) -> ExecutionResult:
        """
        Execute the assigned frontend development task.
        
        Args:
            task_assignment: Dict containing role, action, and task description
            
        Returns:
            ExecutionResult: The result of task execution
        """
        print(f"🎨 {self.name}: Starting task execution...")
        print(f"📋 Task: {task_assignment.get('task', 'No task specified')}")
        
        try:
            task_desc = task_assignment.get('task', '').lower()
            files_created = []
            
            # Parse task requirements from description
            requirements = {
                'title': 'Generated App',
                'authentication': 'login' in task_desc or 'auth' in task_desc,
                'responsive': 'responsive' in task_desc,
                'forms': 'form' in task_desc
            }
            
            # Generate HTML template
            if 'interface' in task_desc or 'ui' in task_desc:
                html_content = self.generate_html_template(requirements)
                html_file = 'templates/index.html'
                
                # Create directory if it doesn't exist
                os.makedirs('templates', exist_ok=True)
                
                # Write HTML file
                with open(html_file, 'w') as f:
                    f.write(html_content)
                files_created.append(html_file)
                print(f"📄 Generated: {html_file}")
            
            # Generate login forms if authentication is needed
            if requirements['authentication']:
                login_forms = self.generate_login_form({})
                for i, form in enumerate(login_forms):
                    form_file = f'templates/auth_form_{i}.html'
                    with open(form_file, 'w') as f:
                        f.write(form)
                    files_created.append(form_file)
                    print(f"🔐 Generated: {form_file}")
            
            # Generate CSS if responsive design is needed
            if requirements['responsive']:
                css_content = self.generate_css_styles({'responsive': True})
                if css_content:
                    os.makedirs('static/css', exist_ok=True)
                    css_file = 'static/css/styles.css'
                    with open(css_file, 'w') as f:
                        f.write(css_content)
                    files_created.append(css_file)
                    print(f"🎨 Generated: {css_file}")
            
            return ExecutionResult(
                success=True,
                message=f"Frontend code generated successfully! Created {len(files_created)} files.",
                files_created=files_created,
                output=f"Generated files: {', '.join(files_created)}"
            )
            
        except Exception as e:
            return ExecutionResult(
                success=False,
                message=f"Frontend task execution failed: {str(e)}",
                files_created=[],
                error=str(e)
            )
    
    def generate_html_template(self, requirements: Dict[str, Any]) -> str:
        """
        Generate HTML template based on requirements using Qwen AI.
        """
        if self.ai_enhanced and self.qwen_service:
            # Use Qwen AI for enhanced HTML generation
            task_desc = f"Create a responsive HTML template with the following requirements: {requirements}"
            ai_response = self.qwen_service.generate_frontend_code(
                task_desc,
                framework="vanilla",
                requirements=requirements
            )
            
            if ai_response.success:
                return ai_response.content
            else:
                print(f"⚠️ AI generation failed, using template: {ai_response.error}")
        
        # Fallback to template-based generation
        return self._generate_html_template_fallback(requirements)
    
    def _generate_html_template_fallback(self, requirements: Dict[str, Any]) -> str:
        """
        Generate HTML template fallback using basic templates.
        """
        # Extract requirements
        title = requirements.get('title', 'My App')
        has_auth = requirements.get('authentication', False)
        
        # Generate HTML using templates
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="#">{title}</a>
            {'<div class="ms-auto"><a href="#login" class="btn btn-outline-light">Login</a></div>' if has_auth else ''}
        </div>
    </nav>
    
    <div class="container mt-4">
        <div class="row">
            <div class="col-md-12">
                <h1>Welcome to {title}</h1>
                {'<div id="auth-section"></div>' if has_auth else ''}
                <div id="main-content">
                    <!-- Generated content will go here -->
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""
        
        return html_template
    
    def generate_css_styles(self, design_specs: Dict[str, Any]) -> str:
        """
        Generate CSS styles based on design specifications.
        
        Args:
            design_specs: Dictionary containing styling requirements
            
        Returns:
            str: Generated CSS content
        """
        print("🎨 Generating CSS styles...")
        
        css_content = f"""/* Generated CSS Styles */
/* Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} */

/* Base Styles */
:root {{
    --primary-color: #007bff;
    --secondary-color: #6c757d;
    --success-color: #28a745;
    --danger-color: #dc3545;
    --warning-color: #ffc107;
    --info-color: #17a2b8;
    --light-color: #f8f9fa;
    --dark-color: #343a40;
    
    --font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    --border-radius: 0.375rem;
    --box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    --transition: all 0.15s ease-in-out;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: var(--font-family);
    line-height: 1.5;
    color: var(--dark-color);
    background-color: var(--light-color);
}}

/* Layout */
.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 15px;
}}

.row {{
    display: flex;
    flex-wrap: wrap;
    margin: 0 -15px;
}}

.col {{
    flex: 1;
    padding: 0 15px;
}}

/* Navigation */
.navbar {{
    background-color: var(--primary-color);
    padding: 1rem 0;
    box-shadow: var(--box-shadow);
}}

.navbar-brand {{
    color: white;
    font-size: 1.5rem;
    font-weight: 700;
    text-decoration: none;
}}

.navbar-nav {{
    display: flex;
    list-style: none;
    margin-left: auto;
}}

.nav-link {{
    color: rgba(255, 255, 255, 0.8);
    text-decoration: none;
    padding: 0.5rem 1rem;
    transition: var(--transition);
}}

.nav-link:hover {{
    color: white;
}}

/* Cards */
.card {{
    background: white;
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    margin-bottom: 1.5rem;
    overflow: hidden;
}}

.card-header {{
    background-color: var(--light-color);
    padding: 1rem;
    border-bottom: 1px solid #dee2e6;
}}

.card-body {{
    padding: 1.5rem;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
}}

/* Forms */
.form-group {{
    margin-bottom: 1rem;
}}

.form-label {{
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
}}

.form-control {{
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ced4da;
    border-radius: var(--border-radius);
    font-size: 1rem;
    transition: var(--transition);
}}

.form-control:focus {{
    outline: 0;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}}

/* Buttons */
.btn {{
    display: inline-block;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    font-weight: 400;
    text-align: center;
    text-decoration: none;
    border: 1px solid transparent;
    border-radius: var(--border-radius);
    cursor: pointer;
    transition: var(--transition);
}}

.btn-primary {{
    color: white;
    background-color: var(--primary-color);
    border-color: var(--primary-color);
}}

.btn-primary:hover {{
    background-color: #0056b3;
    border-color: #0056b3;
}}

.btn-secondary {{
    color: white;
    background-color: var(--secondary-color);
    border-color: var(--secondary-color);
}}

.btn-success {{
    color: white;
    background-color: var(--success-color);
    border-color: var(--success-color);
}}

.btn-danger {{
    color: white;
    background-color: var(--danger-color);
    border-color: var(--danger-color);
}}"""

        # Add responsive design if required
        if design_specs.get('responsive', False):
            css_content += """

/* Responsive Design */
@media (max-width: 768px) {{
    .container {{
        padding: 0 10px;
    }}
    
    .row {{
        margin: 0 -10px;
    }}
    
    .col {{
        padding: 0 10px;
        flex: 100%;
    }}
    
    .navbar-nav {{
        flex-direction: column;
        margin-left: 0;
        margin-top: 1rem;
    }}
    
    .card-body {{
        padding: 1rem;
    }}
    
    .btn {{
        width: 100%;
        margin-bottom: 0.5rem;
    }}
}}

@media (max-width: 576px) {{
    .container {{
        padding: 0 5px;
    }}
    
    .card-body {{
        padding: 0.75rem;
    }}
    
    .form-control {{
        padding: 0.5rem;
    }}
}}"""

        # Add dark mode support
        if design_specs.get('dark_mode', False):
            css_content += """

/* Dark Mode */
@media (prefers-color-scheme: dark) {{
    :root {{
        --light-color: #212529;
        --dark-color: #f8f9fa;
    }}
    
    body {{
        background-color: var(--light-color);
        color: var(--dark-color);
    }}
    
    .card {{
        background-color: #343a40;
        color: var(--dark-color);
    }}
    
    .card-header {{
        background-color: #495057;
        border-bottom-color: #6c757d;
    }}
    
    .form-control {{
        background-color: #495057;
        border-color: #6c757d;
        color: var(--dark-color);
    }}
}}"""

        css_content += "\n"
        
        print("✅ CSS styles generated successfully!")
        return css_content
    
    def generate_login_form(self, auth_config: Dict[str, Any]) -> List[str]:
        """
        Generate login/signup forms.
        
        EXAMPLE: Template-based form generation
        """
        forms = []
        
        # Login form template
        login_form = """
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h4>Login</h4>
                    </div>
                    <div class="card-body">
                        <form id="loginForm">
                            <div class="mb-3">
                                <label for="email" class="form-label">Email</label>
                                <input type="email" class="form-control" id="email" required>
                            </div>
                            <div class="mb-3">
                                <label for="password" class="form-label">Password</label>
                                <input type="password" class="form-control" id="password" required>
                            </div>
                            <button type="submit" class="btn btn-primary w-100">Login</button>
                        </form>
                        <div class="mt-3 text-center">
                            <a href="#" onclick="showSignup()">Don't have an account? Sign up</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            // TODO: Implement login logic
            alert('Login functionality to be implemented');
        });
        
        function showSignup() {
            // TODO: Show signup form
            alert('Signup form to be implemented');
        }
        </script>
        """
        
        forms.append(login_form)
        return forms
    
    def generate_responsive_layout(self, layout_config: Dict[str, Any]) -> str:
        """
        Generate responsive layout templates.
        
        Args:
            layout_config: Configuration for the layout structure
            
        Returns:
            str: Generated HTML layout structure
        """
        print("📱 Generating responsive layout...")
        
        # Default layout configuration
        config = {
            'columns': layout_config.get('columns', 2),
            'sidebar': layout_config.get('sidebar', False),
            'header': layout_config.get('header', True),
            'footer': layout_config.get('footer', True),
            'navigation': layout_config.get('navigation', True),
            'title': layout_config.get('title', 'Responsive Layout')
        }
        
        # Generate grid-based responsive layout
        layout_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config['title']}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="static/css/styles.css">
    <style>
        /* Custom responsive grid */
        .layout-grid {{
            display: grid;
            gap: 1rem;
            min-height: 100vh;
        }}
        
        .grid-header {{
            grid-area: header;
            background: var(--primary-color);
            color: white;
            padding: 1rem;
        }}
        
        .grid-nav {{
            grid-area: nav;
            background: var(--light-color);
            padding: 1rem;
            border-right: 1px solid #dee2e6;
        }}
        
        .grid-main {{
            grid-area: main;
            padding: 1rem;
        }}
        
        .grid-aside {{
            grid-area: aside;
            background: var(--light-color);
            padding: 1rem;
            border-left: 1px solid #dee2e6;
        }}
        
        .grid-footer {{
            grid-area: footer;
            background: var(--secondary-color);
            color: white;
            padding: 1rem;
            text-align: center;
        }}
        
        /* Desktop layout */
        @media (min-width: 768px) {{
            .layout-grid {{"""

        if config['sidebar'] and config['navigation']:
            layout_html += """
                grid-template-areas: 
                    "header header header"
                    "nav main aside"
                    "footer footer footer";
                grid-template-columns: 200px 1fr 200px;
                grid-template-rows: auto 1fr auto;"""
        elif config['sidebar']:
            layout_html += """
                grid-template-areas: 
                    "header header"
                    "main aside"
                    "footer footer";
                grid-template-columns: 1fr 200px;
                grid-template-rows: auto 1fr auto;"""
        elif config['navigation']:
            layout_html += """
                grid-template-areas: 
                    "header header"
                    "nav main"
                    "footer footer";
                grid-template-columns: 200px 1fr;
                grid-template-rows: auto 1fr auto;"""
        else:
            layout_html += """
                grid-template-areas: 
                    "header"
                    "main"
                    "footer";
                grid-template-columns: 1fr;
                grid-template-rows: auto 1fr auto;"""

        layout_html += """
            }}
        }}
        
        /* Mobile layout */
        @media (max-width: 767px) {{
            .layout-grid {{
                grid-template-areas: 
                    "header"
                    "nav"
                    "main"
                    "aside"
                    "footer";
                grid-template-columns: 1fr;
                grid-template-rows: auto auto 1fr auto auto;
            }}
            
            .grid-nav, .grid-aside {{
                border: none;
                border-top: 1px solid #dee2e6;
                border-bottom: 1px solid #dee2e6;
            }}
        }}
        
        /* Content grid for main area */
        .content-grid {{
            display: grid;
            gap: 1rem;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        }}
        
        .content-item {{
            background: white;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            padding: 1.5rem;
        }}
    </style>
</head>
<body>
    <div class="layout-grid">"""

        # Add header if enabled
        if config['header']:
            layout_html += """
        <header class="grid-header">
            <div class="d-flex justify-content-between align-items-center">
                <h1 class="h3 mb-0">{}</h1>
                <div class="header-actions">
                    <button class="btn btn-light btn-sm me-2">Settings</button>
                    <button class="btn btn-outline-light btn-sm">Profile</button>
                </div>
            </div>
        </header>""".format(config['title'])

        # Add navigation if enabled
        if config['navigation']:
            layout_html += """
        <nav class="grid-nav">
            <h5>Navigation</h5>
            <ul class="nav flex-column">
                <li class="nav-item">
                    <a class="nav-link active" href="#dashboard">
                        <i class="bi bi-house"></i> Dashboard
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#projects">
                        <i class="bi bi-folder"></i> Projects
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#analytics">
                        <i class="bi bi-graph-up"></i> Analytics
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#settings">
                        <i class="bi bi-gear"></i> Settings
                    </a>
                </li>
            </ul>
        </nav>"""

        # Add main content area
        layout_html += """
        <main class="grid-main">
            <div class="content-grid">"""

        # Generate content items based on column count
        for i in range(config['columns']):
            layout_html += f"""
                <div class="content-item">
                    <h4>Content Section {i + 1}</h4>
                    <p>This is a responsive content section that adapts to different screen sizes.</p>
                    <div class="mt-3">
                        <button class="btn btn-primary btn-sm">Action {i + 1}</button>
                        <button class="btn btn-outline-secondary btn-sm ms-2">More</button>
                    </div>
                </div>"""

        layout_html += """
            </div>
        </main>"""

        # Add sidebar if enabled
        if config['sidebar']:
            layout_html += """
        <aside class="grid-aside">
            <h5>Sidebar</h5>
            <div class="card">
                <div class="card-body">
                    <h6 class="card-title">Quick Info</h6>
                    <p class="card-text small">Additional information and widgets can be placed here.</p>
                </div>
            </div>
            <div class="card mt-3">
                <div class="card-body">
                    <h6 class="card-title">Statistics</h6>
                    <div class="d-flex justify-content-between">
                        <span class="text-muted">Active:</span>
                        <strong>24</strong>
                    </div>
                    <div class="d-flex justify-content-between">
                        <span class="text-muted">Pending:</span>
                        <strong>7</strong>
                    </div>
                </div>
            </div>
        </aside>"""

        # Add footer if enabled
        if config['footer']:
            layout_html += """
        <footer class="grid-footer">
            <p class="mb-0">&copy; 2024 Generated Layout. All rights reserved.</p>
        </footer>"""

        layout_html += """
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Responsive layout JavaScript
        document.addEventListener('DOMContentLoaded', function() {{
            // Handle mobile menu toggle
            const navLinks = document.querySelectorAll('.nav-link');
            navLinks.forEach(link => {{
                link.addEventListener('click', function(e) {{
                    e.preventDefault();
                    
                    // Remove active class from all links
                    navLinks.forEach(l => l.classList.remove('active'));
                    
                    // Add active class to clicked link
                    this.classList.add('active');
                    
                    console.log('Navigating to:', this.textContent.trim());
                }});
            }});
            
            // Handle responsive behavior
            function handleResize() {{
                const isMobile = window.innerWidth < 768;
                const grid = document.querySelector('.layout-grid');
                
                if (isMobile) {{
                    grid.classList.add('mobile-layout');
                }} else {{
                    grid.classList.remove('mobile-layout');
                }}
            }}
            
            window.addEventListener('resize', handleResize);
            handleResize(); // Initial call
        }});
    </script>
</body>
</html>"""
        
        print("✅ Responsive layout generated successfully!")
        return layout_html
    
    def get_ai_tool(self):
        """Get the AI tool for LangChain/CrewAI integration."""
        if self._ai_tool is None:
            self._ai_tool = FrontendGeneratorTool(self)
        return self._ai_tool
    
    def process_with_ai(self, task_description: str, framework: str = "vanilla") -> str:
        """Process task using AI integration if available."""
        ai_tool = self.get_ai_tool()
        if self.enhanced_mode:
            return ai_tool._run(task_description, framework)
        else:
            # Fallback to standard processing
            requirements = ai_tool._parse_requirements(task_description, framework)
            return f"Standard processing: {requirements}"
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get agent capabilities and status."""
        return {
            "name": self.name,
            "role": self.role,
            "specialties": self.specialties,
            "frameworks": self.supported_frameworks,
            "styles": self.supported_styles,
            "enhanced_mode": self.enhanced_mode,
            "ai_integration": AI_INTEGRATION_AVAILABLE,
            "tools_available": ["html_generator", "css_generator", "layout_generator", "form_generator"]
        }


class FrontendGeneratorTool(object):
    """Tool for frontend code generation (simplified for basic mode)."""
    
    name: str = "Frontend Code Generator"
    description: str = "Generate frontend code including HTML, CSS, JavaScript, and React/Vue components"
    
    def __init__(self, agent_instance=None):
        # Simplified initialization for basic mode
        self.agent = agent_instance
    
    def _run(self, task_description: str, framework: str = "vanilla") -> str:
        """Generate frontend code based on task description."""
        if self.agent:
            # Use the actual agent methods
            requirements = self._parse_requirements(task_description, framework)
            
            generated_files = []
            
            # Generate HTML
            if "html" in task_description.lower() or "interface" in task_description.lower():
                html_content = self.agent.generate_html_template(requirements)
                generated_files.append(f"HTML Template ({len(html_content)} chars)")
            
            # Generate CSS
            if "css" in task_description.lower() or "style" in task_description.lower():
                css_content = self.agent.generate_css_styles(requirements)
                generated_files.append(f"CSS Styles ({len(css_content)} chars)")
            
            # Generate responsive layout
            if "responsive" in task_description.lower() or "layout" in task_description.lower():
                layout_content = self.agent.generate_responsive_layout(requirements)
                generated_files.append(f"Responsive Layout ({len(layout_content)} chars)")
            
            return f"✅ Frontend code generated successfully!\nFiles created: {', '.join(generated_files)}\nFramework: {framework}\nRequirements: {requirements}"
        
        return f"Generated frontend code for: {task_description} using {framework}"
    
    def _parse_requirements(self, task_description: str, framework: str) -> Dict[str, Any]:
        """Parse task description into requirements."""
        desc_lower = task_description.lower()
        
        return {
            'title': 'Generated Application',
            'framework': framework,
            'authentication': any(word in desc_lower for word in ['auth', 'login', 'signup', 'user']),
            'responsive': any(word in desc_lower for word in ['responsive', 'mobile', 'tablet']),
            'forms': any(word in desc_lower for word in ['form', 'input', 'submit']),
            'dashboard': 'dashboard' in desc_lower,
            'ecommerce': any(word in desc_lower for word in ['shop', 'cart', 'payment', 'ecommerce']),
            'admin': 'admin' in desc_lower,
            'api_integration': any(word in desc_lower for word in ['api', 'backend', 'endpoint']),
            'dark_mode': 'dark' in desc_lower,
            'columns': 3 if 'dashboard' in desc_lower else 2,
            'sidebar': any(word in desc_lower for word in ['sidebar', 'navigation', 'nav']),
            'header': True,
            'footer': True,
            'navigation': True
        }
    
    async def _arun(self, task_description: str, framework: str = "vanilla") -> str:
        """Async version of the tool."""
        return self._run(task_description, framework)


def main():
    """Test the frontend coder agent."""
    agent = FrontendCoderAgent()
    
    # Test task assignment
    test_task = {
        "role": "Frontend Developer",
        "action": "Write code",
        "task": "Develop responsive user interface and client-side functionality including login/signup forms"
    }
    
    result = agent.execute_task(test_task)
    print(f"✅ Task completed: {result.success}")
    print(f"📝 Message: {result.message}")


if __name__ == "__main__":
    main()
