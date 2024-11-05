import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Initialize the graph
if 'graph' not in st.session_state:
    st.session_state.graph = nx.Graph()
if 'positions' not in st.session_state:
    st.session_state.positions = {}
if 'saved_graphs' not in st.session_state:
    st.session_state.saved_graphs = {}

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        color: #1E88E5;
        text-align: center;
        padding: 1rem;
        margin-bottom: 2rem;
    }
    .section-header {
        color: #333;
        padding: 0.5rem 0;
        border-bottom: 2px solid #1E88E5;
        margin: 1.5rem 0;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .stButton > button {
        width: 100%;
    }
    .decorative-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 200px;
        height: 100%;
        opacity: 0.1;
        z-index: -1;
        background: linear-gradient(45deg, #1E88E5 25%, transparent 25%),
                  linear-gradient(-45deg, #1E88E5 25%, transparent 25%),
                  linear-gradient(45deg, transparent 75%, #1E88E5 75%),
                  linear-gradient(-45deg, transparent 75%, #1E88E5 75%);
        background-size: 20px 20px;
    }
    .decorative-bg-right {
        position: fixed;
        top: 0;
        right: 0;
        width: 200px;
        height: 100%;
        opacity: 0.1;
        z-index: -1;
        background: linear-gradient(45deg, #1E88E5 25%, transparent 25%),
                  linear-gradient(-45deg, #1E88E5 25%, transparent 25%),
                  linear-gradient(45deg, transparent 75%, #1E88E5 75%),
                  linear-gradient(-45deg, transparent 75%, #1E88E5 75%);
        background-size: 20px 20px;
    }
    .algorithm-step {
        display: flex;
        align-items: center;
        margin: 0.5rem 0;
        padding: 0.5rem;
        background: white;
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .step-number {
        background: #1E88E5;
        color: white;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1rem;
    }
    .side-info {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #1E88E5;
    }
</style>
""", unsafe_allow_html=True)

# Add decorative backgrounds
st.markdown("""
    <div class="decorative-bg"></div>
    <div class="decorative-bg-right"></div>
""", unsafe_allow_html=True)

# Function to draw the graph
def draw_graph(path=None):
    plt.figure(figsize=(10, 8))
    pos = st.session_state.positions
    nx.draw(st.session_state.graph, pos, with_labels=True, 
            node_size=700, 
            node_color='lightblue',
            font_size=10,
            font_weight='bold')

    edge_labels = nx.get_edge_attributes(st.session_state.graph, 'weight')
    nx.draw_networkx_edge_labels(st.session_state.graph, pos, edge_labels=edge_labels)

    if path:
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(st.session_state.graph, pos, edgelist=path_edges, 
                             edge_color='orange', width=2)
        if len(path_edges) > 0:
            nx.draw_networkx_edges(st.session_state.graph, pos, 
                                 edgelist=[path_edges[-1]], 
                                 edge_color='red', width=3)

    plt.xlim(-1, 11)
    plt.ylim(-1, 11)
    plt.grid(True, linestyle='--', alpha=0.7)
    border = patches.Rectangle((-1, -1), 12, 12, linewidth=2, 
                             edgecolor='black', facecolor='none')
    plt.gca().add_patch(border)
    st.pyplot(plt)
    plt.close()

# Function to save the current graph
def save_graph(graph_name):
    graph_data = {
        'nodes': list(st.session_state.graph.nodes),
        'edges': [(u, v, d['weight']) for u, v, d in st.session_state.graph.edges(data=True)],
        'positions': {node: st.session_state.positions[node] for node in st.session_state.graph.nodes}
    }
    st.session_state.saved_graphs[graph_name] = graph_data
    st.success(f"✅ Graph '{graph_name}' saved successfully!")

# Function to load a saved graph
def load_graph(graph_name):
    if graph_name in st.session_state.saved_graphs:
        graph_data = st.session_state.saved_graphs[graph_name]
        st.session_state.graph.clear()
        st.session_state.positions.clear()
        
        for node in graph_data['nodes']:
            st.session_state.graph.add_node(node)
            st.session_state.positions[node] = graph_data['positions'].get(node, (0, 0))
        
        for u, v, weight in graph_data['edges']:
            st.session_state.graph.add_edge(u, v, weight=weight)
        
        st.success(f"✅ Graph '{graph_name}' loaded successfully!")
    else:
        st.error(f"❌ Graph '{graph_name}' does not exist.")

# Create tabs
tabs = st.tabs(["🏠 Home", "ℹ️ About"])

with tabs[0]:
    st.markdown('<h1 class="main-header">Dijkstra\'s Algorithm Visualization</h1>', 
                unsafe_allow_html=True)

    # Create three-column layout
    left_col, main_col, right_col = st.columns([1, 2, 1])

    with left_col:
        st.markdown("""
        <div class="side-info">
            <h4>Algorithm Steps</h4>
            <div class="algorithm-step">
                <div class="step-number">1</div>
                <div>Initialize distances</div>
            </div>
            <div class="algorithm-step">
                <div class="step-number">2</div>
                <div>Select minimum</div>
            </div>
            <div class="algorithm-step">
                <div class="step-number">3</div>
                <div>Update neighbors</div>
            </div>
            <div class="algorithm-step">
                <div class="step-number">4</div>
                <div>Repeat until done</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with main_col:
        # Node creation section
        st.markdown('<h3 class="section-header">Add Node</h3>', 
                   unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            x_coord = st.number_input("X Coordinate", min_value=0, max_value=10, value=0)
        with col2:
            y_coord = st.number_input("Y Coordinate", min_value=0, max_value=10, value=0)
        
        if st.button("➕ Add Node"):
            new_node = f"Node {len(st.session_state.graph.nodes) + 1}"
            st.session_state.graph.add_node(new_node)
            st.session_state.positions[new_node] = (x_coord, y_coord)
            st.success(f"✅ {new_node} added at ({x_coord}, {y_coord})")

        # Edge creation section
        st.markdown('<h3 class="section-header">Create Edge</h3>', 
                   unsafe_allow_html=True)
        if len(st.session_state.graph.nodes) >= 2:
            col1, col2, col3 = st.columns(3)
            with col1:
                node1 = st.selectbox("From Node", list(st.session_state.graph.nodes))
            with col2:
                node2 = st.selectbox("To Node", 
                                   [n for n in st.session_state.graph.nodes if n != node1])
            with col3:
                edge_cost = st.number_input("Cost", min_value=1, value=1)
            
            if st.button("🔗 Add Edge"):
                st.session_state.graph.add_edge(node1, node2, weight=edge_cost)
                st.success(f"✅ Edge added: {node1} ↔ {node2} (cost: {edge_cost})")
        else:
            st.info("ℹ️ Add at least two nodes to create edges.")

        # Path finding section
        st.markdown('<h3 class="section-header">Find Shortest Path</h3>', 
                   unsafe_allow_html=True)
        if len(st.session_state.graph.nodes) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                start_node = st.selectbox("Start From", list(st.session_state.graph.nodes))
            with col2:
                end_node = st.selectbox("Go To", 
                                      [n for n in st.session_state.graph.nodes if n != start_node])
            
            if st.button("🎯 Find Path"):
                try:
                    path = nx.dijkstra_path(st.session_state.graph, start_node, end_node)
                    total_cost = sum(st.session_state.graph[u][v]['weight'] 
                                   for u, v in zip(path[:-1], path[1:]))
                    st.success(f"✅ Shortest path: {' → '.join(path)}")
                    st.success(f"💰 Total cost: {total_cost}")
                    draw_graph(path)
                except nx.NetworkXNoPath:
                    st.error("❌ No path exists between selected nodes!")
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")

        # Graph visualization
        st.markdown('<h3 class="section-header">Graph Visualization</h3>', 
                    unsafe_allow_html=True)
        draw_graph()

    with right_col:
        st.markdown("""
        <div class="side-info">
            <h4>Graph Statistics</h4>
            <ul>
                <li>Nodes: {}</li>
                <li>Edges: {}</li>
            </ul>
        </div>
        <div class="side-info">
            <h4>Did you know?</h4>
            <p>Dijkstra's algorithm is used in:</p>
            <ul>
                <li>GPS Navigation</li>
                <li>Social Networks</li>
                <li>Internet Routing</li>
                <li>Games Pathfinding</li>
            </ul>
        </div>
        """.format(len(st.session_state.graph.nodes), 
                  len(st.session_state.graph.edges)), 
        unsafe_allow_html=True)

    # Save/Load section at the bottom
    st.markdown('<h3 class="section-header">Save & Load Graphs</h3>', 
                unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        graph_name = st.text_input("Enter Graph Name")
        if st.button("💾 Save Graph"):
            if graph_name:
                save_graph(graph_name)
            else:
                st.error("❌ Please enter a graph name.")

    with col2:
        if st.session_state.saved_graphs:
            selected_graph = st.selectbox("Select Saved Graph", 
                                        list(st.session_state.saved_graphs.keys()))
            if st.button("📂 Load Graph"):
                load_graph(selected_graph)
        else:
            st.info("ℹ️ No saved graphs available")

with tabs[1]:
    st.markdown('<h2 class="main-header">About Dijkstra\'s Algorithm</h2>', 
                unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("dijkstra.webp", caption="Edsger W. Dijkstra", use_column_width=True)
        
        st.markdown("""
        <div class="side-info">
            <h4>Timeline</h4>
            <ul>
                <li>1956: Algorithm conceived</li>
                <li>1959: First published</li>
                <li>1960s: Widely adopted</li>
                <li>Present: Essential in computing</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>Overview</h4>
            <p>Dijkstra's algorithm is a fundamental graph algorithm that finds the shortest 
            paths between nodes in a graph.</p>
            
            <h4>Key Features</h4>
            • Optimal pathfinding<br>
            • Efficient computation<br>
            • Versatile applications<br>
            • Industry standard<br>
            
            <h4>Real-world Applications</h4>
            • Network routing protocols<br>
            • GPS and navigation systems<br>
            • Social networks<br>
            • Video game pathfinding<br>
            • Supply chain optimization
        </div>
        
        <div class="side-info">
            <h4>How it Works</h4>
            <p>The algorithm maintains a set of unvisited nodes and continuously updates 
            the shortest known distance to each node until it finds the optimal path.</p>
        </div>
        """, unsafe_allow_html=True)