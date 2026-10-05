# Conditional runtime and infrastructure checks

Use only when the project has the relevant running application or infrastructure files and an identified gap. These are optional choices, not additions to every quality setup. Reuse existing authorization tests, scanners and environments. Apply the [scan evidence contract and finding lifecycle](security-scanning.md) to selected scanners.

## Running web applications and APIs

Start with concrete risks: session expiry, cross-user/role access, unauthorized state changes, response/security configuration and other relevant runtime behavior. Existing API/browser tests may cover these better than adding a generic scanner. Test both a permitted operation and a denied counterpart, and inspect persisted state where applicable; a successful login or absence of scanner findings does not prove authorization isolation.

Consider ZAP or an existing dynamic scanner when it covers a remaining risk in an available test environment. Decide separately between passive analysis of exercised traffic and active probing. A baseline scan typically spiders the application before passive analysis: it still sends requests, and even a route reached by a spider may have side effects. Do not describe it as offline or automatically safe for production.

Before executing, establish the authorized target, representative app readiness, allowed hosts/routes, roles/sessions, isolated test data, external-service boundaries, request/time limits and cleanup. Prefer a disposable local/test environment. Do not use production data, follow off-target hosts, weaken access controls or trigger payments/deletions to make a scan work. Active attack scanning and new external targets need corresponding authorization; ordinary quality setup is not blanket permission for them. Continue independent source/CI work if the runtime environment is unavailable.

Record reached routes and authenticated states, scanner errors and excluded flows. Scanning only a login page leaves authenticated paths unverified. Choose a narrow smoke on PRs or a broader manual/scheduled run according to risk and measured cost. Do not introduce a recurring service or paid scanner automatically.

## Infrastructure as code

Detect actual Terraform, Kubernetes, Helm or other supported configuration before proposing infrastructure scanning. Consider Checkov or an existing equivalent for misconfiguration risks; a container-image vulnerability scan and an infrastructure configuration scan cover different objects. Select supported frameworks/rules and relevant roots instead of scanning every framework by default.

Start with available local source/configuration. Scanning a file does not authorize cloud authentication, `apply`, cluster changes, provider execution or downloading unreviewed modules. If a plan or rendered manifest is needed, establish how it can be produced safely within scope; otherwise report the source-only coverage limit. Plans, state and rendered secrets may contain sensitive values: keep them out of Git and public artifacts and avoid printing them in diagnostics.

Distinguish findings in source from the effective rendered configuration and the live deployed environment. Record unresolved variables/modules, unsupported resources, exclusions and existing mitigations. A passed static scan is not proof of the live cloud's permissions, network exposure or compliance. Remediation proposals do not authorize deployment or infrastructure changes.

## Official references

Verify the selected version's supported modes and output before creating commands/configuration.

- [ZAP baseline scan](https://www.zaproxy.org/docs/docker/baseline-scan/)
- [ZAP full scan](https://www.zaproxy.org/docs/docker/full-scan/)
- [Checkov documentation](https://www.checkov.io/)
- [Checkov project and supported frameworks](https://github.com/bridgecrewio/checkov)
