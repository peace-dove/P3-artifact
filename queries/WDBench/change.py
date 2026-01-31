import re

def cypher_to_gql(query):
    # 1. Convert node type Entity to WDEntity
    query = re.sub(r':Entity', ':WDEntity', query)
    # 2. Add type to x1
    query = re.sub(r'\(x1([^\w:])', r'(x1:WDEntity\1', query)

    # 3. Variable-length relationships (including 0.., 1.., 0..1, 1..2, etc.)
    def rel_multi_replace(m):
        prop = m.group(1)
        rng = m.group(2).replace(' ', '')
        # Parse range
        if '..' in rng:
            n, *m_ = rng.strip('*').split('..')
            if m_ and m_[0] != '':
                rng_gql = f'{{{n},{m_[0]}}}'
            else:
                rng_gql = f'{{{n},}}'
        else:  # e.g., *2
            num = rng.strip('*')
            rng_gql = f'{{{num}}}'
        return f'-[e:WDRel WHERE e.prop = \'{prop}\']->{rng_gql}'
    # Process edges with hop counts first
    query = re.sub(r"-\[:(P\d+)\*(.*?)\]->", rel_multi_replace, query)

    # 4. Single-step relationships
    query = re.sub(
        r"-\[:(P\d+)\]->",
        lambda m: f"-[e:WDRel WHERE e.prop = '{m.group(1)}']->",
        query
    )

    return query

with open('cypher.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open('gql_query.txt', 'w', encoding='utf-8') as fout:
    for line in lines:
        # Skip empty lines
        if line.strip() == '':
            continue
        # Lines start with number and comma like '1,MATCH ...', skip the number
        fout.write(cypher_to_gql(line.split(',')[1].strip()) + '\n')
