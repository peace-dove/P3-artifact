# FinBench Query Templates — GU (GQL w/o SW)

Uses UDFs (`isAsc`, `isDesc`, `minInlist`, `maxInlist`) to express temporal constraints instead of sliding windows. Start node IDs are passed as a batch list via `WHERE ... in {input_ids}`. Placeholders `{input_ids}`, `${startTime}`, `${endTime}` are substituted from `../params/Q{1,2,3,4}_param.csv`.

## Q1

Transfer chain reachability (1–3 hops) with **ascending timestamp** ordering, filtering by blocked medium sign-in within a time window.

```sql
MATCH p = (acc:Account WHERE acc.accountId in {input_ids})-[e1:transfer]->{1,3} (other:Account),
          (other)<-[e2:signIn where e2.timestamp > ${startTime} and e2.timestamp < ${endTime}]-(medium:Medium)
WHERE isAsc(relationships(p), 0) = True
  AND relationships(p)[0].timestamp > ${startTime}
  AND relationships(p)[-1].timestamp < ${endTime}
  AND medium.isBlocked = True
RETURN distinct other.id as otherId,
                length(p) as accountDistance,
                medium.id as mediumId,
                medium.type as mediumType
ORDER BY accountDistance, otherId, mediumId;
```

## Q2

Reverse transfer chain (1–3 hops) with **descending timestamp** ordering, joining loan deposits within a time window.

```sql
MATCH (s:Person WHERE s.PersonId in {input_ids})-[e1:own]->(acc:Account),
      p = (acc) <-[e2:transfer]-{1,3} (other:Account),
      (other)<-[e3:deposit]-(loan:Loan)
WHERE isDesc(relationships(p), 0) = True
  AND relationships(p)[0].timestamp > ${startTime}
  AND relationships(p)[-1].timestamp < ${endTime}
  AND e3.timestamp > ${startTime}
  AND e3.timestamp < ${endTime}
RETURN DISTINCT other.id AS otherId,
                sum(loan.loanAmount) AS sumLoanAmount,
                sum(loan.balance) AS sumLoanBalance
ORDER BY sumLoanAmount DESC, otherId ASC;
```

## Q3

Forward transfer chain (1–3 hops) with **ascending timestamp** ordering, returning full paths within a time window.

```sql
MATCH (person:Person WHERE person.PersonId in {input_ids})-[e1:own]->(src:Account),
      p = (src)-[e2:transfer]->{1,3}(dst:Account)
WHERE isAsc(relationships(p), 0) = true
  AND relationships(p)[0].timestamp > ${startTime}
  AND relationships(p)[-1].timestamp < ${endTime}
RETURN nodes(p)
ORDER BY length(p) DESC;
```

## Q4

Guarantee chain (1–5 hops) where **all edge timestamps** fall within a time window, aggregating linked loan amounts.

```sql
MATCH p = (p1:Person WHERE p1.PersonId in {input_ids})-[e:guarantee]->{1,5}(pN:Person),
          (pN)-[e2:Apply]->(loan:Loan)
WHERE minInlist(relationships(p), 0) > ${startTime} AND
      maxInlist(relationships(p), 0) < ${endTime}
RETURN DISTINCT loan
NEXT
RETURN sum(loan.loanAmount) as sumLoanAmount, count(loan) as numLoans;
```
