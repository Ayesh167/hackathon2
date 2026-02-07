# Auth Security Agent Skills

## Skills

### auth.validate.jwt
- **Purpose**: Validate JWT implementation and token management systems
- **Inputs**: JWT implementation code, token validation requirements, security policies
- **Outputs**: Validation report with identified security vulnerabilities or improvements
- **Specs referenced**: @specs/auth/, @specs/security/

### auth.validate.flow
- **Purpose**: Validate authentication flow security and correctness
- **Inputs**: Authentication flow implementation, security requirements, user validation needs
- **Outputs**: Validation report with identified flow issues or security gaps
- **Specs referenced**: @specs/auth/, @specs/<feature>/spec.md

### auth.validate.authorization
- **Purpose**: Validate authorization and permission systems
- **Inputs**: Authorization implementation, role definitions, access control requirements
- **Outputs**: Validation report with identified authorization issues
- **Specs referenced**: @specs/auth/, @specs/security/

### security.validate.isolation
- **Purpose**: Validate user data isolation and privacy measures
- **Inputs**: User management implementation, data access controls, privacy requirements
- **Outputs**: Validation report with identified isolation or privacy issues
- **Specs referenced**: @specs/security/, @specs/<feature>/spec.md

### security.audit.implementation
- **Purpose**: Audit security implementation for best practices and vulnerabilities
- **Inputs**: Security implementation code, security requirements, vulnerability patterns
- **Outputs**: Security audit report with recommendations
- **Specs referenced**: @specs/security/, @specs/<feature>/plan.md