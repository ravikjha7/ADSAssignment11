import tkinter as tk
from neo4j import GraphDatabase

# Connect to the Neo4j database
uri = "neo4j://localhost:7687"
username = "neo4j"
password = "akshata2002"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Define a function to add a new paper node
def add_paper_node(node_id, subject, features):
    with driver.session() as session:
        session.run("CREATE (:Paper {id: $node_id, subject: $subject, features: $features})", 
                    node_id=node_id, subject=subject, features=features)

# Define a function to delete a paper node
def delete_paper_node(node_id):
    with driver.session() as session:
        session.run("MATCH (n:Paper {id: $node_id}) DETACH DELETE n", node_id=node_id)

# Define a function to update a paper node
def update_paper_node(node_id, subject, features):
    with driver.session() as session:
        session.run("MATCH (n:Paper {id: $node_id}) SET n.subject = $subject, n.features = $features", 
                    node_id=node_id, subject=subject, features=features)

# Define a function to view all paper nodes
def view_paper_nodes():
    with driver.session() as session:
        result = session.run("MATCH (n:Paper) RETURN n.id, n.subject, n.features")
        return [dict(record) for record in result]

# Define the GUI window and its components
root = tk.Tk()
root.title("Paper Database")

# Define the labels and text fields for the input form
node_id_label = tk.Label(root, text="Node ID:")
node_id_entry = tk.Entry(root)
subject_label = tk.Label(root, text="Subject:")
subject_entry = tk.Entry(root)
features_label = tk.Label(root, text="Features:")
features_entry = tk.Entry(root)

# Define the buttons for the CRUD operations
add_button = tk.Button(root, text="Add", command=lambda: add_paper_node(node_id_entry.get(), 
                                                                        subject_entry.get(), 
                                                                        features_entry.get()))
delete_button = tk.Button(root, text="Delete", command=lambda: delete_paper_node(node_id_entry.get()))
update_button = tk.Button(root, text="Update", command=lambda: update_paper_node(node_id_entry.get(), 
                                                                                    subject_entry.get(), 
                                                                                    features_entry.get()))
view_button = tk.Button(root, text="View", command=lambda: display_results(view_paper_nodes()))

# Define the text area for the query results
results_text = tk.Text(root, height=100, width=100)

# Define a function to display the query results in the text area
def display_results(results):
    results_text.delete(1.0, tk.END)
    for record in results:
        results_text.insert(tk.END, f"Node ID: {record['n.id']}\nSubject: {record['n.subject']}\nFeatures: {record['n.features']}\n\n")

# Pack the components into the GUI window
node_id_label.pack()
node_id_entry.pack()
subject_label.pack()
subject_entry.pack()
features_label.pack()
features_entry.pack()
add_button.pack(side=tk.LEFT)
delete_button.pack(side=tk.LEFT)
update_button.pack(side=tk.LEFT)
view_button.pack(side=tk.LEFT)
results_text.pack()

root.mainloop()
