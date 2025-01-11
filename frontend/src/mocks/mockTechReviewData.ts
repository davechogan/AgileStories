export const mockTechReviewResult = {
  technical_analysis: {
    feasibility: {
      score: 8,
      explanation: "Implementation is straightforward with existing notification system. Will require minor updates to the user session tracking."
    },
    complexity: {
      score: 6,
      explanation: "Moderate complexity due to real-time notification requirements and session management across multiple devices."
    },
    dependencies: {
      score: 7,
      explanation: "Main dependencies are the notification service and user session service. Both are stable and well-maintained."
    }
  },
  implementation_details: {
    frontend: [
      "Add notification bell component with animation support",
      "Implement notification state management",
      "Add session tracking for first login of the day",
      "Create notification overlay/modal for message display"
    ],
    backend: [
      "Extend user session API to track daily logins",
      "Add broadcast message endpoints",
      "Implement notification status tracking",
      "Add message relevancy filtering logic"
    ],
    database: [
      "Add broadcast_messages table",
      "Add user_notification_status table",
      "Add daily_login_tracking table"
    ]
  },
  risks_and_considerations: [
    {
      category: "Performance",
      description: "High message volume could impact notification delivery speed",
      mitigation: "Implement message queuing and batch processing"
    },
    {
      category: "Security",
      description: "Message content needs to be secured in transit and storage",
      mitigation: "Use encryption for storage and HTTPS for transmission"
    },
    {
      category: "UX",
      description: "Multiple notifications could overwhelm users",
      mitigation: "Implement notification grouping and priority system"
    }
  ],
  estimated_effort: {
    frontend: "5 days",
    backend: "7 days",
    database: "2 days",
    testing: "4 days",
    total: "18 days"
  },
  recommendations: [
    "Consider implementing a message priority system",
    "Add message expiration functionality",
    "Include read receipts for critical messages",
    "Plan for future localization requirements"
  ]
} 