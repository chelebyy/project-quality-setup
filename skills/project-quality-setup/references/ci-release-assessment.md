# Assess the existing CI-to-release connection

Use when a project already has a publication or deployment path. The goal is to establish whether that path waits for its intended mandatory quality checks. Do not create a delivery system when none is found.

## Evidence to inspect

- Identify actual triggers and destinations: production, staging, preview, package publication or store test channel. Treat these separately; preview publication before full CI is not automatically a production protection gap.
- Start with repository configuration and GitHub run/job/deployment evidence. Follow linked external provider details only with available read access. Repository YAML alone may not reveal an independently configured hosting integration.
- Trace the candidate commit or immutable artifact from validation to deployment. Establish which required checks, conditions or upstream dependencies are consulted and whether they refer to that same revision/artifact.
- Inspect failure, cancelled, skipped, pending and manual-bypass paths. Workflow completion, a successful unrelated check or human approval alone does not establish that mandatory tests passed. Deliberately advisory checks need not block release.
- Distinguish merge restrictions from deployment restrictions: examine direct pushes, tags, manual runs and independent provider triggers where they exist. Do not assume a branch rule blocks every route to production.
- Verify provider- or workflow-specific semantics with current official documentation before drawing conclusions. Use existing recent evidence; do not intentionally fail production checks, push a probe, dispatch a workflow or deploy to test the gate.

## Report one result per path

| Result | Required evidence |
| --- | --- |
| Verified gated | Configuration establishes required successful checks for the deployed revision/artifact; cite supporting settings and available run evidence. State any execution behavior not observed. |
| Demonstrated gap | A configured bypass/independent path or actual run establishes that production can proceed without an intended mandatory check. Distinguish configuration-based inference from observed deployment. |
| Unknown / partial | Missing settings, logs, entitlement/access, artifact identity or unclear conditions prevent a conclusion. Identify exactly what is missing. |
| No path found | No publication/deployment mechanism was found in the inspected scope; do not claim none exists outside that scope. |

Record destination, trigger, revision/artifact relationship, checks expected, evidence links/date, and a concise recommended correction for any demonstrated gap. In implementation mode put this finding in the existing project decision record; assessment-only remains read-only.

This feature authorizes inspection and recommendations only. Do not modify provider settings, deployment workflows, environments, secrets, permissions or branch rules as a consequence of this assessment. A finding does not itself authorize its repair; any delivery change requires separate scope from the user. Continue independent authorized CI work while clearly reporting the delivery gap.
