# Mermaid Example — Flowchart

Demonstrates subgraphs, mixed shapes, edge labels, dashed (async) edges, and styling.

## Source

````markdown
```mermaid
flowchart LR
  user([End User])
  cdn[CloudFront]
  subgraph aws[AWS VPC us-east-1]
    direction TB
    alb[ALB]
    api[[API Service]]
    worker[[Worker]]
    queue((SQS))
    db[(Postgres)]
    cache[(Redis)]
  end
  s3[(S3 static)]

  user --> cdn
  cdn --> alb
  cdn -. assets .-> s3
  alb --> api
  api --> db
  api --> cache
  api -- enqueue --> queue
  queue -. async .-> worker
  worker --> db

  classDef external fill:#e0f2fe,stroke:#0284c7;
  classDef storage fill:#fef3c7,stroke:#d97706;
  class user,cdn,s3 external
  class db,cache storage
```
````

## Rendered

```mermaid
flowchart LR
  user([End User])
  cdn[CloudFront]
  subgraph aws[AWS VPC us-east-1]
    direction TB
    alb[ALB]
    api[[API Service]]
    worker[[Worker]]
    queue((SQS))
    db[(Postgres)]
    cache[(Redis)]
  end
  s3[(S3 static)]

  user --> cdn
  cdn --> alb
  cdn -. assets .-> s3
  alb --> api
  api --> db
  api --> cache
  api -- enqueue --> queue
  queue -. async .-> worker
  worker --> db

  classDef external fill:#e0f2fe,stroke:#0284c7;
  classDef storage fill:#fef3c7,stroke:#d97706;
  class user,cdn,s3 external
  class db,cache storage
```

## Notes

- `subgraph aws[...]` groups the VPC contents in a labeled box.
- `direction TB` inside a subgraph overrides the parent's `LR`.
- `-.->` marks async/CDN-asset paths visually distinct from the request path.
- `classDef` + `class` apply consistent styling to multiple nodes — better than per-node `style`.
- Stadium shape `([...])` for actors, cylinder `[(...)]` for storage, double-square `[[...]]` for services. Reading the diagram, shape alone tells you what each node is.
