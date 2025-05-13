from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Linux")
import subprocess

def run_command(command):
    try:
        result = subprocess.run(
            command, shell=True, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.stderr.strip()}")
        return None

@mcp.tool()
def execute_linux_command(command: str) -> str:
    """
    Executes linux command
    """
    ## VERY DANGEROUS!!!!!!
    # run the command and return the command's output
    return run_command(command)


mcp.run(transport="sse")