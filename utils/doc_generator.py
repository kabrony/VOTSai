import inspect
import os
import re
import importlib.util
import sys
import time  # Added for rate limiting
from typing import Dict, List, Optional, Callable, Any, Tuple

def document_module(module_path: str, output_dir: str, skip_import_errors: bool = False, 
                    verbose: bool = False) -> Tuple[bool, str]:
    """
    Generate markdown documentation for a Python module.
    
    Args:
        module_path: Path to the Python module file
        output_dir: Directory to write the documentation to
        skip_import_errors: If True, continue execution despite import errors
        verbose: If True, print detailed error messages
        
    Returns:
        Tuple of (success, error_message)
    """
    try:
        # Import the module
        module_name = os.path.basename(module_path).replace(".py", "")
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        
        if spec is None:
            return False, f"Could not create spec for {module_path}"
            
        module = importlib.util.module_from_spec(spec)
        
        # Save the original sys.path to restore it later
        original_path = sys.path.copy()
        
        # Add the module's directory to sys.path temporarily
        module_dir = os.path.dirname(os.path.abspath(module_path))
        if module_dir not in sys.path:
            sys.path.insert(0, module_dir)
            
        try:
            mock_imports = False
            if mock_imports and isinstance(e, ImportError):
                missing_module = str(e).split("'")[1] if "'" in str(e) else str(e)
                sys.modules[missing_module] = type(missing_module, (), {})
                if verbose:
                    print(f"Mocked missing import: {missing_module}")
                # Try to continue with the import
                try:
                    spec.loader.exec_module(module)
                except ImportError as e2:
                    if skip_import_errors:
                        if verbose:
                            print(f"Skipping {module_path} due to import error: {e2}")
                        # Restore the original sys.path
                        sys.path = original_path
                        return False, f"Import error: {e2}"
                    else:
                        raise
            else:
                spec.loader.exec_module(module)
        except Exception as e:
            # Restore the original sys.path
            sys.path = original_path
            return False, str(e)
            
        # Restore the original sys.path
        sys.path = original_path
        
        # Prepare output file
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{module_name}.md")
        
        with open(output_file, "w") as f:
            # Write module header
            f.write(f"# {module_name}\n\n")
            
            if module.__doc__:
                f.write(f"{module.__doc__.strip()}\n\n")
                
            # Get all classes and functions
            classes = []
            functions = []
            
            for name, obj in inspect.getmembers(module):
                # Skip private members
                if name.startswith("_") and name != "__init__":
                    continue
                    
                if inspect.isclass(obj):
                    classes.append((name, obj))
                elif inspect.isfunction(obj):
                    functions.append((name, obj))
                    
            # Document classes
            if classes:
                f.write("## Classes\n\n")
                for name, cls in classes:
                    document_class(f, name, cls)
                    
            # Document functions
            if functions:
                f.write("## Functions\n\n")
                for name, func in functions:
                    document_function(f, name, func)
                    
        print(f"Generated documentation for {module_name} at {output_file}")
        return True, ""
        
    except Exception as e:
        error_msg = f"Error documenting module {module_path}: {e}"
        print(error_msg)
        return False, str(e)
        
def document_class(f, name: str, cls: type) -> None:
    """
    Generate documentation for a class.
    
    Args:
        f: File handle to write to
        name: Name of the class
        cls: Class object to document
    """
    try:
        f.write(f"### {name}\n\n")
        
        if cls.__doc__:
            f.write(f"{cls.__doc__.strip()}\n\n")
            
        # Document methods
        methods = []
        for method_name, method in inspect.getmembers(cls, inspect.isfunction):
            # Skip private methods
            if method_name.startswith("_") and method_name not in ["__init__"]:
                continue
                
            methods.append((method_name, method))
            
        if methods:
            f.write("#### Methods\n\n")
            for method_name, method in methods:
                document_method(f, method_name, method)
    except Exception as e:
        f.write(f"Error documenting class {name}: {e}\n\n")
        
def document_method(f, name: str, method: Callable) -> None:
    """
    Generate documentation for a method.
    
    Args:
        f: File handle to write to
        name: Name of the method
        method: Method object to document
    """
    try:
        signature = inspect.signature(method)
        param_str = ", ".join(str(p) for p in signature.parameters.values())
        
        f.write(f"##### {name}\n\n")
        f.write(f"```python\n{name}({param_str})\n```\n\n")
        
        if method.__doc__:
            f.write(f"{method.__doc__.strip()}\n\n")
            
            # Extract parameter descriptions from docstring
            if "Args:" in method.__doc__ or "Parameters:" in method.__doc__:
                f.write("###### Parameters\n\n")
                for param_name in signature.parameters:
                    if param_name == "self":
                        continue
                    
                    pattern = rf"\s+{param_name}:\s*(.*?)(\n\s+\w+:|$)"
                    match = re.search(pattern, method.__doc__, re.DOTALL)
                    if match:
                        param_desc = match.group(1).strip()
                        f.write(f"- **{param_name}**: {param_desc}\n")
                f.write("\n")
                
            # Extract return value description from docstring
            if "Returns:" in method.__doc__:
                f.write("###### Returns\n\n")
                pattern = r"Returns:(.*?)(?:\n\s*\w+:|$)"
                match = re.search(pattern, method.__doc__, re.DOTALL)
                if match:
                    return_desc = match.group(1).strip()
                    f.write(f"{return_desc}\n\n")
                    
    except Exception as e:
        f.write(f"Error documenting method {name}: {e}\n\n")
        
def document_function(f, name: str, func: Callable, indent: bool = False) -> None:
    """
    Generate documentation for a function.
    
    Args:
        f: File handle to write to
        name: Name of the function
        func: Function object to document
        indent: Whether to indent the documentation
    """
    try:
        signature = inspect.signature(func)
        param_str = ", ".join(str(p) for p in signature.parameters.values())
        
        prefix = "    " if indent else ""
        
        f.write(f"{prefix}### {name}\n\n")
        f.write(f"{prefix}```python\n{name}({param_str})\n```\n\n")
        
        if func.__doc__:
            f.write(f"{prefix}{func.__doc__.strip()}\n\n")
            
            # Extract parameter descriptions from docstring
            if "Args:" in func.__doc__ or "Parameters:" in func.__doc__:
                f.write(f"{prefix}#### Parameters\n\n")
                for param_name in signature.parameters:
                    pattern = rf"\s+{param_name}:\s*(.*?)(\n\s+\w+:|$)"
                    match = re.search(pattern, func.__doc__, re.DOTALL)
                    if match:
                        param_desc = match.group(1).strip()
                        f.write(f"{prefix}- **{param_name}**: {param_desc}\n")
                f.write("\n")
                
            # Extract return value description from docstring
            if "Returns:" in func.__doc__:
                f.write(f"{prefix}#### Returns\n\n")
                pattern = r"Returns:(.*?)(?:\n\s*\w+:|$)"
                match = re.search(pattern, func.__doc__, re.DOTALL)
                if match:
                    return_desc = match.group(1).strip()
                    f.write(f"{prefix}{return_desc}\n\n")
    except Exception as e:
        f.write(f"Error documenting function {name}: {e}\n\n")
        
def generate_project_documentation(
    project_dir: str, 
    output_dir: str, 
    exclude_patterns: List[str] = None,
    exclude_modules: List[str] = None,
    skip_import_errors: bool = False,
    dry_run: bool = False,
    max_depth: int = None,
    verbose: bool = False,
    include_standard_lib: bool = False,
    rate_limit: float = 0.0
) -> Dict[str, List[Tuple[str, str]]]:
    """
    Generate documentation for an entire project.
    
    Args:
        project_dir: Root directory of the project
        output_dir: Directory to write documentation to
        exclude_patterns: List of glob patterns to exclude
        exclude_modules: List of specific module names to exclude (e.g., 'cpu_monitor')
        skip_import_errors: If True, continue execution despite import errors
        dry_run: If True, only check for errors without generating docs
        max_depth: Maximum directory depth to traverse
        verbose: If True, print detailed output
        include_standard_lib: If True, document modules from standard library
        rate_limit: Seconds to wait between processing files (to prevent system overload)
        
    Returns:
        Dictionary with successful and failed module documentation attempts
    """
    if exclude_patterns is None:
        exclude_patterns = [
            "**/venv/**", 
            "**/__pycache__/**", 
            "**/.git/**", 
            "**/*.pyc",
            "**/.env/**",
            "**/.venv/**",
            "**/node_modules/**",
            "**/build/**",
            "**/dist/**",
            "**/.pytest_cache/**",
            "**/.mypy_cache/**"
        ]
        
    if exclude_modules is None:
        exclude_modules = []
        
    if not dry_run:
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate README
        with open(os.path.join(output_dir, "README.md"), "w") as f:
            f.write("# API Documentation\n\n")
            f.write("This documentation is automatically generated from the codebase.\n\n")
            f.write("## Modules\n\n")
    
    # Find all Python files
    python_files = []
    for root, _, files in os.walk(project_dir):
        # Check directory depth
        rel_path = os.path.relpath(root, project_dir)
        depth = 0 if rel_path == '.' else len(rel_path.split(os.sep))
        if max_depth is not None and depth > max_depth:
            continue
        
        # Check if this directory should be excluded
        skip_dir = False
        for pattern in exclude_patterns:
            pattern_regex = pattern.replace("**", ".*").replace("*", "[^/]*")
            if re.match(pattern_regex, root):
                skip_dir = True
                break
                
        if skip_dir:
            continue
            
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                
                # Check if this file should be excluded
                skip_file = False
                for pattern in exclude_patterns:
                    pattern_regex = pattern.replace("**", ".*").replace("*", "[^/]*")
                    if re.match(pattern_regex, file_path):
                        skip_file = True
                        break
                        
                if skip_file:
                    continue
                
                # Skip standard library modules unless explicitly included
                if not include_standard_lib:
                    # Check if this might be a standard library module
                    is_std_lib = False
                    if 'site-packages' in file_path or 'dist-packages' in file_path:
                        is_std_lib = True
                    
                    if is_std_lib:
                        continue
                
                python_files.append(file_path)
                
    # Document each file
    results = {"success": [], "failure": []}
    documented_modules = []
    
    total_files = len(python_files)
    if verbose:
        print(f"Found {total_files} Python files to document")
    
    for index, file_path in enumerate(python_files):
        module_name = os.path.basename(file_path).replace(".py", "")
        
        # Skip explicitly excluded modules
        if module_name in exclude_modules:
            if verbose:
                print(f"Skipping excluded module: {module_name}")
            continue
            
        # Show progress if in verbose mode
        if verbose:
            print(f"Processing file {index+1}/{total_files}: {file_path}")
        
        if dry_run:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    compile(content, file_path, 'exec')
                
                if verbose:
                    print(f"Syntax check passed for {file_path}")
                results["success"].append((module_name, ""))
            except Exception as e:
                error_msg = f"Syntax check failed for {file_path}: {e}"
                print(error_msg)
                results["failure"].append((module_name, str(e)))
        else:
            success, error = document_module(file_path, output_dir, skip_import_errors, verbose)
            
            if success:
                # Update README
                rel_path = os.path.relpath(file_path, project_dir)
                module_dir = os.path.dirname(rel_path)
                documented_modules.append((module_dir, module_name))
                results["success"].append((module_name, ""))
            else:
                if verbose:
                    print(f"Failed to document {file_path}: {error}")
                results["failure"].append((module_name, error))
        
        # Apply rate limiting if specified
        if rate_limit > 0 and index < total_files - 1:  # Don't sleep after the last file
            if verbose:
                print(f"Rate limiting: sleeping for {rate_limit} seconds")
            time.sleep(rate_limit)
    
    if not dry_run:
        # Update README with list of modules
        with open(os.path.join(output_dir, "README.md"), "a") as f:
            documented_modules.sort()
            current_dir = None
            
            for module_dir, module_name in documented_modules:
                if module_dir != current_dir:
                    if current_dir is not None:
                        f.write("\n")
                    current_dir = module_dir
                    if module_dir:
                        f.write(f"### {module_dir}\n\n")
                    else:
                        f.write("### Root\n\n")
                        
                f.write(f"- [{module_name}](./{module_name}.md)\n")
    
    # Print summary
    print("\n--- Documentation Generation Summary ---")
    print(f"Successful: {len(results['success'])}")
    print(f"Failed: {len(results['failure'])}")
    
    if results["failure"] and verbose:
        print("\nFailed modules:")
        for module, error in results["failure"]:
            print(f"- {module}: {error}")
            
    if not dry_run:
        print(f"\nProject documentation generated in {output_dir}")
    
    return results

def load_documentation(output_dir: str) -> Dict[str, str]:
    """
    Load generated documentation from the output directory
    
    Args:
        output_dir: Directory containing the documentation files
        
    Returns:
        Dictionary mapping section names to documentation content
    """
    import os
    import re
    
    docs = {}
    
    try:
        # Check if directory exists
        if not os.path.exists(output_dir):
            logger.warning(f"Documentation directory not found: {output_dir}")
            return {"Getting Started": "Documentation not generated yet. Please run the documentation generator first."}
        
        # Read README first as index
        readme_path = os.path.join(output_dir, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, "r") as f:
                docs["Overview"] = f.read()
        
        # Read all markdown files in the directory
        for filename in os.listdir(output_dir):
            if filename.endswith(".md") and filename != "README.md":
                file_path = os.path.join(output_dir, filename)
                
                # Extract section name from filename
                section_name = re.sub(r'\.md$', '', filename)
                section_name = section_name.replace('_', ' ').title()
                
                with open(file_path, "r") as f:
                    docs[section_name] = f.read()
        
        return docs
    except Exception as e:
        logger.error(f"Error loading documentation: {e}")
        return {"Error": f"Failed to load documentation: {str(e)}"}

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate markdown documentation for Python code")
    parser.add_argument("project_dir", help="Path to the project directory")
    parser.add_argument("--output-dir", "-o", default="docs/api", help="Output directory for documentation")
    parser.add_argument("--exclude", "-e", action="append", help="Glob patterns to exclude")
    parser.add_argument("--exclude-modules", "-m", action="append", help="Specific module names to exclude")
    parser.add_argument("--skip-import-errors", "-s", action="store_true", help="Skip modules with import errors")
    parser.add_argument("--dry-run", "-d", action="store_true", help="Check for errors without generating docs")
    parser.add_argument("--max-depth", "-x", type=int, help="Maximum directory depth to traverse")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print detailed output")
    parser.add_argument("--include-std-lib", "-i", action="store_true", help="Include standard library modules")
    parser.add_argument("--rate-limit", "-r", type=float, default=0.0, 
                        help="Seconds to wait between processing files (to prevent system overload)")
    
    args = parser.parse_args()
    
    generate_project_documentation(
        args.project_dir, 
        args.output_dir, 
        args.exclude,
        args.exclude_modules,
        args.skip_import_errors,
        args.dry_run,
        args.max_depth,
        args.verbose,
        args.include_std_lib,
        args.rate_limit
    )