# File Search MCP Server

A Model Context Protocol (MCP) server that provides powerful file and directory search capabilities using keyword matching with context.

## Features

- **File Search**: Search for keywords within a specific file with configurable context lines
- **Directory Search**: Recursively search for keywords across all files in a directory
- **Case Sensitivity**: Optional case-sensitive or case-insensitive search
- **Context Lines**: View surrounding lines for better context
- **File Filtering**: Filter searches by file extension
- **Error Handling**: Comprehensive error handling for file access issues

## Tools

### 1. search_keyword_in_file

Search for a keyword within a specific file and return matching lines with context.

**Parameters:**
- `file_path` (string): Path to the file to search in
- `keyword` (string): The keyword or phrase to search for
- `case_sensitive` (boolean, optional): Whether search should be case-sensitive (default: false)
- `context_lines` (integer, optional): Number of lines before/after match to include (default: 2)

**Returns:**
Formatted string with all matching lines, line numbers, and surrounding context.

**Example:**
```
Found 3 match(es) for 'import' in 'file_search_server.py':

--- Match 1 (Line 1) ---
>>>    1: import os
       2: from typing import Optional
       3: from mcp.server.fastmcp import FastMCP
```

### 2. search_keyword_in_directory

Search for a keyword across all files in a directory recursively.

**Parameters:**
- `directory_path` (string): Path to the directory to search in
- `keyword` (string): The keyword or phrase to search for
- `file_pattern` (string, optional): File extension filter (e.g., '.py', '.txt')
- `case_sensitive` (boolean, optional): Whether search should be case-sensitive (default: false)

**Returns:**
Formatted string with all matching files and their matching lines.

**Example:**
```
Found matches for 'TODO' in 3 file(s):

📄 main.py (2 match(es))
   Line 45: # TODO: Implement error handling
   Line 78: # TODO: Add unit tests
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Steps

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/file-search-mcp-server.git
cd file-search-mcp-server
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

### With MCP Inspector (Testing)

Test your server using the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector python file_search_server.py
```

This opens a web interface where you can:
- View available tools
- Test tool calls with different parameters
- See request/response details

### With Claude Desktop

1. **Locate your Claude Desktop config file:**
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add the server configuration:**
```json
{
  "mcpServers": {
    "file_search": {
      "command": "python",
      "args": [
        "/absolute/path/to/file_search_server.py"
      ]
    }
  }
}
```

3. **Restart Claude Desktop**

4. **Test the connection:**
   - Look for the 🔌 icon in Claude Desktop
   - You should see "file_search" listed with 2 tools

### With Windsurf

1. **Locate Windsurf's MCP config file:**
   - **Windows**: `%APPDATA%\Windsurf\User\globalStorage\windsurf-mcp\mcp_settings.json`

2. **Add the server configuration:**
```json
{
  "mcpServers": {
    "file_search": {
      "command": "python",
      "args": [
        "/absolute/path/to/file_search_server.py"
      ]
    }
  }
}
```

3. **Restart Windsurf**

### With Cursor or VS Code (Cline)

1. **Install the Cline extension** (for VS Code)

2. **Locate the config file:**
   - **VS Code**: `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`
   - **Cursor**: `%APPDATA%\Cursor\User\globalStorage\cursor-mcp\config.json`

3. **Add the server configuration** (same as above)

4. **Restart your editor**

## Example Usage

### Search in a Single File
```
Search for "import" in /path/to/file.py
```

### Search in a Directory
```
Find all occurrences of "TODO" in /path/to/project
```

### Case-Sensitive Search
```
Search for "API_KEY" (case-sensitive) in /path/to/config.py
```

### Search Specific File Types
```
Search for "function" in /path/to/project, only in .js files
```

## Supported File Types

When no file pattern is specified, the server searches these text file extensions:
- **Python**: .py
- **Web**: .html, .css, .js, .ts
- **Config**: .json, .yaml, .yml, .toml, .ini, .cfg, .conf
- **Documentation**: .txt, .md
- **Code**: .java, .cpp, .c, .h, .hpp, .rs, .go, .rb, .php, .sh
- **Data**: .xml

## Troubleshooting

### Server Not Connecting

1. **Verify Python installation:**
```bash
python --version
```

2. **Check FastMCP installation:**
```bash
pip show fastmcp
```

3. **Test server manually:**
```bash
python file_search_server.py
```

### Path Issues on Windows

- Use forward slashes: `C:/Users/name/file.py`
- Or escaped backslashes: `C:\\Users\\name\\file.py`
- Avoid spaces in file paths or use quotes

### Permission Errors

Ensure the server has read permissions for the files/directories you're searching.

## Development

### Project Structure
```
file-search-mcp-server/
├── file_search_server.py   # Main MCP server implementation
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── .gitignore             # Git ignore rules
```

### Running Tests

Use the MCP Inspector to test your server:
```bash
npx @modelcontextprotocol/inspector python file_search_server.py
```

## Technical Details

- **Protocol**: Model Context Protocol (MCP)
- **Transport**: stdio (standard input/output)
- **Framework**: FastMCP
- **Language**: Python 3.8+

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Created as part of an MCP server development assignment by Saqlain Ahmed P.

## Acknowledgments

- Built using [FastMCP](https://github.com/jlowin/fastmcp)
- Follows the [Model Context Protocol](https://modelcontextprotocol.io/) specification
