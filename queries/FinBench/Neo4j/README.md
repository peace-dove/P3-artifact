# FinBench Query Templates — Neo4j (Cypher)

Uses `CYPHER 25` with `allReduce()` for temporal constraint evaluation. Start node IDs are passed as a batch list via `IN [{id_str}]`. Parameters (`{id_str}`, `{start_time}`, `{end_time}`) are substituted from `../params/Q{1,2,3,4}_param.csv`.

## Q1

```cypher
CYPHER 25
MATCH
  p=(account:Account)-[edge1:ACCOUNT_TRANSFER_ACCOUNT*1..3]->(other:Account),
  (other)<-[edge2:MEDIUM_SIGNIN_ACCOUNT]-(medium:Medium {{isBlocked: true}})
WHERE account.accountId IN [{id_str}]
WITH p, [e IN relationships(p) | e.createTime] AS ts, other, medium
WHERE 
      allReduce(prev = null, t IN ts | t, prev IS NULL OR prev < t)
  AND all(e IN edge1 WHERE {start_time} < e.createTime < {end_time})
  AND {start_time} < edge2.createTime < {end_time}
RETURN 
    other.accountId AS otherId, 
    length(p) AS accountDistance, 
    medium.mediumId AS mediumId, 
    medium.mediumType AS mediumType
ORDER BY accountDistance ASC;
```

## Q2

```cypher
CYPHER 25
MATCH
  (person:Person)-[edge1:PERSON_OWN_ACCOUNT]->(accounts:Account),
  p=(accounts)<-[edge2:ACCOUNT_TRANSFER_ACCOUNT*1..3]-(other:Account),
  (other)<-[edge3:LOAN_DEPOSIT_ACCOUNT]-(loan:Loan) 
WHERE person.personId IN [{id_str}]
WITH p, [e IN relationships(p) | e.createTime] AS ts, other, loan 
WHERE allReduce(prev = null, t IN ts | t, prev IS NULL OR prev > t)
  AND all(e IN edge2 WHERE {start_time} < e.createTime < {end_time})
  AND {start_time} < edge3.createTime < {end_time} 
RETURN other.accountId AS otherId, sum(loan.loanAmount) AS sumLoanAmount, sum(loan.balance) AS sumLoanBalance 
ORDER BY sumLoanAmount DESC;
```

## Q3

```cypher
CYPHER 25
MATCH
  (person:Person)-[edge1:PERSON_OWN_ACCOUNT]->(src:Account),
  p=(src)-[edge2:ACCOUNT_TRANSFER_ACCOUNT*1..3]->(dst:Account)
WHERE person.personId IN [{id_str}]
WITH p, [e IN relationships(p) | e.createTime] AS ts
WHERE allReduce(prev = null, t IN ts | t, prev IS NULL OR prev < t)
  AND all(e IN edge2 WHERE {start_time} < e.createTime < {end_time})
RETURN p AS path
ORDER BY length(p) DESC;
```

## Q4

```cypher
CYPHER 25
MATCH path=(p1:Person)-[:PERSON_GUARANTEE_PERSON*1..5]->(pX:Person)
WHERE p1.personId IN [{id_str}] AND 
allReduce(
           acc = true,
           r IN relationships(path) |
           acc AND ({start_time} < r.createTime AND r.createTime < {end_time}),
           acc AND ({start_time} < r.createTime AND r.createTime < {end_time})
       )
UNWIND nodes(path)[1..] AS person
MATCH (person)-[:PERSON_APPLY_LOAN]->(loan:Loan)
RETURN sum(loan.loanAmount) AS sumLoanAmount, count(loan) AS numLoans
```
