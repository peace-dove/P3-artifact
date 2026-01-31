# FinBench Query Templates — P3 (GQL with SW)

Uses the GQL/SW (sliding-window) syntax. Start node IDs are passed as a batch list via `WHERE ... in {input_ids}`. Placeholders `{input_ids}`, `${startTime}`, `${endTime}` are substituted from `../params/Q{1,2,3,4}_param.csv`.

## Q1

```sql
MATCH p = (acc:Account WHERE acc.accountId in {input_ids})-[e1:transfer]->{1,3} (other:Account),
          (other)<-[e2:signIn where e2.timestamp > ${startTime} and e2.timestamp < ${endTime}]-(medium:Medium)
WITH SW(2) ON p AS pp
  [ WHERE relationships(pp)[0].timestamp < relationships(pp)[1].timestamp ]
WHERE relationships(p)[0].timestamp > ${startTime}
  AND relationships(p)[-1].timestamp < ${endTime}
  AND medium.isBlocked = True
RETURN distinct other.id as otherId,
                length(p) as accountDistance,
                medium.id as mediumId,
                medium.type as mediumType
ORDER BY accountDistance, otherId, mediumId;
```

## Q2

```sql
MATCH (s:Person WHERE s.PersonId in {input_ids})-[e1:own]->(acc:Account),
      p = (acc) <-[e2:transfer]-{1,3} (other:Account),
      (other)<-[e3:deposit]-(loan:Loan)
WITH sw(2) ON p AS pp
  [ WHERE relationships(pp)[0].timestamp > relationships(pp)[1].timestamp ]
WHERE relationships(p)[0].timestamp > ${startTime}
  AND relationships(p)[-1].timestamp < ${endTime}
  AND e3.timestamp > ${startTime}
  AND e3.timestamp < ${endTime}
RETURN DISTINCT other.id AS otherId,
                sum(loan.loanAmount) AS sumLoanAmount,
                sum(loan.balance) AS sumLoanBalance
ORDER BY sumLoanAmount DESC, otherId ASC;
```

## Q3

```sql
MATCH (person:Person WHERE person.PersonId in {input_ids})-[e1:own]->(src:Account),
      p = (src)-[e2:transfer]->{1,3}(dst:Account)
WITH sw(2) ON p AS pp
  [ WHERE relationships(pp)[0].timestamp < relationships(pp)[1].timestamp ]
WHERE relationships(p)[0].timestamp > ${startTime}
  AND relationships(p)[-1].timestamp < ${endTime}
RETURN nodes(p)
ORDER BY length(p) DESC;
```

## Q4

```sql
MATCH p = (p1:Person WHERE p1.PersonId in {input_ids})-[e:guarantee]->{1,5}(pN:Person),
          (pN)-[e2:Apply]->(loan:Loan)
WITH sw(1) ON p AS pp
  [ WHERE relationships(pp)[0].timestamp > ${startTime}
      AND relationships(pp)[0].timestamp < ${endTime} ]
RETURN DISTINCT loan
NEXT
RETURN sum(loan.loanAmount) as sumLoanAmount, count(loan) as numLoans;
```
