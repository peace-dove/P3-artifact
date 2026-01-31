# FinBench Query Templates — TuGraphDB (Cypher with helpers)

Uses TuGraphDB helper functions (`getMemberProp`, `isAsc`, `isDesc`, `minInList`, `maxInList`). Start node IDs are passed as a batch list via `WHERE ... in {input_ids}`. `%d` placeholders for timestamps are substituted from `../params/Q{1,2,3,4}_param.csv`.

## Q1

```cypher
MATCH p = (acc:Account)-[e1:transfer *1..3]->(other:Account)<-[e2:signIn]-(medium)
WHERE acc.id in {input_ids}
  AND isAsc(getMemberProp(e1, 'timestamp'))=true
  AND head(getMemberProp(e1, 'timestamp')) > %d
  AND last(getMemberProp(e1, 'timestamp')) < %d
  AND e2.timestamp > %d
  AND e2.timestamp < %d
  AND medium.isBlocked = true
RETURN DISTINCT other.id as otherId,
                length(p)-1 as accountDistance,
                medium.id as mediumId,
                medium.type as mediumType
ORDER BY accountDistance, otherId, mediumId;
```

## Q2

```cypher
MATCH (p:Person)-[e1:own]->(acc:Account) <-[e2:transfer*1..3]-(other:Account)
WHERE p.id in {input_ids}
  AND isDesc(getMemberProp(e2, 'timestamp'))=true
  AND head(getMemberProp(e2, 'timestamp')) < %d
  AND last(getMemberProp(e2, 'timestamp')) > %d
WITH DISTINCT other
MATCH (other)<-[e3:deposit]-(loan:Loan)
WHERE e3.timestamp > %d
  AND e3.timestamp < %d
WITH DISTINCT other.id AS otherId, loan.loanAmount AS loanAmount, loan.balance AS loanBalance
WITH otherId AS otherId, sum(loanAmount) as sumLoanAmount, sum(loanBalance) as sumLoanBalance
RETURN otherId,
       round(sumLoanAmount * 1000) / 1000 as sumLoanAmount,
       round(sumLoanBalance * 1000) / 1000 as sumLoanBalance
ORDER BY sumLoanAmount DESC, otherId ASC;
```

## Q3

```cypher
MATCH (person:Person)-[e1:own]->(src:Account)
WHERE person.id in {input_ids}
WITH src
MATCH p=(src)-[e2:transfer*1..3]->(dst:Account)
WHERE isAsc(getMemberProp(e2, 'timestamp'))=true
  AND head(getMemberProp(e2, 'timestamp')) > %d
  AND last(getMemberProp(e2, 'timestamp')) < %d
WITH DISTINCT getMemberProp(nodes(p), 'id') as path, length(p) as len
ORDER BY len DESC
RETURN path;
```

## Q4

```cypher
MATCH (p1:Person)-[edge:guarantee*1..5]->(pN:Person) -[:apply]->(loan:Loan)
WHERE p1.id in {input_ids} 
  AND minInList(getMemberProp(edge, 'timestamp')) > %d
  AND maxInList(getMemberProp(edge, 'timestamp')) < %d
WITH DISTINCT loan
WITH sum(loan.loanAmount) as sumLoanAmount, count(distinct loan) as numLoans
RETURN round(sumLoanAmount * 1000) / 1000 as sumLoanAmount, numLoans;
```
