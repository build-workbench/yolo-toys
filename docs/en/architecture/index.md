# Architecture Atlas

<div class="yt-chapter-intro">
  <p class="yt-chapter-intro__lead">
    The Architecture Atlas explains why YOLO-Toys looks the way it does: thin routes, a central manager, explicit handler dispatch, and normalization boundaries that let heterogeneous model families share one service contract.
  </p>
  <div class="yt-chapter-callout">
    <strong>Read this chapter when:</strong>
    you need the system map, the request lifecycle, and the decision boundaries that make extension safe.
  </div>
</div>

<div class="yt-chapter-grid">
  <a class="yt-chapter-card" href="/en/architecture/overview">
    <strong>System overview</strong>
    <span>Read the service as a layered runtime, not a flat list of endpoints.</span>
  </a>
  <a class="yt-chapter-card" href="/en/architecture/request-flow">
    <strong>Request lifecycle</strong>
    <span>Trace a request from ingress through cache lookup, handler dispatch, and result shaping.</span>
  </a>
  <a class="yt-chapter-card" href="/en/architecture/handlers">
    <strong>Execution boundaries</strong>
    <span>See how model-specific logic stays localized inside handler implementations.</span>
  </a>
</div>

## Questions this chapter answers

- Why not expose one endpoint per model family?
- Why centralize model resolution through the registry?
- Where does normalization happen, and what does it cost?
- How does the runtime stay extensible without becoming opaque?

## Recommended path

1. Start with [System Overview](/en/architecture/overview)
2. Continue to [Request Lifecycle](/en/architecture/request-flow)
3. Read the ADR set to understand the intentional trade-offs
