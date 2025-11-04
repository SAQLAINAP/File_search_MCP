import os
from typing import Optional
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("file_search")


@mcp.tool()
def search_keyword_in_file(
    file_path: str, 
    keyword: str, 
    case_sensitive: bool = False, 
    context_lines: int = 2
) -> str:
    """
    Search for a specified keyword within a file and return matching lines with context.
    
    Args:
        file_path: The path to the file to search in (relative or absolute path)
        keyword: The keyword or phrase to search for
        case_sensitive: Whether the search should be case-sensitive (default: False)
        context_lines: Number of lines before and after each match to include for context (default: 2)
        
    Returns:
        A formatted string with all matching lines, their line numbers, and surrounding context.
        Returns an error message if the file doesn't exist or can't be read.
    """
    
    # Check if file exists
    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' does not exist."
    
    # Check if it's a file (not a directory)
    if not os.path.isfile(file_path):
        return f"Error: '{file_path}' is not a file."
    
    # Prepare search keyword
    search_keyword = keyword if case_sensitive else keyword.lower()
    
    matches = []
    
    try:
        # Read the file and search for the keyword
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # Search through each line
        for line_num, line in enumerate(lines, start=1):
            line_content = line if case_sensitive else line.lower()
            
            if search_keyword in line_content:
                # Collect context lines
                start_line = max(1, line_num - context_lines)
                end_line = min(len(lines), line_num + context_lines)
                
                context = []
                for ctx_line_num in range(start_line, end_line + 1):
                    ctx_line = lines[ctx_line_num - 1].rstrip('\n')
                    marker = ">>>" if ctx_line_num == line_num else "   "
                    context.append(f"{marker} {ctx_line_num:4d}: {ctx_line}")
                
                matches.append({
                    'line_number': line_num,
                    'line': line.rstrip('\n'),
                    'context': context
                })
        
        # Format results
        if not matches:
            return f"No matches found for '{keyword}' in file '{file_path}'."
        
        result = f"Found {len(matches)} match(es) for '{keyword}' in '{file_path}':\n\n"
        
        for i, match in enumerate(matches, start=1):
            result += f"--- Match {i} (Line {match['line_number']}) ---\n"
            result += "\n".join(match['context'])
            result += "\n\n"
        
        return result
        
    except PermissionError:
        return f"Error: Permission denied. Cannot read file '{file_path}'."
    except UnicodeDecodeError:
        return f"Error: Cannot decode file '{file_path}'. It may be a binary file."
    except Exception as e:
        return f"Error reading file '{file_path}': {str(e)}"


@mcp.tool()
def search_keyword_in_directory(
    directory_path: str, 
    keyword: str, 
    file_pattern: Optional[str] = None, 
    case_sensitive: bool = False
) -> str:
    """
    Search for a keyword across all files in a directory (recursively).
    
    Args:
        directory_path: The path to the directory to search in
        keyword: The keyword or phrase to search for
        file_pattern: Optional file extension pattern (e.g., '.py', '.txt') to filter files. 
                     If None, searches all text files.
        case_sensitive: Whether the search should be case-sensitive (default: False)
        
    Returns:
        A formatted string with all matching files and their matching lines.
    """
    
    if not os.path.exists(directory_path):
        return f"Error: Directory '{directory_path}' does not exist."
    
    if not os.path.isdir(directory_path):
        return f"Error: '{directory_path}' is not a directory."
    
    search_keyword = keyword if case_sensitive else keyword.lower()
    matches_by_file = {}
    
    # Common text file extensions if no pattern specified
    text_extensions = {
        '.py', '.txt', '.md', '.json', '.xml', '.html', '.css', '.js', '.ts', 
        '.java', '.cpp', '.c', '.h', '.hpp', '.rs', '.go', '.rb', '.php', 
        '.sh', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf'
    }
    
    try:
        # Walk through directory recursively
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Filter by file pattern if specified
                if file_pattern:
                    if not file.endswith(file_pattern):
                        continue
                else:
                    # Only search text files if no pattern specified
                    _, ext = os.path.splitext(file)
                    if ext.lower() not in text_extensions:
                        continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                    
                    file_matches = []
                    for line_num, line in enumerate(lines, start=1):
                        line_content = line if case_sensitive else line.lower()
                        if search_keyword in line_content:
                            file_matches.append({
                                'line_number': line_num,
                                'line': line.rstrip('\n')
                            })
                    
                    if file_matches:
                        # Convert to relative path for readability
                        rel_path = os.path.relpath(file_path, directory_path)
                        matches_by_file[rel_path] = file_matches
                        
                except (PermissionError, UnicodeDecodeError):
                    # Skip files we can't read
                    continue
                except Exception:
                    continue
        
        # Format results
        if not matches_by_file:
            return f"No matches found for '{keyword}' in directory '{directory_path}'."
        
        result = f"Found matches for '{keyword}' in {len(matches_by_file)} file(s):\n\n"
        
        for file_path, file_matches in matches_by_file.items():
            result += f"📄 {file_path} ({len(file_matches)} match(es))\n"
            for match in file_matches:
                result += f"   Line {match['line_number']}: {match['line']}\n"
            result += "\n"
        
        return result
        
    except Exception as e:
        return f"Error searching directory '{directory_path}': {str(e)}"


if __name__ == "__main__":
    # Run the server using stdio transport (recommended for editor integrations)
    mcp.run(transport='stdio')