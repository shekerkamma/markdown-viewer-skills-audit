# Architecture Skill — Sample-Prompt Demo

This file exercises the [architecture](SKILL.md) skill against three realistic prompts to verify the output renders in the markdown viewer and follows the skill's hard rules:

- **Rule 1** — HTML is embedded directly (no ` ```html ` fences).
- **Rule 2** — no empty lines inside an HTML diagram block.
- **Rule 4** — layout matches the prompt's complexity (three-column / pipeline / single-stack).
- **Rule 6** — semantic layer colors (`user` / `application` / `ai` / `data` / `infra` / `external`).

Each diagram below is self-contained — the `<style scoped>` block carries its own classes, so styles do not bleed between examples.

---

## Sample 1 — Enterprise three-column

**Prompt:** *"Draw an architecture diagram for an HR onboarding SaaS. We have a web portal and mobile app on the front, an API gateway, a workflow engine plus ML resume-screening, Postgres + Redis + S3 for storage, and we run on EKS. Sidebars should call out monitoring/analytics on the left and security/compliance on the right. Use a banking-grade visual style."*

**Skill choices:** style = [Steel Blue](styles/steel-blue.md) (corporate gravitas) · layout = [three-column](layouts/three-column.md) (cross-cutting concerns on both sides).

<div style="width: 1200px; box-sizing: border-box; position: relative; background: #f0f4f8; padding: 20px; border-radius: 8px; border: 1px solid #c8d6e5;">
  <style scoped>
    .s1-wrapper { display: flex; gap: 12px; }.s1-sidebar { width: 165px; flex-shrink: 0; }.s1-main { flex: 1; min-width: 0; }.s1-title { text-align: center; font-size: 22px; font-weight: bold; color: #1a365d; margin-bottom: 16px; font-family: Georgia, serif; }
    .s1-layer { margin: 8px 0; padding: 14px; border-radius: 6px; box-shadow: 0 1px 4px rgba(30, 58, 138, 0.08); }.s1-layer-title { font-size: 13px; font-weight: bold; margin-bottom: 10px; text-align: center; }
    .s1-grid { display: grid; gap: 8px; }.s1-grid-2 { grid-template-columns: repeat(2, 1fr); }.s1-grid-3 { grid-template-columns: repeat(3, 1fr); }.s1-grid-4 { grid-template-columns: repeat(4, 1fr); }.s1-grid-5 { grid-template-columns: repeat(5, 1fr); }
    .s1-box { border-radius: 4px; padding: 8px; text-align: center; font-size: 11px; font-weight: 600; line-height: 1.35; color: #1e293b; background: #ffffff; border: 1px solid #cbd5e1; }.s1-box.highlight { background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); border: 2px solid #2563eb; }.s1-box.tech { font-size: 10px; color: #475569; background: #f1f5f9; }
    .s1-layer.user { background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); border: 2px solid #3b82f6; }.s1-layer.user .s1-layer-title { color: #1e40af; }
    .s1-layer.application { background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%); border: 2px solid #0284c7; }.s1-layer.application .s1-layer-title { color: #075985; }
    .s1-layer.ai { background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%); border: 2px solid #6366f1; }.s1-layer.ai .s1-layer-title { color: #3730a3; }
    .s1-layer.data { background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); border: 2px solid #10b981; }.s1-layer.data .s1-layer-title { color: #065f46; }
    .s1-layer.infra { background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%); border: 2px solid #7c3aed; }.s1-layer.infra .s1-layer-title { color: #5b21b6; }
    .s1-layer.external { background: linear-gradient(135deg, #edf2f7 0%, #e2e8f0 100%); border: 2px dashed #a0aec0; }.s1-layer.external .s1-layer-title { color: #718096; }
    .s1-sidebar-panel { border-radius: 6px; padding: 10px; background: linear-gradient(135deg, #edf1f7 0%, #dde3eb 100%); border: 2px solid #8da3bd; margin-bottom: 8px; box-shadow: 0 1px 3px rgba(30, 58, 138, 0.06); }
    .s1-sidebar-title { font-size: 12px; font-weight: bold; text-align: center; color: #1a365d; margin-bottom: 6px; }
    .s1-sidebar-item { font-size: 10px; text-align: center; color: #334155; background: #ffffff; padding: 5px; border-radius: 3px; margin: 3px 0; border: 1px solid #d1d9e4; }.s1-sidebar-item.metric { background: #dbeafe; border: 1px solid #93c5fd; color: #1e40af; font-weight: 600; }
  </style>
  <div class="s1-title">HR Onboarding Platform — System Architecture</div>
  <div class="s1-wrapper">
    <div class="s1-sidebar">
      <div class="s1-sidebar-panel"><div class="s1-sidebar-title">Monitoring</div><div class="s1-sidebar-item">Datadog APM</div><div class="s1-sidebar-item">Synthetic Probes</div><div class="s1-sidebar-item">SLO Dashboards</div><div class="s1-sidebar-item metric">99.95% Uptime</div></div>
      <div class="s1-sidebar-panel"><div class="s1-sidebar-title">Analytics</div><div class="s1-sidebar-item">Funnel Tracking</div><div class="s1-sidebar-item">Time-to-Hire</div><div class="s1-sidebar-item">Drop-off Reports</div><div class="s1-sidebar-item">Exec Dashboard</div></div>
      <div class="s1-sidebar-panel"><div class="s1-sidebar-title">Ops</div><div class="s1-sidebar-item">GitHub Actions</div><div class="s1-sidebar-item">ArgoCD</div><div class="s1-sidebar-item">Terraform</div><div class="s1-sidebar-item">PagerDuty</div></div>
    </div>
    <div class="s1-main">
      <div class="s1-layer user">
        <div class="s1-layer-title">User Interface Layer</div>
        <div class="s1-grid s1-grid-4"><div class="s1-box">Candidate Portal<br><small>Next.js</small></div><div class="s1-box">Mobile App<br><small>React Native</small></div><div class="s1-box">HR Console<br><small>Internal admin</small></div><div class="s1-box">Manager Portal<br><small>Approvals</small></div></div>
      </div>
      <div class="s1-layer application">
        <div class="s1-layer-title">Application Services</div>
        <div class="s1-grid s1-grid-4"><div class="s1-box highlight">API Gateway<br><small>Kong + JWT</small></div><div class="s1-box">Onboarding Svc<br><small>Forms + e-sign</small></div><div class="s1-box">Workflow Engine<br><small>Temporal</small></div><div class="s1-box">Notification Svc<br><small>Email/SMS/push</small></div></div>
      </div>
      <div class="s1-layer ai">
        <div class="s1-layer-title">Intelligence Layer</div>
        <div class="s1-grid s1-grid-3"><div class="s1-box">Resume Screening<br><small>BERT classifier</small></div><div class="s1-box">Skills Matcher<br><small>Embedding search</small></div><div class="s1-box">Bias Audit<br><small>Fairness checks</small></div></div>
      </div>
      <div class="s1-layer data">
        <div class="s1-layer-title">Data Layer</div>
        <div class="s1-grid s1-grid-4"><div class="s1-box tech">PostgreSQL<br><small>RDS Multi-AZ</small></div><div class="s1-box tech">Redis<br><small>Sessions + cache</small></div><div class="s1-box tech">S3<br><small>Documents</small></div><div class="s1-box tech">OpenSearch<br><small>Resume index</small></div></div>
      </div>
      <div class="s1-layer infra">
        <div class="s1-layer-title">Infrastructure</div>
        <div class="s1-grid s1-grid-5"><div class="s1-box tech">Amazon EKS<br><small>k8s 1.30</small></div><div class="s1-box tech">ALB<br><small>TLS terminate</small></div><div class="s1-box tech">SQS<br><small>Async jobs</small></div><div class="s1-box tech">CloudFront<br><small>CDN</small></div><div class="s1-box tech">Route 53<br><small>DNS</small></div></div>
      </div>
      <div class="s1-layer external">
        <div class="s1-layer-title">External Services</div>
        <div class="s1-grid s1-grid-4"><div class="s1-box tech">DocuSign<br><small>e-signature</small></div><div class="s1-box tech">Workday<br><small>HRIS sync</small></div><div class="s1-box tech">Checkr<br><small>Background</small></div><div class="s1-box tech">Stripe<br><small>Payouts</small></div></div>
      </div>
    </div>
    <div class="s1-sidebar">
      <div class="s1-sidebar-panel"><div class="s1-sidebar-title">Security</div><div class="s1-sidebar-item">Okta SSO</div><div class="s1-sidebar-item">RBAC</div><div class="s1-sidebar-item">KMS Encryption</div><div class="s1-sidebar-item">WAF + Shield</div></div>
      <div class="s1-sidebar-panel"><div class="s1-sidebar-title">Compliance</div><div class="s1-sidebar-item">SOC 2 Type II</div><div class="s1-sidebar-item">GDPR / CCPA</div><div class="s1-sidebar-item">PII Audit Log</div><div class="s1-sidebar-item">Data Residency</div></div>
      <div class="s1-sidebar-panel"><div class="s1-sidebar-title">Resilience</div><div class="s1-sidebar-item">Multi-AZ</div><div class="s1-sidebar-item">Daily Backups</div><div class="s1-sidebar-item">DR Runbook</div><div class="s1-sidebar-item metric">RPO &lt; 1h</div></div>
    </div>
  </div>
</div>

---

## Sample 2 — Customer-events ETL pipeline

**Prompt:** *"We have a customer-events pipeline: Kafka in, Flink processing, dbt transforms, Snowflake + Pinecone storage, served to BI and the recommendation API. Make it look like a developer-conference talk slide."*

**Skill choices:** style = [Neon Dark](styles/neon-dark.md) (conference-talk vibe) · layout = [pipeline](layouts/pipeline.md) (horizontal stage flow).

<div style="width: 1200px; box-sizing: border-box; position: relative; background: #0f172a; padding: 20px; border-radius: 12px;">
  <style scoped>
    .s2-title { text-align: center; font-size: 22px; font-weight: bold; color: #f1f5f9; margin-bottom: 16px; letter-spacing: 1px; }
    .s2-pipeline { display: flex; gap: 0; align-items: stretch; }
    .s2-stage { flex: 1; padding: 14px; border-radius: 8px; background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(148, 163, 184, 0.2); display: flex; flex-direction: column; }
    .s2-stage-title { font-size: 12px; font-weight: 600; color: #94a3b8; text-align: center; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; }
    .s2-arrow { display: flex; align-items: center; justify-content: center; width: 36px; flex-shrink: 0; font-size: 20px; color: #facc15; }
    .s2-box { border-radius: 6px; padding: 8px; text-align: center; font-size: 11px; font-weight: 600; line-height: 1.35; color: #e2e8f0; background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(148, 163, 184, 0.25); margin: 3px 0; }
    .s2-box.highlight { background: rgba(250, 204, 21, 0.15); border: 1px solid #facc15; color: #fef08a; }
    .s2-box.tech { font-size: 10px; color: #94a3b8; background: rgba(15, 23, 42, 0.6); }
    .s2-stage.ingest { box-shadow: 0 0 12px rgba(14, 165, 233, 0.18); border-color: #0ea5e9; }
    .s2-stage.process { box-shadow: 0 0 12px rgba(245, 158, 11, 0.18); border-color: #f59e0b; }
    .s2-stage.transform { box-shadow: 0 0 12px rgba(16, 185, 129, 0.18); border-color: #10b981; }
    .s2-stage.store { box-shadow: 0 0 12px rgba(236, 72, 153, 0.18); border-color: #ec4899; }
    .s2-stage.serve { box-shadow: 0 0 12px rgba(139, 92, 246, 0.18); border-color: #8b5cf6; }
  </style>
  <div class="s2-title">Customer-Events Pipeline</div>
  <div class="s2-pipeline">
    <div class="s2-stage ingest">
      <div class="s2-stage-title">Ingest</div>
      <div class="s2-box">Kafka Topics<br><small>events.raw</small></div>
      <div class="s2-box">Webhook Gateway<br><small>3rd-party events</small></div>
      <div class="s2-box">Mobile SDK<br><small>tap stream</small></div>
      <div class="s2-box tech">Schema Registry</div>
    </div>
    <div class="s2-arrow">&rarr;</div>
    <div class="s2-stage process">
      <div class="s2-stage-title">Process</div>
      <div class="s2-box highlight">Apache Flink<br><small>Stream jobs</small></div>
      <div class="s2-box">PII Scrubber</div>
      <div class="s2-box">Sessionization</div>
      <div class="s2-box">Dedup &amp; Order</div>
    </div>
    <div class="s2-arrow">&rarr;</div>
    <div class="s2-stage transform">
      <div class="s2-stage-title">Transform</div>
      <div class="s2-box highlight">dbt Cloud<br><small>SQL models</small></div>
      <div class="s2-box">Feature Store<br><small>Feast</small></div>
      <div class="s2-box">Embedding Job<br><small>OpenAI</small></div>
      <div class="s2-box tech">Great Expectations</div>
    </div>
    <div class="s2-arrow">&rarr;</div>
    <div class="s2-stage store">
      <div class="s2-stage-title">Store</div>
      <div class="s2-box">Snowflake<br><small>Warehouse</small></div>
      <div class="s2-box">Iceberg on S3<br><small>Lake</small></div>
      <div class="s2-box">Pinecone<br><small>Vector index</small></div>
      <div class="s2-box tech">Redis<br><small>Hot cache</small></div>
    </div>
    <div class="s2-arrow">&rarr;</div>
    <div class="s2-stage serve">
      <div class="s2-stage-title">Serve</div>
      <div class="s2-box">Looker<br><small>Exec BI</small></div>
      <div class="s2-box highlight">Reco API<br><small>gRPC</small></div>
      <div class="s2-box">Reverse-ETL<br><small>Hightouch</small></div>
      <div class="s2-box tech">Notebooks<br><small>DS access</small></div>
    </div>
  </div>
</div>

---

## Sample 3 — Auth microservice detail view

**Prompt:** *"Show just our auth service stack — what's in it, what it talks to. Keep it minimal; this is going in our developer docs."*

**Skill choices:** style = [Frost Clean](styles/frost-clean.md) (docs / minimalist) · layout = [single-stack](layouts/single-stack.md) (one service, no cross-cutting sidebars).

<div style="width: 1200px; box-sizing: border-box; position: relative; background: #fafbfc; padding: 20px; border-radius: 6px; border: 1px solid #e5e7eb;">
  <style scoped>
    .s3-main { width: 100%; }
    .s3-title { text-align: center; font-size: 22px; font-weight: bold; color: #1f2937; margin-bottom: 16px; }
    .s3-layer { margin: 8px 0; padding: 14px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04); }
    .s3-layer-title { font-size: 13px; font-weight: bold; margin-bottom: 10px; text-align: center; }
    .s3-grid { display: grid; gap: 8px; }.s3-grid-2 { grid-template-columns: repeat(2, 1fr); }.s3-grid-3 { grid-template-columns: repeat(3, 1fr); }.s3-grid-4 { grid-template-columns: repeat(4, 1fr); }
    .s3-box { border-radius: 4px; padding: 8px; text-align: center; font-size: 11px; font-weight: 600; line-height: 1.35; color: #1f2937; background: #ffffff; border: 1px solid #e5e7eb; }
    .s3-box.highlight { background: #f3f4f6; border: 2px solid #6b7280; }
    .s3-box.tech { font-size: 10px; color: #6b7280; background: #f9fafb; }
    .s3-layer.user { background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border: 2px solid #3b82f6; }.s3-layer.user .s3-layer-title { color: #1d4ed8; }
    .s3-layer.application { background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); border: 2px solid #d97706; }.s3-layer.application .s3-layer-title { color: #92400e; }
    .s3-layer.data { background: linear-gradient(135deg, #fdf2f8 0%, #fce7f3 100%); border: 2px solid #db2777; }.s3-layer.data .s3-layer-title { color: #9d174d; }
    .s3-layer.infra { background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); border: 2px solid #6b7280; }.s3-layer.infra .s3-layer-title { color: #374151; }
    .s3-layer.external { background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%); border: 1px dashed #d1d5db; }.s3-layer.external .s3-layer-title { color: #6b7280; }
  </style>
  <div class="s3-title">Auth Service — Stack View</div>
  <div class="s3-main">
    <div class="s3-layer user">
      <div class="s3-layer-title">Callers</div>
      <div class="s3-grid s3-grid-4"><div class="s3-box">Web App<br><small>Browser</small></div><div class="s3-box">Mobile App<br><small>iOS / Android</small></div><div class="s3-box">Public API<br><small>Partner clients</small></div><div class="s3-box">CLI<br><small>Internal tooling</small></div></div>
    </div>
    <div class="s3-layer application">
      <div class="s3-layer-title">Auth Service Internals</div>
      <div class="s3-grid s3-grid-4"><div class="s3-box highlight">Token Issuer<br><small>JWT, RS256</small></div><div class="s3-box">Login Handler<br><small>password + WebAuthn</small></div><div class="s3-box">MFA Module<br><small>TOTP / push</small></div><div class="s3-box">Session Mgr<br><small>refresh + revoke</small></div></div>
    </div>
    <div class="s3-layer data">
      <div class="s3-layer-title">State</div>
      <div class="s3-grid s3-grid-3"><div class="s3-box tech">PostgreSQL<br><small>users, credentials</small></div><div class="s3-box tech">Redis<br><small>sessions, rate limits</small></div><div class="s3-box tech">Vault<br><small>signing keys</small></div></div>
    </div>
    <div class="s3-layer infra">
      <div class="s3-layer-title">Runtime</div>
      <div class="s3-grid s3-grid-4"><div class="s3-box tech">Go 1.22</div><div class="s3-box tech">Kubernetes<br><small>3 replicas</small></div><div class="s3-box tech">Envoy sidecar<br><small>mTLS</small></div><div class="s3-box tech">OpenTelemetry</div></div>
    </div>
    <div class="s3-layer external">
      <div class="s3-layer-title">External Dependencies</div>
      <div class="s3-grid s3-grid-3"><div class="s3-box tech">Okta<br><small>SSO / SAML</small></div><div class="s3-box tech">Twilio<br><small>SMS OTP</small></div><div class="s3-box tech">SendGrid<br><small>magic links</small></div></div>
    </div>
  </div>
</div>

---

## How to view this

The diagrams above are HTML, not code blocks — they only render in viewers that allow inline HTML in Markdown. Tested targets:

- **markdown-viewer / docu.md** — renders fully (this skill's intended target).
- **VS Code preview, GitHub web** — renders most of the layout; `<style scoped>` is sanitized in some sandboxes, so colors may fall back to defaults. The structure stays correct.
- **Plain `cat` / GitHub diff view** — the raw HTML is visible but unstyled.

## Self-check against the skill rules

| Rule | Sample 1 | Sample 2 | Sample 3 |
|---|:---:|:---:|:---:|
| 1 — direct HTML, no fences | yes | yes | yes |
| 2 — no empty lines inside HTML | yes | yes | yes |
| 4 — layout matches complexity | three-column | pipeline | single-stack |
| 5 — layer-based organization | 6 layers | 5 stages | 5 layers |
| 6 — semantic layer colors | user/app/ai/data/infra/external | per-stage glow | user/app/data/infra/external |

Class names are namespaced per sample (`s1-*`, `s2-*`, `s3-*`) so the three diagrams can coexist on one page without `<style scoped>` collisions in viewers that flatten scoping.
