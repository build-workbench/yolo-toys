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
  <a class="yt-chapter-card" href="/en/architecture/middleware-stack">
    <strong>Middleware stack</strong>
    <span>Security, metrics, timeout, rate limit, compression, and CORS in layered order.</span>
  </a>
  <a class="yt-chapter-card" href="/en/architecture/config-injection">
    <strong>Config injection</strong>
    <span>How Pydantic settings flow through adapter classes into the runtime.</span>
  </a>
  <a class="yt-chapter-card" href="/en/architecture/model-cache">
    <strong>Model cache</strong>
    <span>LRU + TTL hybrid caching with memory-pressure eviction and thread safety.</span>
  </a>
</div>

## Questions this chapter answers

- Why not expose one endpoint per model family?
- Why centralize model resolution through the registry?
- Where does normalization happen, and what does it cost?
- How does the runtime stay extensible without becoming opaque?
- How does the middleware stack order reflect production concerns?
- Why is the cache operationally aware rather than just time-based?

## Recommended path

1. Start with [System Overview](/en/architecture/overview)
2. Continue to [Request Lifecycle](/en/architecture/request-flow)
3. Read [Handler Topology](/en/architecture/handlers) for execution boundaries
4. Read [Middleware Stack](/en/architecture/middleware-stack) for operational layers
5. Read [Config Injection](/en/architecture/config-injection) for settings flow
6. Read [Model Cache](/en/architecture/model-cache) for caching strategy
7. Finish with the ADR set to understand intentional trade-offs
