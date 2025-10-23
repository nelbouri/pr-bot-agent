"""Main agent logic."""

import os
import sys
from typing import Dict
from .github_client import GitHubClient
from .analyzers import analyze_pr_changes
from .commenters import generate_review_comment


class PRBotAgent:
    """An agent that reviews PRs and provides feedback."""
    
    def __init__(self, github_token: str):
        """Initialize the agent.
        
        Args:
            github_token: GitHub API token for authentication
        """
        self.github = GitHubClient(github_token)
        
    def review_pr(self, repo: str, pr_number: int, style: str = "helpful") -> Dict:
        """Review a pull request.
        
        Args:
            repo: Repository in format "owner/repo"
            pr_number: PR number to review
            style: Comment style - "helpful", "funny", "roast", or "encouraging"
            
        Returns:
            Dictionary with review results
        """
        print(f"🤖 Reviewing PR #{pr_number} in {repo}...")
        
        # Step 1: SENSE - Get PR details
        print("📡 Fetching PR data...")
        pr_data = self.github.get_pr(repo, pr_number)
        pr_files = self.github.get_pr_files(repo, pr_number)
        
        # Step 2: THINK - Analyze the changes
        print("🧠 Analyzing changes...")
        analysis = analyze_pr_changes(pr_files)
        
        # Step 3: ACT - Generate comment
        print(f"✍️  Generating {style} comment...")
        comment = generate_review_comment(
            pr_data=pr_data,
            analysis=analysis,
            style=style
        )
        
        # Step 4: RESPOND - Post comment
        print("📤 Posting comment...")
        comment_url = self.github.post_pr_comment(repo, pr_number, comment)
        
        print(f"✅ Review complete! {comment_url}")
        
        return {
            "success": True,
            "comment_url": comment_url,
            "analysis": analysis
        }


def main():
    """CLI entry point for GitHub Actions."""
    print("🚀 PR Bot Agent starting...")
    
    # Get environment variables
    github_token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")
    pr_number = os.getenv("PR_NUMBER")
    style = os.getenv("COMMENT_STYLE", "helpful")
    
    # Validate required inputs
    if not github_token:
        print("❌ Error: GITHUB_TOKEN environment variable not set")
        sys.exit(1)
    
    if not repo:
        print("❌ Error: GITHUB_REPOSITORY environment variable not set")
        sys.exit(1)
    
    if not pr_number:
        print("❌ Error: PR_NUMBER environment variable not set")
        sys.exit(1)
    
    try:
        # Create agent and review PR
        agent = PRBotAgent(github_token)
        result = agent.review_pr(repo, int(pr_number), style)
        
        print(f"\n🎉 Success! Comment posted at: {result['comment_url']}")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
