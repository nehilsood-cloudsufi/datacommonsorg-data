#!/usr/bin/env python3
import asyncio
import os
import json
import csv
from datetime import datetime
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AsyncOpenAI

async def execute_and_return_tools(session, tool_calls):
    """Executes tool calls and returns formatted strings for the CSV."""
    if not tool_calls:
        return "", ""

    calls_out = []
    resp_out = []
    
    for call in tool_calls:
        tool_name = call.function.name
        tool_args = json.loads(call.function.arguments)
        
        calls_out.append(f"{tool_name}:\n{json.dumps(tool_args, indent=2)}")
        
        try:
            result = await session.call_tool(tool_name, tool_args)
            for content in result.content:
                if hasattr(content, 'text'):
                    resp_out.append(content.text)
                else:
                    resp_out.append(str(content))
        except Exception as e:
            resp_out.append(f"Error executing {tool_name}: {e}")
            
    return "\n\n".join(calls_out), "\n\n".join(resp_out)

async def main():
    csv_file_path = "mcp_ab_test_results.csv"
    
    # Setup OpenAI clients
    gemini_key = os.environ.get("GEMINI_API_KEY")
    sarvam_key = os.environ.get("SARVAM_API_KEY")
    
    if not gemini_key or not sarvam_key:
        print("Please set both GEMINI_API_KEY and SARVAM_API_KEY environment variables.")
        return

    gemini_client = AsyncOpenAI(api_key=gemini_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    sarvam_client = AsyncOpenAI(api_key=sarvam_key, base_url="https://api.sarvam.ai/v1")
    
    server_params = StdioServerParameters(
        command="datacommons-mcp",
        args=["serve", "--skip-api-key-validation", "stdio"],
        env=os.environ.copy()
    )

    queries = [
        "What is the total population and median age of Japan?",
        "Fetch the Gini index for income inequality in South Africa.",
        "What are the primary economic indicators available for Brazil?",
        "Get the latest observations for the unemployment rate in California.",
        "Retrieve data on life expectancy at birth for both males and females in Canada.",
        "Give me the economic indicators of the BRICS countries (Brazil, Russia, India, China, South Africa).",
        "Compare the annual greenhouse gas emissions of the United States and China over the last 5 years.",
        "I need a tabular comparison of the poverty rate and GDP per capita for all counties in Texas.",
        "What statistical variables do you have related to renewable energy consumption in Europe?",
        "Retrieve the time series data for the number of public elementary schools in New York City.",
        "Search for indicators related to heart disease prevalence and compare the latest data between Florida and New York.",
        "Find all variables related to sustainable development goal 13 (Climate Action) and fetch the data for India.",
        "Give me a detailed breakdown of the population by age group (0-14, 15-64, 65+) for Germany.",
        "I need to download a CSV format containing the historical agricultural GDP and total arable land area of Australia.",
        "What is the ratio of female to male labor force participation in the top 5 most populated cities in Mexico?"
    ]

    print("Connecting to Data Commons MCP server...")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            mcp_tools_response = await session.list_tools()
            openai_tools = []
            for tool in mcp_tools_response.tools:
                openai_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                })
            
            print(f"Extracted {len(openai_tools)} tools.")
            print(f"Starting A/B test and writing to {csv_file_path}...")

            with open(csv_file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                # Write Header
                writer.writerow([
                    "Query", 
                    "Gemini Tool Calls", 
                    "Gemini MCP Response", 
                    "Sarvam Tool Calls", 
                    "Sarvam MCP Response"
                ])
                
                for i, query in enumerate(queries, 1):
                    print(f"Processing query {i}/{len(queries)}: {query}")
                    row = [query, "", "", "", ""]
                    
                    # --- Gemini Phase ---
                    try:
                        gemini_resp = await gemini_client.chat.completions.create(
                            model="gemini-2.5-pro",
                            messages=[{"role": "user", "content": query}],
                            tools=openai_tools,
                            tool_choice="auto"
                        )
                        gemini_calls = gemini_resp.choices[0].message.tool_calls
                        if gemini_calls:
                            calls_str, resp_str = await execute_and_return_tools(session, gemini_calls)
                            row[1] = calls_str
                            row[2] = resp_str
                        else:
                            row[1] = "No Tool Call"
                            row[2] = gemini_resp.choices[0].message.content
                    except Exception as e:
                        row[1] = "Error"
                        row[2] = str(e)

                    # --- Sarvam Phase ---
                    try:
                        sarvam_resp = await sarvam_client.chat.completions.create(
                            model="sarvam-30b",
                            messages=[{"role": "user", "content": query}],
                            tools=openai_tools,
                            tool_choice="auto"
                        )
                        sarvam_calls = sarvam_resp.choices[0].message.tool_calls
                        if sarvam_calls:
                            calls_str, resp_str = await execute_and_return_tools(session, sarvam_calls)
                            row[3] = calls_str
                            row[4] = resp_str
                        else:
                            row[3] = "No Tool Call"
                            row[4] = sarvam_resp.choices[0].message.content
                    except Exception as e:
                        row[3] = "Error"
                        row[4] = str(e)

                    writer.writerow(row)
                    f.flush() # Ensure it writes to disk immediately per query
                    
    print(f"\nDone! Results with full MCP data saved to {csv_file_path}")

if __name__ == "__main__":
    asyncio.run(main())