# cd /data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/import
# rm -f *.csv

# cd /data/dataset/sf10/snapshot

# cp \
#   Account.csv \
#   Loan.csv \
#   Medium.csv \
#   Person.csv \
#   AccountTransferAccount.csv \
#   MediumSignInAccount.csv \
#   PersonOwnAccount.csv \
#   LoanDepositAccount.csv \
#   PersonGuaranteePerson.csv \
#   PersonApplyLoan.csv \
#   /data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/import/

# cd /data/ldbc_finbench_transaction_impls/neo4j/neo/bench
# python3 convert_csv_header.py


# For pokec
cd /data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/import
rm -f *.csv

cd /data/dataset/pokec

cp \
  id.csv \
  relationships.csv \
  /data/ldbc_finbench_transaction_impls/neo4j/neo/scratch/import/
