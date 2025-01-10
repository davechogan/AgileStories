# AgileStories

An AI-powered story writing assistant for Agile teams using SAFe methodology, with support for white-labeling and mobile devices.

## Features

- **AI-Powered Story Creation**
  - Agile Coach Agent for story refinement
  - Senior Developer Agent for technical validation
  - Interactive story improvement workflow

- **Cross-Platform Support**
  - Responsive web interface
  - Mobile-friendly design
  - Progressive Web App (PWA) capabilities

- **White Labeling**
  - Customizable branding
  - Configurable themes
  - Client-specific prompts

- **Theme Support**
  - Dark/Light mode
  - Customizable color schemes
  - Persistent user preferences

## Architecture

### Frontend (Vue.js)
- Responsive UI components
- GraphQL client integration
- Theme management system
- White label configuration

### Backend (FastAPI + GraphQL)
- GraphQL API endpoints
- LangChain AI agents
- Branding configuration management
- Story processing pipeline

### AWS Infrastructure
- VPC (10.0.0.0/16)
- Lambda functions for AI processing
- S3 for static assets
- CloudFront for content delivery

## Project Structure

AgileStories/
├── frontend/ # Vue.js frontend application
├── backend/ # FastAPI backend application
├── ai/ # AI agents and Lambda functions
├── infrastructure/ # Terraform and SAM templates
└── db/ # Database migrations and schemas

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- AWS CLI
- AWS SAM CLI
- Terraform
- Docker (optional for local development)

### Development Setup

1. Clone the repository:

bash
git clone [repository-url]
cd AgileStories

2. Create and configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Install dependencies:
```bash
# Frontend
cd frontend
npm install

# Backend
cd ../backend
pip install -r requirements.txt
```

4. Start local development:
```bash
# Start SAM local API
sam build
sam local start-api

# Start frontend development server
cd frontend
npm run serve
```

### Deployment

1. Deploy infrastructure:
```bash
cd infrastructure/terraform
terraform init
terraform apply
```

2. Deploy SAM application:
```bash
sam build
sam deploy --guided
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

