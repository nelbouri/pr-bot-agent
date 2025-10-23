"""Comment generation."""

import random
from typing import Dict


def generate_review_comment(pr_data: Dict, analysis: Dict, style: str = "helpful") -> str:
    """Generate a review comment.
    
    Args:
        pr_data: PR data from GitHub
        analysis: Analysis results
        style: Comment style - helpful, funny, roast, or encouraging
        
    Returns:
        Comment text in markdown format
    """
    if style == "funny":
        return _generate_funny_comment(analysis)
    elif style == "roast":
        return _generate_roast_comment(analysis)
    elif style == "encouraging":
        return _generate_encouraging_comment(analysis)
    else:
        return _generate_helpful_comment(analysis)


def _generate_helpful_comment(analysis: Dict) -> str:
    """Generate helpful review comment."""
    comment = "## 🤖 PR Bot Review\n\n"
    comment += f"**Files changed:** {analysis['total_files']}\n"
    comment += f"**Lines added:** +{analysis['additions']}\n"
    comment += f"**Lines removed:** -{analysis['deletions']}\n\n"
    
    if analysis["large_files"]:
        comment += "### ⚠️ Large Files Detected\n"
        for file in analysis["large_files"]:
            comment += f"- `{file['name']}` ({file['changes']} changes)\n"
        comment += "\nConsider breaking large changes into smaller PRs for easier review.\n\n"
    
    if analysis["potential_issues"]:
        comment += "### 🔍 Potential Issues\n"
        for issue in analysis["potential_issues"]:
            comment += f"- {issue}\n"
        comment += "\n"
    
    comment += "### ✅ Overall\n"
    comment += "Looking good! Keep up the great work! 🚀"
    
    return comment


def _generate_funny_comment(analysis: Dict) -> str:
    """Generate funny review comment."""
    openers = [
        "🎭 *dramatically enters the chat*",
        "🔮 The prophecy has been fulfilled!",
        "🎪 Ladies and gentlemen, we have a PR!",
        "🎬 And... ACTION!",
    ]
    
    comment = f"{random.choice(openers)}\n\n"
    comment += f"I see you've changed **{analysis['total_files']} files**. "
    
    if analysis['additions'] > analysis['deletions']:
        comment += f"Adding {analysis['additions']} lines while only deleting {analysis['deletions']}? "
        comment += "Someone's feeling productive! 💪\n\n"
    else:
        comment += f"Deleting {analysis['deletions']} lines? Now THAT's what I call refactoring! 🧹\n\n"
    
    if analysis["large_files"]:
        comment += "**⚠️ Plot twist:** Some files are CHONKY:\n"
        for file in analysis["large_files"]:
            comment += f"- `{file['name']}` is an absolute unit ({file['changes']} changes)\n"
        comment += "\n"
    
    comment += "*This PR review brought to you by PR Bot Agent™ - Now with 80% more personality!* 🤖✨"
    
    return comment


def _generate_roast_comment(analysis: Dict) -> str:
    """Generate roasting review comment."""
    comment = "## 🔥 ROAST MODE ACTIVATED 🔥\n\n"
    
    roasts = [
        f"You changed {analysis['total_files']} files? Someone's having a productive day... or a really destructive one. 🤔",
        f"{analysis['additions']} additions? I've seen novels shorter than this PR.",
        "This PR is like a box of chocolates... if chocolates were lines of code and I had no idea what I was going to get.",
    ]
    
    comment += random.choice(roasts) + "\n\n"
    
    if analysis["large_files"]:
        comment += "**Your massive files:**\n"
        for file in analysis["large_files"]:
            comment += f"- `{file['name']}` - Absolute unit. Did you try using functions? They're free! 📦\n"
        comment += "\n"
    
    if analysis["potential_issues"]:
        comment += "**Issues I found** (shocking, I know):\n"
        for issue in analysis["potential_issues"]:
            comment += f"- {issue} 👀\n"
        comment += "\n"
    
    comment += "---\n*Just kidding! Your code is probably fine. Probably. 😅*"
    
    return comment


def _generate_encouraging_comment(analysis: Dict) -> str:
    """Generate encouraging review comment."""
    comment = "## 🌟 Amazing Work! 🌟\n\n"
    
    encouragements = [
        "You're doing great! Every commit is progress! 🚀",
        "This PR shows real dedication! Keep it up! 💪",
        "Your code is making a difference! 🌈",
        "Wow, look at all this awesome work! 🎉",
    ]
    
    comment += random.choice(encouragements) + "\n\n"
    comment += f"**Your awesome stats:**\n"
    comment += f"- Files touched: {analysis['total_files']} 📁\n"
    comment += f"- Lines added: +{analysis['additions']} ➕\n"
    comment += f"- Lines removed: -{analysis['deletions']} ➖\n\n"
    
    if analysis["large_files"]:
        comment += "You're tackling some big files - that takes courage! 🦁\n\n"
    
    comment += "Remember: Every line of code you write is making you a better developer! 🌱\n\n"
    comment += "*You've got this!* 💖"
    
    return comment
