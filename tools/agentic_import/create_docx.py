#!/usr/bin/env python3
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_report():
    doc = docx.Document()
    
    # Title
    title = doc.add_heading('Data Commons MCP A/B Test Report', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    subtitle = doc.add_paragraph('Gemini 2.5 Pro vs Sarvam 30B')
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.runs[0].font.size = Pt(14)
    subtitle.runs[0].font.color.rgb = RGBColor(100, 100, 100)

    doc.add_paragraph()

    # Google Sheets Link Placeholder
    link_para = doc.add_paragraph()
    link_run = link_para.add_run('🔗 Google Sheets Raw Data Link: ')
    link_run.bold = True
    link_run.font.size = Pt(12)
    
    placeholder = link_para.add_run('[PASTE YOUR GOOGLE SHEET LINK HERE]')
    placeholder.italic = True
    placeholder.font.color.rgb = RGBColor(0, 0, 255) # Blue
    
    # Horizontal Line equivalent
    doc.add_paragraph("_" * 70)
    doc.add_paragraph()

    # Executive Summary
    doc.add_heading('Executive Summary', level=1)
    doc.add_paragraph(
        "This document provides a comprehensive comparison of how Gemini 2.5 Pro and Sarvam 30B handled "
        "Natural Language to Tool Call (NL2Tool) translation for the Data Commons MCP server across 15 advanced queries. "
        "The new queries pushed both LLMs to map complex concepts (like \"BRICS\", \"SDG 13\", \"Top 5 most populated cities\") "
        "into actionable API schemas."
    )
    
    p = doc.add_paragraph(style='List Bullet')
    p.add_run("Gemini 2.5 Pro").bold = True
    p.add_run(" demonstrated superior contextual awareness and entity resolution. It successfully unpacked acronyms (like BRICS) into the correct country names, resolved implicit geographic hierarchies, and attempted precise tool calls when users asked for structured data.")
    
    p = doc.add_paragraph(style='List Bullet')
    p.add_run("Sarvam 30B").bold = True
    p.add_run(" maintained a highly eager, search-first approach. It leans heavily on broad keyword searches. While this ensures it always returns some related metadata, it often fails to respect the user's specific formatting, structured intents, or geographic constraints.")

    # Detailed Breakdown
    doc.add_heading('Detailed Capability Breakdown', level=1)

    # Point 1
    doc.add_heading('1. Entity Unpacking & Regional Groupings (The "BRICS" Test)', level=2)
    doc.add_paragraph("Query: \"Give me the economic indicators of the BRICS countries...\"", style='Intense Quote')
    doc.add_paragraph("Gemini 2.5 Pro flawlessly unpacked the \"BRICS\" entity into its constituent countries and mapped them to the places array: [\"Brazil\", \"Russia\", \"India\", \"China\", \"South Africa\"]. Both models handled this successfully, proving strong baseline world knowledge.")

    # Point 2
    doc.add_heading('2. Handling Sustainable Development Goals (SDGs)', level=2)
    doc.add_paragraph("Query: \"Find all variables related to sustainable development goal 13 (Climate Action) and fetch the data for India.\"", style='Intense Quote')
    doc.add_paragraph("Both models acted perfectly, passing explicit SDG terminology directly to the Data Commons search index, which correctly returned the dc/topic/sdg_13 topics.")

    # Point 3
    doc.add_heading('3. Implicit Constraints and "Top N" Queries', level=2)
    doc.add_paragraph("Query: \"What is the ratio of female to male labor force participation in the top 5 most populated cities in Mexico?\"", style='Intense Quote')
    doc.add_paragraph("Gemini 2.5 Pro used its internal knowledge to resolve the implicit constraint. It correctly identified the top 5 cities and explicitly passed them into the tool call. Sarvam 30B ignored the geographic constraints entirely, passing no cities and causing a generic global search.")

    # Point 4
    doc.add_heading('4. Structured Data Intents (Tabular & CSV)', level=2)
    doc.add_paragraph("Query: \"I need to download a CSV format containing the historical agricultural GDP...\"", style='Intense Quote')
    doc.add_paragraph("Gemini 2.5 Pro recognized the precise data requirement and attempted to use get_observations to pull exact time series data. Sarvam 30B ignored the \"CSV\" and \"historical\" intents entirely, throwing the terms into a generic search.")

    # Point 5
    doc.add_heading('5. Multi-Variable Comparative Analysis', level=2)
    doc.add_paragraph("Query: \"Retrieve data on life expectancy at birth for both males and females in Canada.\"", style='Intense Quote')
    doc.add_paragraph("Gemini 2.5 Pro splintered the request into multiple specific tool calls to precisely fetch the male and female variants separately. Sarvam 30B simplified the query to broad keywords and relied on the MCP server to return all variants under a general topic umbrella.")

    # Conclusion
    doc.add_heading('Conclusion & Architectural Recommendations', level=1)
    
    p = doc.add_paragraph()
    p.add_run("Gemini 2.5 Pro is the clear winner for agentic tasks. ").bold = True
    p.add_run("Its ability to resolve implicit constraints (knowing which cities are in the top 5) and its attempt to adhere to format instructions makes it much more powerful.")
    
    p = doc.add_paragraph()
    p.add_run("Architectural Fix for MCP: ").bold = True
    p.add_run("To unlock flawless execution with Gemini, the MCP Server documentation or agent system prompt needs to explicitly instruct the LLM: ")
    p.add_run("\"Always use search_indicators to find the exact dcid BEFORE calling get_observations.\" ").italic = True
    p.add_run("This will prevent the LLM from guessing Data Commons IDs when attempting to fetch structured data.")

    # Save
    out_path = "Data_Commons_MCP_AB_Test_Report.docx"
    doc.save(out_path)
    print(f"Document saved to {out_path}")

if __name__ == "__main__":
    create_report()