# Spec Architect Agent Skills

## Skills

### spec.create
- **Purpose**: Create new feature specification documents based on user requirements
- **Inputs**: Feature description, user stories, acceptance criteria
- **Outputs**: spec.md file with complete feature specification
- **Specs referenced**: @specs/<feature>/spec.md

### spec.update
- **Purpose**: Update existing feature specifications based on new requirements
- **Inputs**: Updated feature description, revised user stories, modified acceptance criteria
- **Outputs**: Updated spec.md file
- **Specs referenced**: @specs/<feature>/spec.md

### spec.validate
- **Purpose**: Validate specification completeness and clarity
- **Inputs**: spec.md content
- **Outputs**: Validation report with identified gaps or ambiguities
- **Specs referenced**: @specs/<feature>/spec.md

### spec.review
- **Purpose**: Review specifications for consistency and testability
- **Inputs**: spec.md content
- **Outputs**: Review report with suggested improvements
- **Specs referenced**: @specs/<feature>/spec.md, @specs/<feature>/plan.md