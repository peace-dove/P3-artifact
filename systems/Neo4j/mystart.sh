# finbench
# docker run \
#     --rm \
#     --publish=7474:7474 \
#     --publish=7687:7687 \
#     --detach \
#     --ulimit nofile=40000:40000 \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/data:/data:z \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/logs:/logs:z \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/import:/var/lib/neo4j/import:z \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/metrics:/var/lib/neo4j/metrics:z \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/plugins:/plugins:z \
#     --env NEO4J_PLUGINS='["graph-data-science"]' \
#     --env NEO4J_AUTH=none \
#     --name finbench-neo4j \
#     neo4j:2026.03.1


# wbench
# docker run \
#     --detach \
#     --name wikidata-neo4j \
#     --publish=7474:7474 \
#     --publish=7687:7687 \
#     --ulimit nofile=40000:40000 \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/data:/data:z \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/logs:/logs:z \
#     --volume=/data/dataset/pathmode:/var/lib/neo4j/import:z \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/plugins:/plugins:z \
#     --env NEO4J_PLUGINS='["graph-data-science"]' \
#     --env NEO4J_AUTH=none \
#     --env NEO4J_dbms_security_procedures_unrestricted="apoc.*" \
#     --env NEO4J_apoc_import_file_enabled=true \
#     --env NEO4J_apoc_export_file_enabled=true \
#     --env NEO4J_apoc_import_file_use__neo4j__config=true \
#     neo4j:2026.03.1

# pokec
# docker run \
#     --detach \
#     --name pokec-neo4j \
#     --publish=7474:7474 \
#     --publish=7687:7687 \
#     --ulimit nofile=40000:40000 \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/data:/data:z \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/logs:/logs:z \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/import:/var/lib/neo4j/import:z \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/plugins:/plugins:z \
#     --env NEO4J_PLUGINS='["graph-data-science"]' \
#     --env NEO4J_AUTH=none \
#     --env NEO4J_dbms_security_procedures_unrestricted="apoc.*" \
#     --env NEO4J_apoc_import_file_enabled=true \
#     --env NEO4J_apoc_export_file_enabled=true \
#     --env NEO4J_apoc_import_file_use__neo4j__config=true \
#     neo4j:2026.03.1


# Start pokec with neo4j:2026.03.1
# Mount custom configuration file
docker run \
    --detach \
    --name pokec-neo4j \
    --publish=7474:7474 \
    --publish=7687:7687 \
    --ulimit nofile=40000:40000 \
    --volume=/data/ldbc_finbench_transaction_impls/neo4j/conf:/var/lib/neo4j/conf:z \
    --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/data:/data:z \
    --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/logs:/logs:z \
    --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/import:/var/lib/neo4j/import:z \
    --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/plugins:/plugins:z \
    --env NEO4J_PLUGINS='["graph-data-science"]' \
    --env NEO4J_AUTH=none \
    --env NEO4J_dbms_security_procedures_unrestricted="apoc.*" \
    --env NEO4J_apoc_import_file_enabled=true \
    --env NEO4J_apoc_export_file_enabled=true \
    --env NEO4J_apoc_import_file_use__neo4j__config=true \
    neo4j:2026.03.1


# temporal
# docker run \
#     --detach \
#     --name temporal-neo4j \
#     --publish=7474:7474 \
#     --publish=7687:7687 \
#     --ulimit nofile=40000:40000 \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/data:/data:z \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/logs:/logs:z \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/import:/var/lib/neo4j/import:z \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/plugins:/plugins:z \
#     --env NEO4J_PLUGINS='["graph-data-science"]' \
#     --env NEO4J_AUTH=none \
#     --env NEO4J_dbms_security_procedures_unrestricted="apoc.*" \
#     --env NEO4J_apoc_import_file_enabled=true \
#     --env NEO4J_apoc_export_file_enabled=true \
#     --env NEO4J_apoc_import_file_use__neo4j__config=true \
#     neo4j:2026.03.1
