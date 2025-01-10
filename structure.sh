# First create ALL directories
# Frontend directories
mkdir -p frontend/src/components/{story,branding,theme}
mkdir -p frontend/src/composables
mkdir -p frontend/src/styles/themes
mkdir -p frontend/src/graphql/{queries,mutations}

# Backend directories
mkdir -p backend/app/api/{graphql,rest}
mkdir -p backend/app/core/{branding,story}
mkdir -p backend/app/config/white_label

# AI directories
mkdir -p ai/agents/agile_coach/{prompts/white_label_templates,validators}
mkdir -p ai/agents/senior_dev/{prompts,validators}
mkdir -p ai/shared

# Infrastructure directories
mkdir -p infrastructure/terraform/{vpc,lambda,s3}
mkdir -p infrastructure/sam

# DB directories
mkdir -p db/{migrations,schemas}

# THEN create all files
touch frontend/src/composables/useTheme.ts
touch frontend/src/composables/useBranding.ts
touch frontend/src/styles/themes/light.scss
touch frontend/src/styles/themes/dark.scss
touch frontend/src/styles/white-label.scss

touch ai/agents/agile_coach/lambda_handler.py
touch ai/agents/senior_dev/lambda_handler.py
touch ai/shared/base_agent.py
touch ai/shared/story_schema.py

touch infrastructure/sam/template.yaml

touch db/schemas/branding.sql
touch db/schemas/stories.sql

echo "Project structure created successfully!"
