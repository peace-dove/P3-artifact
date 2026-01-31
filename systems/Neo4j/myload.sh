# load data once

docker stop finbench-neo4j
docker stop wikidata-neo4j
docker stop pokec-neo4j
docker rm pokec-neo4j

rm -rf /data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/data/*

# docker run \
#     --rm \
#     --publish=7474:7474 \
#     --publish=7687:7687 \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/data:/data:z \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/logs:/logs:z \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/import:/import:z \
#     neo4j:2026.03.1 \
#     neo4j-admin database import full \
#     --nodes=Account="/import/Account.csv" \
#     --nodes=Loan="/import/Loan.csv" \
#     --nodes=Medium="/import/Medium.csv" \
#     --nodes=Person="/import/Person.csv" \
#     --relationships=ACCOUNT_TRANSFER_ACCOUNT="/import/AccountTransferAccount.csv" \
#     --relationships=MEDIUM_SIGNIN_ACCOUNT="/import/MediumSignInAccount.csv" \
#     --relationships=PERSON_OWN_ACCOUNT="/import/PersonOwnAccount.csv" \
#     --relationships=LOAN_DEPOSIT_ACCOUNT="/import/LoanDepositAccount.csv" \
#     --relationships=PERSON_GUARANTEE_PERSON="/import/PersonGuaranteePerson.csv" \
#     --relationships=PERSON_APPLY_LOAN="/import/PersonApplyLoan.csv" \
#     --delimiter '|' \
    # --verbose



# docker run \
#     --rm \
#     --publish=7474:7474 \
#     --publish=7687:7687 \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/data:/data:z \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/logs:/logs:z \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/import:/import:z \
#     neo4j:2026.03.1 \
#     neo4j-admin database import full \
#     --nodes=Account="/import/Account_test.csv" \
#     --relationships=ACCOUNT_TRANSFER_ACCOUNT="/import/AccountTransferAccount_test.csv" \
#     --delimiter '|'



# Load WDBench data into wikidata database

# docker run \
#     --rm \
#     --publish=7474:7474 \
#     --publish=7687:7687 \
#     --volume=/data/dataset/pathmode:/import:z \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/data:/data:z \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/logs:/logs:z \
#     neo4j:2026.03.1 \
#     neo4j-admin database import full \
#         --nodes=Entity="/import/entities.csv" \
#         --nodes "/import/literals.csv" \
#         --relationships "/import/edges.csv" \
#         --delimiter "," \
#         --array-delimiter ";" \
#         --skip-bad-relationships true

# Import pokec with neo4j:2026.03.1
# This was for the 5.x version
# docker run \
#     --rm \
#     --publish=7474:7474 \
#     --publish=7687:7687 \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/data:/data:z \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/logs:/logs:z \
#     --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/import:/import:z \
#     neo4j:2026.03.1 \
#     neo4j-admin database import full \
#     --nodes=Entity="/import/id.csv" \
#     --relationships=Rel="/import/relationships.csv" \
#     --delimiter '|'


# Import pokec with neo4j:2026.03.1
docker run \
    --rm \
    --publish=7474:7474 \
    --publish=7687:7687 \
    --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/data:/data:z \
    --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/logs:/logs:z \
    --volume=/data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/import:/import:z \
    neo4j:2026.03.1 \
    neo4j-admin database import full \
    --nodes=Entity="/import/id.csv" \
    --relationships=Rel="/import/relationships.csv" \
    --delimiter '|'
