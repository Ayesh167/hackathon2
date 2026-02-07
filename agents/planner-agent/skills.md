# Planner Agent Skills

## Skills

### plan.create
- **Purpose**: Create new implementation plans based on feature specifications
- **Inputs**: spec.md content, technology requirements, architectural constraints
- **Outputs**: plan.md file with complete implementation plan
- **Specs referenced**: @specs/<feature>/plan.md, @specs/<feature>/spec.md

### plan.update
- **Purpose**: Update existing implementation plans based on changing requirements
- **Inputs**: Updated spec.md, revised architectural decisions, technology changes
- **Outputs**: Updated plan.md file
- **Specs referenced**: @specs/<feature>/plan.md

### plan.validate
- **Purpose**: Validate plan completeness and technical feasibility
- **Inputs**: plan.md content
- **Outputs**: Validation report with identified technical risks or gaps
- **Specs referenced**: @specs/<feature>/plan.md, @specs/<feature>/spec.md

### plan.architecture.design
- **Purpose**: Design system architecture based on specifications
- **Inputs**: spec.md content, technology constraints, scalability requirements
- **Outputs**: Architecture design recommendations
- **Specs referenced**: @specs/<feature>/plan.md, @specs/<feature>/data-model.md

### plan.dependencies.identify
- **Purpose**: Identify component dependencies and relationships
- **Inputs**: plan.md content, spec.md content
- **Outputs**: Dependency graph and implementation sequence
- **Specs referenced**: @specs/<feature>/plan.md, @specs/<feature>/spec.md