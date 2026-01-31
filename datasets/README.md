# Benchmark Datasets

This directory contains the datasets and preparation scripts used in our evaluation. We employ four well-established benchmark datasets that represent diverse graph characteristics and application domains.

## Overview

| Dataset | Vertices | Edges | Queries | Domain | Source |
|---------|----------|-------|---------|--------|--------|
| **FinBench** | 1.1M (SF10) | 10.4M | 480 | Financial networks | LDBC |
| **Stack Overflow** | 642K | 1.3M | 480 | Temporal graphs | KONECT |
| **Wikidata** | 364M | 1.26B | 480 | Knowledge graphs | WDBench |
| **Pokec** | 1.63M | 30.6M | 360 | Social networks | SNAP |

## Dataset Details

### 1. FinBench

**Description**: FinBench is a financial graph benchmark from the Linked Data Benchmark Council (LDBC), modeling financial transactions and account relationships.

**Characteristics**:
- Heterogeneous vertex types (Person, Account, Company, etc.)
- Temporal transaction networks
- Various scale factors (SF) for scalability testing

**Available Scale Factors**:

| Scale Factor | Download | Checksum |
|--------------|----------|----------|
| SF 0.1 | [Download](https://tugraph-web.oss-cn-beijing.aliyuncs.com/tugraph/datasets/finbench/v0.2.0/sf0.1/sf0.1.tar.xz) | [MD5](https://tugraph-web.oss-cn-beijing.aliyuncs.com/tugraph/datasets/finbench/v0.2.0/sf0.1/sf0.1.tar.xz.md5sum) |
| SF 1 | [Download](https://tugraph-web.oss-cn-beijing.aliyuncs.com/tugraph/datasets/finbench/v0.2.0/sf1/sf1.tar.xz) | [MD5](https://tugraph-web.oss-cn-beijing.aliyuncs.com/tugraph/datasets/finbench/v0.2.0/sf1/sf1.tar.xz.md5sum) |
| SF 3 | [Download](https://tugraph-web.oss-cn-beijing.aliyuncs.com/tugraph/datasets/finbench/v0.2.0/sf3/sf3.tar.xz) | [MD5](https://tugraph-web.oss-cn-beijing.aliyuncs.com/tugraph/datasets/finbench/v0.2.0/sf3/sf3.tar.xz.md5sum) |
| SF 10 | [Download](https://tugraph-web.oss-cn-beijing.aliyuncs.com/tugraph/datasets/finbench/v0.2.0/sf10/sf10.tar.xz) | [MD5](https://tugraph-web.oss-cn-beijing.aliyuncs.com/tugraph/datasets/finbench/v0.2.0/sf10/sf10.tar.xz.md5sum) |
| SF 30 | [Download](https://tugraph-web.oss-cn-beijing.aliyuncs.com/tugraph/datasets/finbench/v0.2.0/sf30/sf30.tar.xz) | [MD5](https://tugraph-web.oss-cn-beijing.aliyuncs.com/tugraph/datasets/finbench/v0.2.0/sf30/sf30.tar.xz.md5sum) |
| SF 100 | [Download](https://tugraph-web.oss-cn-beijing.aliyuncs.com/tugraph/datasets/finbench/v0.2.0/sf100/sf100.tar.xz) | [MD5](https://tugraph-web.oss-cn-beijing.aliyuncs.com/tugraph/datasets/finbench/v0.2.0/sf100/sf100.tar.xz.md5sum) |

**Reference**: LDBC FinBench Benchmark Specification v0.2.0

### 2. Stack Overflow

**Description**: A temporal interaction network extracted from Stack Overflow user activities, including questions, answers, and comments.

**Characteristics**:
- Temporal edges with timestamps
- User-to-user interactions
- Medium-scale graph suitable for temporal path queries

**Download**:
- Main page: [KONECT Stack Overflow Network](http://konect.cc/networks/stackexchange-stackoverflow/)
- Data file: [Download](http://konect.cc/networks/stackexchange-stackoverflow/)

**Reference**: J. Kunegis. KONECT: The Koblenz Network Collection. In Proc. Int. Conf. on World Wide Web Companion, 2013.

### 3. Wikidata (WDBench)

**Description**: A large-scale knowledge graph derived from Wikidata, used in the WDBench benchmark for evaluating property path queries.

**Characteristics**:
- Massive scale (364M vertices, 1.26B edges)
- RDF-style knowledge graph with diverse predicates
- Complex ontology with hundreds of property types

**Setup**: Follow the instructions at [WDBench GitHub Repository](https://github.com/MillenniumDB/WDBench)

**Reference**: D. Vrgoč et al. MillenniumDB: A Persistent, Open-Source, Graph Database. arXiv:2111.01540, 2021.

### 4. Pokec

**Description**: A social network from the Slovak online social network Pokec (similar to Facebook), containing user profiles and friendships.

**Characteristics**:
- Large social network (1.63M users)
- Dense friendship connections (30.6M edges)
- Real-world community structures

**Download**:
- Main page: [SNAP Pokec Dataset](https://snap.stanford.edu/data/soc-Pokec.html)
- Relationships: [Download](https://snap.stanford.edu/data/soc-pokec-relationships.txt.gz)
- Profiles: [Download](https://snap.stanford.edu/data/soc-pokec-profiles.txt.gz)

**Reference**: L. Takac and M. Zabovsky. Data Analysis in Public Social Networks. In International Scientific Conference and International Workshop Present Day Trends of Innovations, 2012.
