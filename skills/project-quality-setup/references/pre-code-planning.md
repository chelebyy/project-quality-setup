# GitHub planning before application code

The skill can design a repository's collaboration and quality structure before technical design or code exists. Do not require an application manifest to provide useful planning. Separate known facts, provisional choices and questions that block actual creation.

## Choose the maturity stage

| Stage | Useful output now | Defer until evidence exists |
| --- | --- | --- |
| Concept only, no design | Repository purpose, proposed ownership/visibility, documentation layout, contribution/PR conventions, solo/team policy and decision backlog | Framework, package manager, runtime CI commands, test thresholds and tool-specific required checks |
| Requirements/design documents available | Derive modules, critical risks, acceptance scenarios, proposed CI layers and staged branch policy from document evidence | Unsettled architecture/runtime decisions and tests lacking executable code |
| Empty/new repository authorized for setup | Minimal relevant documents/templates and supported repository settings; real documentation checks if useful | Application tests/build/security coverage that cannot yet execute |
| First executable implementation | Replace provisional decisions with verified manifests/commands; add meaningful tests and activate observed required checks | Unsupported environments/features, with concrete next steps |
| Established project | Use existing setup/maintenance flow and reconcile drift | Do not restart from a generic scaffold |

## Blueprint from documents

Read the actual PRD, architecture decisions, platform constraints and acceptance criteria supplied or available. Cite their paths/sections in the project decision record. Conflicting documents remain explicit unresolved decisions; do not silently choose a stack from repository names or a wishlist.

Produce a concise blueprint covering:

- Repository boundaries (single repo/monorepo/multiple repos only if justified), proposed owner/name and visibility, default-branch convention, and contributor model.
- Minimal documentation structure and suitable PR/issue templates. Add CODEOWNERS only for real known owners. License selection and public disclosure are explicit decisions, not defaults inferred from a public-repo preference.
- Known product risks and planned acceptance scenarios. Label scenarios as planned/unimplemented, not covered or passed.
- Proposed checks with applicability, activation prerequisite and enforcement stage. Example: documentation validation now if runnable; compiler/build once a toolchain exists; browser checks once a representative app runs; required status only after its real identity and trigger behavior are verified.
- A small bootstrap sequence and unresolved choices; carry this in the existing project decision record rather than generating duplicate planning documents.

Use nonblocking provisional recommendations when details are unknown. Ask for owner/name/visibility or other material choices before dependent remote creation if they cannot be inferred from explicit user context; continue the blueprint meanwhile. Never invent a production domain, credentials, package namespace, license, account entitlement or team member.

## Planning versus provisioning

Designing the GitHub structure does not create a repository, upload confidential requirements, invite collaborators, open issues, buy features, or configure deployment. Provision only when the user requests it and the relevant choices are settled. Reuse authorization; do not add an extra approval ceremony for work already requested.

On authorized creation, check whether the exact target repository already exists and preserve it. Verify creation/default branch state and access before initialization. A repository that does not yet exist has no remote default to fetch: report this as bootstrap, then follow normal freshness rules after a branch exists. Preserve local source and never overwrite an existing checkout to fit the blueprint.

Configure protections in an order that permits the authorized initial content and later PR work. Record any deferred rule and its activation prerequisite. Do not require unavailable approvals or non-existent checks, add permanent all-powerful bypasses, or label a placeholder workflow as application CI. Do not create live GitHub issue/PR messages merely because a template or backlog is planned.

Completion should distinguish blueprint prepared, files created, repository created, settings applied, runnable checks verified and deferred application controls. A successful planning phase is not proof of CI execution or deployment readiness.
