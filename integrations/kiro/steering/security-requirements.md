# Security Requirements Patterns

Use this after Kiro generates requirements.md to add security-specific requirements that user stories don't naturally produce.

## Add These Sections to requirements.md

### Non-Goals (Explicit Scope Exclusions)

After the user stories, add a section listing what the system explicitly does NOT do. This prevents scope creep and makes security boundaries testable.

Example:
- The system does NOT store payment credentials directly (delegated to Stripe)
- The system does NOT support SSO in this phase
- Admin users do NOT have access to raw user data; only aggregated views

### Trust Boundary Map

List every point where trusted meets untrusted:
- Which components accept external input?
- Which services talk to each other, and over what channel?
- Where does authentication happen? Where is it checked?
- What crosses a network boundary?

### Testable Security Requirements

Convert vague security goals into testable acceptance criteria:

**Bad:** "The system should be secure"
**Good:**
- GIVEN an unauthenticated request WHEN it hits any protected endpoint THEN return 401 within 50ms
- GIVEN a user session token WHEN it is older than 24 hours THEN reject it and force re-authentication
- GIVEN a SQL query parameter WHEN it contains injection patterns THEN sanitize and log the attempt

### Data Classification

For each data type the system handles:
- What is it? (PII, credentials, business-sensitive, public)
- Where is it stored? (encrypted at rest? which KMS key?)
- Who can access it? (which roles, which services?)
- How long is it retained? (TTL, deletion policy)

## Review Checklist

Before moving from requirements to design, verify:

- [ ] Every requirement has acceptance criteria in GIVEN/WHEN/THEN format
- [ ] Non-goals section exists and is specific
- [ ] Trust boundaries are identified
- [ ] Data classification is documented for sensitive data
- [ ] No requirement says "secure" or "safe" without defining what that means testably
