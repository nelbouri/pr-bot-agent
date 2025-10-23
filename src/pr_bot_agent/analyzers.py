"""Code analysis functions."""

from typing import Dict, List


def analyze_pr_changes(files: List[Dict]) -> Dict:
    """Analyze PR file changes.
    
    Args:
        files: List of file change objects from GitHub API
        
    Returns:
        Analysis results dictionary
    """
    analysis = {
        "total_files": len(files),
        "additions": sum(f["additions"] for f in files),
        "deletions": sum(f["deletions"] for f in files),
        "file_types": {},
        "large_files": [],
        "potential_issues": []
    }
    
    for file in files:
        # Count file types
        ext = file["filename"].split(".")[-1] if "." in file["filename"] else "none"
        analysis["file_types"][ext] = analysis["file_types"].get(ext, 0) + 1
        
        # Flag large changes
        if file["changes"] > 300:
            analysis["large_files"].append({
                "name": file["filename"],
                "changes": file["changes"]
            })
        
        # Check for potential issues in Python files
        if file["filename"].endswith(".py"):
            if "patch" in file:
                patch = file["patch"]
                if "TODO" in patch:
                    analysis["potential_issues"].append(f"TODO found in {file['filename']}")
                if "print(" in patch:
                    analysis["potential_issues"].append(f"Debug print statement in {file['filename']}")
    
    return analysis
