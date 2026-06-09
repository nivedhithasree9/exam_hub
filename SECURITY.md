Security Policy
===============

Supported Versions
------------------

Security fixes are applied to the latest version on the main branch.

Reporting A Vulnerability
-------------------------

Please report suspected vulnerabilities privately to the project maintainer. Include:

- A clear description of the issue
- Steps to reproduce
- Potential impact
- Any suggested remediation

Do not open public issues containing secrets, exploit details, or private user data.

Security Tooling
----------------

The project uses Bandit, Semgrep, Gitleaks or TruffleHog, and Pip Audit in local
hooks and CI to reduce common security risks.
