import streamlit as st
import pandas as pd
import json
import os
from pathlib import Path
from typing import List, Dict, Set, Tuple
import html

# Page configuration
st.set_page_config(
    page_title="HR Analytics Fabric Catalog",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling for better UX
st.markdown("""
    <style>
    .pattern-header {
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-row {
        display: flex;
        gap: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_data
def load_patterns() -> List[Dict]:
    """Load patterns from JSON file."""
    json_path = Path(__file__).parent.parent / "patterns.json"
    with open(json_path, 'r') as f:
        return json.load(f)


def get_unique_domains(patterns: List[Dict]) -> List[str]:
    """Extract unique domain names from patterns."""
    domains = set()
    for pattern in patterns:
        if "domain" in pattern:
            domains.add(pattern["domain"])
    return sorted(list(domains))


def get_complexity_counts(patterns: List[Dict], filtered_patterns: List[Dict]) -> Dict[str, int]:
    """Count patterns by complexity level."""
    complexity_map = {"Low": 0, "Medium": 0, "High": 0}
    for pattern in filtered_patterns:
        complexity = pattern.get("complexity", "Unknown")
        if complexity in complexity_map:
            complexity_map[complexity] += 1
    return complexity_map


def filter_patterns(
    patterns: List[Dict],
    search_query: str,
    selected_domains: List[str],
    complexity_filter: str,
    maturity_filter: str
) -> List[Dict]:
    """Apply filters to patterns."""
    filtered = patterns

    # Search filter
    if search_query:
        search_lower = search_query.lower()
        filtered = [
            p for p in filtered
            if search_lower in p.get("name", "").lower()
            or search_lower in p.get("description", "").lower()
            or search_lower in p.get("summary", "").lower()
        ]

    # Domain filter
    if selected_domains:
        filtered = [p for p in filtered if p.get("domain") in selected_domains]

    # Complexity filter
    if complexity_filter != "All":
        filtered = [p for p in filtered if p.get("complexity") == complexity_filter]

    # Maturity filter
    if maturity_filter != "All":
        filtered = [p for p in filtered if p.get("maturity") == maturity_filter]

    return filtered


def get_pattern_by_id(patterns: List[Dict], pattern_id: str) -> Dict:
    """Get a single pattern by ID."""
    for pattern in patterns:
        if pattern.get("id") == pattern_id:
            return pattern
    return None


def get_compatible_patterns(
    selected_ids: List[str],
    all_patterns: List[Dict]
) -> Tuple[Set[str], Set[str], Set[str]]:
    """
    Determine compatible pairings, missing prerequisites, and incompatibilities.

    Returns:
        Tuple of (compatible_pairs, missing_prerequisites, incompatibilities)
    """
    compatible_pairs = set()
    missing_prerequisites = set()
    incompatibilities = set()
    pattern_map = {p["id"]: p for p in all_patterns}

    # Check prerequisites
    for pattern_id in selected_ids:
        pattern = pattern_map.get(pattern_id)
        if pattern:
            for prereq_id in pattern.get("prerequisites", []):
                if prereq_id not in selected_ids:
                    missing_prerequisites.add(f"{pattern.get('name')} requires {pattern_map.get(prereq_id, {}).get('name', prereq_id)}")

    # Check compatibilities
    for i, pattern_id1 in enumerate(selected_ids):
        pattern1 = pattern_map.get(pattern_id1)
        if not pattern1:
            continue

        for pattern_id2 in selected_ids[i+1:]:
            pattern2 = pattern_map.get(pattern_id2)
            if not pattern2:
                continue

            # Check if incompatible
            if pattern_id2 in pattern1.get("incompatibleWith", []):
                incompatibilities.add(f"{pattern1.get('name')} is incompatible with {pattern2.get('name')}")
            elif pattern_id2 in pattern1.get("compatibleWith", []):
                compatible_pairs.add(f"{pattern1.get('name')} ↔ {pattern2.get('name')}")

    return compatible_pairs, missing_prerequisites, incompatibilities


def generate_stack_json(selected_patterns: List[Dict]) -> str:
    """Generate JSON export of selected patterns."""
    stack = {
        "patterns": selected_patterns,
        "count": len(selected_patterns),
        "components": list(set(
            comp for pattern in selected_patterns
            for comp in pattern.get("fabricComponents", [])
        ))
    }
    return json.dumps(stack, indent=2)


def generate_html_export(selected_patterns: List[Dict]) -> str:
    """Generate HTML export of selected patterns."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>HR Analytics Fabric Catalog Export</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; color: #333; }
            h1 { color: #1f77b4; }
            .pattern { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
            .pattern h2 { color: #1f77b4; margin-top: 0; }
            .metadata { color: #666; font-size: 0.9em; }
            .section { margin: 10px 0; }
            .section-title { font-weight: bold; color: #1f77b4; }
            ul { margin: 5px 0; padding-left: 20px; }
            li { margin: 3px 0; }
        </style>
    </head>
    <body>
        <h1>HR Analytics Fabric Catalog</h1>
        <p>Generated Stack: {count} patterns selected</p>
    """.format(count=len(selected_patterns))

    for pattern in selected_patterns:
        html_content += f"""
        <div class="pattern">
            <h2>{html.escape(pattern.get('name', 'Unknown'))}</h2>
            <div class="metadata">
                <p><strong>Domain:</strong> {html.escape(pattern.get('domain', 'N/A'))}</p>
                <p><strong>Complexity:</strong> {html.escape(pattern.get('complexity', 'N/A'))} |
                   <strong>Maturity:</strong> {html.escape(pattern.get('maturity', 'N/A'))}</p>
            </div>
            <div class="section">
                <div class="section-title">Description</div>
                <p>{html.escape(pattern.get('description', 'N/A'))}</p>
            </div>
            <div class="section">
                <div class="section-title">Fabric Components</div>
                <ul>
        """
        for component in pattern.get("fabricComponents", []):
            html_content += f"<li>{html.escape(component)}</li>"

        html_content += """
                </ul>
            </div>
        </div>
        """

    html_content += """
    </body>
    </html>
    """
    return html_content


def render_pattern_expander(pattern: Dict, all_patterns: List[Dict]):
    """Render a single pattern as an expander."""
    with st.expander(f"📋 {pattern.get('name', 'Unknown Pattern')}", expanded=False):
        # Description
        st.markdown("### Description")
        st.write(pattern.get("description", "No description available"))

        # Pros and Cons in columns
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### ✅ Pros")
            for pro in pattern.get("pros", []):
                st.write(f"• {pro}")

        with col2:
            st.markdown("#### ❌ Cons")
            for con in pattern.get("cons", []):
                st.write(f"• {con}")

        # Governance considerations
        st.info(f"**🔒 Governance:** {pattern.get('governanceConsiderations', 'No governance guidelines provided')}")

        # Use cases
        st.markdown("#### 🎯 People Analytics Use Cases")
        for use_case in pattern.get("peopleAnalyticsUseCases", []):
            st.write(f"• {use_case}")

        # Additional metadata
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Complexity", pattern.get("complexity", "N/A"))
        with col2:
            st.metric("Maturity", pattern.get("maturity", "N/A"))
        with col3:
            st.metric("Effort", pattern.get("estimatedImplementationEffort", "N/A"))
        with col4:
            st.metric("Cost", pattern.get("costImplications", "N/A")[:20] + "..." if pattern.get("costImplications") else "N/A")

        # Reference links
        if pattern.get("referenceLinks"):
            st.markdown("#### 📚 References")
            for link in pattern.get("referenceLinks", []):
                st.markdown(f"- [{link.get('label', 'Link')}]({link.get('url', '#')})")


def main():
    # Load data
    patterns = load_patterns()

    st.title("📊 HR Analytics Fabric Catalog")
    st.markdown("Discover and explore best practices, patterns, and architectural approaches for building analytics solutions in Microsoft Fabric.")

    # Sidebar filters
    st.sidebar.markdown("### Filters")

    search_query = st.sidebar.text_input(
        "Search patterns",
        placeholder="Enter keywords...",
        help="Search by pattern name, description, or summary"
    )

    available_domains = get_unique_domains(patterns)
    selected_domains = st.sidebar.multiselect(
        "Filter by Domain",
        options=available_domains,
        help="Select one or more domains to filter patterns"
    )

    complexity_filter = st.sidebar.radio(
        "Complexity Level",
        options=["All", "Low", "Medium", "High"],
        help="Filter patterns by implementation complexity"
    )

    maturity_filter = st.sidebar.radio(
        "Maturity",
        options=["All", "Preview", "GA"],
        help="Filter patterns by release maturity"
    )

    # Apply filters
    filtered_patterns = filter_patterns(
        patterns,
        search_query,
        selected_domains,
        complexity_filter,
        maturity_filter
    )

    # Main content tabs
    tab1, tab2 = st.tabs(["Browse Catalog", "Pattern Builder"])

    # ================== TAB 1: BROWSE CATALOG ==================
    with tab1:
        st.markdown("## Catalog Overview")

        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Patterns", len(filtered_patterns))

        complexity_counts = get_complexity_counts(patterns, filtered_patterns)
        with col2:
            st.metric("Low Complexity", complexity_counts["Low"])
        with col3:
            st.metric("Medium Complexity", complexity_counts["Medium"])
        with col4:
            st.metric("High Complexity", complexity_counts["High"])

        st.divider()

        # Pattern list
        if filtered_patterns:
            st.markdown(f"### Showing {len(filtered_patterns)} pattern(s)")
            for pattern in filtered_patterns:
                render_pattern_expander(pattern, patterns)
        else:
            st.warning("No patterns match your filters. Try adjusting your search criteria.")

    # ================== TAB 2: PATTERN BUILDER ==================
    with tab2:
        st.markdown("## Build Your Architecture Stack")
        st.write("Select multiple patterns to create your custom architecture. The builder will identify compatible combinations and missing prerequisites.")

        # Pattern selection
        pattern_names = {p["id"]: p["name"] for p in patterns}
        selected_pattern_names = st.multiselect(
            "Select Patterns",
            options=[p["name"] for p in patterns],
            help="Choose patterns to include in your architecture"
        )

        if selected_pattern_names:
            # Map names back to IDs
            selected_pattern_ids = [
                p["id"] for p in patterns
                if p["name"] in selected_pattern_names
            ]
            selected_patterns = [
                p for p in patterns
                if p["id"] in selected_pattern_ids
            ]

            # Analyze compatibility
            compatible_pairs, missing_prerequisites, incompatibilities = get_compatible_patterns(
                selected_pattern_ids,
                patterns
            )

            # Display compatibility analysis
            st.markdown("### 📋 Compatibility Analysis")

            # Compatible pairings
            if compatible_pairs:
                with st.success(f"✅ Compatible Pairings ({len(compatible_pairs)})"):
                    for pairing in sorted(compatible_pairs):
                        st.write(f"• {pairing}")
            else:
                st.info("No direct compatible pairings found, but patterns may still work together.")

            # Missing prerequisites
            if missing_prerequisites:
                with st.warning(f"⚠️ Missing Prerequisites ({len(missing_prerequisites)})"):
                    for prereq in sorted(missing_prerequisites):
                        st.write(f"• {prereq}")

            # Incompatibilities
            if incompatibilities:
                with st.error(f"❌ Incompatibilities Detected ({len(incompatibilities)})"):
                    for incomp in sorted(incompatibilities):
                        st.write(f"• {incomp}")

            st.divider()

            # Architecture narrative
            st.markdown("### 🏗️ Architecture Narrative")
            narrative = f"""
            Your selected stack consists of **{len(selected_patterns)}** patterns:

            {', '.join([f"**{p.get('name')}**" for p in selected_patterns])}

            **Fabric Components:** {', '.join(sorted(set(
                comp for p in selected_patterns
                for comp in p.get('fabricComponents', [])
            )))}

            **Total Implementation Effort:** {', '.join(set(p.get('estimatedImplementationEffort', 'N/A') for p in selected_patterns))}

            This combination provides a comprehensive approach to building your HR analytics solution,
            covering data organization, transformation, and reporting capabilities across the selected patterns.
            """
            st.write(narrative)

            st.divider()

            # Export buttons
            st.markdown("### 📥 Export Stack")

            col1, col2 = st.columns(2)

            with col1:
                json_export = generate_stack_json(selected_patterns)
                st.download_button(
                    label="📄 Download as JSON",
                    data=json_export,
                    file_name="fabric_architecture_stack.json",
                    mime="application/json",
                    help="Export selected patterns as JSON for documentation"
                )

            with col2:
                html_export = generate_html_export(selected_patterns)
                st.download_button(
                    label="🌐 Download as HTML",
                    data=html_export,
                    file_name="fabric_architecture_stack.html",
                    mime="text/html",
                    help="Export selected patterns as a formatted HTML document"
                )

        else:
            st.info("👆 Select one or more patterns above to get started building your architecture stack.")


if __name__ == "__main__":
    main()
