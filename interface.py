from neo4j import GraphDatabase

class Interface:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        self._driver.verify_connectivity()

    def close(self):
        self._driver.close()

    def bfs(self, start_node, last_node):
        """
        Perform Breadth-First Search (BFS) from start_node to last_node.
        Ensures that the BFS graph is created properly before running the query.
        """ 

        with self._driver.session() as session:
            try:
                graph_exists_query = "CALL gds.graph.exists('bfs_graph') YIELD exists RETURN exists"
                result = session.run(graph_exists_query).single()
                if result and result["exists"]:
                    session.run("CALL gds.graph.drop('bfs_graph') YIELD graphName")

                create_graph_query = """
                CALL gds.graph.project(
                    'bfs_graph',
                    ['Location'],
                    {
                        TRIP: {
                            orientation: 'NATURAL'
                        }
                    }
                )
                """
                session.run(create_graph_query)

                bfs_query = """
                MATCH (source:Location {name: $start_node}), (target:Location {name: $last_node})
                WITH source, [target] AS targetNodes
                CALL gds.bfs.stream('bfs_graph', {
                    sourceNode: source,
                    targetNodes: targetNodes
                })
                YIELD path
                RETURN [node IN nodes(path) | {name: node.name}] AS path
                """
                result = session.run(bfs_query, start_node=start_node, last_node=last_node)
                return result.data()

            except Exception as e:
                print("BFS execution error:", e)
                return None
    

    def pagerank(self, max_iterations, weight_property):
        """
        Runs the PageRank algorithm on the projected graph and returns nodes with max and min PageRank.

        Args:
            max_iterations (int): Maximum number of iterations for the PageRank algorithm.
            weight_property (str): The relationship property used for weighting.

        Returns:
            List[Dict]: A list containing two dictionaries:
                - First dictionary: {'name': <max_page_name>, 'score': <max_score>}
                - Second dictionary: {'name': <min_page_name>, 'score': <min_score>}
        """
        with self._driver.session() as session:
            try:
                exists_query = """
                CALL gds.graph.exists('pagerank_graph')
                YIELD exists
                RETURN exists
                """
                result = session.run(exists_query).single()

                if result and result["exists"]:
                    session.run("CALL gds.graph.drop('pagerank_graph') YIELD graphName")

                session.run("""
                    CALL gds.graph.project(
                        'pagerank_graph',
                        ['Location'],
                        {
                            TRIP: {
                                properties: [$weight_property],
                                orientation: 'NATURAL'
                            }
                        }
                    )
                """, weight_property=weight_property)

                result = session.run("""
                    CALL gds.pageRank.stream('pagerank_graph', {
                        maxIterations: $max_iterations,
                        relationshipWeightProperty: $weight_property
                    })
                    YIELD nodeId, score
                    RETURN gds.util.asNode(nodeId).name AS name, score
                    ORDER BY score DESC
                """, max_iterations=max_iterations, weight_property=weight_property)

                nodes = [record for record in result]

                if len(nodes) >= 2:
                    return [nodes[0], nodes[-1]]
                elif len(nodes) == 1:
                    return [nodes[0], nodes[0]]
                else:
                    return None

            except Exception as e:
                print("PageRank execution error:", e)
                return None