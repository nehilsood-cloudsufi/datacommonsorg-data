#!/usr/bin/env python3
import re

def parse_and_convert():
    input_file = "mcp_ab_test_results.md"
    output_file = "mcp_ab_test_results_tabular.md"
    
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # We will extract queries and tool executions.
    # The file has sections starting with "## QUERY: "
    
    queries_data = []
    
    # Split by "## QUERY:"
    parts = content.split("## QUERY: ")
    
    header_and_intro = parts[0]
    
    for part in parts[1:]:
        # Find where the next analysis section starts, if any
        if "# Phase 2: Advanced Capabilities A/B Test" in part:
            query_part, analysis_part = part.split("# Phase 2: Advanced Capabilities A/B Test", 1)
            analysis_part = "# Phase 2: Advanced Capabilities A/B Test" + analysis_part
        elif "# Data Commons MCP A/B Test: Gemini vs Sarvam 30B - Analysis Summary" in part:
            query_part, analysis_part = part.split("# Data Commons MCP A/B Test: Gemini vs Sarvam 30B - Analysis Summary", 1)
            analysis_part = "# Data Commons MCP A/B Test: Gemini vs Sarvam 30B - Analysis Summary" + analysis_part
        else:
            query_part = part
            analysis_part = ""
            
        lines = query_part.strip().split("\n")
        query = lines[0].strip()
        
        gemini_calls = []
        sarvam_calls = []
        
        current_phase = None
        
        for line in lines:
            if "Phase 1: Gemini Translation" in line:
                current_phase = "gemini"
            elif "Phase 2: Sarvam 30B Translation" in line:
                current_phase = "sarvam"
                
            # Match execution line: **Executing `tool_name`** with args: `{...}`...
            exec_match = re.search(r"\*\*Executing `([^`]+)`\*\* with args: `([^`]+)`", line)
            if exec_match:
                tool_name = exec_match.group(1)
                args = exec_match.group(2)
                # clean up long args slightly for table formatting
                if len(args) > 150:
                    args = args[:147] + "..."
                call_str = f"**{tool_name}**<br>`{args}`"
                
                if current_phase == "gemini":
                    gemini_calls.append(call_str)
                elif current_phase == "sarvam":
                    sarvam_calls.append(call_str)
            
            # Match No Tool Call
            no_call_match = re.search(r"\*\*([^\*]+ Response \(No Tool Call\)):\*\* (.*)", line)
            if no_call_match:
                call_str = f"*No Tool Call*<br>_{no_call_match.group(2)[:100]}..._"
                if current_phase == "gemini":
                    gemini_calls.append(call_str)
                elif current_phase == "sarvam":
                    sarvam_calls.append(call_str)
                    
        queries_data.append({
            "query": query,
            "gemini": "<br><br>".join(gemini_calls) if gemini_calls else "*(Error / No Output)*",
            "sarvam": "<br><br>".join(sarvam_calls) if sarvam_calls else "*(Error / No Output)*",
            "analysis_part": analysis_part
        })

    # Generate Markdown Table
    out_lines = []
    out_lines.append("# Data Commons MCP A/B Test Results (Tabular Format)\n")
    out_lines.append("This document provides a side-by-side comparison of the NL2Tool translation capabilities of Gemini 2.5 Pro and Sarvam 30B against the Data Commons MCP server.\n")
    
    out_lines.append("| Query | Gemini 2.5 Pro (Tool Calls) | Sarvam 30B (Tool Calls) |")
    out_lines.append("|---|---|---|")
    
    for qd in queries_data:
        # Escape pipes in content
        query_safe = qd['query'].replace('|', '&#124;')
        gemini_safe = qd['gemini'].replace('|', '&#124;')
        sarvam_safe = qd['sarvam'].replace('|', '&#124;')
        out_lines.append(f"| **{query_safe}** | {gemini_safe} | {sarvam_safe} |")
        
    out_lines.append("\n--- \n")
    
    # Append the last analysis part found
    for qd in queries_data:
        if qd['analysis_part']:
            out_lines.append(qd['analysis_part'])
            
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))
        
    print(f"Successfully converted to {output_file}")

if __name__ == "__main__":
    parse_and_convert()