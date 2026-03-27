import os
import ast

def generate_map(base_dir=".", output_file="project_map.txt"):
    """
    Generates a full project map including directory structure and python docstrings.
    This acts as a 'Context Window Optimizer' for AI agents.
    """
    ignore_dirs = {".git", "venv", "__pycache__", ".tox", ".pytest_cache", "testme"}
    
    with open(output_file, "w", encoding="utf-8") as out:
        out.write("# 🗺️ Project Architecture Map\n\n")
        
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            level = root.replace(base_dir, "").count(os.sep)
            indent = " " * 4 * level
            folder_name = os.path.basename(root)
            if not folder_name:
                folder_name = base_dir
            
            out.write(f"{indent}📂 {folder_name}/\n")
            sub_indent = " " * 4 * (level + 1)
            
            for file in sorted(files):
                if file.endswith(".py"):
                    out.write(f"{sub_indent}📄 {file}\n")
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            tree = ast.parse(f.read(), filename=file_path)
                            doc = ast.get_docstring(tree)
                            if doc:
                                doc_indent = sub_indent + "    "
                                out.write(f"{doc_indent}\"\"\" {doc.splitlines()[0]}... \"\"\"\n")
                            
                            # Extract function docstrings
                            for node in ast.walk(tree):
                                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                                    func_doc = ast.get_docstring(node)
                                    out.write(f"{sub_indent}    - {node.name}()\n")
                                    if func_doc:
                                        func_doc_indent = sub_indent + "        "
                                        out.write(f"{func_doc_indent}\"\"\"{func_doc.splitlines()[0]}...\"\"\"\n")
                    except Exception:
                        pass
                else:
                    out.write(f"{sub_indent}📄 {file}\n")

if __name__ == "__main__":
    generate_map()
    print("[OK] Project map generated as project_map.txt")
